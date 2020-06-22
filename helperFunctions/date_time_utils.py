from datetime import datetime
import matplotlib.pyplot as plt


# plot revenue over time
def plot_rev_over_time(df, df_gp_by, df_col, df_agg_func, title, xlab, ylab, save_f_name):
    """
    Plot variable over time
    :param df: the data frame which contains the vaiable to be plotted
    :param df_gp_by: group the data frame by
    :param df_col: data frame column to be plotted over time
    :param df_agg_func: function to aggeregate by
    :param title: plot title
    :param xlab: plot x label
    :param ylab: plot y label
    :param save_f_name: Plot file name to be saved on the disk
    :return: plot variable over time and save it to disk in the visualizations folder
    """
    groupedByDate = df.groupby(df_gp_by)
    groupedByDate[df_col].agg(df_agg_func).plot()
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.tight_layout()
    plt.savefig("visualizations/" + save_f_name + ".png", dpi=600)
    plt.draw()
    # plt.show()


# Parse the date to "YYYY-mm-01" to get the month of the transaction only
def get_month(x):
    """
    Parse the date to "YYYY-mm-01" to get the month of the transaction only
    :param x: datetime pandas series column
    :return: Date inf the format "YYYY-mm-01"
    """
    return datetime(x.year, x.month, 1)


# Get year and month from date
def get_date_int(df, column):
    """
    Get year and month from date from a column of a data frame
    :param df: data frame contains the required datetime column
    :param column: datetime column required to extract info from
    :return:
    """
    year = df[column].dt.year
    month = df[column].dt.month

    return year, month
