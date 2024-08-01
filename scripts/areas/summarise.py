import datetime
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__file__)


# Set root directory
ROOT = Path('../..')

# Set up PCON code and name key
PCON_CODE = 'PCON24CD'
PCON_NAME = 'PCON24NM'


def year_fraction(date):
    '''
    A function that takes a date range column of the form "Apr 2020-Mar 2021",
    creates a new column that is a datetime object based on the first part of the date ("Apr 2020"),
    then sorts by the new column
    '''
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return round(date.year + float(date.toordinal() - start) / year_length, 5)



def get_values(data: pd.DataFrame, code: str, weightings: pd.Series = None) -> pd.DataFrame:
    '''
    Extract data from a dataframe for a code, with an optional fallback of weightings
    '''
    logger.debug('Extracting for %s, with fallback %s', code, weightings)

    # Return the values that match this constituency code
    if code in data.index:
        res = data.loc[code, :].copy()
        res['modelled'] = False
        return res.pipe(nan_to_none)

    # If that code fails, try the fallback if it exists
    if weightings:
        logger.warning("Falling back to %s for %s", weightings, code)
        # Create a series from the fallback weights
        weights = pd.Series(weightings, name='weights')
        # Subset the data with the fallback index
        model = data.loc[weights.index, :].copy()
        # Save an index to the old codes for use later
        old_codes = model.index
        # Create a series which will be used as the new index, with every item the code
        new_index = pd.Series(code, index=old_codes,
                              name='ONS_CODE').to_frame()
        # Get the numeric columns - these will be scaled by the weight
        numeric = model.select_dtypes(include=['number']).mul(
            weights.loc[old_codes], axis=0)
        # Get the non-numeric columns - these will not be scaled by the weight
        non_numeric = model.select_dtypes(exclude=['number'])
        # Construct the result dataframe
        res = (
            # Concatenate the numeric, new_index and non_numeric frames
            pd.concat([
                numeric, new_index, non_numeric
            ], axis=1)
            # Group by the new_index and non-numeric columns
            .groupby(new_index.columns.to_list() + non_numeric.columns.to_list())
            # And calculate the sum
            .sum().round(1)
            # Set the index to be the new_index
            .reset_index().set_index(new_index.columns.to_list())
            # Select the original set of columns
            [data.columns.to_list()]
        )
        if len(res.index) == 1:
            res = res.squeeze()
        res['modelled'] = True
        return res.pipe(nan_to_none)

    # Otherwise, we return an empty dataframe
    return pd.DataFrame([])


def sortByDateRangeColumn(df, rangecolumn='variable', newcolumn='parsed_date'):
    # Extract the second part of a date range ("Apr 2020-Mar 2021") and convert that ("Apr 2020") into a python datetime object
    df[newcolumn] = df[rangecolumn].str.replace(r".*?-", "", regex=True).pipe(
        pd.to_datetime, format="%b %Y") + pd.DateOffset(months=1, days=-1)

    # Sort by the parsed dates
    df = df.sort_values(by=[newcolumn], ascending=True)

    return df


def nan_to_none(df: pd.DataFrame | pd.Series):
    '''
    Replace instances of numpy nan in a DataFrame or Series with None.
    Useful when rendering to JSON, as NaN comes up as a string, wheras None is rendered as `null`.
    '''
    return df.replace(np.nan, None)


'''
Summarise the data
'''
# Read in the pcon data
pcons = pd.read_json(
    ROOT / 'src/_data/areas/reference/pcon.json').set_index(PCON_CODE)

# Merge with description data and create the summary dict
summary = pcons.merge(
    pd.read_csv(
        ROOT / 'data/reference/constituency-descriptions.csv',
        index_col='PCON22CD'
    ), how='left', left_index=True, right_index=True,
).pipe(
    nan_to_none
).rename(
    columns={PCON_NAME: 'name'}
).rename(
    columns=lambda x: x.lower()
).to_dict(
    orient='index'
)

