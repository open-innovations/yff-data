import os
import shutil
import json
import math
import pandas as pd
import numpy as np
from transform import DATA_DIR as RAW_DATA_DIR
from scripts.util.util import tick_gen
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
    data = pd.read_csv(path)
  
    tick_min, tick_max, tick_labels = tick_gen(data, dtype='percentage')

    #this is provisionally working, now need to implement the writing of 
    #this to the yaml file.
    #print(tick_max, tick_min, tick_labels)