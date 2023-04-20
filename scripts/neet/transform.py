import os
import pandas as pd

from scripts.util.date import quarter_to_date, most_recent_stats

from extract import NEET_RAW_LATEST

DATA_DIR = os.path.join('data', 'neet')
os.makedirs(DATA_DIR, exist_ok=True)

NEET_16_24 = os.path.join(DATA_DIR, 'neet.csv')

column_mapper = {
    'Young people who were NEET Total': 'age_16_to_24_neet_total_sa',
    'Young people who were NEET Unemployed': 'age_16_to_24_neet_unemployed_sa',
    'Young people who were NEET Economically inactive': 'age_16_to_24_neet_economically_inactive_sa',
    'Total people in relevant population group': 'age_16_to_24_popupation',
    'People who were NEET as a percentage of people in relevant population group': 'age_16_to_24_neet_total_rate_sa',
}


def load_data():
    # Load the relevant sheef from the excel file
    data = pd.read_excel(NEET_RAW_LATEST,
                         sheet_name='People - SA',
                         skiprows=4,
                         header=[0, 1, 2, 3],
                         index_col=0,
                         na_values=['..'])

    # Remove any rows with no information in the first column
    data = data[data.iloc[:, 0].notna()]
    data.columns = data.columns.droplevel(level=[3])

    data.index.names = ['quarter']

    # Return the data
    return data


if __name__ == "__main__":
    data = load_data()
    data.index = quarter_to_date(data.index)

    def collapse_columns(x):
        (level_1, level_2) = x
        if "Unnamed:" in level_2:
            level_2 = ""
        return ' '.join([level_1, level_2]).strip()

    data = data.loc[:, ('Aged 16-24')]
    data.columns = data.columns.map(collapse_columns)

    # Select just the 16-24 age group for the last 16 quarters and save to CSV
    most_recent_stats(data) \
      .rename(columns=column_mapper) \
      .to_csv(NEET_16_24)
