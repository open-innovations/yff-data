import os
import pandas as pd

from extract import NEET_RAW_LATEST

DATA_DIR = os.path.join('data', 'neet')
os.makedirs(DATA_DIR, exist_ok=True)

NEET_16_24 = os.path.join(DATA_DIR, 'neet_16_to_24.csv')


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

    data.index.names = ['quarter']

    # Return the data
    return data


def reindex_columns(data):
    new_index = data.columns.to_frame()

    # Set sensible names for levels
    new_index.columns = ['age_range', 'group', 'measure', 'numeric']

    # Rename measures to make them easier to deal with
    new_index.loc[new_index.group == 'Young people who were NEET',
                  ['measure']] = 'neet_' + new_index.measure.str.lower().str.replace(r"\s+", "_", regex=True)
    new_index.loc[new_index.group == 'Total people in relevant population group',
                  ['measure']] = 'total_popuplation'
    new_index.loc[new_index.group == 'People who were NEET as a percentage of people in relevant population group',
                  ['measure']] = 'percentage_neet'

    # Drop levels 'group' and 'numeric'
    new_index.drop(columns=['group', 'numeric'], inplace=True)

    # Convert back into an index and reassign to dataframe
    data.columns = pd.MultiIndex.from_frame(new_index)

    # Return the data
    return data


if __name__ == "__main__":
    data = load_data()
    data = reindex_columns(data)

    # Select just the 16-24 age group for the last 16 quarters and save to CSV
    data \
      .loc[:, ('Aged 16-24')] \
      .tail(16) \
      .to_csv(NEET_16_24)
