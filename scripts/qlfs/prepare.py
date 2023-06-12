import os

import pandas as pd
from transform import METADATA_FILE

DASHBOARD_DIR = os.path.join('src', 'dashboard', 'labour-market', '_data')
os.makedirs(DASHBOARD_DIR, exist_ok=True)


def dates():
    metadata = pd.read_json(METADATA_FILE).melt(ignore_index=False)
    metadata.index = pd.Index(metadata.variable + '_' + metadata.index)
    latest = metadata.drop(columns=['variable']).value
    latest.to_json(os.path.join(DASHBOARD_DIR, 'dates.json'), indent=2)


if __name__ == "__main__":
    dates()
