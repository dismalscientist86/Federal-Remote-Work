import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from cm_agencies_combined.csv
cm_agencies_df = pd.read_csv('cm_agencies_combined.csv')

# Ensure that 'LOS' and 'EMPLOYMENT' are in the correct numeric format
cm_agencies_df['LOS'] = pd.to_numeric(cm_agencies_df['LOS'], errors='coerce')
cm_agencies_df['EMPLOYMENT'] = pd.to_numeric(cm_agencies_df['EMPLOYMENT'], errors='coerce')

# Map AGYSUB codes to their descriptive names
agysub_labels = {
    'CM51': 'Commerce', 'CM52': 'EDA', 'CM53': 'BEA', 'CM54': 'NOAA', 'CM55': 'ITA',
    'CM56': 'PTO', 'CM57': 'NIST', 'CM59': 'MBDA', 'CM61': 'NTIA', 'CM62': 'NTIS',
    'CM63': 'CENSUS', 'CM64': 'OIG', 'CM67': 'BIS'
}

# Replace AGYSUB codes with their descriptive names
cm_agencies_df['AGYSUB'] = cm_agencies_df['AGYSUB'].map(agysub_labels)

# List of major agencies to keep separate
major_agencies = ['CENSUS', 'PTO', 'NOAA', 'NIST']

# Combine smaller agencies into "Other Commerce"
cm_agencies_df['AGYSUB'] = cm_agencies_df['AGYSUB'].apply(lambda x: x if x in major_agencies else 'Other Commerce')

# Convert 'DATECODE' to string, add a day '01', and convert to datetime format
cm_agencies_df['DATECODE'] = pd.to_datetime(cm_agencies_df['DATECODE'].astype(str) + '01', format='%Y%m%d')

# Convert the datetime to a quarterly period format
cm_agencies_df['DATECODE'] = cm_agencies_df['DATECODE'].dt.to_period('Q')

# Convert 'DATECODE' to string format for seaborn plotting compatibility
cm_agencies_df['DATECODE'] = cm_agencies_df['DATECODE'].astype(str)

### Plot 1: KDE for "PTO" in March 2021, March 2022, and March 2023

# Filter data for "PTO" in the three periods
pto_data = cm_agencies_df[(cm_agencies_df['AGYSUB'] == 'PTO') & (cm_agencies_df['DATECODE'].isin(['2021Q1', '2022Q1', '2023Q1']))]

plt.figure(figsize=(12, 6))

# Plot KDE for each year
for date in ['2021Q1', '2022Q1', '2023Q1']:
    sns.kdeplot(
        data=pto_data[pto_data['DATECODE'] == date],
        x='LOS',
        label=f'PTO {date}',
        fill=True,  # Fill under the KDE curve
        alpha=0.6  # Transparency level for better visibility
    )

# Customize the plot
plt.title('Kernel Density of Length of Service (LOS) for PTO in March 2021, 2022, and 2023')
plt.xlabel('Length of Service (LOS)')
plt.ylabel('Density')
plt.grid(True)
plt.legend(title='Year')

# Show the plot
plt.tight_layout()
plt.show()

### Plot 2: KDE for Aggregated Agencies (Excluding "CENSUS," "PTO," and "BEA") in March 2021, 2022, and 2023

# Filter data excluding "CENSUS," "PTO," and "BEA" for the three periods
aggregated_data = cm_agencies_df[
    (~cm_agencies_df['AGYSUB'].isin(['CENSUS', 'PTO', 'BEA'])) & 
    (cm_agencies_df['DATECODE'].isin(['2021Q1', '2022Q1', '2023Q1']))
]

plt.figure(figsize=(12, 6))

# Plot KDE for each year
for date in ['2021Q1', '2022Q1', '2023Q1']:
    sns.kdeplot(
        data=aggregated_data[aggregated_data['DATECODE'] == date],
        x='LOS',
        label=f'Aggregated Agencies {date}',
        fill=True,  # Fill under the KDE curve
        alpha=0.6  # Transparency level for better visibility
    )

# Customize the plot
plt.title('Kernel Density of Length of Service (LOS) for Aggregated Agencies (Excluding CENSUS, PTO, BEA) in March 2021, 2022, and 2023')
plt.xlabel('Length of Service (LOS)')
plt.ylabel('Density')
plt.grid(True)
plt.legend(title='Year')

# Show the plot
plt.tight_layout()
plt.show()
