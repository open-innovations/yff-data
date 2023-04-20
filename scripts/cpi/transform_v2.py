import os
import pandas as pd
from extract import CPI_LATEST
from scripts.util.date import quarter_to_date, most_recent_stats
from scripts.util.util import slugify

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
def pct_change(col1, col2):
    return ((col1 - col2) / col2)*100
if __name__ == "__main__":

    measures = ['D7BU', 'D7BW', 'D7BX', 'D7C4']

    data = pd.read_excel(CPI_LATEST, sheet_name='Table 21', index_col=1, skiprows=4, header=[0,1])
    table21 = data.loc[measures]
    most_recent_month = table21.iloc[:, -1:]
    last_month = table21.iloc[:, -2:-1]
    quarter = table21.iloc[:, -4:-3]
    year = table21.iloc[:, -13:-12]
    
    m1 = most_recent_month.columns[0][1]
    m2 = quarter.columns[0][1]
    m3 = year.columns[0][1]
    m4 = last_month.columns[0][1]
    df = pd.DataFrame()
    most_recent_month.rename(columns={m1: 'value'}, inplace=True)
    last_month.rename(columns={m4: 'value'}, inplace=True)
    quarter.rename(columns={m2: 'value'}, inplace=True)
    year.rename(columns={m3: 'value'}, inplace=True)

    #print(most_recent_month[most_recent_month.columns[0][0]], quarter[quarter.columns[0][0]], year)
    df['monthly_pct_change'] = pct_change(most_recent_month[most_recent_month.columns[0][0]], last_month[last_month.columns[0][0]])
    df['quarterly_pct_change'] = pct_change(most_recent_month[most_recent_month.columns[0][0]], quarter[quarter.columns[0][0]])
    df['yearly_pct_change'] = pct_change(most_recent_month[most_recent_month.columns[0][0]], year[year.columns[0][0]])
    stats = pd.Series(data={'CPI_most_recent_month': m1, 'CPI_last_month': m4, 'CPI_last_quarter': m2})

    #remap codes to proper names
    column_name = pd.read_csv('working/lookups/MM23_variable_lookup.csv',
                          usecols=['code', 'name'], index_col='code').to_dict()['name']
    df.rename(index=column_name, inplace=True)
    df.rename(index=slugify, inplace=True)
    df.index.name = 'sector'
    print(df)
    df.to_csv(os.path.join(DATA_DIR, 'CPI.csv'))
    stats.to_json(os.path.join(DATA_DIR, 'stats.json'))
    
    

    
    
    
    