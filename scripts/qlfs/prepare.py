import os
import scripts.util.file

from transform import DATA_DIR as RAW_DATA_DIR

DATA_DIR = 'src/_data/sources/qlfs'
os.makedirs(DATA_DIR, exist_ok=True)


if __name__ == "__main__":
    scripts.util.file.copy("long_term_unemployed.csv",
                   from_dir=RAW_DATA_DIR, to_dir=DATA_DIR)
    scripts.util.file.copy("not_in_education.csv",
                   from_dir=RAW_DATA_DIR, to_dir=DATA_DIR)
