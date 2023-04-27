import os
import pandas as pd

RAW_DATA_DIR = os.path.realpath(os.path.join('data', 'vacancies'))
WORK_DIR = os.path.join('working', 'vacancies')


DATA_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'vacancies'))
os.makedirs(DATA_DIR, exist_ok=True)

def prepare_vacancies(): 
    vacancies = pd.read_csv(os.path.join(WORK_DIR, 'vacancies.csv'), skiprows=6)
    vacancies = vacancies.reset_index().rename(columns = { vacancies.index.name: 'Index'})
    vacancies.to_csv(os.path.join(DATA_DIR, 'vacancies.csv'), index = False)

def prepare_vacancies_by_sector():
    vacancies_by_sector = pd.read_csv(os.path.join(WORK_DIR, 'vacancies_by_sector.csv'), skiprows = 6)
    vacancies_by_sector = vacancies_by_sector.rename(columns = 
        { vacancies_by_sector.columns[0]: 'Sector',
        vacancies_by_sector.columns[1]: 'Growth compared with last quarter (%)',
        vacancies_by_sector.columns[2]: 'Growth compared with same quarter in 2020 (%)'
        })
    vacancies_by_sector['Sector'] = vacancies_by_sector['Sector'].str.replace('<br>', '', regex=True).str.wrap(25)
    vacancies_by_sector.to_csv(os.path.join(DATA_DIR, 'vacancies_by_sector.csv'), index = False)

if __name__ == "__main__":
    prepare_vacancies()
    prepare_vacancies_by_sector()