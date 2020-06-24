import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

from helperFunctions.segmantation import *


def get_train_test_data(df, channels_to_keep):
    """
    Get freatures and target variables data from a data frame. It returns the number of transactions in the last month 
    as "y" variable which is the target variable and get the RMT and IHC for the top 5 channels as features "X"
    :param df: Data frame to converted to train and test set
    :param channels_to_keep: list of string with the IHC channels to keep
    :return: Training features dataset as X, and target variables data as y
    """
    global y, X
    # Exclude the last month from the data
    df_X = df[df.InvoiceMonth != df.InvoiceMonth.max()]
    # Define snapshot date
    NOW = df.InvoiceMonth.max()
    features1 = build_rfmt(df_X, NOW, "User_ID")
    features2 = build_ihc(df_X, channels_to_keep)
    features = build_rfmt_ihc(features1, features2)
    features = features[(features.MonetaryValue <= 1027.34) & (features.MonetaryValue > 24.65)].drop("Frequency",
                                                                                                     axis=1)
    # Build a pivot table counting invoices for each customer monthly
    cust_month_tx = pd.pivot_table(data=df, values="Conv_ID",
                                   index=["User_ID"], columns=["InvoiceMonth"],
                                   aggfunc=pd.Series.nunique, fill_value=0)
    target = df.InvoiceMonth.max()
    y = cust_month_tx[target]
    y_valid_ind = [row for row in y.index.to_list() if row in features["key_0"].to_list()]
    # get only the inliers targets
    y = y[y_valid_ind]
    # Split data to training and testing
    # Store customer identifier column name as a list
    custid = ["key_0"]
    # Select feature column names excluding customer identifier
    cols = [col for col in features.columns if col not in custid]
    X = features[cols]

    return X, y


def train_model_to_predict_sales(df, channels_to_keep):
    """
    Train a very simple linear regression model to predict sales for the last month given all previous months data.
    :param df: the row data frame to get training, and testing features from it, and get the training and testing target
    variable from it
    :param channels_to_keep: The IHC channels to keep and use for the model.
    :return: return the linear regression model and print some artifacts such as mse, mae for both train and test sets,
    and print model coefficients
    """
    # Get feature variables and target data
    get_train_test_data(df, channels_to_keep)
    # Split data to training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)

    linreg = LinearRegression()
    # Train a very simple linear regression model
    linreg.fit(X_train, y_train)
    # Predict the target variable for training data
    pred_y_train = linreg.predict(X_train)
    # Predict the target variable for testing data
    pred_y_test = linreg.predict(X_test)
    # Calculate root mean squared error on training data
    rmse_train = np.sqrt(mean_squared_error(y_train, pred_y_train))
    # Calculate mean absolute error on training data
    mae_train = mean_absolute_error(y_train, pred_y_train)
    # Calculate root mean squared error on testing data
    rmse_test = np.sqrt(mean_squared_error(y_test, pred_y_test))
    # Calculate mean absolute error on testing data
    mae_test = mean_absolute_error(y_test, pred_y_test)
    # Print the performance metrics
    print(
        "RMSE train: {}; RMSE test: {}\nMAE train: {}, MAE test: {}".format(rmse_train, rmse_test, mae_train, mae_test))
    print("\nAlthough it's an extremely simple and easy model , it achieved a very good results\n")
    coef_names = {key: linreg.coef_[i] for i, key in enumerate(X.columns.to_list())}
    print("\nGet model coefficients:\n")
    print(pd.Series(coef_names))

    return linreg