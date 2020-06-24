from datetime import timedelta, datetime
import pandas as pd
from main import tidyUserAttr_df


# RFMT IHC segmentation
# Recency - R - days since last customer transaction
# Frequency - F - number of transactions in the last 13 months
# Monetary Value - M - total spend in the last 13 months
# Tenure - T - time since the first transaction
# IHC columns - Initializer, Holder and Closer total value sums and counts,per customer per channel
# IHC counts - how many time customer visited the channel for each customer and channel
# IHC sum - total values assigned to each channel for each customer

# Get a snapshot of the data collection date which is exactly after the maximum date with 1 day
def get_snap_date(df):
    snapshot_date = max(df.Conv_Date) + timedelta(days=1)
    return snapshot_date


# Build rfmt_datamart
def build_rfmt(df, snapshot_date, grp_by='User_ID'):
    """
    Build RFMT Recency Frequency Monetary Tenure for each customer
    :param df: original clean data frame
    :param snapshot_date: date of observation - usually after data set with one day
    :param grp_by: group data frame by - userid or customer ids or sessions etc...
    :return: RFMT data frame
    """
    # Group Data
    dataPerUID = df.groupby(grp_by)

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

    return rfmt_datamart