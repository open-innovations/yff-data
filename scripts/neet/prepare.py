import os
import shutil

from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = 'src/_data/sources/neet'
os.makedirs(DATA_DIR, exist_ok=True)


def copy_file(name):
    shutil.copyfile(
        os.path.join(RAW_DATA_DIR, name),
        os.path.join(DATA_DIR, name)
    )


if __name__ == "__main__":
    copy_file("neet.csv")
