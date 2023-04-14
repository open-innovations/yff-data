import os
import pandas as pd
from extract import CPI_LATEST
from scripts.util.date import quarter_to_date, most_recent_stats

DATA_DIR = os.path.realpath(os.path.join('data', 'cpi'))
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename, sheet_name, header=None, index_col=None):
    data = pd.read_excel(filename, 
                         sheet_name=sheet_name,
                         skiprows=0,
                         header=header,
                         index_col=index_col)
    data = data[data.iloc[:, 0].notna()]
    data.index.names = ['code']
    return data

if __name__ == "__main__":
    data = load_data(CPI_LATEST, sheet_name='Table 4', header=[4, 8, 9], index_col=1)

    measures = ['D7BU', 'D7BW', 'D7BX', 'D7C4']
    columns = [' Percentage change', 'Percentage change over 12 months']
    
    CPI_data = data.loc[measures]
    CPI_data = CPI_data[columns]

    #these are the most recent (end) columns for the 12 month and 
    # most recent month pct change data.
    pct_change_12_months = CPI_data['Percentage change over 12 months'].iloc[:, -1:]
    pct_change_1_month = CPI_data[' Percentage change'].iloc[:, -2:-1]
    
    #merge and rename the two frames
    df = pct_change_1_month.merge(pct_change_12_months, left_index=True, right_index=True)
    df.rename(columns={'Unnamed: 12_level_2': 'pct_change_1_month', 'Unnamed: 22_level_2': 'pct_change_12_months'}, inplace=True)

    #select only the values we need.
    month = df.columns[0][0]
    df = df[month]
    

    #data2 = load_data(CPI_LATEST, sheet_name='Table 21', header=[5,6], index_col=2)
    data2 = pd.read_excel(CPI_LATEST, sheet_name='Table 21', index_col=1, skiprows=4, header=[0,1])
    table21 = data2.loc[measures]
    most_recent_month = table21.iloc[:, -1:]
    quarter = table21.iloc[:, -4:-3]
    
    m1 = most_recent_month.columns[0][1]
    m2 = quarter.columns[0][1]
    
    most_recent_month.rename(columns={m1: 'quarterly_idx_change'}, inplace=True)
    quarter.rename(columns={m2: 'quarterly_idx_change'}, inplace=True)
    quarterly_change = most_recent_month[most_recent_month.columns[0][0]] - quarter[quarter.columns[0][0]]
   
    df['quarterly_idx_change'] = quarterly_change
    column_name = pd.read_csv('working/lookups/MM23_variable_lookup.csv',
                          usecols=['code', 'name'], index_col='code').to_dict()['name']
    dates = pd.Series(data={'latest_month': month, 'quarterly': m2})
    df.rename(index=column_name, inplace=True)
    df.to_csv(os.path.join(DATA_DIR, 'CPI.csv'))
    dates.to_json(os.path.join(DATA_DIR, 'dates.json'))
    
    
    