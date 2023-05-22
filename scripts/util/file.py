import os
import pandas as pd


def copy(name, from_dir, to_dir):
    data = pd.read_csv(os.path.join(from_dir, name))
    data.index = pd.Index(range(0, len(data.index)), name='quarter_index')
    data.to_csv(
        os.path.join(to_dir, name)
    )


def add_index(data):
    data = data.reset_index()
    data.index = pd.Index(range(0, len(data.index)), name='quarter_index')
    return data
