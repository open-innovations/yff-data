import os 
import pandas as pd 

DATA_DIR = os.path.realpath(os.path.join('data', 'vacancies'))
dataset_name = 'UK Vacancies (thousands) - Total'

def transform_vacancies():
    lookup = pd.read_csv(os.path.join('working', 'upstream', 'lms-codes.csv'), index_col=None)
    data = pd.read_csv(os.path.join('working', 'upstream', 'lms.csv'))

    code = lookup.query('Title == @dataset_name').CDID.iloc[0]
    results = data.query('variable == @code').reset_index()
    results = results.drop(columns= ['index'], axis = 1).reset_index().rename(columns = {
                'variable': 'code', 
                })
    results.loc[:, ['index', 'code', 'value', 'date', 'freq']].to_csv(os.path.join(DATA_DIR, 'vacancies_edd.csv'), index=False)


if __name__ == "__main__":
    transform_vacancies()
