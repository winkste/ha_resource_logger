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

################################################################################
# Variables
actuals_file_name:str = parameter.DATA_FOLDER_PATH + "actuals.csv"
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

def load_historical_data()->pd.DataFrame:
    """Load the historical data to dataframe

    Returns:
        pd.dataFrame: Data frame 
    """
    return pd.read_csv(hist_file_name)

################################################################################
# Classes

################################################################################
# Scripts
