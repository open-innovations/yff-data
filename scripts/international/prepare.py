import pandas as pd
import os
import re

COUNTRY_LOOKUP = os.path.join('data', 'reference', 'country-lookup.csv')

WORKING_DIR = os.path.join('working', 'upstream')

OECD_NEET_DATA = os.path.join(
    WORKING_DIR, 'oecd-neet.csv'
)
OECD_WAGE_DATA = os.path.join(
    WORKING_DIR, 'oecd_wage_levels.csv'
)
OECD_ATTAINMENT_DATA = os.path.join(
    WORKING_DIR, 'oecd_education_attainment.csv'
)


DATA_DIR = os.path.join('src', 'areas', 'maps', 'international', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

oecd_neet_data = pd.read_csv(OECD_NEET_DATA).round(1)
oecd_wage_data = pd.read_csv(OECD_WAGE_DATA).round(1)
oecd_edu_attainment_data = pd.read_csv(OECD_ATTAINMENT_DATA).round(1)

country_reference = pd.read_csv(COUNTRY_LOOKUP).set_index('alpha-3')

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

def save_tidy_csv(df, directory, filename, with_index=True):
    # First add the header
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]], columns=df.columns)
    final = pd.concat([new_record, df], ignore_index=True)

    # Get the output as CSV
    csv = final.to_csv(index=with_index)

    # Because we added an index column we will now tidy
    csv = re.sub(r'\n0,---,---', '\n---,---,---', csv)

    text_file = open(os.path.join(directory, filename), "w")
    text_file.write(csv)
    text_file.close()

if __name__ == '__main__':

# PREPARE NEET DATA
    
    # Filter to the allowed fields
    neet_all = oecd_neet_data[['country_code', 'age_range', 'time', 'value']].dropna()

    # Merge in country lookup to add country names
    neet_all = pd.merge(neet_all, country_reference, how='left', left_on='country_code', right_index=True).rename(columns={'name': 'country'})

    # Pivot the table to arrange in columns with each combo
    neet_grouped = neet_all.pivot_table(index=['country_code', 'country'], columns=['age_range', 'time'], values='value').reset_index()

    save_tidy_csv(neet_grouped, os.path.join(DATA_DIR), 'neet_grouped.csv', with_index=False)



# PREPARE WAGES DATA 
    
    # Filter to the allowed fields
    wages_all = oecd_wage_data.drop(columns={'indicator', 'measure','frequency'}).dropna()

    # Merge in country lookup to add country names
    wages_all = pd.merge(wages_all, country_reference, how='left', left_on='country_code', right_index=True).rename(columns={'name':'country'})

    # Pivot the table to arrange in columns with each combo
    wages_grouped = wages_all.pivot_table(index=['country_code', 'country'], columns=['subject', 'time'], values='value').reset_index()

    save_tidy_csv(wages_grouped, os.path.join(DATA_DIR), 'wages_grouped.csv', with_index=False)


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

    
    


    
    
