import os
import shutil
import json
import pandas as pd
import numpy as np
from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = 'src/_data/sources/cpi'
os.makedirs(DATA_DIR, exist_ok=True)


def copy_file(name):
    shutil.copyfile(
        os.path.join(RAW_DATA_DIR, name),
        os.path.join(DATA_DIR, name)
    )


if __name__ == "__main__":
    copy_file("cpi.csv")
    copy_file("stats.json")

    path = 'src/_data/sources/cpi/cpi.csv'
    def tick_gen(filepath, dtype=None):
        df = pd.read_csv(filepath)
        max_val = max(df.max(axis=1, numeric_only=True))
        max_exp = np.log10(max_val)
        r_up = int(-1*max_exp)
        tickMax = round(max_val, r_up)

        min_val = min(df.min(axis=1, numeric_only=True))
        min_exp = np.log10(min_val)
        r_down = int(-1*min_exp)
        if min_val < 1:
            tickMin = 0
        else:
            tickMin = round(min_val, r_down)
        rang = int(tickMax - tickMin)
        ls = []
        check = rang % (tickMax/10)
        #number_of_ticks = 
        #print(number_of_ticks)
        if check == 0:
                ticks = np.arange(tickMin, (tickMax + 10), rang/3)
                ticks = ticks.astype(float)
        else:
             raise Exception('round up did not work properly')
        
        if dtype == 'percentage':
             labels = []
             for i in ticks:
                  labels.append("{}{}".format(i, "%"))

        return ticks, labels
    ticks, labels = tick_gen(path, dtype='percentage')

    tickers = [{'value': tick, 'label': label} for tick, label in zip(ticks, labels)]
    #print(json.dumps(tickers))