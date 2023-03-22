import os
import pandas as pd

DATA_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'cff'))
WORKING_DIR = os.path.realpath(os.path.join('working'))
CFF_APPLICATIONS = os.path.realpath(os.path.join(WORKING_DIR, 'applications.csv'))
LOOKUP = os.path.realpath(os.path.join(WORKING_DIR, 'itl_lookup.csv'))
os.makedirs(DATA_DIR, exist_ok=True)

def main(): 
    # Map CFF applications to ITL regions    
    la_data = pd.read_csv(CFF_APPLICATIONS, usecols=[0]) 
    itl_lookup = pd.read_csv(LOOKUP)
    applications = pd.merge(la_data, itl_lookup, on='Local authority')
    applications['Application count'] = applications.groupby('Local authority')['Local authority'].transform('count')
    applications = applications.drop_duplicates(subset=['Local authority'], keep='first')
    applications.to_csv(os.path.join(DATA_DIR, 'applications_la_itl.csv'), index = False)

    # Applications by ITL2 
    itl2_apps = applications[['ITL221CD', 'ITL221NM', 'Application count']]
    itl2_apps['Application count'] = itl2_apps.groupby('ITL221NM')['ITL221NM'].transform('count')
    itl2_apps = itl2_apps.drop_duplicates(subset=['ITL221NM'], keep='first')
    itl2_apps.to_csv(os.path.join(DATA_DIR, 'application_by_itl2.csv'), index=False)

    # Applications by ITL3
    itl3_apps = applications[['ITL321CD', 'ITL321NM', 'Application count']]
    itl3_apps['Application count'] = itl3_apps.groupby('ITL321NM')['ITL321NM'].transform('count')
    itl3_apps = itl3_apps.drop_duplicates(subset=['ITL321NM'], keep='first')
    itl3_apps.to_csv(os.path.join(DATA_DIR, 'application_by_itl3.csv'), index=False)

if __name__ == "__main__":
    main()




