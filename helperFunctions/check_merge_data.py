import pandas as pd


def merge_check_data(df1, df2):
    """
    Merge 2 data frames with inner joins based on their conversion id field, and print useful insights about data \
    before cleaning, and remove missing data
    :param df1: the first pandas data frame row data
    :param df2: the second pandas data frame row data
    :return: merged data frame with missing data removed and print useful information about the data
    """

    # Merge two tables based on Conversion ID with inner join to get common data only
    row_merged = df1.merge(df2, on="Conv_ID", how="inner")

    # Explore new table
    print("Info\n")
    print(row_merged.info())
    print("\n------------------------------------\nHead\n")
    print(row_merged.head())
    print("\n------------------------------------\nNumber of unique categories in each field\n")
    print("We Can notice that data is not tidy (rows doesn't represent observations and not all columns are variables")
    print("e.g. All data are duplicated data except IHC, and chennel which are spreaded across multiple rows")
    print(row_merged.nunique())
    print("\n------------------------------------\nNumber of missing values and its portion of the data\n")
    print(pd.DataFrame({"count": row_merged.isnull().sum(), "Pct% of the data": row_merged.isnull().mean() * 100}))

    # Remove missing data since only 6638 rows have missing data (about 3%)
    row_merged.dropna(axis=0, how="any", inplace=True)
    row_merged.info()

    # Fix Conv_Date and Channel columns data types
    print("data types before fixing :\n")
    print(row_merged.dtypes)
    row_merged.Conv_Date = pd.to_datetime(row_merged.Conv_Date)
    row_merged.Channel = row_merged.Channel.astype("category")
    print("\n\ndata types after fixing :\n")
    print(row_merged.dtypes)

    # Data range and taking snapshot_date
    print("\nMin snapshot date:{}; Max snapshot date:{}".format(min(row_merged.Conv_Date), max(row_merged.Conv_Date)))
    print("Data duration is about 13 months")

    return row_merged
