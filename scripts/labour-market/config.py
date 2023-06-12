import os

column_mapper = {
    'JN5R': 'age_16_to_24_total_sa',
    'MGUQ': 'age_16_to_24_in_employment_sa',
    'MGVF': 'age_16_to_24_unemployed_sa',
    'MGVU': 'age_16_to_24_economically_inactive_sa',
    'AIVZ': 'age_16_to_24_employment_rate_sa',
    'MGWY': 'age_16_to_24_unemployment_rate_sa',
    'AIYL': 'age_16_to_24_economic_inactivity_rate_sa',

    'JN6B': 'age_16_to_24_not_in_ft_education_total_sa',  # Total not in education, 16-24
    'AGNJ': 'age_16_to_24_not_in_ft_education_in_employment_sa',  # Employed level, 16-24
    'AGOL': 'age_16_to_24_not_in_ft_education_unemployed_sa',  # Unemployed level, 16-24
    'AGPM': 'age_16_to_24_not_in_ft_education_economically_inactive_sa',  # Economivally inactive level, 16-24
    'AIWI': 'age_16_to_24_not_in_ft_education_employment_rate_sa',  # Employed rate, 16-24
    'AIXT': 'age_16_to_24_not_in_ft_education_unemployment_rate_sa',  # Unemployed rate, 16-24
    'AIYU': 'age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa',  # Economically inactive rate, 16-24

    'JN62': 'age_16_to_24_in_ft_education_total_sa',  # Total not in education, 16-24
    'AGNT': 'age_16_to_24_in_ft_education_in_employment_sa',  # Employed level, 16-24
    'AGOU': 'age_16_to_24_in_ft_education_unemployed_sa',  # Unemployed level, 16-24
    'AGPV': 'age_16_to_24_in_ft_education_economically_inactive_sa',  # Economivally inactive level, 16-24
    'AIXB': 'age_16_to_24_in_ft_education_employment_rate_sa',  # Employed rate, 16-24
    'AIYC': 'age_16_to_24_in_ft_education_unemployment_rate_sa',  # Unemployed rate, 16-24
    'AIZD': 'age_16_to_24_in_ft_education_economic_inactivity_rate_sa',  # Economically inactive rate, 16-24

    'JN69': 'age_16_to_17_not_in_ft_education_total_sa',  # Total not in education, 16-17
    'AGNH': 'age_16_to_17_not_in_ft_education_in_employment_sa',  # Employed level, 16-17
    'AGOJ': 'age_16_to_17_not_in_ft_education_unemployed_sa',  # Unemployed level, 16-17
    'AGPK': 'age_16_to_17_not_in_ft_education_economically_inactive_sa',  # Economivally inactive level, 16-17
    'AIWG': 'age_16_to_17_not_in_ft_education_employment_rate_sa',  # Employed rate, 16-17
    'AIXR': 'age_16_to_17_not_in_ft_education_unemployment_rate_sa',  # Unemployed rate, 16-17
    'AIYS': 'age_16_to_17_not_in_ft_education_economic_inactivity_rate_sa',  # Economically inactive rate, 16-17

    'JN6A': 'age_18_to_24_not_in_ft_education_total_sa',  # Total not in education, 18-24
    'AGNI': 'age_18_to_24_not_in_ft_education_in_employment_sa',  # Employed level, 18-24
    'AGOK': 'age_18_to_24_not_in_ft_education_unemployed_sa',  # Unemployed level, 18-24
    'AGPL': 'age_18_to_24_not_in_ft_education_economically_inactive_sa',  # Economivally inactive level, 18-24
    'AIWH': 'age_18_to_24_not_in_ft_education_employment_rate_sa',  # Employed rate, 18-24
    'AIXS': 'age_18_to_24_not_in_ft_education_unemployment_rate_sa',  # Unemployed rate, 18-24
    'AIYT': 'age_18_to_24_not_in_ft_education_economic_inactivity_rate_sa',  # Economically inactive rate, 18-24

    # 16-17
    'YBVH': 'age_16_to_17_unemployed_sa',
    'YBXG': 'age_16_to_17_unemployed_6_to_12_months_sa',
    'YBXJ': 'age_16_to_17_unemployed_over_12_months_sa',
    'YBXM': 'age_16_to_17_unemployed_over_12_months_rate_sa',
    # 18-24
    'YBVN': 'age_18_to_24_unemployed_sa',
    'YBXV': 'age_18_to_24_unemployed_6_to_12_months_sa',
    'YBXY': 'age_18_to_24_unemployed_over_12_months_sa',
    'YBYB': 'age_18_to_24_unemployed_over_12_months_rate_sa',
}

DATA_DIR = os.path.join('data', 'labour-market')
LMS_EXTRACT = os.path.join(DATA_DIR, 'monthly-rolling.csv')

SOURCES_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'labour-market'))
DASHBOARD_DIR = os.path.join('src', 'dashboard', 'labour-market', '_data')
