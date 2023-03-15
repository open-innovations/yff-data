import os

from scripts.util.downloader import download_file
from scripts.util.scraper import get_filename

WORK_DIR = os.path.join('working', 'neet')
os.makedirs(WORK_DIR, exist_ok=True)
NEET_RAW_LATEST = os.path.join(WORK_DIR, 'neetlatest.xlsx')


def download_latest():
    url = get_filename(
        'https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/youngpeoplenotineducationemploymentortrainingneettable1', pattern='.xlsx$')
    download_file(url, NEET_RAW_LATEST)


if __name__ == '__main__':
    download_latest()