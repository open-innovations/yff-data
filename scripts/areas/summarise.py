import json
import logging
import datetime
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__file__)


# Set root directory
ROOT = Path('../..')


def year_fraction(date):
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return round(date.year + float(date.toordinal() - start) / year_length, 5)

# A function that takes a date range column of the form "Apr 2020-Mar 2021",
# creates a new column that is a datetime object based on the first part of the date ("Apr 2020"),
# then sorts by the new column


def get_values(data: pd.DataFrame, code: str, fallback: str = None) -> pd.DataFrame:
    '''Extract data from a dataframe for a code, with an optional fallback'''
    logger.debug('Extracting for %s, with fallback %s', code, fallback)

    # Return the values that match this constituency code
    if code in data.index:
        return data.loc[code, :]

    # If that code fails, try the fallback if it exists
    if fallback and fallback in data.index:
        logger.warning("Falling back to %s for %s", fallback, code)
        return data.loc[fallback, :]
    return pd.DataFrame([])


def sortByDateRangeColumn(df, rangecolumn='variable', newcolumn='parsed_date'):
    # Extract the second part of a date range ("Apr 2020-Mar 2021") and convert that ("Apr 2020") into a python datetime object
    df[newcolumn] = df[rangecolumn].str.replace(r".*?-", "", regex=True).pipe(pd.to_datetime, format="%b %Y") + pd.DateOffset(months=1, days=-1)

    # Sort by the parsed dates
    df = df.sort_values(by=[newcolumn], ascending=True)

    return df


descriptions = pd.read_csv(
    '../../data/reference/constituency-descriptions.csv', index_col='PCON22CD').fillna('')

PCON_CODE = 'PCON24CD'
PCON_NAME = 'PCON24NM'

pcons = pd.read_json(
    '../../src/_data/areas/reference/pcon.json').set_index(PCON_CODE)

summary = pd.merge(pcons, descriptions, how='left',
                   left_index=True, right_index=True)
summary.rename(columns={'PCON24NM': 'name'}, inplace=True)
summary.rename(columns=lambda x: x.lower(), inplace=True)

summary = summary.to_dict(orient='index')

PCON_DATA = ROOT / 'data/area/pcon'

employment_headlines = pd.read_csv(
    PCON_DATA / 'headlines.csv', index_col='ONS_CODE')
education_headlines = pd.read_csv(
    PCON_DATA / 'education_attainment_pcon_2010.csv', index_col='PCON22CD')
econ_inactive = pd.read_csv(
    PCON_DATA / 'econ_inactive_16-24_last_3_years.csv', index_col='ONS_CODE')
unemployment = pd.read_csv(
    PCON_DATA / 'youth_unem_16-24_last_3_years.csv', index_col='ONS_CODE')
economic_activity_16_19 = pd.read_csv(
    PCON_DATA / 'econ_active_16-19_last_3_years.csv', index_col='ONS_CODE')
economic_activity_20_24 = pd.read_csv(
    PCON_DATA / 'econ_active_20-24_last_3_years.csv', index_col='ONS_CODE')


# Make lots of extra rows from the columns
econ_inactive = econ_inactive.melt(ignore_index=False)
# Parse the date range column and sort by the parsed date
econ_inactive = sortByDateRangeColumn(econ_inactive, rangecolumn='variable', newcolumn='parsed_date')

# Make lots of extra rows from the columns
economically_active_16_19 = economic_activity_16_19.melt(ignore_index=False)
# Parse the date range column and sort by the parsed date
economically_active_16_19 = sortByDateRangeColumn(economically_active_16_19, rangecolumn='variable', newcolumn='parsed_date')

# Make lots of extra rows from the columns
economically_active_20_24 = economic_activity_20_24.melt(ignore_index=False)
# Parse the date range column and sort by the parsed date
economically_active_20_24 = sortByDateRangeColumn(economically_active_20_24, rangecolumn='variable', newcolumn='parsed_date')


# Loop over each constituency in the summary
for s in summary:
    old_code = pcons.loc[s, 'PCON21CD']

    logger.info('Preparing employment headlines for %s', s)
    headlines = employment_headlines.pipe(get_values, s, old_code)

    summary[s]['employment_headlines'] = [
        {'h': headline_name, 'v': headline_value, 'suffix': headlines.Suffix}
        for headline_name, headline_value
        in headlines.items()
        if headline_name not in ['Suffix']
    ]

    logger.info('Preparing education headlines for %s', s)
    education = education_headlines.pipe(get_values, s, old_code)
    if len(education.index) == 0:
        logger.warning('No education data available for %s', s)

    summary[s]['education_headlines'] = [
        {'h': name, 'v': value, 'suffix': education.suffix}
        for name, value
        in education.items()
        if name not in ['suffix']
    ]

    # Build the summary for economic in activity
    logger.info('Preparing economic_inactivity for %s', s)
    summary[s]['economic_inactivity'] = [
        {'dates': row.variable, 'x': year_fraction(
            row.parsed_date), 'v': row.value}
        for row
        in econ_inactive.pipe(get_values, s, old_code).itertuples()
    ]

    # Build the summary for 16-19 year olds
    logger.info('Preparing economic_activity_16_19 for %s', s)
    summary[s]['economic_activity_16_19'] = [
        {'dates': row.variable, 'x': year_fraction(
            row.parsed_date), 'v': row.value}
        for row
        in economically_active_16_19.pipe(get_values, s, old_code).itertuples()
    ]

    # Build the summary for 20-24 year olds
    logger.info('Preparing economic_activity_20_24 for %s', s)
    summary[s]['economic_activity_20_24'] = [
        {'dates': row.variable, 'x': year_fraction(
            row.parsed_date), 'v': row.value}
        for row
        in economically_active_20_24.pipe(get_values, s, old_code).itertuples()
    ]


# Create the JSON string
summaryjson = json.dumps(summary, indent=1)
# Fix NaN values
summaryjson = summaryjson.replace(r"NaN", "null")
# Compress data structures 4 spaces deep
summaryjson = summaryjson.replace("\n    ", "").replace("\n   }", "}")

# Save the output
fp = open('../../src/generated/areas/constituency/_data/summary.json', 'w')
fp.write(summaryjson)
fp.close()
