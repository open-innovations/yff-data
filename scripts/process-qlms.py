#!/usr/bin/env python
from os import chdir
from os.path import realpath
from pandas import read_excel
from yff_data.qlms import download_latest


WORK_DIR = realpath('working')
DATA_DIR = realpath('data')
def main():
    chdir(WORK_DIR)
    qlms_file = download_latest()
    data9 = read_excel(qlms_file, sheet_name='9',
                      skiprows=4, header=3)
    data9 = data9[~data9[data9.columns[1]].isna()].reset_index(drop=True)
    data9.rename(columns={
      'Dataset identifier code': 'Quarter'
    }, inplace=True)

    data11 = read_excel(qlms_file, sheet_name='11',
                      skiprows=4, header=3, na_values='..')
    data11 = data11[~data11[data11.columns[1]].isna()].reset_index(drop=True)
    data11.rename(columns={
      'Dataset identifier code': 'Quarter'
    }, inplace=True)

    data12 = read_excel(qlms_file, sheet_name='12',
                      skiprows=4, header=3, na_values='..')
    data12 = data12[~data12[data12.columns[1]].isna()].reset_index(drop=True)
    data12.rename(columns={
      'Dataset identifier code': 'Quarter'
    }, inplace=True)

    data20 = read_excel(qlms_file, sheet_name='20',
                      skiprows=4, header=3, usecols="A:E",
                      na_values='..')
    data20 = data20[~data20[data20.columns[2]].isna()].reset_index(drop=True)
    data20.rename(columns={
      'Unnamed: 0': 'Quarter'
    }, inplace=True)


    chdir(DATA_DIR)
    data9.to_csv('qlms-9.csv', index=False)
    data11.to_csv('qlms-11.csv', index=False)
    data12.to_csv('qlms-12.csv', index=False)
    data20.to_csv('qlms-20.csv', index=False)


if __name__ == "__main__":
    main()
