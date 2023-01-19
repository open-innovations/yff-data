#!/usr/bin/env python
import os
import pandas as pd
from extract import QLMS_RAW_LATEST


DATA_DIR = os.path.realpath(os.path.join('data', 'qlms'))
os.makedirs(DATA_DIR, exist_ok=True)


def main():
    data9 = pd.read_excel(QLMS_RAW_LATEST, sheet_name='9',
                          skiprows=4, header=3)
    data9 = data9[~data9[data9.columns[1]].isna()].reset_index(drop=True)
    data9.rename(columns={
        'Dataset identifier code': 'Quarter'
    }, inplace=True)
    data9.to_csv(os.path.join(DATA_DIR, 'qlms-9.csv'), index=False)

    data11 = pd.read_excel(QLMS_RAW_LATEST, sheet_name='11',
                           skiprows=4, header=3, na_values='..')
    data11 = data11[~data11[data11.columns[1]].isna()].reset_index(drop=True)
    data11.rename(columns={
        'Dataset identifier code': 'Quarter'
    }, inplace=True)
    data11.to_csv(os.path.join(DATA_DIR, 'qlms-11.csv'), index=False)

    data12 = pd.read_excel(QLMS_RAW_LATEST, sheet_name='12',
                           skiprows=4, header=3, na_values='..')
    data12 = data12[~data12[data12.columns[1]].isna()].reset_index(drop=True)
    data12.rename(columns={
        'Dataset identifier code': 'Quarter'
    }, inplace=True)
    data12.to_csv(os.path.join(DATA_DIR, 'qlms-12.csv'), index=False)

    data20 = pd.read_excel(QLMS_RAW_LATEST, sheet_name='20',
                           skiprows=4, header=3, usecols="A:E",
                           na_values='..')
    data20 = data20[~data20[data20.columns[2]].isna()].reset_index(drop=True)
    data20.rename(columns={
        'Unnamed: 0': 'Quarter'
    }, inplace=True)
    data20.to_csv(os.path.join(DATA_DIR, 'qlms-20.csv'), index=False)


if __name__ == "__main__":
    main()
