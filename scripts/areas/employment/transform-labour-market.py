from pathlib import Path

import pandas as pd

WORKING_DIR = Path('working/upstream')

OUT_DIR = Path('data/area/pcon')
OUT_DIR.mkdir(parents=True, exist_ok=True)

labour_market_latest_pcon = pd.read_csv(
    WORKING_DIR / 'labour-market_most_recent_by_pcon.csv')
labour_market_last_3_years_pcon = pd.read_csv(
    WORKING_DIR / 'labour-market_last_3_years_by_pcon_2010.csv')

ONS_CODE = 'ONS_CODE'

COLUMN_MAPPER = {
    'geography_code': ONS_CODE,
    '% of economically inactive student': 'Economically Inactive - Student',
    '% who are economically inactive - aged 16+': 'Economically Inactive - Aged 16+',
    '% who are economically inactive - aged 16-19': 'Economically Inactive - Aged 16-19',
    '% who are economically inactive - aged 16-24': 'Economically Inactive - Aged 16-24',
    '% who are economically inactive - aged 16-64': 'Economically Inactive - Aged 16-64',
    '% who are economically inactive - aged 20-24': 'Economically Inactive - Aged 20-24',
    'Economic activity rate - aged 16-19': 'Economic Activity Rate - Aged 16-19',
    'Economic activity rate - aged 16-64': 'Economic Activity Rate - Aged 16-64',
    'Economic activity rate - aged 20-24': 'Economic Activity Rate - Aged 20-24',
    'Unemployment rate - aged 16+': 'Unemployment Rate - Aged 16+',
    'Unemployment rate - aged 16-19': 'Unemployment Rate - Aged 16-19',
    'Unemployment rate - aged 16-24': 'Unemployment Rate - Aged 16-24',
    'Unemployment rate - aged 16-64': 'Unemployment Rate - Aged 16-64',
    'Unemployment rate - aged 20-24': 'Unemployment Rate - Aged 20-24'
}


def limit_to_england(data):
    return data.loc[data[ONS_CODE].str.startswith('E')]


if __name__ == '__main__':

    # Latest figures

    latest_youth_unem = (
        labour_market_latest_pcon
        .drop(columns=['date', 'variable_code', 'notes'])
    )

    latest_youth_unem = (
        pd.pivot_table(latest_youth_unem, values='value', index=[
                       'geography_code'], columns=['variable_name'])
        .reset_index()
        .rename(columns=COLUMN_MAPPER)
        # .fillna(0)
    )
    latest_youth_unem = limit_to_england(latest_youth_unem).set_index(ONS_CODE)

    latest_youth_unem['Suffix'] = '%'

    latest_youth_unem.to_csv(OUT_DIR / 'headlines.csv', index=True)

# Unemployment rate - last 3 years

    # labour_market_last_3_years_pcon['date_name'] = labour_market_last_3_years_pcon['date_name'].str.replace('-', '-\n')

    youth_unem_last_3_years = (
        labour_market_last_3_years_pcon
        .loc[labour_market_last_3_years_pcon['variable_name'] == 'Unemployment rate - aged 16-24']
        # .fillna(0)
    )

    youth_unem_last_3_years = (
        pd.pivot_table(youth_unem_last_3_years, values='value', index=[
                       'geography_code'], columns=['date_name'])
        .reset_index()
        .rename(columns=COLUMN_MAPPER)
        # .fillna(0)
    )
    youth_unem_last_3_years = limit_to_england(
        youth_unem_last_3_years).set_index(ONS_CODE)

    youth_unem_last_3_years.to_csv(
        OUT_DIR / 'youth_unem_16-24_last_3_years.csv', index=True)

    # Economic inactivity rate

    econ_inactive_last_3_years = (
        labour_market_last_3_years_pcon
        .loc[labour_market_last_3_years_pcon['variable_name'] == '% who are economically inactive - aged 16-24']
        # .fillna(0)
    )

    econ_inactive_last_3_years = (
        pd.pivot_table(econ_inactive_last_3_years, values='value', index=[
                       'geography_code'], columns=['date_name'])
        .reset_index()
        .rename(columns=COLUMN_MAPPER)
        # .fillna(0)
    )
    econ_inactive_last_3_years = limit_to_england(
        econ_inactive_last_3_years).set_index(ONS_CODE)
    econ_inactive_last_3_years.to_csv(
        OUT_DIR / 'econ_inactive_16-24_last_3_years.csv', index=True)

    # Economic activity rate 16-19

    econ_active_last_3_years = (
        labour_market_last_3_years_pcon
        .loc[labour_market_last_3_years_pcon['variable_name'] == 'Economic activity rate - aged 16-19']
        # .fillna(0)
    )

    econ_active_last_3_years = (
        pd.pivot_table(econ_active_last_3_years, values='value',
                       index=['geography_code'], columns=['date_name'])
        .reset_index()
        .rename(columns=COLUMN_MAPPER)
        # .fillna(0)
    )
    econ_active_last_3_years = limit_to_england(
        econ_active_last_3_years).set_index(ONS_CODE)
    econ_active_last_3_years.to_csv(
        OUT_DIR / 'econ_active_16-19_last_3_years.csv', index=True)

    # Economic activity rate 20-24

    econ_active_20_24_last_3_years = (
        labour_market_last_3_years_pcon
        .loc[labour_market_last_3_years_pcon['variable_name'] == 'Economic activity rate - aged 20-24']
        # .fillna(0)
    )
    econ_active_20_24_last_3_years = (
        pd.pivot_table(econ_active_20_24_last_3_years, values='value', index=[
                       'geography_code'], columns=['date_name'])
        .reset_index()
        .rename(columns=COLUMN_MAPPER)
        # .fillna(0)
    )
    econ_active_20_24_last_3_years = limit_to_england(
        econ_active_20_24_last_3_years).set_index(ONS_CODE)
    econ_active_20_24_last_3_years.to_csv(
        OUT_DIR / 'econ_active_20-24_last_3_years.csv', index=True)
