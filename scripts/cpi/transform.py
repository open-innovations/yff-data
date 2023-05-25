import os
import pandas as pd
from extract import CPI_LATEST, CPI_TIME_SERIES
from scripts.util.date import quarter_to_date, most_recent_stats
from scripts.util.util import slugify

DATA_DIR = os.path.realpath(os.path.join('data', 'cpi'))
HEADLINES_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'cpi'))
CPI_METADATA = os.path.join(DATA_DIR, 'metadata.json')
os.makedirs(DATA_DIR, exist_ok=True)

def read_meta():
    #read csv and make a new dataframe
    dates = pd.read_excel(CPI_LATEST, sheet_name='Contents', names=["Consumer Price Inflation"], skiprows=1, nrows=2, header=None)
    dates.columns = ['value']
    dates.index = pd.Index([
        "published",
        "next_update",
    ])
    #get just the dates
    dates.loc['published', 'value'] = dates.loc['published', 'value'].split(':')[1]
    dates.loc['next_update', 'value'] = dates.loc['next_update', 'value'].split(':')[1]
    dates.value.to_json(CPI_METADATA, date_format='iso')
    return dates
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

def summarise(stats): 
    cpi = pd.read_csv(os.path.join(DATA_DIR, 'cpi.csv'))

    latest = pd.DataFrame({
            'Monthly change' : (cpi['monthly_pct_change'].iloc[:1]).round(1),
            'Quarterly change' : (cpi['quarterly_pct_change'].iloc[:1]).round(1),
            'Yearly change' : (cpi['yearly_pct_change'].iloc[:1].round(1))
    }).T.reset_index()

    latest = latest.rename(columns = {'index': 'Title', 0: 'Value'})
    latest['Note'] = [
        "Consumer prices index change (%) on last month, as at {}".format(metadata.loc["published", "value"]),
        "Consumer prices index change (%) on last quarter, as at {}".format(metadata.loc["published", "value"]),
        "Consumer prices index change (%) on the same month last year, as at {}".format(metadata.loc["published", "value"])
    ]
    latest['Suffix'] = '%'
    latest.to_csv(os.path.join(HEADLINES_DIR, 'headlines.csv'), index=False)

if __name__ == "__main__":

    #use only the measures (see lookup table)
    measures = ['D7BT', 'D7BU', 'D7BW', 'D7BX', 'D7C4']

    #read the sheet, using indices as columns have no names
    data = pd.read_excel(CPI_LATEST, sheet_name='Table 21', index_col=1, skiprows=4, header=[0,1])
    table21 = data.loc[measures]
    most_recent_month = table21.iloc[:, -1:]
    last_month = table21.iloc[:, -2:-1]
    quarter = table21.iloc[:, -4:-3]
    year = table21.iloc[:, -13:-12]
    
    #getting the names of values to make a readable csv
    m1 = most_recent_month.columns[0][1]
    date = most_recent_month.columns[0][0]
    m2 = quarter.columns[0][1]
    m3 = year.columns[0][1]
    m4 = last_month.columns[0][1]
    df = pd.DataFrame()
    most_recent_month.rename(columns={m1: 'value'}, inplace=True)
    last_month.rename(columns={m4: 'value'}, inplace=True)
    quarter.rename(columns={m2: 'value'}, inplace=True)
    year.rename(columns={m3: 'value'}, inplace=True)

    #create a nicely formatted dataframe for pct change figures 
    df['monthly_pct_change'] = pct_change(most_recent_month[most_recent_month.columns[0][0]], last_month[last_month.columns[0][0]])
    df['quarterly_pct_change'] = pct_change(most_recent_month[most_recent_month.columns[0][0]], quarter[quarter.columns[0][0]])
    df['yearly_pct_change'] = pct_change(most_recent_month[most_recent_month.columns[0][0]], year[year.columns[0][0]])

    #remap codes to proper names and slugify
    column_name = pd.read_csv('working/lookups/MM23_variable_lookup.csv',
                          usecols=['code', 'name'], index_col='code').to_dict()['name']
    df.rename(index=column_name, inplace=True)
    df.rename(index=slugify, inplace=True)
    df.index.name = 'sector'
    df = df.round(2)
    df.rename(index={'cpi_index_01_food_and_non_alcoholic_beverages_2015_100': "Food & Non-Alcoholic Beverages",
                     'cpi_index_03_clothing_and_footwear_2015_100': "Clothing & Footwear",
                     'cpi_index_04_housing_water_and_fuels_2015_100': "Housing, Energy, Water & Fuels",
                     'cpi_index_09_recreation_&_culture_2015_100': "Recreation & Culture",
                     'cpi_index_00_all_items_2015_100': "All CPI Categories"},
                     inplace=True)
    #write file
    df.to_csv(os.path.join(DATA_DIR, 'cpi.csv'))

    #get the metadat and make headline stats
    metadata = read_meta()
    summarise(metadata)

    # time_series = pd.read_csv(CPI_TIME_SERIES, names=measures, header=0)
    # time_series.drop(labels=['PreUnit', 'Unit', 'Release Date', 'Next release', 'Important Notes'], axis=0, inplace=True)


