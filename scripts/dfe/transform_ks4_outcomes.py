import os
import re
import pandas as pd
from util import save_tidy_csv

WORKING_DIR = os.path.join('working', 'upstream')

KS4_OUTCOMES_DATA = os.path.join(WORKING_DIR, 'ks4_outcomes.csv')

ks4_outcomes_data = pd.read_csv(KS4_OUTCOMES_DATA)

fields = ['new_la_code', 'time_period', 'version', 'gender', 'variable', 'value']
groupby = ['variable','gender','time_period']

DATA_DIR = os.path.join('src', 'maps', 'education', '_data', 'view');
os.makedirs(DATA_DIR, exist_ok=True)

# Let's be extra safe about extracting the years in case 
# there are multiple versions for a year in the file
def latestVersion(df):
    q = ''
    i = 0;
    # Get the unique years
    years = df.time_period.unique()
    for y in years:
        # Get the unique versions for this year
        vs = df.loc[(df.time_period==y)].version.unique();
        # Separate queries with a pipe
        if i > 0:
            q += ' | '
        q += '(time_period == ' + str(y) + ' & version=="'
        if "Final" in vs:
            q += 'Final'
        else:
            q += 'Revised'
        q += '")'
        i += 1;
    return df.query(q);

if __name__ == '__main__':

    # Filter to the allowed fields
    filtered = ks4_outcomes_data[fields].dropna()

    # Limit to the latest versions of each year
    limited = latestVersion(filtered)

    # Pivot the table so that we have columns for variable+gender
    pivotted = limited.pivot_table(index='new_la_code', columns=groupby, values='value')

    # Add a column at the start which is a duplicate of the index (so we can not print the index column)
    pivotted.insert(0,'LADCD',pivotted.index)

    # Get CSV with names and add them
    lad = pd.read_csv(os.path.join('src', 'maps', '_data', 'uk_local_authority_districts.csv'))
    pivotted.insert(1,'LADNM',pivotted.LADCD.map(lad.set_index('LADCD')['LADNM'].to_dict()),True)

    # Need to add a separator row
    save_tidy_csv(pivotted, os.path.join(DATA_DIR), 'ks4_outcomes.csv')
    