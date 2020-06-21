# Import necessary files
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from helperFunctions.read_data import import_data

# Read row files data
rowConvPath = 'data/table_A_conversions.csv'
rowAttrPath = 'data/table_B_attribution.csv'
rowConvData, rowAttrData = import_data(rowConvPath, rowAttrPath)
# rowConvData = pd.read_csv('data/table_A_conversions.csv')
# rowAttrData = pd.read_csv('data/table_B_attribution.csv')

# print files details
print(rowConvData.info())
print('\n')
print(rowAttrData.info())

# Merge two tables based on Conversion ID with inner join to get common data only
rowMerged = rowConvData.merge(rowAttrData, on='Conv_ID', how='inner')


# Explore new table
print('Info\n')
print(rowMerged.info())
print('\n------------------------------------\nHead\n')
print(rowMerged.head())
print('\n------------------------------------\nNumber of unique categories in each field\n')
print(rowMerged.nunique())
print('\n------------------------------------\nNumber of missing values and its portion of the data\n')
print(pd.DataFrame({'count':rowMerged.isnull().sum(), 'Pct% of the data':rowMerged.isnull().mean() * 100}))

# Remove missing data since only 6638 rows have missing data (about 3%)
rowMerged.dropna(axis=0, how='any', inplace=True)
rowMerged.info()

# Fix Conv_Date and Channel columns data types
print('data types before fixing :\n')
print(rowMerged.dtypes)
rowMerged.Conv_Date = pd.to_datetime(rowMerged.Conv_Date)
rowMerged.Channel = rowMerged.Channel.astype('category')
print('\n\ndata types after fixing :\n')
print(rowMerged.dtypes)

# Data range and taking snapshot_date
print('Min:{}; Max:{}'.format(min(rowMerged.Conv_Date),max(rowMerged.Conv_Date)))

snapshot_date = max(rowMerged.Conv_Date) + timedelta(days=1)

# Check whether any users conversed in the same day or more than one day
print((rowMerged.groupby('Conv_ID')['Conv_Date'].agg('nunique') > 1).sum())

ihcPerConv = rowMerged.pivot(index='Conv_ID', columns='Channel', values='IHC_Conv').fillna(-1)
ihcPerConv.sort_index(inplace=True)
ihcPerConv.head()

cleanMerged = rowMerged.drop(['Channel', 'IHC_Conv'], axis=1)
cleanMerged.drop_duplicates(inplace=True)
cleanMerged.set_index('Conv_ID', inplace=True)
cleanMerged.sort_index(inplace=True)
cleanMerged.head()

cleanData = pd.concat([cleanMerged, ihcPerConv], axis=1).reset_index()
cleanData.to_csv('data/cleanData.csv')
cleanData.head()


# Time cohort
# Define a function that will parse the date
def get_day(x): return datetime(x.year, x.month, 1)

cleanData['InvoiceMonth'] = cleanData.Conv_Date.apply(get_day)
grouping = cleanData.groupby('User_ID')['InvoiceMonth']
cleanData['CohortMonth'] = grouping.transform('min')
print(cleanData.head())

# Calculate time offset in days
def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
#     day = df[column].dt.day
    return year, month

# Get the integers for date parts from the `InvoiceMonth` column
invoice_year, invoice_month = get_date_int(cleanData, 'InvoiceMonth')
# Get the integers for date parts from the `CohortMonth` column
cohort_year, cohort_month = get_date_int(cleanData, 'CohortMonth')

# Calculate difference in years
years_diff = invoice_year - cohort_year
# Calculate difference in months
months_diff = invoice_month - cohort_month

# Extract the difference in months from all previous values
cleanData['CohortIndex'] = years_diff * 12 + months_diff + 1
print(cleanData.head())

# Revenue over time
groupedByDate = cleanData.groupby('Conv_Date')
groupedByDate['Revenue'].sum().plot()
plt.title('Revenue Over Time')
plt.xlabel('Transaction Month and Year')
plt.ylabel('Total Revenue')
plt.show()

# Fraction of return cutomers
fracReturnCustomers = (cleanData.groupby('User_ID')['Conv_ID'].nunique() > 1).sum() / cleanData.User_ID.nunique()
print('Fraction of return cutomers is {:.2f} %'.format(fracReturnCustomers * 100))

# Monthly Active customers in each cohort
# groupby(['CohortMonth', 'CohortIndex']
grouping = cleanData.groupby(['CohortMonth', 'CohortIndex'])

# Count the number of unique values per customer ID
cohort_data = grouping['User_ID'].apply(pd.Series.nunique).reset_index()

# Create a pivot
cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='User_ID')
cohort_counts.index = cohort_counts.index.to_period('M')
plt.figure(figsize=(16, 14))
plt.title('Monthly Active customers in each cohort')
sns.heatmap(data=cohort_counts, annot=True, cmap='Blues')
plt.yticks(rotation=0)
plt.show()

# Retention Rate Cohort
cohort_sizes = cohort_counts.iloc[:,0]
retention = cohort_counts.divide(cohort_sizes, axis=0)
plt.figure(figsize=(16, 14))
plt.title('Retention Rate Cohort')
sns.heatmap(data=retention.iloc[:, 1:], annot=True, cmap='Blues')
plt.yticks(rotation=0)
plt.show()

# Calculate total revenue by Monthly Cohorts
grouping = cleanData.groupby(['CohortMonth', 'CohortIndex'])
cohort_data = grouping['Revenue'].sum()
cohort_data = cohort_data.reset_index()
average_revenue = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='Revenue')
average_revenue.index = average_revenue.index.to_period('M')
plt.figure(figsize=(16, 14))
plt.title('Total Revenue by Monthly Cohorts')
sns.heatmap(data=average_revenue, annot=True, fmt=".1f", cmap='Blues')
plt.yticks(rotation=0)
plt.show()