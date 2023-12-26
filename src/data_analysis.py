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
from datetime import date, datetime
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


def set_new_counter_data_set(input_data:list)->str:
    """Sets a new set of data
    Args:
        input_data (list): new data set as list
    Returns:
        str: string with result message of operation
    """

    ops_error_code = _new_counter_set_data_validation(input_data)
    if ops_error_code is None:
        # load the counter data into a time indexed data frame
        data_frame = db.load_counter_data_time_indexed()
        # prepare the new data set to be integrated into the data frame
        # get the column names from the existing data frame as list
        column_names = data_frame.columns.values.tolist()
        # convert the first element in the input data into date object
        new_date_index = pd.to_datetime(input_data[0]).date()
        # slice just the data values without the date
        new_data_set = input_data[1:]
        # create a new dataframe based on the data set,
        # the column names and the new date based index
        new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_date_index])
        # concatenate the two data frames to one
        data_frame = pd.concat([data_frame, pd.DataFrame(new_row)], ignore_index=False)
        #data_frame = data_frame.normalize()
        data_frame.index = pd.to_datetime(data_frame.index)
        data_frame.index = data_frame.index.normalize()
        # store the update dataframe back to file
        db.store_counter_data_time_indexed(data_frame)
        ops_error_code = "data successfully stored"
    return ops_error_code


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


def set_history_from_list(input_data:list)->str:
    """Sets a new set of history
    Args:
        input_data (list): list of strings
    Returns:
        str: operation code
    """
    ops_error_code = None
    ops_error_code = _new_hist_set_data_validation(input_data)
    if ops_error_code is None:
        # load the all data from the csv data set file
        data_frame = db.load_historical_data_time_indexed()
        # prepare the new data set to be integrated into the data frame
        # get the column names from the existing data frame as list
        column_names = data_frame.columns.values.tolist()
        # convert the first element in the input data into date object
        new_data_index = input_data[0]
        # slice just the data values without the date_time
        new_data_set = input_data[1:]
        # create a new dataframe based on the data set, the column names and
        # the new time based index
        new_row = pd.DataFrame([new_data_set], columns=column_names, index=[new_data_index])
        # concatenate the two data frames to one
        data_frame = pd.concat([data_frame, pd.DataFrame(new_row)], ignore_index=False)
        data_frame.index = data_frame.index.astype(int)
        data_frame.sort_index()
        # store the update dataframe back to file
        db.store_historical_data_time_indexed(data_frame)
        ops_error_code = "data successfully stored"
    return ops_error_code

