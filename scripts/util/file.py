import os
import pandas as pd


def copy(name, from_dir, to_dir):
    data = pd.read_csv(os.path.join(from_dir, name))
    data.index = pd.Index(range(1, len(data.index) + 1), name='quarter_index')
    data.to_csv(
        os.path.join(to_dir, name)
    )