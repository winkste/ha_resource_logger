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
#from json import loads, dumps
import pandas as pd
import parameter

################################################################################
# Variables
actuals_file_name:str = parameter.DATA_FOLDER_PATH + "counters.csv"
hist_file_name:str = parameter.DATA_FOLDER_PATH + "consumes.csv"

################################################################################
# Functions

def load_counter_data()->pd.DataFrame:
    """Load the actuals data to dataframe
    Returns:
        pd.dataFrame: Data frame 
    """
    return pd.read_csv(actuals_file_name)


def store_counter_data(data_frame:pd.DataFrame)->None:
    """Capsulates the counter data storage
    Args:
        data_frame (pd.DataFrame): dataframe to be stored
    """
    # store the dataframe to file
    data_frame.to_csv(actuals_file_name, index=False)
    # clean the data set from duplicates
    remove_duplicates_from_data_file(actuals_file_name, 'Date')


def load_counter_data_time_indexed()->pd.DataFrame:
    """Load the actuals counters as time indexed data frame

    Returns:
        pd.DataFrame: Time Indexed Data Frame
    """
    return pd.read_csv(actuals_file_name, index_col='Date', parse_dates=['Date'])


def store_counter_data_time_indexed(data_frame:pd.DataFrame)->None:
    """Capsulates the counter data storage with time indexed data frame
    Args:
        data_frame (pd.DataFrame): time indexed dataframe to be stored
    """
    # store the dataframe to file
    data_frame.to_csv(actuals_file_name, index="Date", index_label="Date")
    # clean the data set from duplicates
    remove_duplicates_from_data_file(actuals_file_name, 'Date')


def load_historical_data()->pd.DataFrame:
    """Load the historical data to dataframe
    Returns:
        pd.dataFrame: Data frame 
    """
    return pd.read_csv(hist_file_name)


def load_historical_data_time_indexed()->pd.DataFrame:
    """Load the historical data to dataframe with time index
    Returns:
        pd.dataFrame: time indexed data frame
    """
    return pd.read_csv(hist_file_name, index_col='Year')


def store_historical_data_time_indexed(data_frame:pd.DataFrame)->None:
    """Capsulates the historical data storage with time indexed data frame
    Args:
        data_frame (pd.DataFrame): time indexed dataframe to be stored
    """
    # store the dataframe to file
    data_frame.to_csv(hist_file_name, index="Year", index_label="Year")
    # clean the data set from duplicates
    remove_duplicates_from_data_file(hist_file_name, 'Year')


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


################################################################################
# Classes

################################################################################
# Scripts