# Load a series of data files
PCON_DATA = ROOT / 'data/area/pcon'

employment_headlines = pd.read_csv(
    PCON_DATA / 'headlines.csv', index_col='ONS_CODE')
education_headlines = pd.read_csv(
    PCON_DATA / 'education_attainment_pcon_2010.csv', index_col='PCON22CD')
economically_inactive = pd.read_csv(PCON_DATA / 'econ_inactive_16-24_last_3_years.csv', index_col='ONS_CODE').melt(
    ignore_index=False).pipe(sortByDateRangeColumn, rangecolumn='variable', newcolumn='parsed_date')
economically_active_16_19 = pd.read_csv(PCON_DATA / 'econ_active_16-19_last_3_years.csv', index_col='ONS_CODE').melt(
    ignore_index=False).pipe(sortByDateRangeColumn, rangecolumn='variable', newcolumn='parsed_date')
economically_active_20_24 = pd.read_csv(PCON_DATA / 'econ_active_20-24_last_3_years.csv', index_col='ONS_CODE').melt(
    ignore_index=False).pipe(sortByDateRangeColumn, rangecolumn='variable', newcolumn='parsed_date')
# unemployment = pd.read_csv(
#     PCON_DATA / 'youth_unem_16-24_last_3_years.csv', index_col='ONS_CODE')

# Loop over each constituency in the summary
for s in summary:
    weights = pcons.loc[s, 'weights']
    summary[s]['weights'] = pd.Series(weights).round(3).to_dict()

    logger.info('Preparing employment headlines for %s', s)
    headlines = employment_headlines.pipe(get_values, s, weights)

    summary[s]['employment_headlines'] = [
        {
            'h': headline_name,
            'v': headline_value,
            'suffix': headlines.Suffix,
            'modelled': headlines.modelled
        }
        for headline_name, headline_value
        in headlines.items()
        if headline_name not in ['Suffix', 'modelled']
    ]

    logger.info('Preparing education headlines for %s', s)
    education = education_headlines.pipe(get_values, s, weights)
    if len(education.index) == 0:
        logger.warning('No education data available for %s', s)

    summary[s]['education_headlines'] = [
        {
            'h': name,
            'v': value,
            'suffix': education.suffix,
            'modelled': education.modelled
        }
        for name, value
        in education.items()
        if name not in ['suffix', 'modelled']
    ]

    # Build the summary for economic inactivity
    logger.info('Preparing economic_inactivity for %s', s)
    summary[s]['economic_inactivity'] = [
        {
            'dates': row.variable,
            'x': year_fraction(row.parsed_date),
            'v': row.value,
            'modelled': bool(row.modelled)
        }
        for row
        in economically_inactive.pipe(get_values, s, weights).itertuples()
    ]

    # Build the summary for 16-19 year olds
    logger.info('Preparing economic_activity_16_19 for %s', s)
    summary[s]['economic_activity_16_19'] = [
        {
            'dates': row.variable,
            'x': year_fraction(row.parsed_date),
            'v': row.value,
            'modelled': bool(row.modelled)
        }
        for row
        in economically_active_16_19.pipe(get_values, s, weights).itertuples()
    ]

    # Build the summary for 20-24 year olds
    logger.info('Preparing economic_activity_20_24 for %s', s)
    summary[s]['economic_activity_20_24'] = [
        {
            'dates': row.variable,
            'x': year_fraction(row.parsed_date),
            'v': row.value,
            'modelled': bool(row.modelled)
        }
        for row
        in economically_active_20_24.pipe(get_values, s, weights).itertuples()
    ]

# Create the JSON string
summaryjson = json.dumps(summary, indent=1, allow_nan=False)
# Compress data structures 8 spaces deep
summaryjson = summaryjson.replace("\n    ", " ").replace("\n   }", " }")

# Save the output
with open(ROOT / 'src/generated/areas/constituency/_data/summary.json', 'w') as fp:
    fp.write(summaryjson)
