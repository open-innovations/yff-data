import os
import shutil

from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = 'src/_data/sources/qlfs'
os.makedirs(DATA_DIR, exist_ok=True)


def copy_file(name):
    shutil.copyfile(
        os.path.join(RAW_DATA_DIR, name),
        os.path.join(DATA_DIR, name)
    )


if __name__ == "__main__":
    copy_file("long_term_unemployed.csv")
    copy_file("not_in_education.csv")
