import pandas as pd
import os

WORKING_DIR = os.path.join('working', 'upstream')
OECD_EXAMPLE_DATA = os.path.join(
    WORKING_DIR, 'international.csv')

DATA_DIR = os.path.join('src', 'maps', 'international', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

oecd_example_data = pd.read_csv(OECD_EXAMPLE_DATA)

def filter_data(data, variable, filter_field):
    return data.loc[data[filter_field] == variable]

def save_to_file(data, filename):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data

def calculate_rates(data):
    data.value = data.value.astype(float)
    data['value'] = (data['value']  * 100).round(1)
    return data

if __name__ == '__main__':

    oecd_example_data = oecd_example_data.rename(columns={
        'COUNTRY': 'country_code'
    })
    oecd_example_data.columns = oecd_example_data.columns.str.lower()

    unemployment_all_15_24 = filter_data(oecd_example_data, 2022, 'time').pipe(
        filter_data, 'Unemployment', 'series').pipe(
            filter_data, 'All persons', 'sex').pipe(
                filter_data, '15 to 24', 'age').pipe(
                    save_to_file, 'unemployment_all_15_24.csv') 
    
    unemployment_all_15_24_table = unemployment_all_15_24.sort_values(by=['value'], ascending=False).head(20).iloc[1:].rename(columns= { 'country': 'Country', 'value':'Number of people (thousands)'}).pipe(
        save_to_file, 'unemployment_all_15_24_table.csv'
    )
    
    unemployment_women_15_24 = filter_data(oecd_example_data, 2022, 'time').pipe(
        filter_data, 'Unemployment', 'series').pipe(
            filter_data, 'Women', 'sex').pipe(
                filter_data, '15 to 24', 'age').pipe(
                    save_to_file, 'unemployment_women_15_24.csv') 
    
    unemployment_women_15_24_table = unemployment_women_15_24.sort_values(by=['value'], ascending=False).head(20).iloc[1:].rename(columns= { 'country': 'Country', 'value':'Number of people (thousands)'}).pipe(
        save_to_file, 'unemployment_women_15_24_table.csv')
    
    unemployment_men_15_24 = filter_data(oecd_example_data, 2022, 'time').pipe(
        filter_data, 'Unemployment', 'series').pipe(
            filter_data, 'Men', 'sex').pipe(
                filter_data, '15 to 24', 'age').pipe(
                    save_to_file, 'unemployment_men_15_24.csv') 
    
    unemployment_men_15_24_table = unemployment_men_15_24.sort_values(by=['value'], ascending=False).head(20).iloc[1:].rename(columns= { 'country': 'Country', 'value':'Number of people (thousands)'}).pipe(
    save_to_file, 'unemployment_men_15_24_table.csv')

    #Employment 

    employment_all_15_24 = filter_data(oecd_example_data, 2022, 'time').pipe(
        filter_data, 'Employment', 'series').pipe(
            filter_data, 'All persons', 'sex').pipe(
                filter_data, '15 to 24', 'age').pipe(
                    save_to_file, 'employment_all_15_24.csv') 
    
    employment_all_15_24_table = employment_all_15_24.sort_values(by=['value'], ascending=False).head(20).iloc[1:].rename(columns= { 'country': 'Country', 'value':'Number of people (thousands)'}).pipe(
        save_to_file, 'employment_all_15_24_table.csv'
    )
    
    employment_women_15_24 = filter_data(oecd_example_data, 2022, 'time').pipe(
        filter_data, 'Employment', 'series').pipe(
            filter_data, 'Women', 'sex').pipe(
                filter_data, '15 to 24', 'age').pipe(
                    save_to_file, 'employment_women_15_24.csv') 
    
    employment_women_15_24_table = employment_women_15_24.sort_values(by=['value'], ascending=False).head(20).iloc[1:].rename(columns= { 'country': 'Country', 'value':'Number of people (thousands)'}).pipe(
        save_to_file, 'employment_women_15_24_table.csv')
    
    employment_men_15_24 = filter_data(oecd_example_data, 2022, 'time').pipe(
        filter_data, 'Employment', 'series').pipe(
            filter_data, 'Men', 'sex').pipe(
                filter_data, '15 to 24', 'age').pipe(
                    save_to_file, 'employment_men_15_24.csv') 
    
    employment_men_15_24_table = employment_men_15_24.sort_values(by=['value'], ascending=False).head(20).iloc[1:].rename(columns= { 'country': 'Country', 'value':'Number of people (thousands)'}).pipe(
    save_to_file, 'employment_men_15_24_table.csv')

    
    
    


    
    
