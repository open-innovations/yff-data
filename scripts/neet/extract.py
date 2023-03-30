import os

from scripts.util.scraper import download_latest

WORK_DIR = os.path.join('working', 'neet')
os.makedirs(WORK_DIR, exist_ok=True)
NEET_RAW_LATEST = os.path.join(WORK_DIR, 'neetlatest.xlsx')

NEET_DATA_SOURCE = 'https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/youngpeoplenotineducationemploymentortrainingneettable1'


if __name__ == '__main__':
    download_latest(NEET_DATA_SOURCE, NEET_RAW_LATEST)
