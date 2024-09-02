import pandas as pd

# Define the base path for the data files
PATH1 = r"C:\\Users\\sandl305\\Documents\\GitHub\\Federal_remote_work\\opm_datasets\\unzipped_files\\"

# Define the file paths
sepdata_file = f"{PATH1}SEPDATA_FY2020-2024.txt"
dtagy_file = f"{PATH1}DTagy.txt"
dtsep_file = f"{PATH1}DTsep.txt"
dtefdate_file = f"{PATH1}DTefdate.txt"
dtagelvl_file = f"{PATH1}DTagelvl.txt"
dtedlvl_file = f"{PATH1}DTedlvl.txt"
dtgsegrd_file = f"{PATH1}DTgsegrd.txt"
dtloslvl_file = f"{PATH1}DTloslvl.txt"
dtloc_file = f"{PATH1}DTloc.txt"
dtocc_file = f"{PATH1}DTocc.txt"
dtpatco_file = f"{PATH1}DTpatco.txt"
dtppgrd_file = f"{PATH1}DTppgrd.txt"
dtsallvl_file = f"{PATH1}DTsallvl.txt"
dtstem_file = f"{PATH1}DTstemocc.txt"
dttoa_file = f"{PATH1}DTtoa.txt"
dtwrksch_file = f"{PATH1}DTwrksch.txt"
dtwkstat_file = f"{PATH1}DTwkstat.txt"

# Function to read in a CSV file with specific parameters
def read_csv_file(file_path, columns, dtypes):
    return pd.read_csv(file_path, delimiter=',', header=0, dtype=dtypes, usecols=columns, skipinitialspace=True)

# Define column names and data types for SEPDATA table
sepdata_columns = [
    "AGYSUB", "SEP", "EFDATE", "AGELVL", "EDLVL", "GSEGRD", "LOSLVL", "LOC", "OCC", "PATCO",
    "PPGRD", "SALLVL", "STEMOCC", "TOA", "WORKSCH", "WORKSTAT", "COUNT", "SALARY", "LOS"
]
sepdata_dtypes = {
    "AGYSUB": 'string', "SEP": 'string', "EFDATE": 'string', "AGELVL": 'string', "EDLVL": 'string', 
    "GSEGRD": 'string', "LOSLVL": 'string', "LOC": 'string', "OCC": 'string', "PATCO": 'string', 
    "PPGRD": 'string', "SALLVL": 'string', "STEMOCC": 'string', "TOA": 'string', "WORKSCH": 'string', 
    "WORKSTAT": 'string', "COUNT": 'string', "SALARY": 'float', "LOS": 'float'
}

# Read in SEPDATA table
sepdata_df = read_csv_file(sepdata_file, sepdata_columns, sepdata_dtypes)

# Reading Agency Dimension Translation Table (DTagy)
dtagy_columns = ["AGYTYP", "AGYTYPT", "AGY", "AGYT", "AGYSUB", "AGYSUBT"]
dtagy_dtypes = {"AGYTYP": 'string', "AGYTYPT": 'string', "AGY": 'string', "AGYT": 'string', "AGYSUB": 'string', "AGYSUBT": 'string'}
dtagy_df = read_csv_file(dtagy_file, dtagy_columns, dtagy_dtypes)

# Reading Separation Dimension Translation Table (DTsep)
dtsep_columns = ["SEP", "SEPT"]
dtsep_dtypes = {"SEP": 'string', "SEPT": 'string'}
dtsep_df = read_csv_file(dtsep_file, dtsep_columns, dtsep_dtypes)

# Reading Effective Date Dimension Translation Table (DTefdate)
dtefdate_columns = ["FY", "FYT", "QTR", "QTRT", "EFDATE", "EFDATET"]
dtefdate_dtypes = {"FY": 'string', "FYT": 'string', "QTR": 'string', "QTRT": 'string', "EFDATE": 'string', "EFDATET": 'string'}
dtefdate_df = read_csv_file(dtefdate_file, dtefdate_columns, dtefdate_dtypes)

# Reading Age Level Dimension Translation Table (DTagelvl)
dtagelvl_columns = ["AGELVL", "AGELVLT"]
dtagelvl_dtypes = {"AGELVL": 'string', "AGELVLT": 'string'}
dtagelvl_df = read_csv_file(dtagelvl_file, dtagelvl_columns, dtagelvl_dtypes)

# Reading Education Level Dimension Translation Table (DTedlvl)
dtedlvl_columns = ["EDLVLTYP", "EDLVLTYPT", "EDLVL", "EDLVLT"]
dtedlvl_dtypes = {"EDLVLTYP": 'string', "EDLVLTYPT": 'string', "EDLVL": 'string', "EDLVLT": 'string'}
dtedlvl_df = read_csv_file(dtedlvl_file, dtedlvl_columns, dtedlvl_dtypes)

# Similarly, read the other files as needed...

# Example: Reading Work Status Dimension Translation Table (DTwkstat)
dtwkstat_columns = ["WORKSTAT", "WORKSTATT"]
dtwkstat_dtypes = {"WORKSTAT": 'string', "WORKSTATT": 'string'}
dtwkstat_df = read_csv_file(dtwkstat_file, dtwkstat_columns, dtwkstat_dtypes)

# Repeat for other dimension tables with appropriate columns and types...

print(sepdata_df.head())  # Displaying first few rows for validation

# Save the combined DataFrame for all agencies as a CSV file
sepdata_df.to_csv('sepdata_all_agencies.csv', index=False)
print("All agencies data saved to 'sepdata_all_agencies.csv'")

# Filter to keep only rows where AGYSUB starts with 'CM' for CM agencies
cm_agencies_df = sepdata_df[sepdata_df['AGYSUB'].str.startswith('CM', na=False)]

# Save the filtered DataFrame for CM agencies as a CSV file
cm_agencies_df.to_csv('sepdata_cm_agencies.csv', index=False)
print("CM agencies data saved to 'sepdata_cm_agencies.csv'")
