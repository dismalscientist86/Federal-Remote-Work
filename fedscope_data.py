import pandas as pd

# Set the path to the raw data files
PATH1 = r'C:\\Users\\sandl305\\Documents\\GitHub\\Federal_remote_work\\opm_datasets\\unzipped_files\\'

# Define a helper function to read files with specific data types and formats
def read_csv_file(filename, dtype_dict, column_names=None):
    try:
        # Use 'names' to set the correct column names and avoid skipping any rows
        df = pd.read_csv(filename, dtype=dtype_dict, delimiter=',', names=column_names, skiprows=1 if column_names else 0)
        return df
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return pd.DataFrame()

# Define quarters and years to loop through
quarters = ['MAR', 'JUN', 'SEP', 'DEC']
years = range(2019, 2024)

# List to store all DataFrames for combination
all_factdata = []

# Loop through each year and quarter
for year in years:
    for quarter in quarters:
        # Construct the filename dynamically based on the year and quarter
        factdata_file = f"{PATH1}FACTDATA_{quarter}{year}.txt"
        
        # Define columns and data types for FACTDATA
        factdata_columns = [
            'AGYSUB', 'LOC', 'AGELVL', 'EDLVL', 'GSEGRD', 'LOSLVL', 'OCC', 'PATCO', 'PP', 'PPGRD',
            'SALLVL', 'STEMOCC', 'SUPERVIS', 'TOA', 'WORKSCH', 'WORKSTAT', 'DATECODE', 'EMPLOYMENT',
            'SALARY', 'LOS'
        ]
        factdata_dtypes = {
            'AGYSUB': str, 'LOC': str, 'AGELVL': str, 'EDLVL': str, 'GSEGRD': str,
            'LOSLVL': str, 'OCC': str, 'PATCO': str, 'PP': str, 'PPGRD': str,
            'SALLVL': str, 'STEMOCC': str, 'SUPERVIS': str, 'TOA': str, 'WORKSCH': str,
            'WORKSTAT': str, 'DATECODE': str, 'EMPLOYMENT': str, 'SALARY': 'float64',
            'LOS': 'float64'
        }

        # Read the file
        df = read_csv_file(factdata_file, factdata_dtypes, factdata_columns)
        
        # Append the DataFrame to the list
        all_factdata.append(df)

# Combine all DataFrames into one DataFrame for all agencies across all quarters
all_agencies_df = pd.concat(all_factdata, ignore_index=True)

# Filter to keep only rows where AGYSUB starts with 'CM' for CM agencies
cm_agencies_df = all_agencies_df[all_agencies_df['AGYSUB'].str.startswith('CM', na=False)]

# Save the combined DataFrame for all agencies as a CSV file
all_agencies_df.to_csv('all_agencies_combined.csv', index=False)
print("All agencies data saved to 'all_agencies_combined.csv'")

# Save the filtered DataFrame for CM agencies as a CSV file
cm_agencies_df.to_csv('cm_agencies_combined.csv', index=False)
print("CM agencies data saved to 'cm_agencies_combined.csv'")

