import os
import pandas as pd

from scripts.util.date import lms_period_to_quarter_label
from scripts.util.util import iso_to_named_date
from scripts.util.metadata import read_meta, extract_dates

DATA_DIR = os.path.join('src', '_data', 'sources', 'vacancies')
RAW_DATA_DIR = os.path.realpath(os.path.join('data', 'vacancies'))
DASHBOARD_DIR = os.path.join('src', 'dashboard', 'vacancies', '_data')
VACANCIES_GROWTH_CSV = os.path.join('working', 'upstream', 'vacancies-growth-by-sector.csv')
os.makedirs(DATA_DIR, exist_ok=True)


def prepare_vacancies():
    vacancies = pd.read_csv(os.path.join(
        RAW_DATA_DIR, 'vacancies_by_date.csv'))
    vacancies.sort_values(by='date', ascending=True, inplace=True)
    vacancies['quarter_label'] = pd.to_datetime(
        vacancies.date).map(lms_period_to_quarter_label)
    vacancies['quarter_axis_label'] = vacancies.quarter_label.str.replace(
        ' ', '\\n')

    quarterly = vacancies.loc[vacancies['freq'] == 'q']
    quarterly = quarterly.drop(columns=['freq'], axis=1).reset_index(drop=True)
    quarterly.index.name = 'row'
    quarterly.to_csv(os.path.join(
        DATA_DIR, 'quarterly_vacancies.csv'), index=True)

    monthly = vacancies.loc[vacancies['freq'] == 'm']
    monthly = monthly.drop(columns=['freq'], axis=1).reset_index(drop=True)
    monthly.index.name = 'row'
    monthly.to_csv(os.path.join(
        DATA_DIR, 'monthly_vacancies.csv'), index=True)


def prepare_vacancies_by_sector():
    vacancies_by_sector = pd.read_csv(VACANCIES_GROWTH_CSV).pivot(
        index=['date', 'Sector', 'key_youth_sectors', 'wanted_youth_sectors'],
        columns='variable',
        values='value'
    ).reset_index()

    vacancies_by_sector['Sector'] = vacancies_by_sector['Sector'].replace(
        ['Electricity gas steam & air conditioning supply',
         'Administrative & support service activities',
         'Professional scientific & technical activities',
         'Human health & social work activities',
         'Wholesale & retail trade; repair of motor vehicles and motor cycles',
         'Financial & insurance activities',
         'Accommodation & food service activities'
         ],
        ['Electricity, gas & air conditioning',
         'Administrative & support',
         'Professional & technical',
         'Health & social work',
         'Wholesale & retail; motor vehicles',
         'Financial & insurance',
         'Accommodation & food service',
         ]
    )
    vacancies_by_sector.to_csv(os.path.join(
        DATA_DIR, 'quarterly_growth_all_sectors.csv'), index=False)

    # TODO: Use sector names instead of index - order may change
    key_youth_sectors = vacancies_by_sector.loc[vacancies_by_sector.key_youth_sectors == True]
    key_youth_sectors.loc[:, 'Sector'] = key_youth_sectors['Sector'].str.wrap(25)
    key_youth_sectors.to_csv(os.path.join(
        DATA_DIR, 'growth_key_youth_sectors.csv'), index=False)

    wanted_youth_sectors = vacancies_by_sector.loc[vacancies_by_sector.wanted_youth_sectors == True]
    wanted_youth_sectors.loc[:, 'Sector'] = wanted_youth_sectors['Sector'].str.wrap(
        25)
    wanted_youth_sectors.to_csv(os.path.join(
        DATA_DIR, 'growth_wanted_youth_sectors.csv'), index=False)


def summarise():
    monthly_vacancies = pd.read_csv(
        os.path.join(DATA_DIR, 'monthly_vacancies.csv'))
    quarterly_vacancies = pd.read_csv(
        os.path.join(DATA_DIR, 'quarterly_vacancies.csv'))
    last_monthly_date = monthly_vacancies.date.iloc[-1]
    last_quarterly_date = quarterly_vacancies.date.iloc[-1]

    last_quarterly_value = quarterly_vacancies.value.iloc[-1]

    growth_last_quarter = (
        (last_quarterly_value - quarterly_vacancies.value.iloc[-2]) / last_quarterly_value) * 100

    last_period_label = lms_period_to_quarter_label(
        pd.to_datetime(last_monthly_date))
    last_quarter_label = lms_period_to_quarter_label(
        pd.to_datetime(last_quarterly_date))

    summary = pd.DataFrame({
        'Value': [
            monthly_vacancies.value.iloc[-1].round(1) * 1000,
            quarterly_vacancies.value.iloc[-1].round(1) * 1000,
            growth_last_quarter.round(1),
        ],
        'Note': [
            "Estimated number of open job vacancies in the last reported rolling quarter across the UK, {}.".format(
                last_period_label),
            "Estimated number of job vacancies in the last quarter across the UK, {}".format(
                last_quarter_label),
            "Estimated percentage change on last quarter, {}".format(
                last_quarter_label),
        ],
        'Suffix': [
            '',
            '',
            '%',
        ],
    },
        index=pd.Index([
            'Latest monthly vacancies',
            'Latest quarterly vacancies',
            'Growth on previous quarter',
        ], name='Title')
    )
    summary.loc['Growth on previous quarter', 'Suffix'] = '%'

    summary.fillna('N/A').to_csv(os.path.join(DATA_DIR, 'headlines.csv'))

    latest = pd.concat([
        pd.Series({
            'last_monthly_date': last_period_label,
            'last_quarterly_date': last_quarter_label,
        })
    ])
    latest.to_json(os.path.join(DASHBOARD_DIR, 'latest.json'), indent=2)


def get_dates():
    # read csv and make a new dataframe
    metadata = read_meta().pipe(extract_dates, 'LMS')
    next_update = iso_to_named_date(metadata['next_update'])
    published = iso_to_named_date(metadata['last_update'])
    dates = pd.Series(data={'published': published, 'next_update': next_update}, index=[
                      'published', 'next_update'])
    dates.to_json(os.path.join(DATA_DIR, 'metadata.json'), date_format='iso')
    return dates


if __name__ == "__main__":
    prepare_vacancies()
    prepare_vacancies_by_sector()
    summarise()
    get_dates()
