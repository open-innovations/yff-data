import os 
import pandas as pd 

WORKING_DIR = os.path.join('working', 'upstream')
CONSTITUENCY_DATA = os.path.join(WORKING_DIR, 'labour-market_latest_by_pcon_2010.csv')
COMBINED_DATA = os.path.join(WORKING_DIR, 'labour-market_most_recent_by_pcon_2010.csv')
LOCAL_AUTHORITY_DATA = os.path.join(WORKING_DIR, 'labour-market_by_local_authority.csv')

DATA_DIR = os.path.join('src', 'maps', 'employment', '_data')

constituency_data = pd.read_csv(CONSTITUENCY_DATA)
local_authority_data = pd.read_csv(LOCAL_AUTHORITY_DATA)
combined_data = pd.read_csv(COMBINED_DATA)

def filter_data(data, variable):
    return data.loc[
        data.variable_name == variable, 
        ['geography_code', 'value', 'notes']
    ]

if __name__ == '__main__':


# Consituencies
  unemployment_rate_16_24 = filter_data(constituency_data, 'Unemployment rate - aged 16-64')
  unemployment_rate_16_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_64.csv'), index=False)

  unemployment_rate_16_19 = filter_data(constituency_data, 'Unemployment rate - aged 16-19')
  unemployment_rate_16_19.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_19.csv'), index=False)

  unemployment_rate_20_24 = filter_data(constituency_data, 'Unemployment rate - aged 20-24')
  unemployment_rate_20_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_20_24.csv'), index=False)

# Combined dates
  unemployment_rate_16_24 = filter_data(combined_data, 'Unemployment rate - aged 16-64')
  unemployment_rate_16_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_64_combined.csv'), index=False)

  unemployment_rate_16_19 = filter_data(combined_data, 'Unemployment rate - aged 16-19')
  unemployment_rate_16_19.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_19_combined.csv'), index=False)

  unemployment_rate_20_24 = filter_data(combined_data, 'Unemployment rate - aged 20-24')
  unemployment_rate_20_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_20_24_combined.csv'), index=False)


# Local authority
  unemployment_rate_16_24 = filter_data(local_authority_data, 'Unemployment rate - aged 16-64')
  unemployment_rate_16_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_64_LA.csv'), index=False)

  unemployment_rate_16_19 = filter_data(local_authority_data, 'Unemployment rate - aged 16-19')
  unemployment_rate_16_19.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_16_19_LA.csv'), index=False)

  unemployment_rate_20_24 = filter_data(local_authority_data, 'Unemployment rate - aged 20-24')
  unemployment_rate_20_24.fillna(0).to_csv(os.path.join(DATA_DIR, 'unemployment_rate_20_24_LA.csv'), index=False)



