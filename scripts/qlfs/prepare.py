import os

import pandas as pd
from transform import METADATA_FILE

DASHBOARD_DIR = os.path.join('src', 'dashboard', 'labour-market', '_data')
os.makedirs(DASHBOARD_DIR, exist_ok=True)


<<<<<<< HEAD
def dates():
=======
def read_source_data(filename, **kwargs):
    return pd.read_csv(os.path.join(RAW_DATA_DIR, filename), **kwargs)


def summarise(**datasets):
    long_term_unemployed = datasets['long_term_unemployed']
    education_status = datasets['education_status']

    last_period_ltu = long_term_unemployed.quarter_label.iloc[-1]
    last_period_es = education_status.quarter_label.iloc[-1]

    summary = pd.DataFrame({
        'Value': [
            education_status.age_16_to_24_not_in_ft_education_unemployment_rate_sa \
                .iloc[-1].round(1),
            education_status.age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa \
                .iloc[-1].round(1),
            long_term_unemployed.age_16_to_24_unemployed_6_to_12_months_rate_sa \
                .iloc[-1].round(1),
            long_term_unemployed.age_16_to_24_unemployed_over_12_months_rate_sa \
                .iloc[-1].round(1),
        ],
        'Note': [
            "Young people aged 16-24, not in full-time education, unemployed as at {} (seasonally adjusted)".format(last_period_es),
            "Young people aged 16-24, not in full-time education, economically inactive as at {} (seasonally adjusted)".format(last_period_es),
            "Young people aged 16-24, unemployed between 6 and 12 months as at {} (seasonally adjusted)".format(last_period_ltu),
            "Young people aged 16-24, unemployed over 12 months as at {} (seasonally adjusted)".format(last_period_ltu),
        ],
        'Suffix': '%',
    },
        index=pd.Index([
            'Unemployment rate',
            'Economic inactivity rate',
            'Long-term unemployment rate 6 to 12 months',
            'Long-term unemployment rate over 12 months',
        ], name='Title')
    )
    summary.fillna('N/A').to_csv(os.path.join(DATA_DIR, 'headlines.csv'))

    latest = summary.loc[:, 'Value']
    latest.index = latest.index.str.replace(r'[\s-]+', '_', regex=True).str.lower()

>>>>>>> parent of 74cfb67 (Merge branch 'main' of https://github.com/open-innovations/yff-data)
    metadata = pd.read_json(METADATA_FILE).melt(ignore_index=False)
    metadata.index = pd.Index(metadata.variable + '_' + metadata.index)
    latest = metadata.drop(columns=['variable']).value
    latest.to_json(os.path.join(DASHBOARD_DIR, 'dates.json'), indent=2)


if __name__ == "__main__":
    dates()
