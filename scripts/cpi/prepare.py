import os
import shutil
import json
import math
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

    def round_half_down(n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n*multiplier - 0.5) / multiplier
    
    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def tick_gen(filepath, dtype=None):

        df = pd.read_csv(filepath)

        max_val = max(df.max(axis=1, numeric_only=True))
        max_exp = np.log10(max_val)
        r_up = int(-1*max_exp)
        tickMax = round(max_val, r_up)

        #min_val = min(df.min(axis=1, numeric_only=True))
        min_val = -5.3
        done = False
        if min_val < 0:
            min_val = abs(min_val)

            if min_val > 5:
                tickMin = -1*round(min_val, -1)
                done = True
            else:
                tickMin = -1*math.ceil(min_val)
                done = True
        if done == False:
            if 0 < min_val < 1:
                tickMin = 0
        
            else:
                tickMin = truncate(min_val)

        print(tickMin, tickMax)
        rang = int(tickMax - tickMin)
        print(rang)
        
        fact = []
        for i in range(2, 10):
            check = rang % i
            if check == 0:
                fact = i
                break
        ticks = np.arange(tickMin, (tickMax + 10), rang/fact)
        ticks = ticks.astype(float)

        if dtype == 'percentage':
             labels = []
             for i in ticks:
                  labels.append("{}{}".format(i, "%"))

        return ticks, labels
    ticks, labels = tick_gen(path, dtype='percentage')

    tickers = [{'value': tick, 'label': label} for tick, label in zip(ticks, labels)]
    print(json.dumps(tickers))

    #This is my logic:
    # 1. Read the csv file into a pandas dataframe
    # 2. find the maximum of the maximum in each column.
    # 3. Find the order of magnitude (power of 10) using log10(max)
    # 4. Round this number up to that nearest power (e.g. 10, 100, 1000 etc).
    # 5. Set this value as the maximum tick.
    # 6. Do the same for minimum values as above, but round down instead. If the 0 < log10(min) < 1, this means the minimum value is 1< x <10, therefore set min to 0.
    # 7. If log10(min) < 0, minimum value is negative, so set the minimum value to this negative number rounded down to nearest power of 10.