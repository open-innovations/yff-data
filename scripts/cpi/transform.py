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
    data = load_data(CPI_LATEST, sheet_name='Table 4', header=[4, 8, 9], index_col=0)
    measures = ['CHZR', 'CHZT', 'CHZU', 'CHZZ']
    columns = [' Percentage change', 'Percentage change over 12 months']
    
    CPI_data = data.loc[measures]
    CPI_data = CPI_data[columns]

    #these are the most recent (end) columns for the 12 month and 
    # most recent month pct change data.
    pct_change_12_months = CPI_data['Percentage change over 12 months'].iloc[:, -1:]
    pct_change_1_month = CPI_data[' Percentage change'].iloc[:, -2:-1]
    #print(pct_change_12_months)
    #rint(pct_change_1_month)
    df = pct_change_1_month.merge(pct_change_12_months, left_index=True, right_index=True)
    df.rename(columns={'Unnamed: 12_level_2': 'pct_change_1_month', 'Unnamed: 22_level_2': 'pct_change_12_months'}, inplace=True)
    #print(df.droplevel(df.columns[0]))
    month = df.columns[0][0]
    df = df[month]
    df.to_csv(os.path.join(DATA_DIR, 'CPI.csv'))

    #data2 = load_data(CPI_LATEST, sheet_name='Table 21', header=[5,6], index_col=2)
    data2 = pd.read_excel(CPI_LATEST, sheet_name='Table 21', index_col=1, skiprows=4, header=[0,1])
    measures2 = ['D7BU', 'D7BW', 'D7BX', 'D7C4']
    table21 = data2.loc[measures2]
    most_recent_month = table21.iloc[:, -1:]
    quarter = table21.iloc[:, -4:-3]
    most_recent_month.astype('float', errors='ignore')
    quarter.astype('float', errors='ignore')
    quarterly_change = most_recent_month.subtract(quarter, fill_value=None)
    print(quarterly_change)

    
    