import os
import pandas as pd
from extract import CPI_LATEST
from scripts.util.date import quarter_to_date, most_recent_stats

DATA_DIR = os.path.realpath(os.path.join('data', 'cpi'))
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename, sheet_name):
    data = pd.read_excel(filename, 
                         sheet_name=sheet_name,
                         skiprows=0,
                         header = [4, 8, 9],
                         index_col=0)
    data = data[data.iloc[:, 0].notna()]
    data.index.names = ['code']
    return data

if __name__ == "__main__":
    data = load_data(CPI_LATEST, sheet_name='Table 4')
    measures = ['CHZR', 'CHZT', 'CHZU', 'CHZZ']
    columns = [' Percentage change', 'Percentage change over 12 months']
    
    CPI_data = data.loc[measures]
    CPI_data = CPI_data[columns]

    #these are the most recent (end) columns for the 12 month and 
    # most recent month pct change data.
    print(CPI_data['Percentage change over 12 months'].iloc[:, -1:])
    print(CPI_data[' Percentage change'].iloc[:, -2:-1])
    