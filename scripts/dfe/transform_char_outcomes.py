import os
import re
import pandas as pd

from scripts.util.file import save_tidy_csv

WORKING_DIR = os.path.join('working', 'upstream')

KS4_CHAR_OUTCOMES_DATA = os.path.join(
    WORKING_DIR, 'ks4_char_outcomes.csv')

char_outcomes_data = pd.read_csv(KS4_CHAR_OUTCOMES_DATA)

fields = ['new_la_code', 'time_period', 'version', 'gender', 'breakdown', 'ethnicity_major', 
          'free_school_meals', 'sen_status', 'sen_description', 'disadvantage', 'first_language', 'variable', 'value']
groupby = ['variable','breakdown','gender','ethnicity_major','free_school_meals','sen_status','sen_description','disadvantage','first_language']

DATA_DIR = os.path.join('src', 'maps', 'education', '_data', 'view');
os.makedirs(DATA_DIR, exist_ok=True)


def add_header_end(df):
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]],columns=df.columns)
    df = pd.concat([new_record, df], ignore_index=True)
    return df

if __name__ == '__main__':

    # Filter to the allowed fields
    filtered = char_outcomes_data[fields].dropna()

    # Limit to rows that match 202223 and Revised
    limited = filtered.loc[(filtered['time_period']==202223) & (filtered['version']=='Revised') & (filtered['breakdown']!='Ethnicity minor')]

    # Pivot the table to arrange in columns with each combo
    pivotted = limited.pivot_table(index='new_la_code', columns=groupby, values='value');

    # Add a column at the start which is a duplicate of the index (so we can not print the index column)
    pivotted.insert(0,'LADCD',pivotted.index)

    pivotted.pipe(save_tidy_csv, os.path.join(DATA_DIR), 'ks4_char_outcomes.csv')
