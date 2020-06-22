import pandas as pd


def import_data(file1: str, file2: str) -> object:
    """
    Read 2 csv files and return them in 2 pandas data frames
    :param file1: path of the first file
    :param file2: path of the second file
    :return: 2 pandas data frames
    """

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    return df1, df2
