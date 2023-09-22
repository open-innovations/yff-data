import os
import pandas as pd

TOP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
METADATA_FILE = os.path.join(TOP_DIR, 'working/metadata.csv')


def read_meta():
    # read csv and make a new dataframe
    metadata = pd.read_csv(METADATA_FILE)
    metadata.last_update = pd.to_datetime(metadata.last_update, format='ISO8601')
    metadata.next_update = pd.to_datetime(metadata.next_update, format='ISO8601')
    return metadata


def filter_for_dataset(metadata, id):
    metadata = metadata[metadata.id == id].reset_index()
    return metadata


def extract_dates(metadata):
    return metadata.loc[0, ['last_update', 'next_update']]
    # next_update = metadata['next_update'].iloc[0]
    # published = metadata['last_update'].iloc[0]
    # dates = pd.Series(data={'published': published, 'next_update': next_update}, index=['published', 'next_update'])
    # return dates
