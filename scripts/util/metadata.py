import os
import pandas as pd

TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
METADATA_FILE = os.path.join(TOP_DIR, 'working/upstream/metadata.csv')


def read_meta():
    # read csv and make a new dataframe
    metadata = pd.read_csv(METADATA_FILE, parse_dates=['last_update', 'next_update'], index_col=['id'])
    return metadata


def extract_dates(metadata, id):
    return metadata.loc[id, ['last_update', 'next_update']]
    # next_update = metadata['next_update'].iloc[0]
    # published = metadata['last_update'].iloc[0]
    # dates = pd.Series(data={'published': published, 'next_update': next_update}, index=['published', 'next_update'])
    # return dates
