# Import necessary files
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Import helper customized functions
from helperFunctions.read_data import import_data
from helperFunctions.check_merge_data import merge_check_data
from helperFunctions.tidy_data import clean_data
from helperFunctions.cohorts import *

# Read row files data
rowConvPath = "data/table_A_conversions.csv"
rowAttrPath = "data/table_B_attribution.csv"
rowConvData, rowAttrData = import_data(rowConvPath, rowAttrPath)

# Merge data
rowDataMerged = merge_check_data(rowConvData, rowAttrData)

# Get unique Channels
uniqueChannels = sorted(rowDataMerged.Channel.unique().to_list())

# Get clean data frame
cleanUserAttr_df = clean_data(rowDataMerged)

# Save the new tidy data frame to a new CSV file
cleanUserAttr_df.to_csv("data/cleanUserAttr_df.csv")

# Get some KPI"s and insights
# Revenue over time
plot_rev_over_time(df=cleanUserAttr_df, df_gp_by="Conv_Date", df_col="Revenue", df_agg_func="sum",
                   title="Revenue Over Time", xlab="Transaction Month and Year", ylab="Total Revenue",
                   save_f_name="Revenue_Over_Time")
print("We can notice that revenue is always high between march and april every year thus we conclude seasonal offers "
      "or purchasing during this period")

# Fraction of return customers
fracReturnCustomers = (cleanUserAttr_df.groupby("User_ID")[
                           "Conv_ID"].nunique() > 1).sum() / cleanUserAttr_df.User_ID.nunique()
print("Fraction of return cutomers is {:.2f} %".format(fracReturnCustomers * 100))

# Add cohort columns to the data frame
add_cohort_columns(cleanUserAttr_df, "User_ID")
print(cleanUserAttr_df.head())

# Monthly Active customers in each cohort
cohort_counts = build_time_cohort(df=cleanUserAttr_df, df_grp_by=["CohortMonth", "CohortIndex"], cohort_slic="User_ID",
                                  func=pd.Series.nunique)
vis_cohort(cohort_counts, "Monthly Active customers in each cohort", "Monthly_Active_customers_in_each_cohort")
print("We can notice that the first column contains the total of active cohort customers in each cohort month")
print("We can notice also that April 2017 has the most number of active users and cohort users")

# Retention Rate Cohort
# Get the total cohort sizes or counts from the first column of the cohort_counts
cohort_sizes = cohort_counts.iloc[:, 0]
retention = cohort_counts.divide(cohort_sizes, axis=0)
# Plot the Retention Rate Cohort and exclude the first column of the total for better visualization in the heat map
vis_cohort(retention.iloc[:, 1:], "Retention Rate Cohort", "Retention_Rate_Cohort")
print("I excluded the first column of the total for better visualization in the heat map")

# Calculate total revenue by Monthly Cohorts
rev_counts = build_time_cohort(df=cleanUserAttr_df, df_grp_by=["CohortMonth", "CohortIndex"], cohort_slic="Revenue",
                               func=sum)
vis_cohort(df=rev_counts, plt_title="Total Revenue by Monthly Cohorts", frmt=".1f",
           save_f_name="Total_Revenue_by_Monthly_Cohorts")

# Get a snapshot of the data collection date which is exactly after the maximum date with 1 day
snapshot_date = max(cleanUserAttr_df.Conv_Date) + timedelta(days=1)
print("Snapshot date " + str(snapshot_date))

# RFMT segmentation
# Recency - R - days since last customer transaction
# Frequency - F - number of transactions in the last 13 months
# Monetary Value - M - total spend in the last 13 months
# Tenure - T - time since the first transaction

# Get RFMT data
# rfmtDatamart = build_rfmt(cleanUserAttr_cleanUserAttr_df, snapshot_date)

# Group Data
dataPerUID = cleanUserAttr_df.groupby('User_ID')

# Calculate Recency, Frequency, Monetary and Tenure values for each customer
recency = lambda x: (snapshot_date - x.max()).days
tenure = lambda x: (snapshot_date - x.min()).days

# Build RFMT
rfmt_datamart = dataPerUID.agg(
    Recency=('InvoiceDay', recency),
    Frequency=('Conv_ID', 'count'),
    MonetaryValue=('Revenue', sum),
    Tenure=('InvoiceDay', tenure))
print(rfmt_datamart.head())

# Show plots at the end of the run
plt.show()
