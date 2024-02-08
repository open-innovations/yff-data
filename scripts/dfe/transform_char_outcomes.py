import os
import pandas as pd 

WORKING_DIR = os.path.join('working', 'upstream')

KS4_CHAR_OUTCOMES_DATA = os.path.join(
    WORKING_DIR, 'ks4_char_outcomes.csv')

char_outcomes_data = pd.read_csv(KS4_CHAR_OUTCOMES_DATA)

fields = ['new_la_code', 'time_period', 'version', 'gender', 'breakdown', 'ethnicity_major', 
          'free_school_meals', 'sen_status', 'sen_description', 'disadvantage', 'first_language', 'variable', 'value']

ATT8_DIR = os.path.join('src', 'maps', 'education', '_data', 'view', 'ks4_char_outcomes', 'avg_att8')
os.makedirs(ATT8_DIR, exist_ok=True)

P8_DIR = os.path.join('src', 'maps', 'education', '_data', 'view', 'ks4_char_outcomes', 'avg_p8')
os.makedirs(P8_DIR, exist_ok=True)

def filter_data(data, variable, fields, filter_field):
    return data.loc[data[filter_field] == variable, fields]

def save_to_file(data, filename, DATA_DIR):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data

def clean_nulls(data):
    return data.dropna()


if __name__ == '__main__':

    char_outcomes_data = char_outcomes_data.dropna().drop(columns= [
        'education_investment_area_flag',
        'priority_area_flag',
        'establishment_type'
    ])

    # ATTAINMENT 8 SCORES
    
    # Filter by gender

    boys_total_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Total', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Boys', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'boys_total_char_outcomes.csv', ATT8_DIR) 
    
    girls_total_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Total', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Girls', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'girls_total_char_outcomes.csv', ATT8_DIR) 
    

    # Filter by ethnicity

    ethnicity_asian_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Asian', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_asian_ks4_char_outcomes.csv', ATT8_DIR) 
    
    ethnicity_black_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Black', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_black_ks4_char_outcomes.csv', ATT8_DIR) 
    
    ethnicity_mixed_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Mixed', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_mixed_ks4_char_outcomes.csv', ATT8_DIR) 
    
    ethnicity_other_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Other', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_other_ks4_char_outcomes.csv', ATT8_DIR)
    
    ethnicity_unclassified_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Unclassified', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_unclassified_ks4_char_outcomes.csv', ATT8_DIR)
    
    ethnicity_white_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'White', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_white_ks4_char_outcomes.csv', ATT8_DIR)
    

    # Filter by free school meal eligibility

    fsm_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Free school meals', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'FSM', fields=fields, filter_field='free_school_meals').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'fsm_char_outcomes.csv', ATT8_DIR)
    
    fsm_all_other_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Free school meals', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'FSM all other', fields=fields, filter_field='free_school_meals').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'fsm_all_other_char_outcomes.csv', ATT8_DIR)
    
    # Filter by SEN status 

    no_SEN_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN status', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'No SEN', fields=fields, filter_field='sen_status').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'no_SEN_char_outcomes.csv', ATT8_DIR)
    
    SEN_state_EHC_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN status', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'SEN State EHC', fields=fields, filter_field='sen_status').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'SEN_state_EHC_char_outcomes.csv', ATT8_DIR)
    
    SEN_supp_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN status', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'SEN Supp', fields=fields, filter_field='sen_status').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'SEN_supp_char_outcomes.csv', ATT8_DIR)
    
    # Filter by SEN description

    any_SEN_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN description', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Any SEN', fields=fields, filter_field='sen_description').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'any_SEN_char_outcomes.csv', ATT8_DIR)
    
    no_identified_SEN_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN description', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'No identified SEN', fields=fields, filter_field='sen_description').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'no_identified_SEN_char_outcomes.csv', ATT8_DIR)
    
    # Filter by disadvantage    
    
    disadvantaged_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Disadvantage', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Disadvantaged', fields=fields, filter_field='disadvantage').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'disadvantaged_char_outcomes.csv', ATT8_DIR)
    
    disadvantaged_all_other_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Disadvantage', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Disadvantaged all other', fields=fields, filter_field='disadvantage').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'disadvantaged_all_other_char_outcomes.csv', ATT8_DIR)
    
    # Filter by first language

    
    first_lang_english_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'First language', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'English', fields=fields, filter_field='first_language').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'first_lang_english_char_outcomes.csv', ATT8_DIR)

    first_lang_not_english_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'First language', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Other than English', fields=fields, filter_field='first_language').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_att8', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'first_lang_not_english_char_outcomes.csv', ATT8_DIR)
    

    
    
    
    # PROGRESS 8 SCORES
    
    # Filter by gender

    boys_total_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Total', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Boys', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'boys_total_char_outcomes.csv', P8_DIR) 
    
    girls_total_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Total', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Girls', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'girls_total_char_outcomes.csv', P8_DIR) 
    

    # Filter by ethnicity

    ethnicity_asian_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Asian', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_asian_ks4_char_outcomes.csv', P8_DIR) 
    
    ethnicity_black_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Black', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_black_ks4_char_outcomes.csv', P8_DIR) 
    
    ethnicity_mixed_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Mixed', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_mixed_ks4_char_outcomes.csv', P8_DIR) 
    
    ethnicity_other_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Other', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_other_ks4_char_outcomes.csv', P8_DIR)
    
    ethnicity_unclassified_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Unclassified', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_unclassified_ks4_char_outcomes.csv', P8_DIR)
    
    ethnicity_white_ks4_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Ethnicity major', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'White', fields=fields, filter_field='ethnicity_major').pipe(
                    filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                        filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                            save_to_file, 'ethnicity_white_ks4_char_outcomes.csv', P8_DIR)
    

    # Filter by free school meal eligibility

    fsm_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Free school meals', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'FSM', fields=fields, filter_field='free_school_meals').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'fsm_char_outcomes.csv', P8_DIR)
    
    fsm_all_other_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Free school meals', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'FSM all other', fields=fields, filter_field='free_school_meals').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'fsm_all_other_char_outcomes.csv', P8_DIR)
    
    # Filter by SEN status 

    no_SEN_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN status', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'No SEN', fields=fields, filter_field='sen_status').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'no_SEN_char_outcomes.csv', P8_DIR)
    
    SEN_state_EHC_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN status', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'SEN State EHC', fields=fields, filter_field='sen_status').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'SEN_state_EHC_char_outcomes.csv', P8_DIR)
    
    SEN_supp_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN status', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'SEN Supp', fields=fields, filter_field='sen_status').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'SEN_supp_char_outcomes.csv', P8_DIR)
    
    # Filter by SEN description

    any_SEN_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN description', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Any SEN', fields=fields, filter_field='sen_description').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'any_SEN_char_outcomes.csv', P8_DIR)
    
    no_identified_SEN_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'SEN description', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'No identified SEN', fields=fields, filter_field='sen_description').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'no_identified_SEN_char_outcomes.csv', P8_DIR)
    
    # Filter by disadvantage    
    
    disadvantaged_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Disadvantage', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Disadvantaged', fields=fields, filter_field='disadvantage').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'disadvantaged_char_outcomes.csv', P8_DIR)
    
    disadvantaged_all_other_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'Disadvantage', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Disadvantaged all other', fields=fields, filter_field='disadvantage').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'disadvantaged_all_other_char_outcomes.csv', P8_DIR)
    
    # Filter by first language

    
    first_lang_english_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'First language', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'English', fields=fields, filter_field='first_language').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'first_lang_english_char_outcomes.csv', P8_DIR)

    first_lang_not_english_char_outcomes = char_outcomes_data.pipe(
        filter_data, 202223, fields=fields, filter_field='time_period').pipe(
            filter_data, 'First language', fields=fields, filter_field='breakdown').pipe(
                filter_data, 'Other than English', fields=fields, filter_field='first_language').pipe(
                    filter_data, 'Total', fields=fields, filter_field='ethnicity_major').pipe(
                        filter_data, 'Total', fields=fields, filter_field='gender').pipe(
                            filter_data, 'avg_p8score', fields=fields, filter_field='variable').pipe(
                                save_to_file, 'first_lang_not_english_char_outcomes.csv', P8_DIR)