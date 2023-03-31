#!/usr/bin/env python
import os
import re
import pandas as pd
from extract import A06_SA_LATEST, UNEM01_SA_LATEST


DATA_DIR = os.path.realpath(os.path.join('data', 'qlfs'))
os.makedirs(DATA_DIR, exist_ok=True)


def clean_column_name(x):
    return re.sub(r'[\s\(\)]+', '_', x.lower())


def load_data(filename):
    data = pd.read_excel(filename,
                         sheet_name='People',
                         skiprows=4,
                         header=[0, 1, 2, 3],
                         index_col=0)
    data = data[data.iloc[:, 0].notna()]
    data.index.names = ['quarter']

    return data


def extract_quarters(data):
    '''
      Extracts quarterly data from a frame where the index comprises strings
      which start with the months of the year.
    '''
    return data.loc[data.index.str.slice(
        stop=3).isin(['Jan', 'Apr', 'Jul', 'Oct'])]


def quarter_to_date(index):
    new_index = pd.to_datetime(
        index.str.slice(stop=3) + '-' + index.str.slice(start=8)
    ) + pd.DateOffset(months=3, days=-1)
    new_index.name = 'quarter_end'
    return new_index


def most_recent_stats(data, level=0, years=3):
    idx = data.index.get_level_values(level=level)
    return data.loc[idx > idx.max() - pd.DateOffset(years=years)]


def transform_A06():
    # Read the latest A06 data
    A06_data = load_data(A06_SA_LATEST)

    A06_data = extract_quarters(A06_data)
    A06_data.index = quarter_to_date(A06_data.index)

    # Reshape the index...
    # Drop the dataset identifier code
    A06_data.columns = A06_data.columns.droplevel(level=[2, 3])

    # print(A06_data)
    most_recent_stats(A06_data, level=0, years=4) \
        .loc[:, ('All aged 16 to 24 not in full-time education 1')] \
        .rename(columns=clean_column_name) \
        .to_csv(os.path.join(DATA_DIR, '16_to_24_not_in_education.csv'))

    return A06_data


def transform_UNEM01():
    UNEM01_data = load_data(UNEM01_SA_LATEST)

    UNEM01_data = extract_quarters(UNEM01_data)
    UNEM01_data.index = quarter_to_date(UNEM01_data.index)

    # Reshape the index...
    new_index = UNEM01_data.columns.to_frame()
    new_index.columns = ['age_group', 'measure', 'measure_2', 'numeric']
    new_index.loc[new_index.measure_2.str.contains('Unnamed'), [
        'measure_2']] = ''
    new_index.measure = (new_index.measure + ' ' +
                         new_index.measure_2).str.strip()
    new_index.drop(columns=['measure_2', 'numeric'], inplace=True)
    UNEM01_data.columns = pd.MultiIndex.from_frame(new_index)
    UNEM01_data = UNEM01_data.rename(columns=clean_column_name)

    # Work out long term unemployed stats
    long_term_unemployed = UNEM01_data \
        .melt(ignore_index=False).reset_index()
    # Could additionally extract 16-17 and create aggregated 16-24 figures
    long_term_unemployed = long_term_unemployed.loc[long_term_unemployed.age_group.isin(
        ['18-24']
    )]
    # PCT Long term unemployed can be calculated by all_over_12_months / all_level
    long_term_unemployed = long_term_unemployed.loc[long_term_unemployed.measure.isin(
        ['all_level', 'all_over_12_months_level'])]
    table = long_term_unemployed \
        .pivot(index=['quarter_end', 'age_group'], columns='measure', values='value')

    most_recent_stats(table, level=0, years=4) \
        .to_csv(os.path.join(DATA_DIR, '18_to_24_long_term_unemployed.csv'))

    return long_term_unemployed


if __name__ == "__main__":
    transform_A06()
    transform_UNEM01()
