import os
import pandas as pd

DATA_DIR = os.path.realpath(os.path.join('src', '_data', 'sources', 'cff'))
WORKING_DIR = os.path.realpath(os.path.join('working'))
CFF_APPLICATIONS = os.path.realpath(os.path.join(WORKING_DIR, 'applications.csv'))
SHORTLISTED = os.path.realpath(os.path.join(DATA_DIR, 'shortlisted_awarded.csv'))
LOOKUP = os.path.realpath(os.path.join(WORKING_DIR, 'itl_lookup.csv'))
os.makedirs(DATA_DIR, exist_ok=True)

def main(): 
    # Map CFF applications to ITL regions    
    cff_data = pd.read_csv(CFF_APPLICATIONS, usecols=[0]) 
    cff_data['Application count'] = cff_data.groupby('Local authority')['Local authority'].transform('count')
    cff_data = cff_data.drop_duplicates(subset=['Local authority'], keep='first')
    itl_lookup = pd.read_csv(LOOKUP)
    applications_mapped = pd.merge(cff_data, itl_lookup, how='left', on='Local authority')
    print(applications_mapped)
    # # TODO: Manually match up LA codes that haven't merged.
    applications_mapped.to_csv(os.path.join(DATA_DIR, 'applications_mapped_la_itl.csv'), index = False)

    # Applications by ITL2 
    itl2_apps = applications_mapped[['ITL221CD', 'ITL221NM', 'Application count']]
    itl2_apps['Application count'] = itl2_apps.groupby('ITL221NM')['ITL221NM'].transform('count')
    itl2_apps = itl2_apps.drop_duplicates(subset=['ITL221NM'], keep='first')
    # itl2_apps.to_csv(os.path.join(DATA_DIR, 'application_by_itl2.csv'), index=False)

    # # applications_mapped by ITL3
    itl3_apps = applications_mapped[['ITL321CD', 'ITL321NM', 'Application count']]
    itl3_apps['Application count'] = itl3_apps.groupby('ITL321NM')['ITL321NM'].transform('count')
    itl3_apps = itl3_apps.drop_duplicates(subset=['ITL321NM'], keep='first')
    # itl3_apps.to_csv(os.path.join(DATA_DIR, 'application_by_itl3.csv'), index=False)

    # Shortlisted and awarded applications
    shortlisted = pd.read_csv(SHORTLISTED)
    applied = pd.merge(itl_lookup, shortlisted, how='left', on='Local authority')
    applied['Status'] = applied['Status'].fillna(0)
    applied.to_csv(os.path.join(DATA_DIR, 'apps_shortlisted.csv'), index=False)

    # Create csvs for SVG maps 
    itl2_shortlisted = pd.merge(itl2_apps, applied, how='left', on='ITL221CD')
    itl2_shortlisted.to_csv(os.path.join(DATA_DIR, 'itl2_shortlisted.csv'))


if __name__ == "__main__":
    main()




