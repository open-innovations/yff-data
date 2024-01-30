import pandas as pd
import os

WORKING_DIR = os.path.join('working', 'upstream')
OECD_LFS_DATA = os.path.join(
    WORKING_DIR, 'oecd_lfs_by_sex_and_age.csv')

DATA_DIR = os.path.join('src', 'maps', 'international', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

oecd_lfs_data = pd.read_csv(OECD_LFS_DATA).round(1)

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


    employment_rate_total = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Employment rate', 'measure').pipe(
            filter_data, 'Total', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'employment_rate_total_15_over.csv') 
    
    #     unemployment_all_15_24_table = unemployment_all_15_24.sort_values(by=['value'], ascending=False).head(20).iloc[1:].rename(columns= { 'country': 'Country', 'value':'Number of people (thousands)'}).pipe(
    #     save_to_file, 'unemployment_all_15_24_table.csv'
    # )
    
    employment_rate_female = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Employment rate', 'measure').pipe(
            filter_data, 'Female', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'employment_rate_female_15_over.csv') 
    

    employment_rate_male = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Employment rate', 'measure').pipe(
            filter_data, 'Male', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'employment_rate_male_15_over.csv') 
    


    # Unemployment

    umemployment_rate_total = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Unemployment rate', 'measure').pipe(
            filter_data, 'Total', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'unemployment_rate_total_15_over.csv') 
    
    unemployment_rate_female = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Unemployment rate', 'measure').pipe(
            filter_data, 'Female', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'unemployment_rate_female_15_over.csv') 
    

    unemployment_rate_male = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Unemployment rate', 'measure').pipe(
            filter_data, 'Male', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'unemployment_rate_male_15_over.csv') 
    

    
    # Economic Inactivity rate

    economic_inactivity_rate_total = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Inactivity rate', 'measure').pipe(
            filter_data, 'Total', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'economic_inactivity_rate_total.csv') 
    
    economic_inactivity_rate_female = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Inactivity rate', 'measure').pipe(
            filter_data, 'Female', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'economic_inactivity_rate_female.csv') 
    

    economic_inactivity_rate_male = filter_data(oecd_lfs_data, 2022, 'time_period').pipe(
        filter_data, 'Inactivity rate', 'measure').pipe(
            filter_data, 'Male', 'sex').pipe(
                filter_data, '15 years or over', 'age').pipe(
                    save_to_file, 'economic_inactivity_rate_male.csv') 


    


    
    
    


    
    
