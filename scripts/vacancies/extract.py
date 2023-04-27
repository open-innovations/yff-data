import os

from scripts.util.scraper import download_latest, get_link_by_text

WORK_DIR = os.path.join('working', 'vacancies')
os.makedirs(WORK_DIR, exist_ok=True)

VACANCIES_URL = 'https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/jobsandvacanciesintheuk/previousReleases'



if __name__ == '__main__':
    url = get_link_by_text(VACANCIES_URL, pattern=r'Vacancies and jobs in the UK')

    # Pulling latest URL from a list is fragile as the page layout may change. TODO: Alternative way to find urls
    download_latest(url, os.path.join(WORK_DIR, 'vacancies.csv'), pattern='&format=csv$')
    download_latest(url, os.path.join(WORK_DIR, 'vacancies_by_sector.csv'), pattern='&format=csv$', index=1)

