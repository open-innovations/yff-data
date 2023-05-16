import os
import pandas as pd
from transform import NEET_16_24, DATA_DIR as RAW_DATA_DIR
from scripts.util.date import most_recent_stats
from scripts.util.file import add_index

DATA_DIR = os.path.join('src', '_data', 'sources', 'neet')
os.makedirs(DATA_DIR, exist_ok=True)


def read_source_data(filename, **kwargs):
    return pd.read_csv(os.path.join(RAW_DATA_DIR, filename), **kwargs)


def summarise(): 
    neet = pd.read_csv(NEET_16_24)

    latest = pd.DataFrame(
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

    latest['Note'] = [
        "Percentage of young people aged 16-24 who are NEET (seasonally adjusted)", 
        "Percentage of young men aged 16-24 who are NEET (seasonally adjusted)", 
        "Percentage of young women aged 16-24 who are NEET (seasonally adjusted)"
    ]
    latest['Suffix'] = '%'

    latest.to_csv(os.path.join(DATA_DIR, 'headlines.csv'))


def transfer_files(filename):
    data = read_source_data(filename, index_col=[
                            'quarter_start'], parse_dates=['quarter_start'])

    data.pipe(add_index).to_csv(os.path.join(
        DATA_DIR, filename.replace('.', '_all_data.')))
    data.pipe(most_recent_stats).pipe(add_index).to_csv(
        os.path.join(DATA_DIR, filename.replace('.', '_last_3_years.')))

    return data.pipe(most_recent_stats)


if __name__ == "__main__":
    neet = transfer_files("neet.csv")
    summarise()
