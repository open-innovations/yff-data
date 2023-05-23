import pandas as pd


def quarter_to_date(index):
    new_index = pd.to_datetime(
        index.str.slice(stop=3) + '-' + index.str.slice(start=8),
        format="%b-%Y"
    )
    new_index.name = 'quarter_start'
    return new_index


def most_recent_stats(data, level=0, years=3):
    idx = data.index.get_level_values(level=level)
    return data.loc[idx > idx.max() - pd.DateOffset(years=years)]


def format_timestamp_as_quarter(start):
    '''
    Converts a quarter period start into a period as published by the ONS
    e.g. 2023-01-01 becomes Jan-Mar 2023. 2022-11-01 becomes Nov-Jan 2023
    '''
    end = start + pd.DateOffset(months=2)
    return '{}-{} {}'.format(
        start.strftime('%b'),
        end.strftime('%b'),
        end.strftime('%Y')
    )


def date_to_quarter(series):
    timestamp = pd.to_datetime(series)
    return timestamp.apply(format_timestamp_as_quarter)
