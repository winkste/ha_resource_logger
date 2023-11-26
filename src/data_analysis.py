#!/usr/bin/env python
""" This script capsulate the data analysis and data structure handling.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "winkste"
__contact__ = "via github account"
__copyright__ = "Copyright 2022, WShield"
__date__ = "2022/02/20"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "winkste"
__status__ = "Development"
__version__ = "0.0.1"

################################################################################
# Imports
#from json import loads, dumps
import pandas as pd
import database_hdl as db

################################################################################
# Variables

################################################################################
# Functions

def get_counters_as_string()->str:
    """Returns the counter dataset from file and returns it as CSV - string
    Returns:
        str: comma separated string replacement of counter dataset
    """
    data_frame = db.load_counter_data_time_indexed()
    return data_frame.to_csv().strip('\n').split('\n')


def get_counters_as_list()->list:
    """returns the counter data as list
    Returns:
        list: list of counter data
    """
    data_frame = db.load_counter_data()
    list_of_data = data_frame.values.tolist()
    return list_of_data


def get_last_counter_row_as_list()->list:
    """Returns the last data set from the actuals set.
    Returns:
        list: row entry of actuals set as list
    """
    # read data to data frame
    data_frame = db.load_counter_data()
    # return the latest data row as list (expected data is sorted)
    return data_frame.iloc[-1].tolist()


def get_counter_column_names()->list:
    """returns the column names of the counter data frame
    Returns:
        list: list of strings
    """
    data_frame = db.load_counter_data()
    column_names = data_frame.columns.values.tolist()
    return column_names


def set_new_counter_data_set(input_data:list)->None:
    """Sets a new set of data
    Args:
        input_data (list): list of strings
    """
    # load the counter data into a time indexed data frame
    data_frame = db.load_counter_data_time_indexed()
    # prepare the new data set to be integrated into the data frame
    # get the column names from the existing data frame as list
    column_names = data_frame.columns.values.tolist()
    # convert the first element in the input data into date object
    new_date_index = pd.to_datetime(input_data[0]).date()
    # slice just the data values without the date_time
    new_data_set = input_data[1:]
    # create a new dataframe based on the data set, the column names and the new time based index
    new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_date_index])
    # concatenate the two data frames to one
    data_frame = pd.concat([data_frame, pd.DataFrame(new_row)], ignore_index=False)
    # store the update dataframe back to file
    db.store_counter_data_time_indexed(data_frame)


def get_historical_data_as_df()->pd.DataFrame:
    """Returns the historical data to dataframe
    Returns:
        pd.dataFrame: Data frame 
    """
    return db.load_historical_data()


def get_historical_as_string()->str:
    """Returns the historical data and returns it as string
    Returns:
        str: comma separated string replacement of historical dataset
    """
    data_frame = db.load_historical_data_time_indexed()
    return data_frame.to_csv().strip('\n').split('\n')


def get_history_as_list()->list:
    """returns the history data as list
    Returns:
        list: list of history data
    """
    data_frame = db.load_historical_data()
    list_of_data = data_frame.values.tolist()
    return list_of_data


def get_last_history_row_as_list()->list:
    """Returns the last data set from the history set.
    Returns:
        list: row entry of history set as list
    """
    # load data into data frame with index on column year
    data_frame = db.load_historical_data_time_indexed()
    # convert latest data set to list, note: toList here returns a list of lists
    list_data = data_frame.tail(1).values.tolist()[0]
    # add the index as a first item into the list
    list_data.insert(0, data_frame.tail(1).index.item())
    return list_data


def get_history_column_names()->list:
    """returns the column names of the history data frame
    Returns:
        list: list of strings
    """
    data_frame = db.load_historical_data()
    column_names = data_frame.columns.values.tolist()
    return column_names


def set_history_from_list(input_data:list)->None:
    """Sets a new set of history
    Args:
        input_data (list): list of strings
    """
    # load the all data from the csv data set file
    data_frame = db.load_historical_data_time_indexed()
    # prepare the new data set to be integrated into the data frame
    # get the column names from the existing data frame as list
    column_names = data_frame.columns.values.tolist()
    # convert the first element in the input data into date object
    new_data_index = input_data[0]
    # slice just the data values without the date_time
    new_data_set = input_data[1:]
    # create a new dataframe based on the data set, the column names and the new time based index
    new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_data_index])
    # concatenate the two data frames to one
    data_frame = pd.concat([data_frame, pd.DataFrame(new_row)], ignore_index=False)
    data_frame.index = data_frame.index.astype(int)
    data_frame.sort_index()
    # store the update dataframe back to file
    db.store_historical_data_time_indexed(data_frame)


def get_statistics()->dict:
    """calculates the statistics of the actual data
    Returns:
        dict: dict of statistics
    """
    stats_dict = {}
    df = db.load_counter_data_time_indexed()
    stats_dict["Gasverbrauch (kWh)"] = df["Gas"][-1] - df["Gas"][0]
    stats_dict["Wasserverbrauch (qm)"] = df["Water"][-1] - df["Water"][0]
    stats_dict["Strombezug (kWh)"] = df["Power In"][-1] - df["Power In"][0]
    stats_dict["Strompeinspeisung (kWh)"] = df["Power Out"][-1] - df["Power Out"][0]
    stats_dict["Stromproduktion (kWh)"] = round(df["Power Gen"].sum(), 2)
    stats_dict["Eigenverbrauch (kWh)"] = df["Power PV used"].sum()
    stats_dict["Stromverbrauch (kWh)"] = df["Power used"].sum()
    stats_dict["Strom für V60 (kWh)"] = df["Power Car Stephan"][-1] - df["Power Car Stephan"][0]
    stats_dict["Strom für XC40 (kWh)"] = df["Power Car Heike"][-1] - df["Power Car Heike"][0]
    stats_dict["Strom für alle Autos (kWh)"] = (df["Power Car Stephan"][-1] - df["Power Car Stephan"][0]) + (df["Power Car Heike"][-1] - df["Power Car Heike"][0]) + (df["Power Car Wink"][-1] - df["Power Car Wink"][0])
    return stats_dict

################################################################################
# Classes

################################################################################
# Scripts
