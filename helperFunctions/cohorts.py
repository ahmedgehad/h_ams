# Import necessary files
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from helperFunctions.date_time_utils import *


# Add cohort columns to the data frame
def add_cohort_columns(df, df_grp_by):
    """
    Add InvoiceMonth, CohortMonth, and CohortIndex columns to a data frame
    Add also InvoiceDay, CohortDoy, and CohortDayIndex columns to a data frame
    :param df: e passed data frame to add columns to
    :param df_grp_by: the required column names of the data frame to be grouped by
    :return: e new data frame with new columns added
    """
    # Create InvoiceMonth column
    df['InvoiceMonth'] = df.Conv_Date.apply(get_month)
    # Create CohortMonth column
    df['CohortMonth'] = df.groupby(df_grp_by)['InvoiceMonth'].transform('min')
    # Create InvoiceDay Column
    df['InvoiceDay'] = df.Conv_Date.apply(get_day)
    # Create CohortDay column
    df['CohortDay'] = df.groupby(df_grp_by)['InvoiceDay'].transform('min')
    # Get the integers for date parts from the `InvoiceDay` column
    invoice_year, invoice_month = get_date_int(df, 'InvoiceMonth')
    # Get the integers for date parts from the `CohortDay` column
    cohort_year, cohort_month = get_date_int(df, 'CohortMonth')
    # Calculate difference in years
    years_diff = invoice_year - cohort_year
    # Calculate difference in months
    months_diff = invoice_month - cohort_month
    # Extract the difference in months from all previous values
    df['CohortIndex'] = years_diff * 12 + months_diff + 1
    # Get Cohort Day Index
    df['CohortDayIndex'] = (df.InvoiceDay - df.CohortDay).dt.days + 1

    return df


# Build some Cohorts
def build_time_cohort(df, df_grp_by, cohort_slic, func='count'):
    """
    Build a time cohort from a data frame.
    :param df: the data frame to be converted to timely cohort
    :param df_grp_by: list contains the required column names of the data frame to be grouped by 
    :param cohort_slic: the column name or list of columns to be used for the cohort
    :param func: the function which will be applied on the group
    :return: a pivot table contains a time cohort
    """
    # Monthly cohort
    grouping = df.groupby(df_grp_by)
    cohort_data = grouping[cohort_slic].apply(func).reset_index()
    # Create a pivot
    cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values=cohort_slic)

    return cohort_counts


# Visualize cohort
def vis_cohort(df, plt_title, save_f_name, frmt=".2g"):
    """
    Plot the cohort from a cohort pivot table
    :param df: the cohort pivot table
    :param plt_title: Plot title
    :param save_f_name: Plot file name to be saved on the disk
    :param frmt: format of the heat map values - default is .2g
    :return: save cohort plot into the disk in the visualizations folder and view it
    """
    if type(df.index) != pd.core.indexes.period.PeriodIndex:
        df.index = df.index.to_period('M')
    plt.figure(figsize=(16, 14))
    plt.title(plt_title)
    sns.heatmap(data=df, annot=True, fmt=frmt, cmap='Blues')
    plt.yticks(rotation=0)
    plt.savefig("visualizations/" + save_f_name + ".png", dpi=600)
    plt.draw()
    # plt.show()
