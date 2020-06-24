# from datetime import timedelta, datetime
# import pandas as pd
# from main import cleanUserAttr_df
#
#
# # RFMT IHC segmentation
# # Recency - R - days since last customer transaction
# # Frequency - F - number of transactions in the last 13 months
# # Monetary Value - M - total spend in the last 13 months
# # Tenure - T - time since the first transaction
# # IHC columns - Initializer, Holder and Closer total value sums and counts,per customer per channel
# # IHC counts - how many time customer visited the channel for each customer and channel
# # IHC sum - total values assigned to each channel for each customer
#
# # Get a snapshot of the data collection date which is exactly after the maximum date with 1 day
# def get_snap_date(df):
#     snapshot_date = max(df.Conv_Date) + timedelta(days=1)
#     return snapshot_date
#
#
# # Build rfmt_datamart
# def build_rfmt(df, snapshot_date, grp_by='User_ID'):
#     """
#     Build RFMT Recency Frequency Monetary Tenure for each customer
#     :param df: original clean data frame
#     :param snapshot_date: date of observation - usually after data set with one day
#     :param grp_by: group data frame by - userid or customer ids or sessions etc...
#     :return: RFMT data frame
#     """
#     # Group Data
#     dataPerUID = df.groupby(grp_by)
#
#     # Calculate Recency, Frequency, Monetary and Tenure values for each customer
#     recency = lambda x: (snapshot_date - x.max()).days
#     tenure = lambda x: (snapshot_date - x.min()).days
#
#     # Build RFMT
#     rfmt_datamart = dataPerUID.agg(
#         Recency=('InvoiceDay', recency),
#         Frequency=('Conv_ID', 'count'),
#         MonetaryValue=('Revenue', sum),
#         Tenure=('InvoiceDay', tenure))
#     print(rfmt_datamart.head())
#
#     return rfmt_datamart
#
# #
# # # Build ihc_datamart
# # def build_ihc(df, chnels, grp_by='User_ID'):
# #     """
# #     Build IHC Initializer Holder Closer dataFrame for each customer to be used for customer segmentation
# #     :param df: original clean data frame
# #     :param chnels: unique channel ids
# #     :param grp_by: group data frame by - userid or customer ids or sessions etc...
# #     :return: IHC data
# #     """
# #     # Group Data
# #     dataPerUID = df.groupby(grp_by)
# #
# #     # Build IHC counts and sums per customer per channel
# #     ihc_rfmt_datamart = dataPerUID.agg({i: ['sum', 'count'] for i in chnels})
# #     ihc_rfmt_datamart.columns = ["_".join(x) for x in ihc_rfmt_datamart.columns]
# #     print(ihc_rfmt_datamart.head())
# #
# #     return ihc_rfmt_datamart
# #
# #
# # # Build rfmtihc_datamart
# # def build_rfmt_ihc(rfmt_dm, ihc_dm):
# #     """
# #     Build RFMT, IHC, and RFMT_IHC Recency Frequency Monetary Tenure Initializer Holder Closer dataFrame for each customer
# #     to be used for customer segmentation this is a combination of RFMT and IHC data frames
# #     :rfmt_dm: RFMT data frame
# #     :ihc_dm: IHC data frame
# #     :return: a data frames RFMT_IHC as a combination of the first 2 data frames merged together
# #     """
# #
# #     # Build Full RFMT_IHC
# #     rfmtihc_datamart = rfmt_dm.merge(ihc_dm, left_on=rfmt_dm.index, right_on=ihc_dm.index)
# #     print(rfmtihc_datamart.head())
# #     print(rfmtihc_datamart.describe())
# #
# #     return rfmtihc_datamart
# #
# # # # Calculate 3 groups for Recency and Frequency and MonetaryValue & Calculate RFM Score
# # # # Create labels for Recency and Frequency
# # # asc_labels=range(3, 0, -1); dec_labels = range(1, 4)
# # #
# # # # Assign these labels to three equal percentile groups
# # # r_groups = pd.qcut(datamart['Recency'], q=3, labels=asc_labels)
# # #
# # # # Assign these labels to three equal percentile groups
# # # f_groups = pd.qcut(datamart['Frequency'], q=3, labels=dec_labels)
# # #
# # # # Create new columns R and F
# # # datamart = datamart.assign(R=r_groups.values, F=f_groups.values)
# # # grp_by='User_ID')
