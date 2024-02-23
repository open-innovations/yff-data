import os
import re
import pandas as pd


def copy(name, from_dir, to_dir):
    data = pd.read_csv(os.path.join(from_dir, name))
    data.index = pd.Index(range(0, len(data.index)), name='quarter_index')
    data.to_csv(
        os.path.join(to_dir, name)
    )


def add_index(data):
    data = data.reset_index()
    data.index = pd.Index(range(0, len(data.index)), name='quarter_index')
    return data


def save_tidy_csv(df, directory, filename, with_index=True):
    # First add the header
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]], columns=df.columns)
    final = pd.concat([new_record, df], ignore_index=True)

    # Get the output as CSV
    csv = final.to_csv(index=with_index)

    # Because we added an index column we will now tidy
    csv = re.sub(r'\n0,---,---', '\n---,---,---', csv)

    text_file = open(os.path.join(directory, filename), "w")
    text_file.write(csv)
    text_file.close()
