import os
import re
import pandas as pd

WORKING_DIR = os.path.join('working', 'upstream')

KS4_OUTCOMES_DATA = os.path.join(
    WORKING_DIR, 'ks4_outcomes.csv')

ks4_outcomes_data = pd.read_csv(KS4_OUTCOMES_DATA)

fields = ['new_la_code', 'time_period', 'version', 'gender', 'variable', 'value']
groupby = ['variable','gender']

DATA_DIR = os.path.join('src', 'maps', 'education', '_data', 'view');
os.makedirs(DATA_DIR, exist_ok=True)

def save_tidy_csv(file,df):
    # First add the header
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]],columns=df.columns)
    final = pd.concat([new_record, df], ignore_index=True)

    # Get the output as CSV
    csv = final.to_csv(index=True)

    # Because we added an index column we will now tidy 
    csv = re.sub(r'\n0,---,---', '\n---,---,---', csv)

    text_file = open(os.path.join(DATA_DIR, 'ks4_outcomes.csv'), "w")
    text_file.write(csv)
    text_file.close()


if __name__ == '__main__':

    # Filter to the allowed fields
    filtered = ks4_outcomes_data[fields].dropna()

    # Limit to rows that match 202223 and Revised
    limited = filtered.loc[(filtered['time_period']==202223) & (filtered['version']=='Revised')]

    # Pivot the table so that we have columns for variable+gender
    pivotted = limited.pivot_table(index='new_la_code', columns=groupby, values='value');

    # Add a column at the start which is a duplicate of the index (so we can not print the index column)
    pivotted.insert(0,'LADCD',pivotted.index)

    # Need to add a separator row
    save_tidy_csv(os.path.join(DATA_DIR, 'ks4_outcomes.csv'),pivotted)
    