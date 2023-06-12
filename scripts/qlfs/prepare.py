import os
import pandas as pd
from scripts.util.date import date_to_quarter, most_recent_stats
from scripts.util.file import add_index

from transform import DATA_DIR as RAW_DATA_DIR, METADATA_FILE

DATA_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'qlfs'))
os.makedirs(DATA_DIR, exist_ok=True)
DASHBOARD_DIR = os.path.join('src', 'dashboard', 'labour-market', '_data')
os.makedirs(DASHBOARD_DIR, exist_ok=True)


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

    latest = summary.loc[:, 'Value']
    latest.index = latest.index.str.replace(r'[\s-]+', '_', regex=True).str.lower()

    metadata = pd.read_json(METADATA_FILE).melt(ignore_index=False)
    metadata.index = pd.Index(metadata.variable + '_' + metadata.index)
    latest = pd.concat([
      latest,
      pd.Series({
          'a06_quarter': last_period_es,
          'unem01_quarter': last_period_ltu,
      }),
      metadata.drop(columns=['variable']).value,
    ])
    latest.to_json(os.path.join(DASHBOARD_DIR, 'latest.json'), indent=2)


def transfer_files(filename):
    data = read_source_data(filename, index_col=[
                            'quarter_start'], parse_dates=['quarter_start'])
    data['quarter_label'] = pd.to_datetime(data.index.values).to_series().pipe(date_to_quarter)

    # data.pipe(add_index).to_csv(os.path.join(
    #     DATA_DIR, filename.replace('.', '_all_data.')))
    # data.pipe(most_recent_stats).pipe(add_index).to_csv(
    #     os.path.join(DATA_DIR, filename.replace('.', '_last_3_years.')))

    return data.pipe(most_recent_stats)


if __name__ == "__main__":
    long_term_unemployed = transfer_files("long_term_unemployed.csv")
    education_status = transfer_files("education_status.csv")

    summarise(
        long_term_unemployed=long_term_unemployed,
        education_status=education_status
    )
