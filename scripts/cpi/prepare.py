import os
import pandas as pd
import shutil
from scripts.util.util import slugify
from transform import DATA_DIR as INPUTS_DIR
from transform import n
OUTPUTS_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'cpi'))
CPI_METADATA = os.path.join(INPUTS_DIR, 'metadata.json')

def read_meta():
    #read csv and make a new dataframe
    metadata = pd.read_csv('working/metadata.csv')
    metadata = metadata[metadata.id == 'MM23'].reset_index()
    next_update = iso_to_named_date(metadata['next_update'].iloc[0])
    published = iso_to_named_date(metadata['last_update'].iloc[0])
    dates = pd.Series(data={'published': published, 'next_update': next_update}, index=['published', 'next_update'])
    dates.to_json(CPI_METADATA, date_format='iso')
    return dates

def pct_change(col1, col2):
    return ((col1 - col2) / col2)*100

def iso_to_named_date(date):
    stamp = pd.Timestamp(f'{date}')
    text = [f'{stamp.day}', stamp.month_name(), f'{stamp.year}']
    sep = ' ' 
    return sep.join(text)

def summarise(metadata): 
    cpi = pd.read_csv(os.path.join(INPUTS_DIR, 'cpi_barchart.csv'))
    
    latest = pd.DataFrame({
            'monthly_pct_change' : (cpi['monthly_pct_change'].iloc[:1]),
            'quarterly_pct_change' : (cpi['quarterly_pct_change'].iloc[:1]),
            'yearly_pct_change' : (cpi['yearly_pct_change'].iloc[:1])
    }).T.reset_index()

    latest = latest.rename(columns = {'index': 'sector', 0: 'Value'})
    latest['Suffix'] = '%'
    latest = latest.round(1)
    indicator = pd.read_csv('data/cpi/indicator.csv', index_col='sector')
    d = metadata.loc['published']
    latest['Note'] = [
        "As at {date}. This is {indicator} since the last update.".format(date=d, indicator=indicator.iloc[0,0]),
        "As at {date}. This is {indicator} since the last update.".format(date=d, indicator=indicator.iloc[1,0]),
        "As at {date}. This is {indicator} since the last update.".format(date=d, indicator=indicator.iloc[2,0])
    ]
    merged_df = latest.join(indicator, on='sector').set_index('sector')
    merged_df = merged_df.rename(index={'monthly_pct_change': 'Monthly', 'quarterly_pct_change':'Quarterly', 'yearly_pct_change':'Yearly'})
    merged_df.to_csv(os.path.join(INPUTS_DIR, 'headlines.csv'), index=True)


