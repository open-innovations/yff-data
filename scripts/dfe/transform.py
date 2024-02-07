import os 
import pandas as pd

WORKING_DIR = os.path.join('working', 'upstream')

KS4_OUTCOMES_DATA = os.path.join(
    WORKING_DIR, 'ks4_outcomes.csv')

ks4_outcomes_data = pd.read_csv(KS4_OUTCOMES_DATA)

fields = ['new_la_code', 'time_period', 'version', 'gender', 'variable', 'value']

DATA_DIR = os.path.join('src', 'maps', 'education', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

def filter_data(data, variable, fields, filter_field):
    return data.loc[data[filter_field] == variable, fields]

def save_to_file(data, filename):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data

def clean_nulls(data):
    return data.dropna()


if __name__ == '__main__':

    avg_att8_total = filter_data(ks4_outcomes_data, 'Total', fields=fields, filter_field='gender').pipe(
        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
            filter_data, 'Revised', fields=fields, filter_field='version').pipe(
                filter_data, 202223, fields=fields, filter_field='time_period').pipe(
                    clean_nulls).pipe(save_to_file, 'avg_att8_total.csv')    

    avg_att8_girls = filter_data(ks4_outcomes_data, 'Girls', fields=fields, filter_field='gender').pipe(
        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
            filter_data, 'Revised', fields=fields, filter_field='version').pipe(
                filter_data, 202223, fields=fields, filter_field='time_period').pipe(
                    save_to_file, 'avg_att8_girls.csv')
    
    avg_att8_boys = filter_data(ks4_outcomes_data, 'Boys', fields=fields, filter_field='gender').pipe(
        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
            filter_data, 'Revised', fields=fields, filter_field='version').pipe(
                filter_data, 202223, fields=fields, filter_field='time_period').pipe(
                    save_to_file, 'avg_att8_boys.csv') 
    
    avg_p8score_total = filter_data(ks4_outcomes_data, 'Total', fields=fields, filter_field='gender').pipe(
        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
            filter_data, 'Revised', fields=fields, filter_field='version').pipe(
                filter_data, 202223, fields=fields, filter_field='time_period').pipe(
                    save_to_file, 'avg_p8score_total.csv') 
    
    avg_p8score_girls = filter_data(ks4_outcomes_data, 'Girls', fields=fields, filter_field='gender').pipe(
        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
            filter_data, 'Revised', fields=fields, filter_field='version').pipe(
                filter_data, 202223, fields=fields, filter_field='time_period').pipe(
                    save_to_file, 'avg_p8score_girls.csv') 

    avg_p8score_boys = filter_data(ks4_outcomes_data, 'Boys', fields=fields, filter_field='gender').pipe(
        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
            filter_data, 'Revised', fields=fields, filter_field='version').pipe(
                filter_data, 202223, fields=fields, filter_field='time_period').pipe(
                    save_to_file, 'avg_p8score_boys.csv') 