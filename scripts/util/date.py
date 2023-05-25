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


def lms_period_to_quarter_label(quarter):
    '''
    Converts a quarter period into a period string as published by the ONS
    e.g. 2023-02-01 becomes Jan-Mar 2023. 2022-11-01 becomes Nov-Jan 2023
    '''
    start = quarter - pd.DateOffset(months=1)
    end = quarter + pd.DateOffset(months=1)
    return '{}-{} {}'.format(
        start.strftime('%b'),
        end.strftime('%b'),
        end.strftime('%Y')
    )


def date_to_quarter(series):
    timestamp = pd.to_datetime(series)
    return timestamp.apply(format_timestamp_as_quarter)


def extract_every_third_from_end(data):
    '''
      Extracts quarterly data from a frame by slicing.
      The first slice progresses backwards in 3s.
      The second slice reverses the dataframe.
    '''
    return data.iloc[::-3].iloc[::-1]
