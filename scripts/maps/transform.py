import os
import pandas as pd

WORKING_DIR = os.path.join('working', 'upstream')
COMBINED_DATA = os.path.join(
    WORKING_DIR, 'labour-market_most_recent_by_pcon.csv')

CLAIMANT_DATA = os.path.join(
    WORKING_DIR, 'claimants-per-population-latest.csv')

CENSUS_DATA = os.path.join(
    WORKING_DIR, 'census-employment-status.csv')

DATA_DIR = os.path.join('src', 'areas', 'maps', 'employment', '_data', 'view')
os.makedirs(DATA_DIR, exist_ok=True)

combined_data = pd.read_csv(COMBINED_DATA)
claimant_data = pd.read_csv(CLAIMANT_DATA)
census_data = pd.read_csv(CENSUS_DATA)

aps_fields = ['geography_code', 'date', 'date_name', 'value', 'notes']
claimants_fields = ['geography_code', 'Claimants percentage']
census_fields = ['geography_code', 'rate']

def filter_data(data, variable, fields, filter_field='variable_name'):
    return data.loc[data[filter_field] == variable, fields]


def limit_to_england(data):
    return data.loc[data.geography_code.str.startswith('E')]


def clean_nulls(data):
    return data.dropna()


def save_to_file(data, filename):
    full_filename = os.path.join(DATA_DIR, filename)
    data.to_csv(full_filename, index=False)
    return data


if __name__ == '__main__':

    combined_data.pipe(
        filter_data, 'Unemployment rate - aged 16-64', aps_fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'unemployment_rate_all_working_age.csv'
    )

    combined_data.pipe(
        filter_data, 'Unemployment rate - aged 16-24', aps_fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'unemployment_rate_youth.csv'
    )

    combined_data.pipe(
        filter_data, '% who are economically inactive - aged 16-64', aps_fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'economic_inactivity_rate_all_working_age.csv'
    )

    combined_data.pipe(
        filter_data, '% who are economically inactive - aged 16-24', aps_fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'economic_inactivity_rate_youth.csv'
    )

    combined_data.pipe(
        filter_data, '% of economically inactive student', aps_fields
    ).pipe(clean_nulls).pipe(limit_to_england).pipe(
        save_to_file, 'economic_inactivity_students_combined.csv'
    )

    # Claimants

    claimant_data.loc[
        claimant_data.age == 'Aged 16+',
        claimants_fields
    ].pipe(clean_nulls).pipe(limit_to_england).to_csv(
        os.path.join(DATA_DIR, 'claimants_16_plus.csv'), index=False
    )

    claimant_data.loc[
        claimant_data.age == 'Aged 16-24',
        claimants_fields
    ].pipe(clean_nulls).pipe(limit_to_england).to_csv(
        os.path.join(DATA_DIR, 'claimants_16_24.csv'), index=False
    )

    #Census 

    census_data.loc[
        (census_data.age == 'Aged 16 to 24 years') &
        (census_data.gender == 'All persons') &
        (census_data.variable_name == 'Economically active (excluding full-time students): Unemployed'),
        census_fields
    ].pipe(clean_nulls).pipe(limit_to_england).to_csv(
        os.path.join(DATA_DIR, 'census_unemployed_youth.csv'), index=False
    )

    census_data.loc[
        (census_data.age == 'Aged 16 to 24 years') &
        (census_data.gender == 'All persons') &
        (census_data.variable_name == 'Economically inactive (excluding full-time students)'),
        census_fields
    ].pipe(clean_nulls).pipe(limit_to_england).to_csv(
        os.path.join(DATA_DIR, 'census_economically_inactive_youth.csv'), index=False
    )

    census_data.loc[
        (census_data.age == 'Aged 16 to 24 years') &
        (census_data.gender == 'All persons') &
        (census_data.variable_name == 'Unemployed or economically inactive and not in full-time education'),
        census_fields
    ].pipe(clean_nulls).pipe(limit_to_england).to_csv(
        os.path.join(DATA_DIR, 'census_unemployed_or_economically_inactive_and_not_in_fte_youth.csv'), index=False
    )
