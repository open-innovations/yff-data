import os
import pandas as pd

from config import column_mapper, DATA_DIR, LMS_EXTRACT

os.makedirs(DATA_DIR, exist_ok=True)

if __name__ == '__main__':
    variables = column_mapper.keys()
    lms_data = pd.read_csv('working/LMS_data.csv')

    extract = lms_data.loc[
        (lms_data.variable.isin(variables)) &
        (lms_data['dates.freq'] == 'm')
    ]

    extract = extract.drop(columns=['dates.freq']).rename(columns={'dates.date': 'lms_period'})

    extract.to_csv(LMS_EXTRACT, index=False)
