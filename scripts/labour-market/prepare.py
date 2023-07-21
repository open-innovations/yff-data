import os
import pandas as pd
from scripts.util.date import extract_every_third_from_end, lms_period_to_quarter_label, most_recent_stats
from scripts.util.file import add_index

from config import column_mapper, LMS_EXTRACT, SOURCES_DIR, DASHBOARD_DIR


os.makedirs(SOURCES_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DIR, exist_ok=True)


labour_market_status_variables = [
    'LF2Q', 'LF2S',
    'JN5R', 'MGUQ', 'MGVF', 'MGVU', 'AIVZ', 'MGWY', 'AIYL',
    'JN6B', 'AGNJ', 'AGOL', 'AGPM', 'AIWI', 'AIXT', 'AIYU',
    'JN62', 'AGNT', 'AGOU', 'AGPV', 'AIXB', 'AIYC', 'AIZD',
    'JN69', 'AGNH', 'AGOJ', 'AGPK', 'AIWG', 'AIXR', 'AIYS',
    'JN6A', 'AGNI', 'AGOK', 'AGPL', 'AIWH', 'AIXS', 'AIYT',
    'JN6E', 'AGNM', 'AGOO', 'AGPP', 'AIWL', 'AIXW', 'AIYX',
    'JN6H', 'AGNP', 'AGOR', 'AGPS', 'AIWX', 'AIXZ', 'AIZA',
]

long_term_unemployed_variables = [
    'YBVH', 'YBXG', 'YBXJ', 'YBXM',
    'YBVN', 'YBXV', 'YBXY', 'YBYB',
]



def summarise(**datasets):
    long_term_unemployed = datasets['long_term_unemployed']
    labour_market_status = datasets['labour_market_status']

    last_period_ltu = long_term_unemployed.quarter_label.iloc[-1]
    most_recent_lms_period = labour_market_status.quarter_label.iloc[-1]

    summary = pd.concat([
        labour_market_status.loc[:, [
            'unemployment_rate_sa',
            'economic_inactivity_rate_sa',
            'age_16_to_24_unemployment_rate_sa',
            'age_16_to_24_economic_inactivity_rate_sa',
            'age_16_to_24_not_in_ft_education_unemployment_rate_sa',
            'age_16_to_24_not_in_ft_education_economic_inactivity_rate_sa',
        ]],
        long_term_unemployed.loc[:, [
            'age_16_to_24_unemployed_6_to_12_months_rate_sa',
            'age_16_to_24_unemployed_over_12_months_sa',
        ]]
    ], axis=1).iloc[-1].round(1).to_frame()

    summary.columns = ['Value']

    summary.index = pd.Index([
        'Unemployment rate (all working age)',
        'Economic inactivity rate (all working age)',
        'Unemployment rate (young people)',
        'Economic inactivity rate (young people)',
        'Unemployment rate (Not in full-time education)',
        'Economic inactivity rate (Not in full-time education)',
        'Long-term unemployment rate 6 to 12 months',
        'Long-term unemployment rate over 12 months',
    ], name="Title")

    summary['Note'] = [       
        "People aged 16-64, unemployed as at {} (seasonally adjusted)".format(most_recent_lms_period),
        "People aged 16-64, economically inactive as at {} (seasonally adjusted)".format(most_recent_lms_period),
        "Young people aged 16-24, unemployed as at {} (seasonally adjusted)".format(most_recent_lms_period),
        "Young people aged 16-24, economically inactive as at {} (seasonally adjusted)".format(most_recent_lms_period),
        "Young people aged 16-24, not in full-time education, unemployed as at {} (seasonally adjusted)".format(most_recent_lms_period),
        "Young people aged 16-24, not in full-time education, economically inactive as at {} (seasonally adjusted)".format(most_recent_lms_period),
        "Young people aged 16-24, unemployed between 6 and 12 months as at {} (seasonally adjusted)".format(last_period_ltu),
        "Young people aged 16-24, unemployed over 12 months as at {} (seasonally adjusted)".format(last_period_ltu),
    ]

    summary['Suffix'] = '%'
    summary.fillna('N/A').to_csv(os.path.join(SOURCES_DIR, 'headlines.csv'))

    latest = summary.loc[:, 'Value']
    latest.index = latest.index.str.replace(r'[\s\-\(\)]+', '_', regex=True).str.lower().str.strip('_')

    # metadata = pd.read_json(METADATA_FILE).melt(ignore_index=False)
    # metadata.index = pd.Index(metadata.variable + '_' + metadata.index)
    latest = pd.concat([
      latest,
      pd.Series({
          'most_recent_lms_period': most_recent_lms_period,
      }),
      # metadata.drop(columns=['variable']).value,
    ])
    return latest


def create_table(data, columns):
    table = data[data.variable.isin(columns)].pivot(
        index='lms_period',
        columns='variable',
        values='value'
    ).rename(
        columns=column_mapper
    ).pipe(
        extract_every_third_from_end
    )

    table['quarter_label'] = pd.to_datetime(table.index.values).to_series().apply(lms_period_to_quarter_label)
    table['quarter_axis_label'] = table.quarter_label.str.replace(' ', '\\n')
    return table


def save_files(data, prefix):
    data.pipe(add_index).to_csv(os.path.join(SOURCES_DIR, prefix + '_all_data.csv'))
    data.pipe(most_recent_stats).pipe(add_index).to_csv(os.path.join(SOURCES_DIR, prefix + '_last_3_years.csv'))
    return data
    

if __name__ == "__main__":
    lms_extract = pd.read_csv(
        LMS_EXTRACT,
        parse_dates=['lms_period']
    )

    labour_market_status = create_table(lms_extract, labour_market_status_variables)
    save_files(labour_market_status, 'labour_market_status')

    long_term_unemployed = create_table(lms_extract, long_term_unemployed_variables)

    long_term_unemployed = pd.DataFrame({
        'age_16_to_24_unemployed_sa': (long_term_unemployed.age_18_to_24_unemployed_sa + long_term_unemployed.age_16_to_17_unemployed_sa).round(0),
        'age_16_to_24_unemployed_6_to_12_months_sa':  (long_term_unemployed.age_18_to_24_unemployed_6_to_12_months_sa + long_term_unemployed.age_16_to_17_unemployed_6_to_12_months_sa).round(0),
        'age_16_to_24_unemployed_over_12_months_sa': (long_term_unemployed.age_18_to_24_unemployed_over_12_months_sa + long_term_unemployed.age_16_to_17_unemployed_over_12_months_sa).round(0),
        'quarter_label': long_term_unemployed.quarter_label,
        'quarter_axis_label': long_term_unemployed.quarter_label.str.replace(' ', '\\n'),
    })
    long_term_unemployed['age_16_to_24_unemployed_6_to_12_months_rate_sa'] = (long_term_unemployed['age_16_to_24_unemployed_6_to_12_months_sa'] / \
        long_term_unemployed['age_16_to_24_unemployed_sa'] * 100).round(1)
    long_term_unemployed['age_16_to_24_unemployed_over_12_months_rate_sa'] = (long_term_unemployed['age_16_to_24_unemployed_over_12_months_sa'] / \
        long_term_unemployed['age_16_to_24_unemployed_sa'] * 100).round(1)

    save_files(long_term_unemployed, 'long_term_unemployed')

    summarise(
        long_term_unemployed=long_term_unemployed,
        labour_market_status=labour_market_status,
    )
