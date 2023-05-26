import os
import pandas as pd
from scripts.util.util import slugify

DATA_DIR = os.path.realpath(os.path.join('data', 'cpi'))
CPI_DATA = 'working/MM23_data.csv'
os.makedirs(DATA_DIR, exist_ok=True)

measures = ['D7BT', 'D7BU', 'D7BW', 'D7BX', 'D7C4']
n = int(len(measures))

def load_data(filepath):
    #read the csv and tidy up
    data = pd.read_csv(filepath)
    data = data.loc[(data['variable'].isin(measures))
                    & (data['dates.freq'] == 'm')].set_index('variable')
    return data
if __name__ == "__main__":

    #use only the measures (see lookup table)
    data = load_data(CPI_DATA)
    data.to_csv(os.path.join(DATA_DIR, 'transformed_cpi.csv'))
    