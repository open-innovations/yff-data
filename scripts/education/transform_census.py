import os 
import pandas as pd 

from transform import WORKING_DIR, DATA_DIR, filter_data, limit_to_england, clean_nulls

QUAL_DATA = os.path.join(WORKING_DIR, 'census_qualifications.csv')
qual_data = pd.read_csv(QUAL_DATA)

fields = ['constituency_code', 'constituency_name', 'value', 'percent']

def filter_data(data, variable, fields, filter_field='variable'):
    return data.loc[data[filter_field] == variable, fields]

def save_to_file(data, filename):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data


if __name__ == '__main__':

    no_qualifications = filter_data(qual_data, 'No qualifications', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'census_no_qualifications.csv')

    one_to_four_gcses = filter_data(qual_data, '1 to 4 GCSE passes', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'census_one_to_four_gcses.csv')  

    five_or_more_gcses = filter_data(qual_data, '5 or more GCSE passes', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'census_five_or_more_gcses.csv')  

    apprenticeship = filter_data(qual_data, 'Apprenticeship', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'census_apprenticeship.csv')  

    two_or_more_a_levels = filter_data(qual_data, '2 or more A levels', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'census_two_or_more_a_levels.csv')  

    higher_education_qualifications = filter_data(qual_data, 'Higher education qualifications', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'census_higher_education_qualifications.csv')  

    other_qualifications = filter_data(qual_data, 'Other qualifications', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'census_other_qualifications.csv')        