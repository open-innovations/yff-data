import os 
import pandas as pd 
import shutil

WORKING_DIR = os.path.join('working', 'upstream')
OUT_DIR = os.path.join('data', 'area', 'pcon')

data = pd.read_csv(
    os.path.join(WORKING_DIR, 'education_attainment_pcon_2010.csv')).drop(
        columns={'pcon_name'}).rename(
            columns={'pcon_code': 'PCON22CD'})
data['suffix'] = '%'

data = data.rename(columns={
    'avg_att8': 'Average Attainment 8 Score',
    'avg_p8score': 'Average Progress 8 Score',
    'pt_l2basics_94': 'Percentage Achieving Grade 4 English & Maths',
    'pt_l2basics_95': 'Percentage Achieving Grade 5 English & Maths',
})

# TODO Calculate projected versions for each 2024 constituency, if possible

data.to_csv(os.path.join(OUT_DIR, 'education_attainment_pcon_2010.csv'), index=False)