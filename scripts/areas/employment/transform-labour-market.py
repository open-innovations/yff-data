from pathlib import Path

import pandas as pd

WORKING_DIR = Path('working/upstream')

OUT_DIR = Path('data/area/pcon')
OUT_DIR.mkdir(parents=True, exist_ok=True)

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


def get_latest_available(data):
    # Calculate dates
    failsafe_date = data.date.min() - pd.Timedelta("1 days")
    latest_date = data.date.max()

    # Subset the input data
    test_data = data.loc[:, ['geography_code',
                             'date', 'variable_name', 'value']]

    # Construct a failsafe (to be used in the event that there is no data available)
    # This will have the same index as the most recent values, which we use below...
    failsafe_data = test_data.loc[test_data.date == latest_date]
    failsafe_data.loc[:, ['date', 'value']] = (failsafe_date, -1)

    # Concatenate the test and failsafe_data
    test_data = pd.concat([test_data, failsafe_data]
                          ).sort_values('date', ascending=True)

    # Get the indexes for the non-zero values
    indexes = test_data.dropna(subset='value').groupby(
        ['geography_code', 'variable_name'])['date'].idxmax()

    return data.loc[indexes]


def get_timeline(data: pd.DataFrame, variable: str) -> pd.DataFrame:
    return (
        data
          .loc[ data.variable_name == variable ]
          .pivot(
              index=['geography_code'],
              columns=['date', 'date_name'],
              values=['value'],
          )
          .rename_axis(axis=0, mapper=ONS_CODE)
          .droplevel(axis=1, level=[0,1])
    )


if __name__ == '__main__':

    # Latest figures
    labour_market = pd.read_parquet(
        WORKING_DIR / 'labour_market_by_pcon.parquet').query('geography_code.str.startswith("E")')

    most_recent_values = (
        labour_market
        .pipe(get_latest_available)
        .pivot(
            index=['geography_code'],
            columns=['variable_name'],
            values=['value']
        )
        # Drop the first level of the columns axis
        .droplevel(axis=1, level=0)
        # Rename the index
        .rename_axis(axis=0, mapper=ONS_CODE)
        .rename(columns=COLUMN_MAPPER)
        .sort_index(axis=1)
    )

    most_recent_values['Suffix'] = '%'

    most_recent_values.loc[
        :,
        [
            "Economically Inactive - Student", "Economically Inactive - Aged 16+", "Economically Inactive - Aged 16-19", "Economically Inactive - Aged 16-24", "Economically Inactive - Aged 16-64", "Economically Inactive - Aged 20-24", "Economic Activity Rate - Aged 16-19", "Economic Activity Rate - Aged 16-64", "Economic Activity Rate - Aged 20-24", "Unemployment Rate - Aged 16+", "Unemployment Rate - Aged 16-19", "Unemployment Rate - Aged 16-24", "Unemployment Rate - Aged 16-64", "Unemployment Rate - Aged 20-24", "Suffix"
        ]
    ].to_csv(OUT_DIR / 'headlines.csv', index=True)


    # Unemployment rate - last 3 years
    labour_market.pipe(
        get_timeline, 'Unemployment rate - aged 16-24'
    ).to_csv(
        OUT_DIR / 'youth_unem_16-24_last_3_years.csv', index=True
    )

    # Economic inactivity rate
    labour_market.pipe(
        get_timeline, '% who are economically inactive - aged 16-24'
    ).to_csv(
        OUT_DIR / 'econ_inactive_16-24_last_3_years.csv', index=True
    )

    # Economic activity rate 16-19
    labour_market.pipe(
        get_timeline, 'Economic activity rate - aged 16-19'
    ).to_csv(
        OUT_DIR / 'econ_active_16-19_last_3_years.csv', index=True
    )

    # Economic activity rate 20-24
    labour_market.pipe(
        get_timeline, 'Economic activity rate - aged 20-24'
    ).to_csv(
        OUT_DIR / 'econ_active_20-24_last_3_years.csv', index=True
    )
