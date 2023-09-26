import os 
import pandas as pd 

WORKING_DIR = os.path.join('working', 'upstream')
WORKING_DATA = os.path.join(WORKING_DIR, 'labour-market_latest_by_pcon_2010.csv')

DATA_DIR = os.path.join('src', 'maps', 'employment', '_data')

all_data = pd.read_csv(WORKING_DATA)

def filter_data(data, variable):
    return data.loc[
        data.variable_name == variable, 
        ['geography_code', 'value', 'notes']
    ]

if __name__ == '__main__':
  employment_rate_16_24 = filter_data(all_data, 'Employment rate - aged 16-24')
  employment_rate_16_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'employment_rate_16_24.csv'), index=False)

  unemployment_rate_16_64 = filter_data(all_data, 'Unemployment rate - aged 16-64 ')
  unemployment_rate_16_64.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_64.csv'), index=False)

  unemployment_rate_16_24 = filter_data(all_data, 'Unemployment rate - aged 16-24')
  unemployment_rate_16_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_24.csv'), index=False)