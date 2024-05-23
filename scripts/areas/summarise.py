import json
import math
import datetime
import pandas as pd

def year_fraction(date):
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return round(date.year + float(date.toordinal() - start) / year_length,3)

# A function that takes a date range column of the form "Apr 2020-Mar 2021",
# creates a new column that is a datetime object based on the first part of the date ("Apr 2020"),
# then sorts by the new column
def sortByDateRangeColumn(df, opts={}):

    if not 'rangecolumn' in opts:
        opts['rangecolumn'] = 'variable'
    if not 'newcolumn' in opts:
        opts['newcolumn'] = 'parsed_date'

    # Extract the first part of a date range ("Apr 2020-Mar 2021") and convert that ("Apr 2020") into a python datetime object
    df[opts['newcolumn']] = pd.to_datetime(df[opts['rangecolumn']].str.replace(r"\-.*",'',regex=True), format='%b %Y')

    # Sort by the parsed dates
    df = df.sort_values(by=[opts['newcolumn']], ascending=True)

    return df


descriptions=pd.read_csv('../../data/reference/constituency-descriptions.csv', index_col='PCON22CD').fillna('')

pcons=pd.read_json('../../src/_data/areas/reference/pcon.json')

summary=pd.merge(pcons, descriptions, how='left', left_on='PCON22CD', right_index=True).set_index('PCON22CD')
summary.rename(columns={ 'PCON22NM': 'name'}, inplace=True)
summary.rename(columns=lambda x: x.lower(), inplace=True)

summary = summary.to_dict(orient='index')

employment_headlines = pd.read_csv('../../data/area/pcon/headlines.csv', index_col='PCON22CD')
education_headlines = pd.read_csv('../../data/area/pcon/education_attainment_pcon_2010.csv', index_col='PCON22CD')
econ_inactive = pd.read_csv('../../data/area/pcon/econ_inactive_16-24_last_3_years.csv', index_col='PCON22CD')
unemployment = pd.read_csv('../../data/area/pcon/youth_unem_16-24_last_3_years.csv', index_col='PCON22CD')
economic_activity_16_19 = pd.read_csv('../../data/area/pcon/econ_active_16-19_last_3_years.csv', index_col='PCON22CD')
economic_activity_20_24 = pd.read_csv('../../data/area/pcon/econ_active_20-24_last_3_years.csv', index_col='PCON22CD')


# Make lots of extra rows from the columns
econ_inactive = econ_inactive.melt(ignore_index=False)
# Parse the date range column and sort by the parsed date
econ_inactive = sortByDateRangeColumn(econ_inactive,{'rangecolumn':'variable','newcolumn':'parsed_date'});

# Make lots of extra rows from the columns
economically_active_16_19 = economic_activity_16_19.melt(ignore_index=False)
# Parse the date range column and sort by the parsed date
economically_active_16_19 = sortByDateRangeColumn(economically_active_16_19,{'rangecolumn':'variable','newcolumn':'parsed_date'});

# Make lots of extra rows from the columns
economically_active_20_24 = economic_activity_20_24.melt(ignore_index=False)
# Parse the date range column and sort by the parsed date
economically_active_20_24 = sortByDateRangeColumn(economically_active_20_24,{'rangecolumn':'variable','newcolumn':'parsed_date'});


# Loop over each constituency in the summary
for s in summary:

    suffix = employment_headlines.loc[s, :].Suffix
    summary[s]['employment_headlines'] = [
        { 'h': headline_name, 'v': headline_value, 'suffix': suffix }
        for headline_name, headline_value in employment_headlines.loc[s, :].drop(labels="Suffix").items()
        ]
    summary[s]['education_headlines'] = [
        { 'h': name, 'v': value, 'suffix': suffix}
        for name, value in education_headlines.loc[s, :].drop(labels="suffix").items()
        ]

    # Build the summary for economic in activity
    summary[s]['economic_inactivity'] = []
    try:
        # Get the values that match this constituency code, s
        vals = econ_inactive.loc[s, :]
        # Loop over the rows
        for index, row in vals.iterrows():
            summary[s]['economic_inactivity'].append({'dates':row.variable,'x':year_fraction(row.parsed_date),'v':row.value})
    except KeyError as e:
        pass

    # Build the summary for 16-19 year olds
    summary[s]['economic_activity_16_19'] = []
    try:
        # Get the values that match this constituency code, s
        vals = economically_active_16_19.loc[s, :]
        # Loop over the rows
        for index, row in vals.iterrows():
            summary[s]['economic_activity_16_19'].append({'dates':row.variable,'x':year_fraction(row.parsed_date),'v':row.value})
    except KeyError as e:
        pass

    # Build the summary for 20-24 year olds
    summary[s]['economic_activity_20_24'] = []
    try:
        # Get the values that match this constituency code, s
        vals = economically_active_20_24.loc[s, :]
        # Loop over the rows
        for index, row in vals.iterrows():
            summary[s]['economic_activity_20_24'].append({'dates':row.variable,'x':year_fraction(row.parsed_date),'v':row.value})
    except KeyError as e:
        pass



# Create the JSON string
summaryjson = json.dumps(summary, indent = 1)
# Fix NaN values
summaryjson = summaryjson.replace(r"NaN","null")
# Compress data structures 4 spaces deep
summaryjson = summaryjson.replace("\n    ", "").replace("\n   }", "}")

# Save the output
fp = open('../../src/generated/areas/constituency/_data/summary.json', 'w')
fp.write(summaryjson);
fp.close()
