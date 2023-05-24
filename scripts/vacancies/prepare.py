import os 
import pandas as pd 


DATA_DIR = os.path.join('src', '_data', 'sources', 'vacancies')
RAW_DATA_DIR = os.path.realpath(os.path.join('data', 'vacancies'))
WORK_DIR = os.path.join('working', 'vacancies')
os.makedirs(DATA_DIR, exist_ok=True)

def prepare_vacancies(): 
    vacancies = pd.read_csv(os.path.join(RAW_DATA_DIR, 'vacancies_edd.csv'), index_col= ['index'])
    vacancies.sort_values(by='date', ascending = True, inplace = True) 

    quarterly = vacancies.loc[vacancies['freq'] == 'q'].reset_index()
    quarterly = quarterly.drop(columns= ['index', 'freq'], axis = 1).reset_index()
    quarterly.to_csv(os.path.join(DATA_DIR, 'quarterly_vacancies.csv'), index=False)

    monthly = vacancies.loc[vacancies['freq'] == 'm'].reset_index()
    monthly = monthly.drop(columns= ['index', 'freq'], axis = 1).reset_index()
    monthly.to_csv(os.path.join(DATA_DIR, 'monthly_vacancies.csv'), index=False)

def prepare_vacancies_by_sector(): 
    vacancies_by_sector = pd.read_csv(os.path.join(WORK_DIR, 'vacancies_by_sector.csv'), skiprows = 6, index_col = 0)
    vacancies_by_sector = vacancies_by_sector.drop(index = [
        'Electricity gas steam & air conditioning supply', 
        'Administrative & support service activities',
        'Mining & quarrying',
    ]).reset_index()
    vacancies_by_sector = vacancies_by_sector.rename(columns = 
        { vacancies_by_sector.columns[0]: 'Sector',
        vacancies_by_sector.columns[1]: 'Growth compared with last quarter (%)',
        vacancies_by_sector.columns[2]: 'Growth compared with same quarter in 2020 (%)'
        })
    vacancies_by_sector['Sector'] = vacancies_by_sector['Sector'].str.replace('<br>', '', regex=True).str.wrap(25)
    vacancies_by_sector.to_csv(os.path.join(DATA_DIR, 'vacancies_by_sector.csv'), index = False)

def summarise():
    monthly_vacancies = pd.read_csv(os.path.join(DATA_DIR, 'monthly_vacancies.csv'))
    quarterly_vacancies = pd.read_csv(os.path.join(DATA_DIR, 'quarterly_vacancies.csv'))
    last_monthly_date = monthly_vacancies.date.iloc[-1]
    last_quarterly_date = quarterly_vacancies.date.iloc[-1]


    summary = pd.DataFrame({
    'Value': [
        monthly_vacancies.value.iloc[-1].round(1),
        quarterly_vacancies.value.iloc[-1].round(1),
    ],
    'Note': [
        "Estimated number of open job vacancies in the last month, as at {}.".format(last_monthly_date),
        "Estimated number of job vacancies in the last quarter, as at {}".format(last_quarterly_date),
    ],
    },
    index=pd.Index([
        'Latest monthly vacancies',
        'Latest quarterly vacancies',
    ], name='Title')
    )
    summary.fillna('N/A').to_csv(os.path.join(DATA_DIR, 'headlines.csv'))


if __name__ == "__main__":
    prepare_vacancies()
    prepare_vacancies_by_sector()
    summarise()