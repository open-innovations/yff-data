import os

from scripts.util.scraper import download_latest

WORK_DIR = os.path.join('working', 'qlms')
os.makedirs(WORK_DIR, exist_ok=True)
A06_SA_LATEST = os.path.join(WORK_DIR, 'a06latest.xls')
UNEM01_SA_LATEST = os.path.join(WORK_DIR, 'unem01latest.xls')

A06_SA_URL = 'https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/educationalstatusandlabourmarketstatusforpeopleagedfrom16to24seasonallyadjusteda06sa'
UNEM01_SA_URL = 'https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/unemploymentbyageanddurationseasonallyadjustedunem01sa'


if __name__ == '__main__':
    download_latest(A06_SA_URL, A06_SA_LATEST)
    download_latest(UNEM01_SA_URL, UNEM01_SA_LATEST)
