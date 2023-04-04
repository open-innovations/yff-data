#!/usr/bin/env python
import os
import pandas as pd
from extract import A06_SA_LATEST, UNEM01_SA_LATEST

DATA_DIR = os.path.realpath(os.path.join('data', 'qlfs'))
os.makedirs(DATA_DIR, exist_ok=True)

column_name = pd.read_csv('working/lookups/lms_lookups.csv',
                          usecols=['code', 'name'], index_col='code').to_dict()['name']


def load_data(filename):
    data = pd.read_excel(filename,
                         sheet_name='People',
                         skiprows=7,
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
    )
    new_index.name = 'quarter_start'
    return new_index


def most_recent_stats(data, level=0, years=3):
    idx = data.index.get_level_values(level=level)
    return data.loc[idx > idx.max() - pd.DateOffset(years=years)]


def transform_A06():
    # Read the latest A06 data
    A06_data = load_data(A06_SA_LATEST)
    measures = ['JN6B', 'AGNJ', 'AGOL', 'AGPM']
    A06_data = A06_data[measures]
    A06_data = extract_quarters(A06_data)
    A06_data.index = quarter_to_date(A06_data.index)

    most_recent_stats(A06_data, level=0, years=4) \
        .rename(columns=column_name) \
        .to_csv(os.path.join(DATA_DIR, '16_to_24_not_in_education.csv'))

    return A06_data


def transform_UNEM01():
    UNEM01_data = load_data(UNEM01_SA_LATEST)
    measures = ['YBVN', 'YBXY']
    UNEM01_data = UNEM01_data[measures]
    UNEM01_data = extract_quarters(UNEM01_data)
    UNEM01_data.index = quarter_to_date(UNEM01_data.index)

    most_recent_stats(UNEM01_data, level=0, years=4) \
        .rename(columns=column_name) \
        .to_csv(os.path.join(DATA_DIR, '18_to_24_long_term_unemployed.csv'))

    return UNEM01_data


if __name__ == "__main__":
    transform_A06()
    transform_UNEM01()
