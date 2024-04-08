import os
import pandas as pd

WORKING_DIR = os.path.join('working', 'upstream')
EDUCATION_ATTAINMENT_DATA = os.path.join(
    WORKING_DIR, 'education.csv')

education_data = pd.read_csv(EDUCATION_ATTAINMENT_DATA)

fields = ['constituency_code', 'constituency_name', 'value']

DATA_DIR = os.path.join('src', 'areas', 'maps', 'education', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

column_name_mapper = {
  'Constituency ID': 'constituency_code',
  'Constituency Name': 'constituency_name',
  'Region ID': 'region_ID',
  'Region Name': 'region_name'
}

def filter_data(data, variable, fields, filter_field='variable'):
    return data.loc[data[filter_field] == variable, fields]


def limit_to_england(data):
    return data.loc[data.constituency_code.str.startswith('E')]


def clean_nulls(data):
    return data.dropna()

def calculate_percent(data):
    data.value = data.value.astype(float)
    data['value'] = (data['value']  * 100).round(1)
    return data


def save_to_file(data, filename):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data

def prepare_hexmap(data, variable, filter_field):
    filter_data(data, ).pipe(clean_nulls).pipe(limit_to_england)
    return data 

def prepare_barchart(data, filename):
    data.drop(columns=['constituency_code']).sort_values(by=['value'], ascending=False).head(20).pipe(
        save_to_file, filename
    )


if __name__ == '__main__':

    education_data = education_data.rename(
            columns=column_name_mapper)
    
    achievement_A_to_C = filter_data(education_data, 'Cons. A*-C %', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'achievement_A_to_C.csv')    

    attainment_8_score = filter_data(education_data, 'Cons. KS4 Avg Att. 8', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'attainment_8_score.csv')    

    outstanding_secondary_school = filter_data(education_data, 'Cons. % Outstanding (Secondary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'outstanding_secondary_school.csv')    

    good_secondary_school = filter_data(education_data, 'Cons. % Good (Secondary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'good_secondary_school.csv')    

    needs_improvement_secondary_school = filter_data(education_data, 'Cons. % In need of Improvement (Secondary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'needs_improvement_secondary_school.csv')    

    inadequate_secondary_school = filter_data(education_data, 'Cons. % Inadequate (Secondary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'inadequate_secondary_school.csv')    

    outstanding_primary_school = filter_data(education_data, 'Cons. % Outstanding (Primary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'outstanding_primary_school.csv')    

    good_primary_school = filter_data(education_data, 'Cons. % Good (Primary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'good_primary_school.csv')    

    needs_improvement_primary_school = filter_data(education_data, 'Cons. % In need of Improvement (Primary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'needs_improvement_primary_school.csv')    

    inadequate_primary_school = filter_data(education_data, 'Cons. % Inadequate (Primary)', fields=fields).pipe(calculate_percent).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'inadequate_primary_school.csv')    

    KS2_expected_standard = filter_data(education_data, 'KS2 cons metexp', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'KS2_expected_standard.csv')    

    KS2_higher_standard = filter_data(education_data, 'KS2 cons higher', fields=fields).pipe(clean_nulls).pipe(
        limit_to_england).pipe(save_to_file, 'KS2_higher_standard.csv')        