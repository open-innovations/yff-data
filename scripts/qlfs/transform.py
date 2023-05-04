#!/usr/bin/env python
import os
import pandas as pd
import yaml
from extract import A06_SA_LATEST, UNEM01_SA_LATEST
from scripts.util.date import quarter_to_date, most_recent_stats

DATA_DIR = os.path.realpath(os.path.join('data', 'qlfs'))
SUMMARY_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'qlfs'))
os.makedirs(DATA_DIR, exist_ok=True)

column_name = pd.read_csv('working/lookups/lms_lookups.csv',
                          usecols=['code', 'name'], index_col='code').name.to_dict()

column_mapper = {
    'JN6B': 'age_16_to_24_not_in_ft_education_total_sa',  # Total not in education, 16-24
    'AGNJ': 'age_16_to_24_not_in_ft_education_in_employment_sa',  # Employed level, 16-24
    'AGOL': 'age_16_to_24_not_in_ft_education_unemployed_sa',  # Unemployed level, 16-24
    'AGPM': 'age_16_to_24_not_in_ft_education_economically_inactive_sa',  # Economivally inactive level, 16-24
    'AIWI': 'age_16_to_24_not_in_ft_education_employment_rate_sa',  # Employed rate, 16-24
    'AIXT': 'age_16_to_24_not_in_ft_education_unemployment_rate_sa',  # Unemployed rate, 16-24
    'AIYU': 'age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa',  # Economivally inactive rate, 16-24
    # 16-17
    'YBVH': 'age_16_to_17_unemployed_sa',
    'YBXJ': 'age_16_to_17_unemployed_over_12_months_sa',
    'YBXM': 'age_16_to_17_unemployed_over_12_months_rate_sa',
    # 18-24
    'YBVN': 'age_18_to_24_unemployed_sa',
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
    measures = [
        'JN6B',  # Total not in education, 16-24
        'AGNJ',  # Employed level, 16-24
        'AGOL',  # Unemployed level, 16-24
        'AGPM',  # Economivally inactive level, 16-24
        'AIWI',  # Employed rate, 16-24
        'AIXT',  # Unemployed rate, 16-24
        'AIYU',  # Economivally inactive rate, 16-24
    ]
    A06_data = A06_data[measures]
    A06_data = extract_quarters(A06_data)
    A06_data.index = quarter_to_date(A06_data.index)

    most_recent_stats(A06_data) \
        .rename(columns=column_mapper) \
        .to_csv(os.path.join(DATA_DIR, 'not_in_education.csv'))

    return A06_data


def transform_UNEM01():
    UNEM01_data = load_data(UNEM01_SA_LATEST)
    measures = [
        'YBVH', 'YBXJ', 'YBXM',  # 16-17
        'YBVN', 'YBXY', 'YBYB',  # 18-24
    ]
    UNEM01_data = UNEM01_data[measures]
    UNEM01_data = extract_quarters(UNEM01_data)
    UNEM01_data.index = quarter_to_date(UNEM01_data.index)

    data_16_to_24 = pd.DataFrame({
        'age_16_to_24_unemployed_sa': UNEM01_data.YBVN + UNEM01_data.YBVH,
        'age_16_to_24_unemployed_over_12_months_sa': UNEM01_data.YBXY + UNEM01_data.YBXJ
    })
    data_16_to_24['age_16_to_24_unemployed_over_12_months_rate_sa'] = data_16_to_24['age_16_to_24_unemployed_over_12_months_sa'] / \
        data_16_to_24['age_16_to_24_unemployed_sa'] * 100

    most_recent_stats(data_16_to_24) \
        .to_csv(os.path.join(DATA_DIR, 'long_term_unemployed.csv'))

    return UNEM01_data

def summarise(): 
    long_term_unemployed = pd.read_csv(os.path.join(DATA_DIR, 'long_term_unemployed.csv'))
    not_in_education = pd.read_csv(os.path.join(DATA_DIR, 'not_in_education.csv'))

    summary = pd.DataFrame({
            'Unemployment rate' : (not_in_education.age_16_to_24_not_in_ft_education_unemployment_rate_sa.tail(1)).round(1),
            'Long-term unemployment rate':(long_term_unemployed.age_16_to_24_unemployed_over_12_months_rate_sa.tail(1)).round(1),
            'Economic inactivity rate':(not_in_education.age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa.tail(1)).round(1)
    }).T.reset_index()
    summary = summary.rename(columns = {'index': 'Title', 11: 'Value'})
    summary['Note'] = [
        "Young people aged 16-24, not in full-time education (seasonally adjusted)",
        "Young people aged 16-24, unemployed over 12 months (seasonally adjusted)",
        "Young people age 16-24 not in full-time education, economically inactive (seasonally adjusted)"
        ]
    summary['Suffix'] = '%'
    summary.to_csv(os.path.join(SUMMARY_DIR, 'headlines.csv'), index=False)

if __name__ == "__main__":
    transform_A06()
    transform_UNEM01()
    summarise()

    notes = [
        'Long-term unemoployment levels for 16-24 are derived from aggregates 16-17 and 18-24 rates',
        'Long-term unemployment rates for 16-24 are calcualted from the aggregated values',
    ]

    with open(os.path.join(DATA_DIR, 'notes.yaml'), 'w', encoding="utf-8") as f:
        f.write('# DO NOT EDIT - this file is automatatically generated by the {0} script\n'.format(
            'scripts/qlfs/transform.py'))
        f.write(yaml.dump(notes))
