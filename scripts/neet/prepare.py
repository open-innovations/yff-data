import os
import scripts.util.file

from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = 'src/_data/sources/neet'
os.makedirs(DATA_DIR, exist_ok=True)


if __name__ == "__main__":
    scripts.util.file.copy("neet.csv", from_dir=RAW_DATA_DIR, to_dir=DATA_DIR)
