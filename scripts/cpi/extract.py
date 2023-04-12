import os

from scripts.util.scraper import download_latest

WORK_DIR = os.path.join('working', 'cpi')
os.makedirs(WORK_DIR, exist_ok=True)
CPI_LATEST = os.path.join(WORK_DIR, 'consumerpriceinflationdetailedreferencetables.xlsx')

CPI_URL = 'https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceinflation'


if __name__ == '__main__':
    download_latest(CPI_URL, CPI_LATEST)
