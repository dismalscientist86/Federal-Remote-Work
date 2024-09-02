import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from cm_agencies_combined.csv
sepdata_df = pd.read_csv('sepdata_all_agencies.csv')

# 1. Bar Plot: Distribution of Separations by Age Level
plt.figure(figsize=(10, 6))
sns.countplot(data=sepdata_df, x='AGELVL', palette='viridis')
plt.title('Distribution of Separations by Age Level')
plt.xlabel('Age Level')
plt.ylabel('Count of Separations')
plt.show()

# 2. Histogram: Distribution of Salaries
plt.figure(figsize=(10, 6))
sns.histplot(sepdata_df['SALARY'], bins=30, kde=True, color='blue')
plt.title('Distribution of Salaries')
plt.xlabel('Salary')
plt.ylabel('Frequency')
plt.show()

# 3. Line Plot: Separations Over Time
# Convert EFDATE to datetime format for plotting
sepdata_df['EFDATE'] = pd.to_datetime(sepdata_df['EFDATE'], format='%Y%m')
sepdata_df_grouped = sepdata_df.groupby('EFDATE').size().reset_index(name='Separations')

plt.figure(figsize=(10, 6))
sns.lineplot(data=sepdata_df_grouped, x='EFDATE', y='Separations', marker='o', color='red')
plt.title('Separations Over Time')
plt.xlabel('Effective Date')
plt.ylabel('Count of Separations')
plt.show()

# 4. Scatter Plot: Salary vs. Length of Service (LOS)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=sepdata_df, x='LOS', y='SALARY', hue='AGELVL', palette='coolwarm')
plt.title('Salary vs. Length of Service (LOS)')
plt.xlabel('Length of Service (LOS)')
plt.ylabel('Salary')
plt.show()

# 5. Pie Chart: Count of Work Status
workstat_counts = sepdata_df['WORKSTAT'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(workstat_counts, labels=workstat_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Distribution of Work Status')
plt.show()

# Group by EFDATE and calculate the average LOS
avg_los_by_date = sepdata_df.groupby('EFDATE')['LOS'].mean().reset_index()

# Plotting Average Length of Service by Separation Effective Date
plt.figure(figsize=(10, 6))
sns.lineplot(data=avg_los_by_date, x='EFDATE', y='LOS', marker='o', color='blue')
plt.title('Average Length of Service (LOS) by Separation Effective Date')
plt.xlabel('Effective Date')
plt.ylabel('Average Length of Service (LOS)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()