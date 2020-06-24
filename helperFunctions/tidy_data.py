import pandas as pd


def clean_data(df):
    """
    Clean data frames
    :param df: the pandas data frame with missy data
    :return: Clean data frame, and channel name which will be kept
    """

    # Check whether any users conversed in the same day or more than one day
    print("Check how many users conversed in more than one day (if 0 means that all users conversed in the same day)")
    print((df.groupby("Conv_ID")["Conv_Date"].agg("nunique") > 1).sum())

    ihc_per_conv = df.pivot(index="Conv_ID", columns="Channel", values="IHC_Conv")
    ihc_per_conv.sort_index(inplace=True)
    print("First 5 values of IHC values per unique conversion ID")
    print(ihc_per_conv.head())

    print("Range of Sum of all IHC for each Conversion ID is below: so we can conclude that it equals 1 for each "
          "conversion")
    print(ihc_per_conv.sum(axis=1).quantile([0, 1]).round(2).set_axis(['min', 'max'], axis=0))

    # Check number of complete cases channels columns (columns without missing values)
    print("Number of complete cases channels columns (columns without missing values):")
    print(ihc_per_conv.count(axis=0).sort_values(ascending=False))

    # Keeping only the first 5 channels and removing all remaining channels
    ch_to_keep = ihc_per_conv.count(axis=0).sort_values(ascending=False).iloc[0:5].index.to_list()
    ch_to_drop = [x for x in ihc_per_conv.columns.to_list() if x not in ch_to_keep]
    ihc_per_conv.drop(ch_to_drop, axis=1, inplace=True)
    ihc_per_conv.info()

    clean_merged = df.drop(["Channel", "IHC_Conv"], axis=1)
    clean_merged.drop_duplicates(inplace=True)
    clean_merged.set_index("Conv_ID", inplace=True)
    clean_merged.sort_index(inplace=True)
    print("First 5 values of the clean data without Channel, and IHC")
    print(clean_merged.head())

    tidy_data = pd.concat([clean_merged, ihc_per_conv], axis=1).reset_index()
    print("First 5 values of the final clean data")
    print(tidy_data.head())

    return tidy_data, ch_to_keep