# Read in other dimension translation tables
dimension_files = {
    "DTagy": {"filename": f"{PATH1}DTagy.txt", "columns": ['AGYTYP', 'AGYTYPT', 'AGY', 'AGYT', 'AGYSUB', 'AGYSUBT'], "dtype": {'AGYTYP': str, 'AGYTYPT': str, 'AGY': str, 'AGYT': str, 'AGYSUB': str, 'AGYSUBT': str}},
    "DTloc": {"filename": f"{PATH1}DTloc.txt", "columns": ['LOCTYP', 'LOCTYPT', 'LOC', 'LOCT'], "dtype": {'LOCTYP': str, 'LOCTYPT': str, 'LOC': str, 'LOCT': str}},
    "DTagelvl": {"filename": f"{PATH1}DTagelvl.txt", "columns": ['AGELVL', 'AGELVLT'], "dtype": {'AGELVL': str, 'AGELVLT': str}},
    "DTedlvl": {"filename": f"{PATH1}DTedlvl.txt", "columns": ['EDLVLTYP', 'EDLVLTYPT', 'EDLVL', 'EDLVLT'], "dtype": {'EDLVLTYP': str, 'EDLVLTYPT': str, 'EDLVL': str, 'EDLVLT': str}},
    "DTgsegrd": {"filename": f"{PATH1}DTgsegrd.txt", "columns": ['GSEGRD'], "dtype": {'GSEGRD': str}},
    "DTloslvl": {"filename": f"{PATH1}DTloslvl.txt", "columns": ['LOSLVL', 'LOSLVLT'], "dtype": {'LOSLVL': str, 'LOSLVLT': str}},
    "DTocc": {"filename": f"{PATH1}DTocc.txt", "columns": ['OCCTYP', 'OCCTYPT', 'OCCFAM', 'OCCFAMT', 'OCC', 'OCCT'], "dtype": {'OCCTYP': str, 'OCCTYPT': str, 'OCCFAM': str, 'OCCFAMT': str, 'OCC': str, 'OCCT': str}},
    "DTpatco": {"filename": f"{PATH1}DTpatco.txt", "columns": ['PATCO', 'PATCOT'], "dtype": {'PATCO': str, 'PATCOT': str}},
    "DTpp": {"filename": f"{PATH1}DTpp.txt", "columns": ['PP_AGG', 'PP_AGGT', 'PP', 'PPT'], "dtype": {'PP_AGG': str, 'PP_AGGT': str, 'PP': str, 'PPT': str}},
    "DTppgrd": {"filename": f"{PATH1}DTppgrd.txt", "columns": ['PPTYP', 'PPTYPT', 'PPGROUP', 'PPGROUPT', 'PAYPLAN', 'PAYPLANT', 'PPGRD'], "dtype": {'PPTYP': str, 'PPTYPT': str, 'PPGROUP': str, 'PPGROUPT': str, 'PAYPLAN': str, 'PAYPLANT': str, 'PPGRD': str}},
    "DTsallvl": {"filename": f"{PATH1}DTsallvl.txt", "columns": ['SALLVL', 'SALLVLT'], "dtype": {'SALLVL': str, 'SALLVLT': str}},
    "DTstemocc": {"filename": f"{PATH1}DTstemocc.txt", "columns": ['STEMAGG', 'STEMAGGT', 'STEMTYP', 'STEMTYPT', 'STEMOCC', 'STEMOCCT'], "dtype": {'STEMAGG': str, 'STEMAGGT': str, 'STEMTYP': str, 'STEMTYPT': str, 'STEMOCC': str, 'STEMOCCT': str}},
    "DTsuper": {"filename": f"{PATH1}DTsuper.txt", "columns": ['SUPERTYP', 'SUPERTYPT', 'SUPERVIS', 'SUPERVIST'], "dtype": {'SUPERTYP': str, 'SUPERTYPT': str, 'SUPERVIS': str, 'SUPERVIST': str}},
    "DTtoa": {"filename": f"{PATH1}DTtoa.txt", "columns": ['TOATYP', 'TOATYPT', 'TOA', 'TOAT'], "dtype": {'TOATYP': str, 'TOATYPT': str, 'TOA': str, 'TOAT': str}},
    "DTwrksch": {"filename": f"{PATH1}DTwrksch.txt", "columns": ['WSTYP', 'WSTYPT', 'WORKSCH', 'WORKSCHT'], "dtype": {'WSTYP': str, 'WSTYPT': str, 'WORKSCH': str, 'WORKSCHT': str}},
    "DTwkstat": {"filename": f"{PATH1}DTwkstat.txt", "columns": ['WORKSTAT', 'WORKSTATT'], "dtype": {'WORKSTAT': str, 'WORKSTATT': str}},
    "DTdate": {"filename": f"{PATH1}DTdate.txt", "columns": ['DATECODE', 'DATECODET'], "dtype": {'DATECODE': str, 'DATECODET': str}},
}

# Store each DataFrame in a dictionary for access
dimension_dfs = {}
for key, info in dimension_files.items():
    dimension_dfs[key] = read_csv_file(info["filename"], info["dtype"], info["columns"])

# Now, dimension_dfs contains all the dimension tables as DataFrames

# Example of accessing the data:
print(all_agencies_df.head())  # Combined DataFrame for all agencies
print(cm_agencies_df.head())   # Filtered DataFrame for CM agencies
