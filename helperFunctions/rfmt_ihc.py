from datetime import timedelta


# Get a snapshot of the data collection date which is exactly after the maximum date with 1 day
def extract_snap_date(df):
    snapshot_date = max(df.Conv_Date) + timedelta(days=1)
    return snapshot_date


# RFMT IHC segmentation
# Recency - R - days since last customer transaction
# Frequency - F - number of transactions in the last 13 months
# Monetary Value - M - total spend in the last 13 months
# Tenure - T - time since the first transaction
# IHC means - Initializer, Holder and Closer average values per customer per channel

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
    data_per_uid = df.groupby(grp_by)

    # Calculate Recency, Frequency, Monetary and Tenure values for each customer
    recency = lambda x: (snapshot_date - x.max()).days
    tenure = lambda x: (snapshot_date - x.min()).days

    # Build RFMT
    rfmt_datamart = data_per_uid.agg(
        Recency=('InvoiceDay', recency),
        Frequency=('Conv_ID', 'count'),
        MonetaryValue=('Revenue', sum),
        Tenure=('InvoiceDay', tenure))
    print(rfmt_datamart.head())

    return rfmt_datamart


# Build ihc_datamart
def build_ihc(df, channels, grp_by='User_ID'):
    """
    Build IHC Initializer Holder Closer dataFrame for each customer to be used for customer segmentation
    :param df: original clean data frame
    :param channels: unique channel ids
    :param grp_by: group data frame by - userid or customer ids or sessions etc...
    :return: IHC data
    """
    # Group Data
    data_per_uid = df.groupby(grp_by)

    # Build IHC averages per customer per channel and fill missing values with 0 value to the mean ihc
    ihc_dm = data_per_uid.agg({i: 'mean' for i in channels}).fillna(0)
    ihc_dm.columns = ["_".join(x) for x in ihc_dm.columns]
    print(ihc_dm.head())

    return ihc_dm


# Build rfmt_ihc_dm
def build_rfmt_ihc(rfmt_dm, ihc_dm):
    """
    Build RFMT, IHC, and RFMT_IHC Recency Frequency Monetary Tenure Initializer Holder Closer dataFrame for each customer
    to be used for customer segmentation this is a combination of RFMT and IHC data frames
    :rfmt_dm: Left data frame (RFMT data frame)
    :ihc_dm: Right data frame (IHC data frame)
    :return: a data frames RFMT_IHC as a combination of the first 2 data frames merged together
    """

    # Build Full RFMT_IHC
    rfmt_ihc_dm = rfmt_dm.merge(ihc_dm, left_on=rfmt_dm.index, right_on=ihc_dm.index)
    print(rfmt_ihc_dm.head())
    print(rfmt_ihc_dm.describe().T)

    return rfmt_ihc_dm
