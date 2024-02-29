import pandas as pd
import os

WORKING_DIR = os.path.join('working', 'upstream')
OECD_LFS_DATA = os.path.join(
    WORKING_DIR, 'oecd_lfs_by_sex_and_age.csv')
OECD_NEET_DATA = os.path.join(
    WORKING_DIR, 'oecd-neet.csv'
)
OECD_WAGE_DATA = os.path.join(
    WORKING_DIR, 'oecd_wage_levels.csv'
)
OECD_ATTAINMENT_DATA = os.path.join(
    WORKING_DIR, 'oecd_education_attainment.csv'
)


DATA_DIR = os.path.join('src', 'maps', 'international', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

oecd_lfs_data = pd.read_csv(OECD_LFS_DATA).round(1)
oecd_neet_data = pd.read_csv(OECD_NEET_DATA).round(1)
oecd_wage_data = pd.read_csv(OECD_WAGE_DATA).round(1)
oecd_edu_attainment_data = pd.read_csv(OECD_ATTAINMENT_DATA).round(1)



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

# PREPARE NEET DATA
    

    neet_15_19_all = filter_data(oecd_neet_data, '15_19', 'age_range').pipe(
        filter_data, 2022, 'time').pipe(save_to_file, 'neet_15_19_all.csv')

    neet_15_19_women = filter_data(oecd_neet_data, '15_19_WOMEN', 'age_range').pipe(
        filter_data, 2022, 'time').pipe(save_to_file, 'neet_15_19_women.csv')

    neet_15_19_men = filter_data(oecd_neet_data, '15_19_MEN', 'age_range').pipe(
        filter_data, 2022, 'time').pipe(save_to_file, 'neet_15_19_men.csv')

    neet_20_24_all = filter_data(oecd_neet_data, '20_24', 'age_range').pipe(
        filter_data, 2022, 'time').pipe(save_to_file, 'neet_20_24_all.csv')
    
    neet_20_24_women = filter_data(oecd_neet_data, '20_24_WOMEN', 'age_range').pipe(
    filter_data, 2022, 'time').pipe(save_to_file, 'neet_20_24_women.csv')

    neet_20_24_men = filter_data(oecd_neet_data, '20_24_MEN', 'age_range').pipe(
        filter_data, 2022, 'time').pipe(save_to_file, 'neet_20_24_men.csv')
    
    neet_15_29_all = filter_data(oecd_neet_data, '15_29', 'age_range').pipe(
        filter_data, 2022, 'time').pipe(save_to_file, 'neet_15_29_all.csv')
    
    neet_15_29_women = filter_data(oecd_neet_data, '15_29_WOMEN', 'age_range').pipe(
    filter_data, 2022, 'time').pipe(save_to_file, 'neet_15_29_women.csv')

    neet_15_29_men = filter_data(oecd_neet_data, '15_29_MEN', 'age_range').pipe(
        filter_data, 2022, 'time').pipe(save_to_file, 'neet_15_29_men.csv')


# PREPARE WAGES DATA 
    
    wages_lpay = filter_data(oecd_wage_data, 2021, 'time').pipe(
        filter_data, 'LPAY', 'subject').pipe(save_to_file, 'wages_lpay.csv')

    wages_hpay = filter_data(oecd_wage_data, 2021, 'time').pipe(
        filter_data, 'HPAY', 'subject').pipe(save_to_file, 'wages_hpay.csv')


# PREPARE EDUCATION ATTAINMENT
    
    # Level 0/1 
    empl_rates_lit_0_1_below_sec = filter_data(oecd_edu_attainment_data, 'Below upper secondary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L0_1', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_0_1_below_sec.csv')

    empl_rates_lit_0_1_upper_sec = filter_data(oecd_edu_attainment_data, 'Upper secondary education or post-secondary non-tertiary', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L0_1', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_0_1_upper_sec.csv')
    
    empl_rates_lit_0_1_tertiary = filter_data(oecd_edu_attainment_data, 'Tertiary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L0_1', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_0_1_tertiary.csv')


    # Level 2
    empl_rates_lit_level_2_below_sec = filter_data(oecd_edu_attainment_data, 'Below upper secondary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L2', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_2_below_sec.csv')
    
    empl_rates_lit_level_2_upper_sec = filter_data(oecd_edu_attainment_data, 'Upper secondary education or post-secondary non-tertiary', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L2', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_2_upper_sec.csv')
    
    empl_rates_lit_level_2_tertiary = filter_data(oecd_edu_attainment_data, 'Tertiary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L2', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_2_tertiary.csv')


    # Level 3
    empl_rates_num_level_3_below_sec = filter_data(oecd_edu_attainment_data, 'Below upper secondary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L3', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_3_below_sec.csv')
    
    empl_rates_num_level_3_upper_sec = filter_data(oecd_edu_attainment_data, 'Upper secondary education or post-secondary non-tertiary', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L3', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_3_upper_sec.csv')
    
    empl_rates_num_level_3_tertiary = filter_data(oecd_edu_attainment_data, 'Tertiary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L3', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_3_tertiary.csv')

    # Level 4/5
    empl_rates_num_level_4_5_below_sec = filter_data(oecd_edu_attainment_data, 'Below upper secondary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L4_5', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_4_5_below_sec.csv')
    
    empl_rates_num_level_4_5_upper_sec = filter_data(oecd_edu_attainment_data, 'Upper secondary education or post-secondary non-tertiary', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L4_5', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_4_5_upper_sec.csv')
    
    empl_rates_num_level_4_5_tertiary = filter_data(oecd_edu_attainment_data, 'Tertiary education', 'isced').pipe(
        filter_data, 'Employment rates, by literacy proficiency level ', 'indicator').pipe(
            filter_data, 'L4_5', 'piaac_category_code').pipe(
                filter_data, 'Value', 'measure').pipe(save_to_file, 'empl_rates_lit_level_4_5_tertiary.csv')



    
    


    
    
