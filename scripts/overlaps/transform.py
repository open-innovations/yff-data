import os
import pandas as pd

WORKING_DIR = os.path.join('working', 'upstream')
NEET_FACTORS_DATA = os.path.join(
    WORKING_DIR, 'neet-factors.csv')

factors_data = pd.read_csv(NEET_FACTORS_DATA)

fields = ['local_authority_code', 'value']

DATA_DIR = os.path.join('src', 'maps', 'overlaps', '_data', 'view')
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


if __name__ == '__main__':

    factors_data = factors_data.rename(
            columns=column_name_mapper)
    
    children_in_poverty = factors_data.pipe(
        filter_data, 'Children in poverty', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'children_in_poverty.csv'
    )

    children_looked_after = factors_data.pipe(
        filter_data, 'Children looked after', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'children_looked_after.csv'
    )

    disability_under_25 = factors_data.pipe(
        filter_data, 'Disability (age < 25)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'disability_under_25.csv'
    )

    disability_all = factors_data.pipe(
        filter_data, 'Disability (all)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'disability_all.csv'
    )

    economic_inactivity_neet = factors_data.pipe(
        filter_data, 'Economic inactivity (NEET)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'economic_inactivity_neet.csv'
    )

    fertility_rates_aged_20_24 = factors_data.pipe(
        filter_data, 'Fertility rates (age 20-24)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'fertility_rates_aged_20_24.csv'
    )

    fertility_rates_under_20 = factors_data.pipe(
        filter_data, 'Fertility rates (age < 20)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'fertility_rates_under_20.csv'
    )

    imd_crime = factors_data.pipe(
        filter_data, 'IMD Crime', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'imd_crime.csv'
    )

    imd_health = factors_data.pipe(
        filter_data, 'IMD Health', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'imd_health.csv'
    )


    lone_parent_households = factors_data.pipe(
        filter_data, 'Lone parent households', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'lone_parent_households.csv'
    )


    pupils_with_sen_support = factors_data.pipe(
        filter_data, 'Pupils with SEN support', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'pupils_with_sen_support.csv'
    )

    qualification_below_level_2_aged_16_24 = factors_data.pipe(
        filter_data, 'Qualification below level 2 (age 16-24)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'qualification_below_level_2_aged_16_24.csv'
    )

    qualification_below_level_2_all = factors_data.pipe(
        filter_data, 'Qualification below level 2 (all)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'qualification_below_level_2_all.csv'
    )

    school_absences = factors_data.pipe(
        filter_data, 'School Absences', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'school_absences.csv'
    )

    school_exclusions = factors_data.pipe(
        filter_data, 'School Exclusions', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'school_exclusions.csv'
    )

    school_suspensions = factors_data.pipe(
        filter_data, 'School Suspensions', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'school_suspensions.csv'
    )

    
    socially_renting_households = factors_data.pipe(
        filter_data, 'Socially Renting Households', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'socially_renting_households.csv'
    )

        
    total_score = factors_data.pipe(
        filter_data, 'Total Score', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'total_score.csv'
    )

        
    unpaid_carer_aged_16_24 = factors_data.pipe(
        filter_data, 'Unpaid carer (age 16-24)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'unpaid_carer_aged_16_24.csv'
    )

        
    weighted_scores_double = factors_data.pipe(
        filter_data, 'Weighted scores (double)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'weighted_scores_double.csv'
    )

    weighted_scores_triple = factors_data.pipe(
        filter_data, 'Weighted scores (triple)', fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'weighted_scores_triple.csv'
    )

    factors_data = factors_data.pivot(
        index=['local_authority_code', 'local_authority_name', 'group'], columns='variable', values='value').reset_index().rename(
            columns=column_name_mapper).pipe(
            clean_nulls).pipe(
                limit_to_england).pipe(
                        save_to_file, 'neet_factors_table.csv')

    