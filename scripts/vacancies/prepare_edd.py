import os 
import pandas as pd 


DATA_DIR = os.path.join('src', '_data', 'sources', 'vacancies')
RAW_DATA_DIR = os.path.realpath(os.path.join('data', 'vacancies'))


def prepare_vacancies(): 
    vacancies = pd.read_csv(os.path.join(RAW_DATA_DIR, 'vacancies_edd.csv'), index_col= ['index'])
    vacancies.sort_values(by='date', ascending = True, inplace = True) 

    quarterly = vacancies.loc[vacancies['freq'] == 'q'].reset_index()
    quarterly = quarterly.drop(columns= ['index', 'freq'], axis = 1).reset_index()
    quarterly.to_csv(os.path.join(DATA_DIR, 'quarterly_vacancies.csv'), index=False)

    monthly = vacancies.loc[vacancies['freq'] == 'q'].reset_index()
    monthly = monthly.drop(columns= ['index', 'freq'], axis = 1).reset_index()
    monthly.to_csv(os.path.join(DATA_DIR, 'monthly_vacancies.csv'), index=False)


if __name__ == "__main__":
    prepare_vacancies()