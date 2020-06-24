# Import necessary files
from helperFunctions.check_merge_data import merge_check_data
from helperFunctions.clustering import *
from helperFunctions.cohorts import *
from helperFunctions.outlier_detection import outlier_detection
from helperFunctions.read_data import import_data
from helperFunctions.segmantation import *
from helperFunctions.tidy_data import clean_data

# Read row files data
rowConvPath = "data/table_A_conversions.csv"
rowAttrPath = "data/table_B_attribution.csv"
rowConvData, rowAttrData = import_data(rowConvPath, rowAttrPath)

# Merge data
rowDataMerged = merge_check_data(rowConvData, rowAttrData)

# Get tidy data frame and get unique Channels
tidyUserAttr_df, uniqueChannels = clean_data(rowDataMerged)

# Save the new tidy data frame to a new CSV file
tidyUserAttr_df.to_csv("data/cleanUserAttr_df.csv")

# Get some KPI"s and insights
# Revenue over time
plot_rev_over_time(df=tidyUserAttr_df, df_gp_by="Conv_Date", df_col="Revenue", df_agg_func="sum",
                   title="Revenue Over Time", xlab="Transaction Month and Year", ylab="Total Revenue",
                   save_f_name="Revenue_Over_Time")
print("We can notice that revenue is always high between march and april every year thus we conclude seasonal offers "
      "or purchasing during this period")

# Fraction of return customers
fracReturnCustomers = (tidyUserAttr_df.groupby("User_ID")[
                           "Conv_ID"].nunique() > 1).sum() / tidyUserAttr_df.User_ID.nunique()
print("Fraction of return cutomers is {:.2f} %".format(fracReturnCustomers * 100))

# Add cohort columns to the data frame
add_cohort_columns(tidyUserAttr_df, "User_ID")
print(tidyUserAttr_df.head())

# Monthly Active customers in each cohort
cohort_counts = build_time_cohort(df=tidyUserAttr_df, df_grp_by=["CohortMonth", "CohortIndex"], cohort_slic="User_ID",
                                  func=pd.Series.nunique)
vis_cohort(cohort_counts, "Monthly Active customers in each cohort", "Monthly_Active_customers_in_each_cohort")
print("We can notice that the first column contains the total of active cohort customers in each cohort month")
print("We can notice also that April 2017 has the most number of active users and cohort users")

# Retention Rate Cohort
# Get the total cohort sizes or counts from the first column of the cohort_counts
cohort_sizes = cohort_counts.iloc[:, 0]
retention = cohort_counts.divide(cohort_sizes, axis=0)
# Plot the Retention Rate Cohort and exclude the first column of the total for better visualization in the heat map
vis_cohort(retention, "Retention Rate Cohort", "Retention_Rate_Cohort")

# Calculate total revenue by Monthly Cohorts
rev_counts = build_time_cohort(df=tidyUserAttr_df, df_grp_by=["CohortMonth", "CohortIndex"], cohort_slic="Revenue",
                               func=sum)
vis_cohort(df=rev_counts, plt_title="Total Revenue by Monthly Cohorts", frmt=".1f",
           save_f_name="Total_Revenue_by_Monthly_Cohorts")

# Get a snapshot of the data collection date which is exactly after the maximum date with 1 day
snapshot_date = extract_snap_date(tidyUserAttr_df)
print("Snapshot date :" + str(snapshot_date))

# RFMT IHC segmentation
# Recency - R - days since last customer transaction
# Frequency - F - number of transactions in the last 13 months
# Monetary Value - M - total spend in the last 13 months
# Tenure - T - time since the first transaction
# IHC means - Initializer, Holder and Closer average values per customer per channel

# Get RFMT data
rfmtDM = build_rfmt(df=tidyUserAttr_df, snapshot_date=snapshot_date)

# Get IHC data
ihcDM = build_ihc(df=tidyUserAttr_df, channels=uniqueChannels)

# Get RFMT_IHC data
RfmtIhcDM = build_rfmt_ihc(rfmt_dm=rfmtDM, ihc_dm=ihcDM)

RfmtIhcDM.set_index('key_0', inplace=True)

# Data Exploration and cleaning process
# Exploratory Data Analysis (EDA)
for x in RfmtIhcDM.columns:
    print(x + ' Column Outliers Metrics:')
    outlier_detection(RfmtIhcDM[x])
    sns.distplot(RfmtIhcDM[x])
    plt.title('Column ' + x + ' Distribution Plot Before Cleaning')
    plt.savefig("visualizations/" + x + "_Distribution_Plot_b4_clean.png", dpi=600)
    plt.show()
    print('----------------------')

# By looking visually at these data we see almost 85% of Frequency data are = 1 so it's better to drop this column
# We also notice that the MonetaryValue also suffer from outliers which has been identified by Modified Z-Score to be
# outside of the range [24.65, 1027.34]. Resulting outlier proportion: 0.02855.

rmtihc = RfmtIhcDM[(RfmtIhcDM.MonetaryValue <= 1027.34) & (RfmtIhcDM.MonetaryValue > 24.65)].drop('Frequency', axis=1)
print('Data loss = ' + str(RfmtIhcDM.shape[0] - rmtihc.shape[0]) + " which is " +
      str(np.round((RfmtIhcDM.shape[0] - rmtihc.shape[0]) / RfmtIhcDM.shape[0] * 100, 2)) + "%")
print(rmtihc.describe().T)

# Save the clean and tidy rmtihc data set
rmtihc.to_csv("clean_rmtihc.csv")

# Data distribution after dropping Frequency column, and removing outliers and from the MonetaryValue column
for x in rmtihc.columns:
    print(x + ' Showing dist plots of data after cleaning:')
    sns.distplot(rmtihc[x])
    plt.title('Column ' + x + ' Distribution Plot After Cleaning')
    plt.savefig("visualizations/" + x + "_Distribution_Plot_after_clean.png", dpi=600)
    plt.show()
    print('----------------------')


# Clustering (using Kmeans)
# Data preprocessing (feature transformation and scaling )
sse, clusters_labels = create_kmeans_clusters(rmtihc)
plot_clusters(sse)
show_clusters_hmap(df=rmtihc, km_labels=km_labels, k=6)
show_clusters_hmap(df=rmtihc, km_labels=km_labels, k=7)