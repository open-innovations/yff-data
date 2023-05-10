import os
import scripts.util.file
import pandas as pd

from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'qlfs'))
os.makedirs(DATA_DIR, exist_ok=True)

def summarise(): 
    long_term_unemployed = pd.read_csv(os.path.join(DATA_DIR, 'long_term_unemployed.csv'))
    not_in_education = pd.read_csv(os.path.join(DATA_DIR, 'not_in_education.csv'))

    summary = pd.DataFrame({
            'Unemployment rate' : (not_in_education.age_16_to_24_not_in_ft_education_unemployment_rate_sa.tail(1)).round(1),
            'Long-term unemployment rate':(long_term_unemployed.age_16_to_24_unemployed_over_12_months_rate_sa.tail(1)).round(1),
            'Economic inactivity rate':(not_in_education.age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa.tail(1)).round(1)
    }).T.reset_index()
    summary = summary.rename(columns = {'index': 'Title', 11: 'Value'})
    summary['Note'] = [
        "Young people aged 16-24, not in full-time education (seasonally adjusted)",
        "Young people aged 16-24, unemployed over 12 months (seasonally adjusted)",
        "Young people age 16-24 not in full-time education, economically inactive (seasonally adjusted)"
        ]
    summary['Suffix'] = '%'
    summary.to_csv(os.path.join(DATA_DIR, 'headlines.csv'), index=False)


if __name__ == "__main__":
    scripts.util.file.copy("long_term_unemployed.csv",
                   from_dir=RAW_DATA_DIR, to_dir=DATA_DIR)
    scripts.util.file.copy("not_in_education.csv",
                   from_dir=RAW_DATA_DIR, to_dir=DATA_DIR)
    summarise()