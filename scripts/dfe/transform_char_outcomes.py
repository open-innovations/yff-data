import os
import re
import pandas as pd 

WORKING_DIR = os.path.join('working', 'upstream')

KS4_CHAR_OUTCOMES_DATA = os.path.join(
    WORKING_DIR, 'ks4_char_outcomes.csv')

char_outcomes_data = pd.read_csv(KS4_CHAR_OUTCOMES_DATA)

fields = ['new_la_code', 'time_period', 'version', 'gender', 'breakdown', 'ethnicity_major', 
          'free_school_meals', 'sen_status', 'sen_description', 'disadvantage', 'first_language', 'variable', 'value']
groupby = ['variable','breakdown','gender','ethnicity_major','free_school_meals','sen_status','sen_description','disadvantage','first_language']

DATA_DIR = os.path.join('src', 'maps', 'education', '_data', 'view');
os.makedirs(DATA_DIR, exist_ok=True)


def save_tidy_csv(file,df):
    # First add the header
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]],columns=df.columns)
    final = pd.concat([new_record, df], ignore_index=True)

    # Get the output as CSV
    csv = final.to_csv(index=True)

    # Because we added an index column we will now tidy 
    csv = re.sub(r'\n0,---,---', '\n---,---,---', csv)

    text_file = open(os.path.join(DATA_DIR, 'ks4_char_outcomes.csv'), "w")
    text_file.write(csv)
    text_file.close()

def add_header_end(df):
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]],columns=df.columns)
    df = pd.concat([new_record, df], ignore_index=True)
    return df

if __name__ == '__main__':

    # Filter to the allowed fields
    filtered = char_outcomes_data[fields].dropna()

    # Limit to rows that match 202223 and Revised
    limited = filtered.loc[(filtered['time_period']==202223) & (filtered['version']=='Revised') & (filtered['breakdown']!='Ethnicity minor')]

    # Pivot the table to arrange in columns with each combo
    pivotted = limited.pivot_table(index='new_la_code', columns=groupby, values='value');

    # Add a column at the start which is a duplicate of the index (so we can not print the index column)
    pivotted.insert(0,'LADCD',pivotted.index)

    save_tidy_csv(os.path.join(DATA_DIR, 'ks4_char_outcomes.csv'),pivotted);


    exit()





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