import os

from scripts.util.scraper import download_latest

WORK_DIR = os.path.join('working', 'cpi')
os.makedirs(WORK_DIR, exist_ok=True)
CPI_LATEST = os.path.join(WORK_DIR, 'consumerpriceinflationdetailedreferencetables.xlsx')
CPI_TIME_SERIES = os.path.join(WORK_DIR, 'mm23.csv')

CPI_URL = 'https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceinflation'
TIME_SERIES_URL = 'https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceindices'

if __name__ == '__main__':
    download_latest(CPI_URL, CPI_LATEST)
    download_latest(TIME_SERIES_URL, CPI_TIME_SERIES)