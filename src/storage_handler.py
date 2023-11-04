#!/usr/bin/env python
""" This script capsulate the data load and store

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
import pandas as pd
import parameter
from json import loads, dumps

################################################################################
# Variables
actuals_file_name:str = parameter.DATA_FOLDER_PATH + "2023.csv"
hist_file_name:str = parameter.DATA_FOLDER_PATH + "history.csv"

################################################################################
# Functions

def load_actuals_data()->pd.DataFrame:
    """Load the actuals data to dataframe

    Returns:
        pd.dataFrame: Data frame 
    """
    return pd.read_csv(actuals_file_name)

def store_actuals_data(data_frame:pd.DataFrame)->None:
    """Capsulates the actuals data storage

    Args:
        data_frame (pd.DataFrame): dataframe to be stored
    """
    data_frame.to_csv(actuals_file_name, index=False)

def store_actuals_from_list(input_data:list)->None:
    """Stores a new set of data

    Args:
        input_data (list): list of strings
    """
    # load the all data from the csv data set file
    data_frame = pd.read_csv(actuals_file_name, index_col='date', parse_dates=['date'])

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
    data_frame.to_csv(actuals_file_name, index="date", index_label="date")
    remove_duplicates_from_data_file(actuals_file_name, 'date')

def store_history_from_list(input_data:list)->None:
    """Stores a new set of history

    Args:
        input_data (list): list of strings
    """
    # load the all data from the csv data set file
    data_frame = pd.read_csv(hist_file_name, index_col='year')
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
    data_frame.sort_index()
    # store the update dataframe back to file
    data_frame.to_csv(hist_file_name, index="year", index_label="year")
    # clean the data set from duplicates
    remove_duplicates_from_data_file(hist_file_name, 'year')

def remove_duplicates_from_data_file(file_name:str, column:str)->None:
    """This function removes all duplicates and leaves the latest.
    Args:
        file_name (str): file name to be modified
        column (str): column to search for duplicates
    """
    data_frame = pd.read_csv(file_name)
    clean_data = data_frame.drop_duplicates(subset=column, keep='last')
    clean_data = clean_data.set_index(column)
    clean_data.to_csv(file_name)

def load_historical_data()->pd.DataFrame:
    """Load the historical data to dataframe

    Returns:
        pd.dataFrame: Data frame 
    """
    return pd.read_csv(hist_file_name)

def load_historical_to_string()->str:
    """Load the historical data to a string

    Returns:
        str: historical data
    """
    data_frame = pd.read_csv(hist_file_name, index_col="year")
    return data_frame.to_csv().strip('\n').split('\n')

def load_actuals_to_string()->str:
    """Loads the actuals dataset from file and returns it as CSV - string

    Returns:
        str: comma separated string replacement of actuals dataset
    """
    data_frame = pd.read_csv(actuals_file_name, index_col='date', parse_dates=['date'])
    return data_frame.to_csv().strip('\n').split('\n')

################################################################################
# Classes

################################################################################
# Scripts
