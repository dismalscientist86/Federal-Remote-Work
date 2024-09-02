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

# Combine smaller agencies into "CM00=Other Commerce"
cm_agencies_df['AGYSUB'] = cm_agencies_df['AGYSUB'].apply(lambda x: x if x in major_agencies else 'Other Commerce')

# Convert 'DATECODE' to string, add a day '01', and convert to datetime format
cm_agencies_df['DATECODE'] = pd.to_datetime(cm_agencies_df['DATECODE'].astype(str) + '01', format='%Y%m%d')

# Convert the datetime to a quarterly period format (e.g., '2019Q1', '2019Q2', etc.)
cm_agencies_df['DATECODE'] = cm_agencies_df['DATECODE'].dt.to_period('Q')

# Convert 'DATECODE' to string format for seaborn plotting compatibility
cm_agencies_df['DATECODE'] = cm_agencies_df['DATECODE'].astype(str)

# Group by 'DATECODE' and 'AGYSUB', then calculate the mean of 'LOS'
average_los_by_agency = cm_agencies_df.groupby(['DATECODE', 'AGYSUB'], as_index=False)['LOS'].mean()

# Rename columns for clarity
average_los_by_agency.rename(columns={'LOS': 'Average_LOS'}, inplace=True)

# Plot for Average Length of Service (LOS) by Agency
plt.figure(figsize=(14, 8))

# Use seaborn to create a line plot with multiple lines (one for each AGYSUB)
sns.lineplot(data=average_los_by_agency, x='DATECODE', y='Average_LOS', hue='AGYSUB', marker='o')

# Customize the plot
plt.title('Average Length of Service (LOS) by Quarter for Each AGYSUB in CM Agencies')
plt.xlabel('Quarter')
plt.ylabel('Average LOS')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Agency', bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()

# Group by 'DATECODE' and 'AGYSUB', then calculate the total of 'EMPLOYMENT'
total_employment_by_agency = cm_agencies_df.groupby(['DATECODE', 'AGYSUB'], as_index=False)['EMPLOYMENT'].sum()

# Rename columns for clarity
total_employment_by_agency.rename(columns={'EMPLOYMENT': 'Total_Employment'}, inplace=True)

# Extract employment data for March 2022 (first quarter of 2022)
march_2022_data = total_employment_by_agency[total_employment_by_agency['DATECODE'] == '2022Q1']

# Create a dictionary of March 2022 employment values per agency
march_2022_employment = march_2022_data.set_index('AGYSUB')['Total_Employment'].to_dict()

# Function to normalize employment data by March 2022 employment
def normalize_by_march_2022(row):
    if row['AGYSUB'] in march_2022_employment:
        return row['Total_Employment'] / march_2022_employment[row['AGYSUB']]
    else:
        return None  # Handle cases where March 2022 data is missing

# Apply the normalization to the 'Total_Employment' column
total_employment_by_agency['Normalized_Employment'] = total_employment_by_agency.apply(normalize_by_march_2022, axis=1)

# Remove rows with missing normalization values
total_employment_by_agency.dropna(subset=['Normalized_Employment'], inplace=True)

# Plot for Total Employment by Agency
plt.figure(figsize=(14, 8))

# Use seaborn to create a line plot with multiple lines (one for each AGYSUB)
sns.lineplot(data=total_employment_by_agency, x='DATECODE', y='Total_Employment', hue='AGYSUB', marker='o', legend=None)

# Add end-of-line labels
for agency in total_employment_by_agency['AGYSUB'].unique():
    # Get the data for the current agency
    agency_data = total_employment_by_agency[total_employment_by_agency['AGYSUB'] == agency]
    
    # Get the last point data for each agency
    last_point = agency_data.iloc[-1]
    
    # Add the text label near the end of the line
    plt.text(
        last_point['DATECODE'], 
        last_point['Total_Employment'], 
        agency,
        horizontalalignment='left', 
        size='medium', 
        color='black'
    )

# Customize the plot
plt.title('Total Employment by Quarter for Each AGYSUB in CM Agencies')
plt.xlabel('Quarter')
plt.ylabel('Normalized Employment')
plt.xticks(rotation=45)
plt.grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()


# Plot for Normalized Employment by Agency
plt.figure(figsize=(14, 8))

# Use seaborn to create a line plot with multiple lines (one for each AGYSUB)
sns.lineplot(data=total_employment_by_agency, x='DATECODE', y='Normalized_Employment', hue='AGYSUB', marker='o', legend=None)

# Add end-of-line labels
for agency in total_employment_by_agency['AGYSUB'].unique():
    # Get the data for the current agency
    agency_data = total_employment_by_agency[total_employment_by_agency['AGYSUB'] == agency]
    
    # Get the last point data for each agency
    last_point = agency_data.iloc[-1]
    
    # Add the text label near the end of the line
    plt.text(
        last_point['DATECODE'], 
        last_point['Normalized_Employment'], 
        agency,
        horizontalalignment='left', 
        size='medium', 
        color='black'
    )

# Customize the plot
plt.title('Normalized Total Employment by Quarter for Each AGYSUB in CM Agencies (March 2022 Baseline)')
plt.xlabel('Quarter')
plt.ylabel('Normalized Employment')
plt.xticks(rotation=45)
plt.grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()

# Extract March 2022 data for KDE plot (including LOS column)
march_2022_data = cm_agencies_df[cm_agencies_df['DATECODE'] == '2022Q1']

# KDE Plot for Length of Service (LOS) by Agency for March 2022
plt.figure(figsize=(12, 6))

# Plot KDE for each agency
for agency in march_2022_data['AGYSUB'].unique():
    sns.kdeplot(
        data=march_2022_data[march_2022_data['AGYSUB'] == agency],
        x='LOS',
        label=agency,
        fill=True,  # Fill under the KDE curve
        common_norm=False,  # Do not normalize across different agencies
        alpha=0.6  # Transparency level for better visibility
    )

# Customize the plot
plt.title('Kernel Density of Length of Service (LOS) by Major Agencies and Other Commerce (March 2022)')
plt.xlabel('Length of Service (LOS)')
plt.ylabel('Density')
plt.grid(True)
plt.legend(title='Agency')

# Show the plot
plt.tight_layout()
plt.show()
