import os
import pandas as pd
from scripts.util.date import extract_every_third_from_end, lms_period_to_quarter_label, most_recent_stats
from scripts.util.file import add_index

from config import column_mapper, LMS_EXTRACT, SOURCES_DIR


os.makedirs(SOURCES_DIR, exist_ok=True)
# os.makedirs(DASHBOARD_DIR, exist_ok=True)


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
    summary.fillna('N/A').to_csv(os.path.join(SOURCES_DIR, 'headlines.csv'))

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


def create_table(data, columns):
    table = data[lms_extract.variable.isin(columns)].pivot(
        index='lms_period',
        columns='variable',
        values='value'
    ).rename(
        columns=column_mapper
    ).pipe(
        extract_every_third_from_end
    )

    table['quarter_label'] = pd.to_datetime(table.index.values).to_series().apply(lms_period_to_quarter_label)
    return table


def save_files(data, prefix):
    data.pipe(add_index).to_csv(os.path.join(SOURCES_DIR, prefix + '_all_data.csv'))
    data.pipe(most_recent_stats).pipe(add_index).to_csv(os.path.join(SOURCES_DIR, prefix + '_last_3_years.csv'))
    

if __name__ == "__main__":
    lms_extract = pd.read_csv(
        LMS_EXTRACT,
        parse_dates=['lms_period']
    )

    education_status = create_table(lms_extract, [
        'JN6B', 'AGNJ', 'AGOL', 'AGPM', 'AIWI', 'AIXT', 'AIYU',
        'JN62', 'AGNT', 'AGOU', 'AGPV', 'AIXB', 'AIYC', 'AIZD',
    ])
    save_files(education_status, 'education_status')

    long_term_unemployed = create_table(lms_extract, [
        'YBVH', 'YBXG', 'YBXJ', 'YBXM',
        'YBVN', 'YBXV', 'YBXY', 'YBYB',
    ])

    long_term_unemployed = pd.DataFrame({
        'age_16_to_24_unemployed_sa': (long_term_unemployed.age_18_to_24_unemployed_sa + long_term_unemployed.age_16_to_17_unemployed_sa).round(0),
        'age_16_to_24_unemployed_6_to_12_months_sa':  (long_term_unemployed.age_18_to_24_unemployed_6_to_12_months_sa + long_term_unemployed.age_16_to_17_unemployed_6_to_12_months_sa).round(0),
        'age_16_to_24_unemployed_over_12_months_sa': (long_term_unemployed.age_18_to_24_unemployed_over_12_months_sa + long_term_unemployed.age_16_to_17_unemployed_over_12_months_sa).round(0),
        'quarter_label': long_term_unemployed.quarter_label,
    })
    long_term_unemployed['age_16_to_24_unemployed_6_to_12_months_rate_sa'] = (long_term_unemployed['age_16_to_24_unemployed_6_to_12_months_sa'] / \
        long_term_unemployed['age_16_to_24_unemployed_sa'] * 100).round(1)
    long_term_unemployed['age_16_to_24_unemployed_over_12_months_rate_sa'] = (long_term_unemployed['age_16_to_24_unemployed_over_12_months_sa'] / \
        long_term_unemployed['age_16_to_24_unemployed_sa'] * 100).round(1)

    save_files(long_term_unemployed, 'long_term_unemployed')
