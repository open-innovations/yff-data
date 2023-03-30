#!/usr/bin/env python
import os
import pandas as pd
from extract import A06_SA_LATEST


DATA_DIR = os.path.realpath(os.path.join('data', 'qlms'))
os.makedirs(DATA_DIR, exist_ok=True)


if __name__ == "__main__":
    # Read the latest A06 data
    A06_data = pd.read_excel(A06_SA_LATEST,
                             sheet_name='People',
                             skiprows=4,
                             header=[0, 1, 2, 3],
                             index_col=0)
    # Drop any rows with nothin in columns 1
    A06_data = A06_data[A06_data.iloc[:, 0].notna()]
    A06_data.index.names = ['quarter']

    # Reshape the index...
    # Drop the dataset identifier code
    A06_data.columns = A06_data.columns.droplevel(level=[2, 3])

    # Get just quarters
    A06_data = A06_data.loc[A06_data.index.str.slice(
        stop=3).isin(['Jan', 'Apr', 'Jul', 'Oct'])]

    A06_data.loc[:, ('All aged 16 to 24 not in full-time education 1')] \
      .rename(columns=lambda x: x.lower().replace(' ', '_')) \
      .to_csv(os.path.join(DATA_DIR, '16_to_24_not_in_education.csv'))
