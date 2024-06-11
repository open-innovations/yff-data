import os
import pandas as pd

WORKING_DIR = os.path.join('working', 'upstream')
NEET_FACTORS_DATA = os.path.join(
    WORKING_DIR, 'neet-factors.csv')

factors_data = pd.read_csv(NEET_FACTORS_DATA)
combined_authority_lookup = pd.read_csv(os.path.join('data', 'reference', 'local_authority_combined_authority_lookup.csv'))

fields = ['local_authority_code', 'local_authority_name', 'value']

fields_combined = ['combined_authority_name', 'local_authority_code', 'local_authority_name', 'value']

selected_authorities = ['West Midlands', 'North East', 'Liverpool City Region','Greater Manchester', 'Greater London','West Yorkshire']

DATA_DIR = os.path.join('src', 'areas', 'maps', 'neet-factors', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

column_name_mapper = {
  'Local Authority Code': 'local_authority_code',
  'Local Authority Name': 'local_authority_name',
  'Group': 'group',
  'Children in poverty': 'children_in_poverty',
  'Children looked after': 'children_looked_after',
  'Disability (age < 25)': 'disability_under_25',
  'Disability (all)': 'disability_all',
  'Economic inactivity (NEET)': 'economic_inactivity_neet',
  'Fertility rates (age 20-24)': 'fertility_rates_aged_20_24',
  'Fertility rates (age < 20)': 'fertility_rates_under_20',
  'IMD Crime': 'imd_crime',
  'IMD Health': 'imd_health',
  'Lone parent households': 'lone_parent_households',
  'Pupils with SEN support': 'pupils_with_sen_support',
  'Qualification below level 2 (age 16-24)': 'qualification_below_level_2_aged_16_24',
  'Qualification below level 2 (all)': 'qualification_below_level_2_all',
  'School Absences': 'school_absences',
  'School Exclusions': 'school_exclusions',
  'School Suspensions': 'school_suspensions',
  'Socially renting households': 'socially_renting_households',
  'Total Score': 'total_score',
  'Unpaid carer (age 16-24)': 'unpaid_carer_aged_16_24',
  'Weighted scores (double)': 'weighted_scores_double',
  'Weighted scores (triple)': 'weighted_scores_triple'
}

def filter_data(data, variable, fields, filter_field='variable'):
    return data.loc[data[filter_field] == variable, fields]


def limit_to_england(data):
    return data.loc[data.local_authority_code.str.startswith('E')]


def clean_nulls(data):
    return data.dropna()


def save_to_file(data, filename):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data

def prepare_barchart(data, filename):
    data.drop(columns=['local_authority_code']).sort_values(by=['value'], ascending=False).head(20).pipe(
        save_to_file, filename
    )


if __name__ == '__main__':


    factors_data = factors_data.rename(
            columns=column_name_mapper)

    factors_data = combined_authority_lookup.merge(factors_data, how="right", left_on='LAD21CD', right_on='local_authority_code')
    factors_data = factors_data.drop(columns={'LAD21CD', 'LAD21NM'}).rename(columns={'CAUTH21CD': 'combined_authority_code', 'CAUTH21NM': 'combined_authority_name'})


    # Children in poverty

    children_in_poverty = filter_data(factors_data, 'Children in poverty', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'children_in_poverty.csv')

    prepare_barchart(children_in_poverty, 'children_in_poverty_barchart.csv')

    children_in_poverty_combined_authority = (
        filter_data(factors_data, 'Children in poverty', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    children_in_poverty_combined_authority['value'] = children_in_poverty_combined_authority['value'].round(2)

    children_in_poverty_combined_authority = (
        children_in_poverty_combined_authority[
            children_in_poverty_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'children_in_poverty_combined.csv')
    )

    # Children looked after

    children_looked_after = (
        filter_data(factors_data, 'Children looked after', fields=fields)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
        .pipe(save_to_file, 'children_looked_after.csv')
    )
    prepare_barchart(children_looked_after, 'children_looked_after_barchart.csv')

    children_looked_after_combined_authority = (
        filter_data(factors_data, 'Children looked after', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    children_looked_after_combined_authority['value'] = children_looked_after_combined_authority['value'].round(2)

    children_looked_after_combined_authority = (
        children_looked_after_combined_authority[
            children_looked_after_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'children_looked_after_combined.csv')
    )

    # Disability under 25

    disability_under_25 = filter_data(factors_data, 'Disability (age < 25)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'disability_under_25.csv')
    
    prepare_barchart(disability_under_25, 'disability_under_25_barchart.csv')

    disability_under_25_combined_authority = (
        filter_data(factors_data, 'Disability (age < 25)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    disability_under_25_combined_authority['value'] = disability_under_25_combined_authority['value'].round(2)

    disability_under_25_combined_authority = (
        disability_under_25_combined_authority[
            disability_under_25_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'disability_under_25_combined.csv')
    )

    # Disability all

    disability_all = filter_data(factors_data, 'Disability (all)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'disability_all.csv')
    
    prepare_barchart(disability_all, 'disability_all_barchart.csv')

    disability_all_combined_authority = (
        filter_data(factors_data, 'Disability (all)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    disability_all_combined_authority['value'] = disability_all_combined_authority['value'].round(2)

    disability_all_combined_authority = (
        disability_all_combined_authority[
            disability_all_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'disability_all_combined.csv')
    )

    # Economic inactivity NEET

    economic_inactivity_neet = filter_data(factors_data, 'Economic inactivity (NEET)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'economic_inactivity_neet.csv')
    
    prepare_barchart(economic_inactivity_neet, 'economic_inactivity_neet_barchart.csv')

    economic_inactivity_neet_combined_authority = (
        filter_data(factors_data, 'Economic inactivity (NEET)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    economic_inactivity_neet_combined_authority['value'] = economic_inactivity_neet_combined_authority['value'].round(2)

    economic_inactivity_neet_combined_authority = (
        economic_inactivity_neet_combined_authority[
            economic_inactivity_neet_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'economic_inactivity_neet_combined.csv')
    )

    # Fertility rates under 20

    fertility_rates_under_20 = filter_data(factors_data, 'Fertility rates (age < 20)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'fertility_rates_under_20.csv')
    
    prepare_barchart(fertility_rates_under_20, 'fertility_rates_under_20_barchart.csv')

    fertility_rates_under_20_combined_authority = (
        filter_data(factors_data, 'Fertility rates (age < 20)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    fertility_rates_under_20_combined_authority['value'] = fertility_rates_under_20_combined_authority['value'].round(2)

    fertility_rates_under_20_combined_authority = (
        fertility_rates_under_20_combined_authority[
            fertility_rates_under_20_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'fertility_rates_under_20_combined.csv')
    )


    # Fertility rates 20 to 24

    fertility_rates_20_to_24 = filter_data(factors_data, 'Fertility rates (age 20-24)', fields=fields).pipe(
    clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'fertility_rates_20_to_24.csv')
    
    prepare_barchart(fertility_rates_20_to_24, 'fertility_rates_20_to_24_barchart.csv')

    fertility_rates_20_to_24_combined_authority = (
        filter_data(factors_data, 'Fertility rates (age 20-24)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    fertility_rates_20_to_24_combined_authority['value'] = fertility_rates_20_to_24_combined_authority['value'].round(2)

    fertility_rates_20_to_24_combined_authority = (
        fertility_rates_20_to_24_combined_authority[
            fertility_rates_20_to_24_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'fertility_rates_20_to_24_combined.csv')
    )

    # IMD Crime

    imd_crime = filter_data(factors_data, 'IMD Crime', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'imd_crime.csv')
    
    prepare_barchart(imd_crime, 'imd_crime_barchart.csv')

    imd_crime_combined_authority = (
        filter_data(factors_data, 'IMD Crime', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    imd_crime_combined_authority['value'] = imd_crime_combined_authority['value'].round(2)

    imd_crime_combined_authority = (
        imd_crime_combined_authority[
            imd_crime_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'imd_crime_combined.csv')
    )

    # IMD Health

    imd_health = filter_data(factors_data, 'IMD Health', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'imd_health.csv')
    
    prepare_barchart(imd_health, 'imd_health_barchart.csv')

    imd_health_combined_authority = (
        filter_data(factors_data, 'IMD Health', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    imd_health_combined_authority['value'] = imd_health_combined_authority['value'].round(2)

    imd_health_combined_authority = (
        imd_health_combined_authority[
            imd_health_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'imd_health_combined.csv')
    )

    # Lone parent households

    lone_parent_households = filter_data(factors_data, 'Lone parent households', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'lone_parent_households.csv')
    
    prepare_barchart(lone_parent_households, 'lone_parent_households_barchart.csv')

    lone_parent_households_combined_authority = (
        filter_data(factors_data, 'Lone parent households', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    lone_parent_households_combined_authority['value'] = lone_parent_households_combined_authority['value'].round(2)

    lone_parent_households_combined_authority = (
        lone_parent_households_combined_authority[
            lone_parent_households_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'lone_parent_households_combined.csv')
    )

    # Pupils with SEN support

    pupils_with_sen_support = filter_data(factors_data, 'Pupils with SEN support', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'pupils_with_sen_support.csv')
    
    prepare_barchart(pupils_with_sen_support, 'pupils_with_sen_support_barchart.csv')

    pupils_with_sen_support_combined_authority = (
        filter_data(factors_data, 'Pupils with SEN support', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    pupils_with_sen_support_combined_authority['value'] = pupils_with_sen_support_combined_authority['value'].round(2)

    pupils_with_sen_support_combined_authority = (
        pupils_with_sen_support_combined_authority[
            pupils_with_sen_support_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'pupils_with_sen_support_combined.csv')
    )

    # Qualification below level 2 aged 16-24

    qualification_below_level_2_aged_16_24 = filter_data(factors_data, 'Qualification below level 2 (age 16-24)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'qualification_below_level_2_aged_16_24.csv')
    
    prepare_barchart(qualification_below_level_2_aged_16_24, 'qualification_below_level_2_aged_16_24_barchart.csv')

    qualification_below_level_2_aged_16_24_combined_authority = (
        filter_data(factors_data, 'Qualification below level 2 (age 16-24)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    qualification_below_level_2_aged_16_24_combined_authority['value'] = qualification_below_level_2_aged_16_24_combined_authority['value'].round(2)

    qualification_below_level_2_aged_16_24_combined_authority = (
        qualification_below_level_2_aged_16_24_combined_authority[
            qualification_below_level_2_aged_16_24_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'qualification_below_level_2_aged_16_24_combined.csv')
    )

    # Qualification below level 2 all 

    qualification_below_level_2_all = filter_data(factors_data, 'Qualification below level 2 (all)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'qualification_below_level_2_all.csv')
    
    prepare_barchart(qualification_below_level_2_all, 'qualification_below_level_2_all_barchart.csv')

    qualification_below_level_2_all_combined_authority = (
        filter_data(factors_data, 'Qualification below level 2 (all)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    qualification_below_level_2_all_combined_authority['value'] = qualification_below_level_2_all_combined_authority['value'].round(2)

    qualification_below_level_2_all_combined_authority = (
        qualification_below_level_2_all_combined_authority[
            qualification_below_level_2_all_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'qualification_below_level_2_all_combined.csv')
    )

    # School absences 

    school_absences = filter_data(factors_data, 'School Absences', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'school_absences.csv')
    
    prepare_barchart(school_absences, 'school_absences_barchart.csv')

    school_absences_combined_authority = (
        filter_data(factors_data, 'School Absences', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    school_absences_combined_authority['value'] = school_absences_combined_authority['value'].round(2)

    school_absences_combined_authority = (
        school_absences_combined_authority[
            school_absences_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'school_absences_combined.csv')
    )


    # School exclusions

    school_exclusions = filter_data(factors_data, 'School Exclusions', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'school_exclusions.csv')
    
    prepare_barchart(school_exclusions, 'school_exclusions_barchart.csv')

    school_exclusions_combined_authority = (
        filter_data(factors_data, 'School Exclusions', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    school_exclusions_combined_authority['value'] = school_exclusions_combined_authority['value'].round(2)

    school_exclusions_combined_authority = (
        school_exclusions_combined_authority[
            school_exclusions_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'school_exclusions_combined.csv')
    )

    # School suspensions

    school_suspensions = filter_data(factors_data, 'School Suspensions', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'school_suspensions.csv')
    
    prepare_barchart(school_suspensions, 'school_suspensions_barchart.csv')

    school_suspensions_combined_authority = (
        filter_data(factors_data, 'School Suspensions', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    school_suspensions_combined_authority['value'] = school_suspensions_combined_authority['value'].round(2)

    school_suspensions_combined_authority = (
        school_suspensions_combined_authority[
            school_suspensions_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'school_suspensions_combined.csv')
    )


    # Socially renting households

    socially_renting_households = filter_data(factors_data, 'Socially renting households', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'socially_renting_households.csv')
    
    prepare_barchart(socially_renting_households, 'socially_renting_households_barchart.csv')

    socially_renting_households_combined_authority = (
        filter_data(factors_data, 'Socially renting households', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    socially_renting_households_combined_authority['value'] = socially_renting_households_combined_authority['value'].round(2)

    socially_renting_households_combined_authority = (
        socially_renting_households_combined_authority[
            socially_renting_households_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'socially_renting_households_combined.csv')
    )


    # Unpaid carer aged 16-24

    unpaid_carer_aged_16_24 = filter_data(factors_data, 'Unpaid carer (age 16-24)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'unpaid_carer_aged_16_24.csv')
    
    prepare_barchart(unpaid_carer_aged_16_24, 'unpaid_carer_aged_16_24_barchart.csv')

    unpaid_carer_aged_16_24_combined_authority = (
        filter_data(factors_data, 'Unpaid carer (age 16-24)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    unpaid_carer_aged_16_24_combined_authority['value'] = unpaid_carer_aged_16_24_combined_authority['value'].round(2)

    unpaid_carer_aged_16_24_combined_authority = (
        unpaid_carer_aged_16_24_combined_authority[
            unpaid_carer_aged_16_24_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'unpaid_carer_aged_16_24_combined.csv')
    )


    # Total Score 

    total_score = (
        filter_data(factors_data, 'Total Score', fields=fields)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
        .pipe(save_to_file, 'total_score.csv')
    )
    prepare_barchart(total_score, 'total_score_barchart.csv')

    total_score_combined_authority = (
        filter_data(factors_data, 'Total Score', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    total_score_combined_authority['value'] = total_score_combined_authority['value'].round(2)

    total_score_combined_authority = (
        total_score_combined_authority[
            total_score_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'total_score_combined.csv')
    )

    # Weighted scores double 

    weighted_scores_double = filter_data(factors_data, 'Weighted scores (double)', fields=fields).pipe(
        clean_nulls).pipe(limit_to_england).pipe(save_to_file, 'weighted_scores_double.csv')
    
    prepare_barchart(weighted_scores_double, 'weighted_scores_double_barchart.csv')

    weighted_scores_double_combined_authority = (
        filter_data(factors_data, 'Weighted scores (double)', fields=fields_combined)
        .pipe(clean_nulls)
        .pipe(limit_to_england)
    )

    weighted_scores_double_combined_authority['value'] = weighted_scores_double_combined_authority['value'].round(2)

    weighted_scores_double_combined_authority = (
        weighted_scores_double_combined_authority[
            weighted_scores_double_combined_authority['combined_authority_name'].isin(selected_authorities)
        ]
        .rename(columns={
            'combined_authority_name': 'Combined Authority',
            'local_authority_code': 'Local Authority Code',
            'local_authority_name': 'Local Authority Name',
            'value': 'Value'        
        })
        .sort_values('Combined Authority')
        .pipe(save_to_file, 'weighted_scores_double_combined.csv')
    )

    scores_table = weighted_scores_double.sort_values(by=['value'], ascending=False).head(20).rename(columns= { 'local_authority_name': 'Local Authority', 'value':'Weighted Score'}).pipe(
        save_to_file, 'weighted_scores_table.csv'
    )



