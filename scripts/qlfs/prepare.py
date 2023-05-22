import os
import pandas as pd
from scripts.util.date import date_to_quarter, most_recent_stats
from scripts.util.file import add_index

from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'qlfs'))
os.makedirs(DATA_DIR, exist_ok=True)


def read_source_data(filename, **kwargs):
    return pd.read_csv(os.path.join(RAW_DATA_DIR, filename), **kwargs)


def summarise(**datasets):
    long_term_unemployed = datasets['long_term_unemployed']
    education_status = datasets['education_status']

    summary = pd.DataFrame({
        'Value': [
            education_status.age_16_to_24_not_in_ft_education_unemployment_rate_sa \
                .iloc[-1].round(1),
            long_term_unemployed.age_16_to_24_unemployed_over_12_months_rate_sa \
                .iloc[-1].round(1),
            long_term_unemployed.age_16_to_24_unemployed_over_6_months_rate_sa \
                .iloc[-1].round(1),
            education_status.age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa \
                .iloc[-1].round(1)
        ],
        'Note': [
            "Young people aged 16-24, not in full-time education (seasonally adjusted)",
            "Young people aged 16-24, unemployed over 12 months (seasonally adjusted)",
            "Young people aged 16-24, unemployed over 6 months (seasonally adjusted)",
            "Young people aged 16-24, not in full-time education, economically inactive (seasonally adjusted)"
        ],
        'Suffix': '%',
    },
        index=pd.Index([
            'Unemployment rate',
            'Long-term unemployment rate 12 months',
            'Long-term unemployment rate 6 months',
            'Economic inactivity rate',
        ], name='Title')
    ).fillna('N/A')
    summary.to_csv(os.path.join(DATA_DIR, 'headlines.csv'))


def transfer_files(filename):
    data = read_source_data(filename, index_col=[
                            'quarter_start'], parse_dates=['quarter_start'])
    data['quarter_label'] = pd.to_datetime(data.index.values).to_series().pipe(date_to_quarter)

    data.pipe(add_index).to_csv(os.path.join(
        DATA_DIR, filename.replace('.', '_all_data.')))
    data.pipe(most_recent_stats).pipe(add_index).to_csv(
        os.path.join(DATA_DIR, filename.replace('.', '_last_3_years.')))

    return data.pipe(most_recent_stats)


if __name__ == "__main__":
    long_term_unemployed = transfer_files("long_term_unemployed.csv")
    education_status = transfer_files("education_status.csv")

    summarise(
        long_term_unemployed=long_term_unemployed,
        education_status=education_status
    )
