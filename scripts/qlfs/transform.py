#!/usr/bin/env python
import os
import pandas as pd
import yaml
from extract import A06_SA_LATEST, UNEM01_SA_LATEST
from scripts.util.date import quarter_to_date

DATA_DIR = os.path.realpath(os.path.join('data', 'qlfs'))
os.makedirs(DATA_DIR, exist_ok=True)
METADATA_FILE = os.path.join(DATA_DIR, 'metadata.json')

column_mapper = {
    'JN6B': 'age_16_to_24_not_in_ft_education_total_sa',  # Total not in education, 16-24
    'AGNJ': 'age_16_to_24_not_in_ft_education_in_employment_sa',  # Employed level, 16-24
    'AGOL': 'age_16_to_24_not_in_ft_education_unemployed_sa',  # Unemployed level, 16-24
    'AGPM': 'age_16_to_24_not_in_ft_education_economically_inactive_sa',  # Economivally inactive level, 16-24
    'AIWI': 'age_16_to_24_not_in_ft_education_employment_rate_sa',  # Employed rate, 16-24
    'AIXT': 'age_16_to_24_not_in_ft_education_unemployment_rate_sa',  # Unemployed rate, 16-24
    'AIYU': 'age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa',  # Economically inactive rate, 16-24

    'JN62': 'age_16_to_24_in_ft_education_total_sa',  # Total not in education, 16-24
    'AGNT': 'age_16_to_24_in_ft_education_in_employment_sa',  # Employed level, 16-24
    'AGOU': 'age_16_to_24_in_ft_education_unemployed_sa',  # Unemployed level, 16-24
    'AGPV': 'age_16_to_24_in_ft_education_economically_inactive_sa',  # Economivally inactive level, 16-24
    'AIXB': 'age_16_to_24_in_ft_education_employment_rate_sa',  # Employed rate, 16-24
    'AIYC': 'age_16_to_24_in_ft_education_unemployment_rate_sa',  # Unemployed rate, 16-24
    'AIZD': 'age_16_to_24_in_ft_education_economic_inactivity_rate_sa',  # Economically inactive rate, 16-24

    # 16-17
    'YBVH': 'age_16_to_17_unemployed_sa',
    'YBXG': 'age_16_to_17_unemployed_6_to_12_months_sa',
    'YBXJ': 'age_16_to_17_unemployed_over_12_months_sa',
    'YBXM': 'age_16_to_17_unemployed_over_12_months_rate_sa',
    # 18-24
    'YBVN': 'age_18_to_24_unemployed_sa',
    'YBXV': 'age_18_to_24_unemployed_6_to_12_months_sa',
    'YBXY': 'age_18_to_24_unemployed_over_12_months_sa',
    'YBYB': 'age_18_to_24_unemployed_over_12_months_rate_sa',

}


def load_data(filename):
    data = pd.read_excel(filename,
                         sheet_name='People',
                         skiprows=7,
                         index_col=0)
    data = data[data.iloc[:, 0].notna()]
    data.index.names = ['quarter']

    return data


def force_numeric(series):
    return pd.to_numeric(series, errors='coerce')


def extract_every_third(data):
    '''
      Extracts quarterly data from a frame by slicing.
      The first slice progresses backwards in 3s.
      The second slice reverses the dataframe.
    '''
    return data.iloc[::-3].iloc[::-1]


def transform_A06():
    # Read the latest A06 data
    A06_data = load_data(A06_SA_LATEST)
    measures = [
        'JN6B',  # Not in FTE - Total not in education, 16-24
        'AGNJ',  # Not in FTE - Employed level, 16-24
        'AGOL',  # Not in FTE - Unemployed level, 16-24
        'AGPM',  # Not in FTE - Economivally inactive level, 16-24
        'AIWI',  # Not in FTE - Employed rate, 16-24
        'AIXT',  # Not in FTE - Unemployed rate, 16-24
        'AIYU',  # Not in FTE - Economivally inactive rate, 16-24
        'JN62',  # In FTE - Total not in education, 16-24
        'AGNT',  # In FTE - Employed level, 16-24
        'AGOU',  # In FTE - Unemployed level, 16-24
        'AGPV',  # In FTE - Economivally inactive level, 16-24
        'AIXB',  # In FTE - Employed rate, 16-24
        'AIYC',  # In FTE - Unemployed rate, 16-24
        'AIZD',  # In FTE - Economically inactive rate, 16-24
    ]
    A06_data = A06_data[measures].round(1)
    A06_data = A06_data.pipe(extract_every_third)
    A06_data.index = quarter_to_date(A06_data.index)

    A06_data \
        .rename(columns=column_mapper) \
        .to_csv(os.path.join(DATA_DIR, 'education_status.csv'))

    return A06_data


def transform_UNEM01():
    UNEM01_data = load_data(UNEM01_SA_LATEST)
    measures = [
        'YBVH', 'YBXG', 'YBXJ', 'YBXM',  # 16-17
        'YBVN', 'YBXV', 'YBXY', 'YBYB',  # 18-24
    ]
    # The data has '*' characters in it - added to_numeric
    UNEM01_data = UNEM01_data[measures].apply(force_numeric)
    UNEM01_data = UNEM01_data.pipe(extract_every_third)
    UNEM01_data.index = quarter_to_date(UNEM01_data.index)

    data_16_to_24 = pd.DataFrame({
        'age_16_to_24_unemployed_sa': (UNEM01_data.YBVN + UNEM01_data.YBVH).round(0),
        'age_16_to_24_unemployed_over_12_months_sa': (UNEM01_data.YBXY + UNEM01_data.YBXJ).round(0),
        'age_16_to_24_unemployed_6_to_12_months_sa':  (UNEM01_data.YBXV + UNEM01_data.YBXG).round(0)
    })
    data_16_to_24['age_16_to_24_unemployed_over_12_months_rate_sa'] = (data_16_to_24['age_16_to_24_unemployed_over_12_months_sa'] / \
        data_16_to_24['age_16_to_24_unemployed_sa'] * 100).round(1)
    data_16_to_24['age_16_to_24_unemployed_6_to_12_months_rate_sa'] = (data_16_to_24['age_16_to_24_unemployed_6_to_12_months_sa'] / \
        data_16_to_24['age_16_to_24_unemployed_sa'] * 100).round(1)

    data_16_to_24 \
        .to_csv(os.path.join(DATA_DIR, 'long_term_unemployed.csv'))

    return UNEM01_data


def read_dates(file, key, **kwargs):
    dates = pd.read_excel(file, sheet_name="People", skiprows=1, nrows=1, header=None, usecols=kwargs.get('usecols', [1,8])).transpose()
    dates.columns = [key]
    dates.index = pd.Index([
        "published",
        "next_update",
    ])
    return dates


if __name__ == "__main__":
    pd.concat([
        read_dates(A06_SA_LATEST, 'a06', usecols=[1,8]),
        read_dates(UNEM01_SA_LATEST, 'unem01', usecols=[1,9]),
    ], axis=1).to_json(METADATA_FILE, date_format='iso', indent=2)

    notes = [
        'Long-term unemoployment levels for 16-24 are derived from aggregates 16-17 and 18-24 rates',
        'Long-term unemployment rates for 16-24 are calcualted from the aggregated values',
    ]

    with open(os.path.join(DATA_DIR, 'notes.yaml'), 'w', encoding="utf-8") as f:
        f.write('# DO NOT EDIT - this file is automatatically generated by the {0} script\n'.format(
            'scripts/qlfs/transform.py'))
        f.write(yaml.dump(notes))
