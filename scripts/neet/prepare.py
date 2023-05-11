import os
import scripts.util.file
import pandas as pd
from transform import NEET_16_24

from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = os.path.join('src', '_data', 'sources', 'neet')
os.makedirs(DATA_DIR, exist_ok=True)

def summarise(): 
    neet = pd.read_csv(NEET_16_24)

    latest = pd.DataFrame({
            'Latest NEET Rate' : (neet.people_age_16_to_24_neet_total_rate_sa.tail(1)).round(1),
            'Latest NEET Rate - Men' : (neet.men_age_16_to_24_neet_total_rate_sa.tail(1)).round(1), 
            'Latest NEET Rate - Women' : (neet.women_age_16_to_24_neet_total_rate_sa.tail(1)).round(1)
    }).T.reset_index()
    latest = latest.rename(columns = {'index': 'Title', 11: 'Value'})
    latest['Note'] = [
        "Percentage of young people aged 16-24 who are NEET (seasonally adjusted)", 
        "Percentage of young men aged 16-24 who are NEET (seasonally adjusted)", 
        "Percentage of young women aged 16-24 who are NEET (seasonally adjusted)"
    ]
    latest['Suffix'] = '%'
    latest.to_csv(os.path.join(DATA_DIR, 'headlines.csv'), index=False)


if __name__ == "__main__":
    scripts.util.file.copy("neet.csv", from_dir=RAW_DATA_DIR, to_dir=DATA_DIR)
    summarise()
