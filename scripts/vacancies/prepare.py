import os 
import pandas as pd

from scripts.util.date import lms_period_to_quarter_label 


DATA_DIR = os.path.join('src', '_data', 'sources', 'vacancies')
RAW_DATA_DIR = os.path.realpath(os.path.join('data', 'vacancies'))
DASHBOARD_DIR = os.path.join('src', 'dashboard', 'vacancies', '_data')
WORK_DIR = os.path.join('working', 'vacancies')
os.makedirs(DATA_DIR, exist_ok=True)

def prepare_vacancies(): 
    vacancies = pd.read_csv(os.path.join(RAW_DATA_DIR, 'vacancies_edd.csv'), index_col= ['index'])
    vacancies.sort_values(by='date', ascending = True, inplace = True)
    vacancies['quarter_label'] = pd.to_datetime(vacancies.date).map(lms_period_to_quarter_label)

    quarterly = vacancies.loc[vacancies['freq'] == 'q'].reset_index()
    quarterly = quarterly.drop(columns= ['index', 'freq'], axis = 1).reset_index()
    quarterly.to_csv(os.path.join(DATA_DIR, 'quarterly_vacancies.csv'), index=False)

    monthly = vacancies.loc[vacancies['freq'] == 'm'].reset_index()
    monthly = monthly.drop(columns= ['index', 'freq'], axis = 1).reset_index()
    monthly.to_csv(os.path.join(DATA_DIR, 'monthly_vacancies.csv'), index=False)

def prepare_vacancies_by_sector(): 
    vacancies_by_sector = pd.read_csv(os.path.join(WORK_DIR, 'vacancies_by_sector.csv'), skiprows = 6)

    vacancies_by_sector = vacancies_by_sector.rename(columns = 
        { vacancies_by_sector.columns[0]: 'Sector',
        vacancies_by_sector.columns[1]: 'Growth compared with last quarter (%)',
        vacancies_by_sector.columns[2]: 'Growth compared with same quarter in 2020 (%)'
        })
    vacancies_by_sector['Sector'] = vacancies_by_sector['Sector'].str.replace('<br>', '', regex=True)
    vacancies_by_sector.to_csv(os.path.join(DATA_DIR, 'quarterly_growth_all_sectors.csv'), index = False)
    
    #TODO: Use sector names instead of index - order may change
    key_youth_sectors = vacancies_by_sector.drop([0,1,2,3,5,7,8])
    key_youth_sectors['Sector'] = key_youth_sectors['Sector'].str.wrap(25)
    key_youth_sectors.to_csv(os.path.join(DATA_DIR, 'growth_key_youth_sectors.csv'), index = False)

    wanted_youth_sectors = vacancies_by_sector.drop([0,1,3,4,5,6,7])
    wanted_youth_sectors['Sector'] = wanted_youth_sectors['Sector'].str.wrap(25)
    wanted_youth_sectors.to_csv(os.path.join(DATA_DIR, 'growth_wanted_youth_sectors.csv'), index = False)

def summarise():
    monthly_vacancies = pd.read_csv(os.path.join(DATA_DIR, 'monthly_vacancies.csv'))
    quarterly_vacancies = pd.read_csv(os.path.join(DATA_DIR, 'quarterly_vacancies.csv'))
    last_monthly_date = monthly_vacancies.date.iloc[-1]
    last_quarterly_date = quarterly_vacancies.date.iloc[-1]

    last_quarterly_value = quarterly_vacancies.value.iloc[-1]

    growth_last_quarter = ((last_quarterly_value - quarterly_vacancies.value.iloc[-2]) / last_quarterly_value ) * 100
    
    last_period_label = lms_period_to_quarter_label(pd.to_datetime(last_monthly_date))
    last_quarter_label = lms_period_to_quarter_label(pd.to_datetime(last_quarterly_date))

    summary = pd.DataFrame({
    'Value': [
        monthly_vacancies.value.iloc[-1].round(1) * 1000,
        quarterly_vacancies.value.iloc[-1].round(1) * 1000,
        growth_last_quarter.round(1),
    ],
    'Note': [
        "Estimated number of open job vacancies in the last reported rolling quarter, {}.".format(last_period_label),
        "Estimated number of job vacancies in the last quarter, {}".format(last_quarter_label),
        "Estimated percentage change on last quarter, {}".format('TBC'),
    ], 
    'Suffix': [
        '',
        '',
        '%',
    ],
    },
    index=pd.Index([
        'Latest monthly vacancies',
        'Latest quarterly vacancies',
        'Growth on previous quarter',
    ], name='Title')
    )
    summary.loc['Growth on previous quarter', 'Suffix'] = '%'

    summary.fillna('N/A').to_csv(os.path.join(DATA_DIR, 'headlines.csv'))

    latest = pd.concat([
      pd.Series({
          'last_monthly_date': last_period_label,
          'last_quarterly_date': last_quarter_label,
      })
    ])
    latest.to_json(os.path.join(DASHBOARD_DIR, 'latest.json'), indent=2)


if __name__ == "__main__":
    prepare_vacancies()
    prepare_vacancies_by_sector()
    summarise()