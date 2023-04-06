#!/usr/bin/env python
import os
import pandas as pd
from extract import A06_SA_LATEST, UNEM01_SA_LATEST
from scripts.util.date import quarter_to_date, most_recent_stats

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


def transform_A06():
    # Read the latest A06 data
    A06_data = load_data(A06_SA_LATEST)
    measures = ['JN6B', 'AGNJ', 'AGOL', 'AGPM']
    A06_data = A06_data[measures]
    A06_data = extract_quarters(A06_data)
    A06_data.index = quarter_to_date(A06_data.index)

    most_recent_stats(A06_data) \
        .rename(columns=column_name) \
        .to_csv(os.path.join(DATA_DIR, '16_to_24_not_in_education.csv'))

    return A06_data


def transform_UNEM01():
    UNEM01_data = load_data(UNEM01_SA_LATEST)
    measures = ['YBVN', 'YBXY', 'YBVH', 'YBXJ']
    UNEM01_data = UNEM01_data[measures]
    UNEM01_data = extract_quarters(UNEM01_data)
    UNEM01_data.index = quarter_to_date(UNEM01_data.index)

    UNEM01_data['16_to_24_unemployed'] = UNEM01_data.YBVN + UNEM01_data.YBVH
    UNEM01_data['16_to_24_unemployed_over_12_months'] = UNEM01_data.YBVN + UNEM01_data.YBVH

    most_recent_stats(UNEM01_data) \
        .rename(columns=column_name) \
        .to_csv(os.path.join(DATA_DIR, '16_to_24_long_term_unemployed.csv'))

    return UNEM01_data


if __name__ == "__main__":
    transform_A06()
    transform_UNEM01()
