from pathlib import Path
import pandas as pd

county_lookup_file = Path(__file__).parent.joinpath(
    '../../data/reference/county-to-local-authority.csv').resolve()

county_lookup = pd.read_csv(county_lookup_file, usecols=['County', 'LADCD'])


def explode_counties(data, la_code_name='new_la_code'):
    exploded = county_lookup.merge(
        data, how="left", left_on='County', right_on=la_code_name)
    exploded.new_la_code = exploded.LADCD
    exploded.drop(columns=['LADCD'], inplace=True)

    remainder = data.loc[~data.new_la_code.isin(exploded.County)]

    return pd.concat([remainder, exploded])
