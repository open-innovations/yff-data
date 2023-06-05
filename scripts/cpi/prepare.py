import os
import pandas as pd
import shutil
from extract import CPI_LATEST
from scripts.util.util import slugify
from transform import DATA_DIR as INPUTS_DIR
from transform import n
OUTPUTS_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'cpi'))
CPI_METADATA = os.path.join(INPUTS_DIR, 'metadata.json')

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

def pct_change(col1, col2):
    return ((col1 - col2) / col2)*100

def summarise(metadata): 
    cpi = pd.read_csv(os.path.join(INPUTS_DIR, 'cpi_barchart.csv'))

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
    latest.to_csv(os.path.join(INPUTS_DIR, 'headlines.csv'), index=False)


def bar_chart(data, n):
    most_recent_month = data.iloc[-n:]
    last_month = data.iloc[int(-2*n):-n]
    last_quarter = data.iloc[int(-4*n):int(-3*n)]
    last_year = data.iloc[int(-13*n):int(-12*n)]
    df = pd.DataFrame()
    df['monthly_pct_change'] = pct_change(most_recent_month.value, last_month.value)
    df['quarterly_pct_change'] = pct_change(most_recent_month.value, last_quarter.value)
    df['yearly_pct_change'] = pct_change(most_recent_month.value, last_year.value)
    #print(df)

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
    return df

def line_chart(data, n, num_years):
    #times by 12 as the data is monthly.
    #n is number of measures we are using
    df = data.iloc[int(-n*12*num_years):].reset_index()
    df = df.pivot(index='dates.date', values='value', columns='variable').reset_index()
    df.index.rename('index', inplace=True)
    column_name = pd.read_csv('working/lookups/MM23_variable_lookup.csv',
                          usecols=['code', 'name'], index_col='code').to_dict()['name']
    df.rename(columns=column_name, inplace=True)
    df.rename(columns=slugify, inplace=True)
    df['named_date'] = pd.to_datetime(df['dates.date']).dt.strftime('%b %Y')
    return df

def copy_file(name):
    shutil.copyfile(
        os.path.join(INPUTS_DIR, name),
        os.path.join(OUTPUTS_DIR, name)
    )

if __name__ == '__main__':

    data = pd.read_csv(os.path.join(INPUTS_DIR, 'transformed_cpi.csv'), index_col='variable')
    bar = bar_chart(data, n=5)
    line = line_chart(data, n=5, num_years=10)
    
    #write file
    bar.to_csv(os.path.join(INPUTS_DIR, 'cpi_barchart.csv'))
    line.to_csv(os.path.join(INPUTS_DIR, 'cpi_linechart.csv'))
    #get the metadat and make headline stats
    metadata = read_meta()
    summarise(metadata)

    #copy file to other directory
    copy_file("cpi_barchart.csv")
    copy_file("cpi_linechart.csv")
    copy_file("metadata.json")
    copy_file("headlines.csv")