# Import necessary files
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from helperFunctions.read_data import import_data
from helperFunctions.merge_view_data import merge_check_data
from helperFunctions.tidy_data import clean_data

# Read row files data
rowConvPath = "data/table_A_conversions.csv"
rowAttrPath = "data/table_B_attribution.csv"
rowConvData, rowAttrData = import_data(rowConvPath, rowAttrPath)

# Merge data
row_data_merged = merge_check_data(rowConvData, rowAttrData)

# Get clean data frame
clean_cust_attr_df = clean_data(row_data_merged)

# Save the new tidy data frame to a new CSV file
clean_cust_attr_df.to_csv("data/cleanData.csv")

# Get a snapshot of the data collection date which is exactly after the maximum date with 1 day
snapshot_date = max(clean_cust_attr_df.Conv_Date) + timedelta(days=1)

