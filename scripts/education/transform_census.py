import os 
import pandas as pd 
import numpy as np
from scripts.util.file import save_tidy_csv

from transform import WORKING_DIR, DATA_DIR, filter_data, limit_to_england, clean_nulls

CONST_QUAL_DATA = os.path.join(WORKING_DIR, 'census_qualifications.csv')
const_qual_data = pd.read_csv(CONST_QUAL_DATA)

LA_QUAL_DATA = os.path.join(WORKING_DIR, 'qualifications_local_authority.csv')
la_qual_data = pd.read_csv(LA_QUAL_DATA, index_col=0)

fields = ['constituency_code', 'constituency_name', 'value', 'percent']

def filter_data(data, variable, fields, filter_field='variable'):
    return data.loc[data[filter_field] == variable, fields]

def save_to_file(data, filename):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data

def calculate_rates(data, variable):
    df = data.loc[:,(variable)]
    df = df.replace('',np.nan).astype(float)
    df = df.div(df.total, axis=0).mul(100).round(1).drop(columns='total')
    return df


if __name__ == '__main__':

    # Local authority data

    la_qual_data = la_qual_data.reset_index().set_index(['local_authority_code', 'local_authority_name'])

    la_qual_data = la_qual_data.iloc[2:]

    data = pd.MultiIndex.from_product([['total','asian', 'black_british', 'mixed_multiple', 'white', 'other'],
                                        ['total','no_qualification','level_1', 'level_2', 'apprenticeship','level_3', 'level_4', 'other']])

    la_qual_data.columns = data

    total = calculate_rates(
        la_qual_data, 'total'
      ).reset_index().pipe(
        save_tidy_csv, os.path.join(DATA_DIR), 'census_la_total.csv'
      )
    
    asian = calculate_rates(
        la_qual_data, 'asian'
      ).reset_index().pipe(
        save_tidy_csv, os.path.join(DATA_DIR), 'census_la_asian.csv'
      )
    
    black_british = calculate_rates(
        la_qual_data, 'black_british'
      ).reset_index().pipe(
        save_tidy_csv, os.path.join(DATA_DIR), 'census_la_black_british.csv'
      )
    
    mixed_multiple = calculate_rates(
        la_qual_data, 'mixed_multiple'
      ).reset_index().pipe(
        save_tidy_csv, os.path.join(DATA_DIR), 'census_la_mixed_multiple.csv'
      )
    
    white = calculate_rates(
        la_qual_data, 'white'
      ).reset_index().pipe(
        save_tidy_csv, os.path.join(DATA_DIR), 'census_la_white.csv'
      )
    
    other = calculate_rates(
        la_qual_data, 'other'
      ).reset_index().pipe(
        save_tidy_csv, os.path.join(DATA_DIR), 'census_la_other.csv'
      )
    


    # Constituency data

    # no_qualifications = filter_data(const_qual_data, 'No qualifications', fields=fields).pipe(clean_nulls).pipe(
    #     limit_to_england).pipe(save_to_file, 'census_no_qualifications.csv')

    # one_to_four_gcses = filter_data(const_qual_data, '1 to 4 GCSE passes', fields=fields).pipe(clean_nulls).pipe(
    #     limit_to_england).pipe(save_to_file, 'census_one_to_four_gcses.csv')  

    # five_or_more_gcses = filter_data(const_qual_data, '5 or more GCSE passes', fields=fields).pipe(clean_nulls).pipe(
    #     limit_to_england).pipe(save_to_file, 'census_five_or_more_gcses.csv')  

    # apprenticeship = filter_data(const_qual_data, 'Apprenticeship', fields=fields).pipe(clean_nulls).pipe(
    #     limit_to_england).pipe(save_to_file, 'census_apprenticeship.csv')  

    # two_or_more_a_levels = filter_data(const_qual_data, '2 or more A levels', fields=fields).pipe(clean_nulls).pipe(
    #     limit_to_england).pipe(save_to_file, 'census_two_or_more_a_levels.csv')  

    # higher_education_qualifications = filter_data(const_qual_data, 'Higher education qualifications', fields=fields).pipe(clean_nulls).pipe(
    #     limit_to_england).pipe(save_to_file, 'census_higher_education_qualifications.csv')  

    # other_qualifications = filter_data(const_qual_data, 'Other qualifications', fields=fields).pipe(clean_nulls).pipe(
    #     limit_to_england).pipe(save_to_file, 'census_other_qualifications.csv')        