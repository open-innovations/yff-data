import os
import pandas as pd

from config import column_mapper, DATA_DIR, LMS_EXTRACT

os.makedirs(DATA_DIR, exist_ok=True)

if __name__ == '__main__':
    variables = column_mapper.keys()
    lms_data = pd.read_csv('working/upstream/lms.csv')

    extract = lms_data.loc[
        (lms_data.variable.isin(variables)) &
        (lms_data['freq'] == 'm')
    ]

    extract = extract.drop(columns=['freq']).rename(columns={'date': 'lms_period'})
    extract.lms_period = pd.to_datetime(extract.lms_period)

    extract.loc[extract.lms_period >= '2000-01-01', ['variable', 'value', 'lms_period']].to_csv(LMS_EXTRACT, index=False)