def bar_chart(data, n, make_indicator=True):
    most_recent_month = data.iloc[-n:]
    last_month = data.iloc[int(-2*n):-n]
    last_quarter = data.iloc[int(-4*n):int(-3*n)]
    last_year = data.iloc[int(-13*n):int(-12*n)]

    second_last_month = data.iloc[int(-3*n):int(-2*n)]
    second_last_quarter = data.iloc[int(-5*n):int(-4*n)]
    second_last_year = data.iloc[int(-14*n):int(-13*n)]
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
    df.rename(index={'cpi_index_00_all_items_2015_100': "All CPI Categories",
                     'cpi_index_01_food_and_non_alcoholic_beverages_2015_100': "Food & non-alcoholic beverages",
                     'cpi_index_02_alcoholic_beverages_tobacco_&_narcotics_2015_100': 'Alcoholic beverages & tobacco',
                     'cpi_index_03_clothing_and_footwear_2015_100': "Clothing & footwear",
                     'cpi_index_04_housing_water_and_fuels_2015_100': "Housing, water, electricity, gas & other fuels",
                     'cpi_index_05_furn_hh_equip_&_routine_repair_of_house_2015_100': 'Furniture, household equipment & maintenance',
                     'cpi_index_06_health_2015_100': 'Health',
                     'cpi_index_07_transport_2015_100': 'Transport',
                     'cpi_index_08_communication_2015_100': 'Communication',
                     'cpi_index_09_recreation_&_culture_2015_100': "Recreation & culture",
                     'cpi_index_10_education_2015_100': 'Education',
                     'cpi_index_11_hotels_cafes_and_restaurants_2015_100': 'Restaurants & hotels',
                     'cpi_index_12_miscellaneous_goods_and_services_2015_100': 'Miscellaneous goods & services'},
                     inplace=True)
    indicators = []
    sgn = []
    index = ['monthly_pct_change', 'quarterly_pct_change', 'yearly_pct_change']
    for i in index:
        if df.loc['All CPI Categories', i] > 0:
            sgn.append('+')
    if pct_change(last_month.loc['D7BT'].value, second_last_month.loc['D7BT'].value) < pct_change(most_recent_month.loc['D7BT'].value, last_month.loc['D7BT'].value):
        indicators.append('an increase')
    else:
        indicators.append('a decrease')

    if pct_change(second_last_month.loc['D7BT'].value, second_last_quarter.loc['D7BT'].value) < pct_change(most_recent_month.loc['D7BT'].value, last_quarter.loc['D7BT'].value):
        indicators.append('an increase')
    else:
        indicators.append('a decrease')

    if pct_change(second_last_month.loc['D7BT'].value, second_last_year.loc['D7BT'].value) < pct_change(most_recent_month.loc['D7BT'].value, last_year.loc['D7BT'].value):
        indicators.append('an increase')
    else:
        indicators.append('a decrease')
    if make_indicator == True:
        indicator = pd.DataFrame(data={'indicator': indicators, 'sign': sgn}, index=index)
        indicator.index.rename('sector', inplace=True)
        indicator.to_csv(os.path.join(INPUTS_DIR, 'indicator.csv'))
        #print(indicator)
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
    df['date_axis_label'] = df.named_date.str.replace(' ', '\\n')
    return df

def copy_file(name):
    shutil.copyfile(
        os.path.join(INPUTS_DIR, name),
        os.path.join(OUTPUTS_DIR, name)
    )
def youth_average(data):
    data.loc['Youth-focused average',:] = data.iloc[1:].mean(axis=0, numeric_only=True)
    return data
if __name__ == '__main__':

    data = pd.read_csv(os.path.join(INPUTS_DIR, 'transformed_cpi.csv'), index_col='variable')
    bar = bar_chart(data, n).drop(index=["Furniture, household equipment & maintenance",
                                          'Health',
                                          'Transport',
                                          'Communication',
                                          'Alcoholic beverages & tobacco',
                                          'Education',
                                          "Restaurants & hotels",
                                          'Miscellaneous goods & services'])
    bar = youth_average(bar)
    summary_bar = bar.reindex(index=['All CPI Categories', 'Youth-focused average'])
    bar = bar.reindex(index=['Food & non-alcoholic beverages', "Clothing & footwear",
                             "Housing, water, electricity, gas & other fuels",'Recreation & culture'])
    all_categories = bar_chart(data, n, make_indicator=False)
    line = line_chart(data, n, num_years=10)
    line['Youth-focused average'] = line[['cpi_index_01_food_and_non_alcoholic_beverages_2015_100',
                                         'cpi_index_03_clothing_and_footwear_2015_100',
                                         'cpi_index_04_housing_water_and_fuels_2015_100',
                                         'cpi_index_09_recreation_&_culture_2015_100']].mean(axis=1, numeric_only=True)
    #print(line)
    #write file
    bar.to_csv(os.path.join(INPUTS_DIR, 'cpi_barchart.csv'))
    summary_bar.to_csv(os.path.join(INPUTS_DIR, 'cpi_summary_barchart.csv'))
    all_categories.to_csv(os.path.join(INPUTS_DIR, 'cpi_all_category_bar_chart.csv'))
    line.to_csv(os.path.join(INPUTS_DIR, 'cpi_linechart.csv'))
    #get the metadat and make headline stats
    metadata = read_meta()
    summarise(metadata)

    #copy files to other directory
    copy_file("cpi_barchart.csv")
    copy_file("cpi_summary_barchart.csv")
    copy_file("cpi_linechart.csv")
    copy_file("metadata.json")
    copy_file("headlines.csv")
    copy_file("cpi_all_category_bar_chart.csv")
    copy_file("indicator.csv")