def get_statistics(year:int)->dict:
    """Returns the statistics for the year hand over as parameter.
    Args:
        year (int): year of the statistics
    Returns:
        dict: A dictionary with all statistics.
    """
    # get the start and end dates of the year
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    # load the data frame
    df = db.load_counter_data_time_indexed()
    # filter for year
    actuals_df = df[start_date:end_date]
    # generate the statistics
    stats_dict = {}
    if actuals_df.index.size >= 2:
        consumtion = round(actuals_df["Gas"].iloc[-1] - actuals_df["Gas"].iloc[0], 2)
        stats_dict["Gasverbrauch (kWh)"] = consumtion
        consumtion = round(actuals_df["Water"].iloc[-1] - actuals_df["Water"].iloc[0], 2)
        stats_dict["Wasserverbrauch (qm)"] = consumtion
        consumtion = round(actuals_df["Power In"].iloc[-1] - actuals_df["Power In"].iloc[0], 2)
        stats_dict["Strombezug (kWh)"] = consumtion

        # vehicle energy consumption
        consumtion = round(actuals_df["Power Car Stephan"].iloc[-1] -
                            actuals_df["Power Car Stephan"].iloc[0], 2)
        stats_dict["Strom für V60 (kWh)"] = consumtion
        consumtion = round(actuals_df["Power Car Heike"].iloc[-1] -
                           actuals_df["Power Car Heike"].iloc[0], 2)
        stats_dict["Strom für XC40 (kWh)"] = consumtion
        consumtion = stats_dict["Strom für V60 (kWh)"]
        consumtion = consumtion + stats_dict["Strom für XC40 (kWh)"] 
        consumtion = round(consumtion + (actuals_df["Power Car Wink"].iloc[-1] -
                                        actuals_df["Power Car Wink"].iloc[0]), 2)
        stats_dict["Strom für alle Autos (kWh)"] = consumtion

        # energy production statistics
        stats_dict["Tagessummen Stromproduktion (kWh)"] = round(actuals_df["Power Gen"].sum(), 2)
        stats_dict["Tagessummen Eigenverbrauch (kWh)"] = round(actuals_df["Power PV used"].sum(), 2)
        stats_dict["Tagessummen Stromverbrauch (kWh)"] = round(actuals_df["Power used"].sum(), 2)
        stats_dict["Max Stromproduktion per Tag (kWh)"] = round(actuals_df["Power Gen"].max(), 2)
        stats_dict["Max Stromproduktion Tag"] = actuals_df["Power Gen"].idxmax()

        # get a subset of the data frame where the power generation is not 0.0
        actuals_with_pwr_df = actuals_df[actuals_df["Power PV used"] > 0.0]
        stats_dict["Mittelwert Stromproduktion (kWh)"] = round(actuals_with_pwr_df["Power Gen"].mean(), 2)
        stats_dict["Mittelwert Eigenverbrauch (kWh)"] = round(actuals_with_pwr_df["Power PV used"].mean(), 2)
        stats_dict["Mittelwert Tagesverbrauch (kWh)"] = round(actuals_with_pwr_df["Power used"].mean(), 2)
        stats_dict["Aktueller Verbrauch pro Jahr (kWh)"] = round(stats_dict["Tagessummen Eigenverbrauch (kWh)"] + stats_dict["Strombezug (kWh)"], 2)
        stats_dict["Geschätzter Verbrauch pro Jahr (kWh)"] = round(actuals_with_pwr_df["Power used"].mean() * 356, 2)
        stats_dict["Geschätzter Autarkiegrad (%)"] = round(stats_dict["Mittelwert Eigenverbrauch (kWh)"] /
                                                        stats_dict["Mittelwert Tagesverbrauch (kWh)"] * 100.0, 2)
        stats_dict["Stromanteil Autos (%)"] = round(stats_dict["Strom für alle Autos (kWh)"] /
                                                    stats_dict["Strombezug (kWh)"] * 100.0, 2)

        # get the autakie value of each day and add it to the actuals data frame
        autarks_s = actuals_with_pwr_df["Power PV used"] / actuals_with_pwr_df["Power used"] * 100.0
        autarks_s = autarks_s.rename('Autark')
        # normalize it to 100%, everything about 100% is not interesting as this is feed back
        autarks_s = autarks_s.where(autarks_s <= 100, 100)
        # add the new autarkie data set to the actuals data frame
        actuals_with_pwr_df = pd.concat([actuals_with_pwr_df, autarks_s], axis=1)

        stats_dict["Realer Autarkiegrad pro Tag(%)"] = round(actuals_with_pwr_df["Autark"].mean(), 2)
    return stats_dict

def _is_valid_datetime(date_string, date_format='%Y-%m-%d'):
    """Check if a string is a valid date format
    Args:
        date_string (_type_): string to be analysed
        date_format (str, optional): expected format. Defaults to '%Y-%m-%d'.

    Returns:
        _type_: _description_
    """
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

def _new_counter_set_data_validation(input_data:list)->str:
    """Validates the input data set
    Args:
        input_data (list): input data set
    Returns:
        str: None if ok, in case of error: error string
    """
    if not _is_valid_datetime(input_data[0]):
        return "date format is not accepted"

    # check all numbers are integer or floating point numbers
    # with the "." as decimal separator
    for idx, item in enumerate(input_data[1:]):
        if "," in item:
            input_data[idx + 1] = item.replace(",", ".")
        if _is_float_string(input_data[idx + 1]) is False:
            return f"Value {input_data[idx + 1]} is not a number representation."
    return None

def _new_hist_set_data_validation(input_data:list)->str:
    """Validates the input history data set
    Args:
        input_data (list): string list of history data
    Returns:
        str: execution error or none in case of success
    """
    # check if the year is a decimal value
    if not input_data[0].isdecimal():
        return f"year format: {input_data[0]} not accepted"

    # check all numbers are integer or floating point numbers
    # with the "." as decimal separator
    for idx, item in enumerate(input_data[1:]):
        if "," in item:
            input_data[idx + 1] = item.replace(",", ".")
        if _is_float_string(input_data[idx + 1]) is False:
            return f"Value {input_data[idx + 1]} is not a number representation."

    return None

def _is_float_string(input_string)->bool:
    """checks if string represents a number
    Args:
        input_string (_type_): input string representation of a float or integer
    Returns:
        bool: true if the string is a representation of float or integer
    """
    try:
        float(input_string)
        return True
    except ValueError:
        return False
################################################################################
# Classes

################################################################################
# Scripts
