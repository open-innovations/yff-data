import os 
import pandas as pd

WORKING_DIR = os.path.join('working', 'upstream')

KS4_OUTCOMES_DATA = os.path.join(
    WORKING_DIR, 'ks4_outcomes.csv')

ks4_outcomes_data = pd.read_csv(KS4_OUTCOMES_DATA)

fields = ['new_la_code', 'time_period', 'version', 'gender', 'variable', 'value']

DATA_DIR = os.path.join('src', 'maps', 'education', '_data', 'view');
os.makedirs(DATA_DIR, exist_ok=True)


def add_header_end(df):
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]],columns=df.columns)
    df = pd.concat([new_record, df], ignore_index=True)
    return df

if __name__ == '__main__':

    # Filter to the allowed fields
    filtered = ks4_outcomes_data[fields].dropna()

    # Limit to rows that match 202223 and Revised
    limited = filtered.loc[(filtered['time_period']==202223) & (filtered['version']=='Revised')]

    # Pivot the table so that we have columns for variable+gender
    pivotted = limited.pivot_table(index='new_la_code', columns=['variable','gender'], values='value');

    # Add a column at the start which is a duplicate of the index (so we can not print the index column)
    pivotted.insert(0,'LADCD',pivotted.index)

    # Add a row of dashes
    final = add_header_end(pivotted)

    # Need to add a separator row
    final.to_csv(os.path.join(DATA_DIR, 'ks4_outcomes.csv'),index=False)
    