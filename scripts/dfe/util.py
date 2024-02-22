import os 
import re 
import pandas as pd

def save_tidy_csv(df, directory, filename, index=True):
    # First add the header
    ncol = len(df.columns)
    new_record = pd.DataFrame([[*['---'] * ncol]],columns=df.columns)
    final = pd.concat([new_record, df], ignore_index=True)

    # Get the output as CSV
    csv = final.to_csv(index=index)

    # Because we added an index column we will now tidy 
    csv = re.sub(r'\n0,---,---', '\n---,---,---', csv)

    text_file = open(os.path.join(directory, filename), "w")
    text_file.write(csv)
    text_file.close()