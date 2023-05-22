import os
import pandas as pd
from transform import NEET_16_24
from scripts.util.date import most_recent_stats
from scripts.util.file import add_index

DATA_DIR = os.path.join('src', '_data', 'sources', 'neet')
os.makedirs(DATA_DIR, exist_ok=True)


def read_source_data(filename, **kwargs):
    return pd.read_csv(filename, **kwargs)


def timestamp_to_neet_period(date):
    timestamp = pd.to_datetime(date)
    return '{}-{} {}'.format(
        timestamp.strftime('%b'),
        (timestamp + pd.DateOffset(months=3, days=-1)).strftime('%b'),
        timestamp.strftime('%Y')
    )


def summarise(neet):
    neet_period = timestamp_to_neet_period(neet.quarter_start.iloc[-1])

    headlines = pd.DataFrame(
        {
            'Value': [
                neet.people_age_16_to_24_neet_total_rate_sa.iloc[-1].round(1),
                neet.men_age_16_to_24_neet_total_rate_sa.iloc[-1].round(1),
                neet.women_age_16_to_24_neet_total_rate_sa.iloc[-1].round(1)
            ]
        },
        index=pd.Index([
            'Latest NEET Rate',
            'Latest NEET Rate - Men',
            'Latest NEET Rate - Women',
        ], name='Title')
    )

    headlines['Note'] = [
        "Percentage of young people aged 16-24 who are NEET as at {} (seasonally adjusted)".format(neet_period), 
        "Percentage of young men aged 16-24 who are NEET as at {} (seasonally adjusted)".format(neet_period), 
        "Percentage of young women aged 16-24 who are NEET as at {} (seasonally adjusted)".format(neet_period)
    ]
    headlines['Suffix'] = '%'

    headlines.to_csv(os.path.join(DATA_DIR, 'headlines.csv'))

    latest = headlines.loc[:, 'Value']
    latest.index = latest.index.str.replace(r'[\s-]+', '_', regex=True).str.lower()
    latest = pd.concat([
        latest,
        pd.Series({ 'last_date': neet_period })
      ])
    latest.to_json(os.path.join(DATA_DIR, 'latest.json'))


def transfer_files(filename):
    data = read_source_data(filename, index_col=[
                            'quarter_start'], parse_dates=['quarter_start'])
    data['quarter_label'] = pd.to_datetime(data.index.values).map(timestamp_to_neet_period)

    data.pipe(add_index).to_csv(os.path.join(
        DATA_DIR, os.path.basename(filename).replace('.', '_all_data.')))
    data.pipe(most_recent_stats).pipe(add_index).to_csv(
        os.path.join(DATA_DIR, os.path.basename(filename).replace('.', '_last_3_years.')))

    return data.reset_index()


if __name__ == "__main__":
    neet = transfer_files(NEET_16_24)
    summarise(neet)


