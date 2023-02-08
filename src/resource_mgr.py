#!/usr/bin/env python
""" This module handles the resource management

This script will:
- handle the monitored resources
- allows to read out the last values
- stores new values in RAM
- checks if data has been changed and gives a feedback
- supports storing the data

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
__date__ = "2023/02/05"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "winkste"
__status__ = "Development"
__version__ = "0.0.1"


################################################################################
# Imports
import copy
import datetime
import pandas as pd
import data_handler
import resource_param

################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
class ResMgr:
    """
    A class to represent the resources consumed at home:
        - Gas
        - Power
        - Water
    """
    ############################################################################
    # Member Variables

    ############################################################################
    # Member Functions
    def __init__(self, name:str = "ResourceManager")->None:
        """Constructor for the Resource Manager class

        Args:
            name:str - name of the object
        Returns:
            None
        """
        self.obj_name:str = name
        self.data_frame :pd.DataFrame = None
        self.last_entry:pd.Series = None
        self.new_entry:pd.Series = None
        self.data_changed:bool = False
        self._initialize_object_data()

    def _initialize_object_data(self)->None:
        """This function initializes the object data

        Returns:
            None
        """
        self.data_frame = data_handler.load_data()
        # sort the data frame according to the dates
        self.data_frame.sort_values(by="date", inplace = True)
        # clean data frame from any duplicated dates
        self.data_frame = self.data_frame.drop_duplicates("date", keep="last")
        # get the last entry from data frame
        self.last_entry = self.data_frame.iloc[-1]
        # initialize the new data entry with the last data entry and actual date
        self.new_entry = copy.deepcopy(self.last_entry)
        self.new_entry["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        self.new_entry["date"] = pd.to_datetime(self.new_entry['date'])
        self.data_changed = False

    def get_object_name(self)->None:
        """Returns the object name

        Returns:
            str:name of the object
        """
        return self.obj_name

    def set_object_name(self, name:str = "ResourceManager")->None:
        """Sets the object name

        Args:
            name:str, optional name of the object
        Returns:
            None
        """
        self.obj_name = name

    def get_last_gas(self)->int:
        """Returns the last gas value

        Returns:
            int:last gas value
        """
        return self.last_entry["gas"]

    def set_new_gas(self, gas:int):
        """Sets the new gas value

        Args:
            gas:int, the new gas value
        """
        self.new_entry["gas"] = gas
        self.data_changed = True

    def get_last_power(self)->int:
        """Returns the last power value

        Return
            int : Last power value
        """
        return self.last_entry["power"]

    def set_new_power(self, power:int):
        """Sets the new gas value

        Args:
            power:int, the new power value
        """
        self.new_entry["power"] = power
        self.data_changed = True

    def get_last_water(self)->int:
        """Returns the last water value

        Returns:
            int:last water value
        """
        return self.last_entry["water"]

    def set_new_water(self, water:int):
        """Sets the new water value

        Args:
            gas:int, the new water value
        """
        self.new_entry["water"] = water
        self.data_changed = True

    def is_data_unsaved(self)->bool:
        """Returns true if there is unsaved data

        Returns:
            bool:True if unsaved data exists
        """
        return self.data_changed

    def save_new_data(self)->None:
        """Saves the new data set to log

        Returns:
            bool : True if save was successful
        """
        if self.is_data_unsaved():
            self.data_frame = pd.concat([self.data_frame, self.new_entry.to_frame().T],
                                            ignore_index=True)
            data_handler.store_data(self.data_frame)
            self._initialize_object_data()

    def get_last_date(self)->datetime:
        """Returns the date of the last saved record.
        
        Returns:
            datetime: date of last record stored
        """
        return self.last_entry["date"]

    def get_new_date(self)->datetime:
        """Returns the date of the new data record.
        
        Returns:
            datetime: date of new record 
        """
        return self.last_entry["date"]

    def print_all_values(self)->None:
        """This function prints all values in the dict.
        """
        print(self.data_frame)

    def get_gas_year_consum(self)->int:
        """This function returns the overall year gas consumtion
        
        Return:
            int:gas year consumption
        """
        return self.get_last_gas() - resource_param.GAS_LAST_YEAR

    def get_power_year_consum(self)->int:
        """This function returns the overall year power consumtion
        
        Return:
            int:power year consumption
        """
        return self.get_last_power() - resource_param.POWER_LAST_YEAR

    def get_water_year_consum(self)->int:
        """This function returns the overall year water consumtion
        
        Return:
            int:water year consumption
        """
        return self.get_last_water() - resource_param.WATER_LAST_YEAR

    def get_gas_serial(self)->str:
        """This function returns the gas serial number
        
        Return:
            str:serial number
        """
        return resource_param.GAS_NR

    def get_power_serial(self)->str:
        """This function returns the power serial number
        
        Return:
            str:serial number
        """
        return resource_param.POWER_NR

    def get_water_serial(self)->str:
        """This function returns the water serial number
        
        Return:
            str:serial number
        """
        return resource_param.WATER_NR

    def get_history(self)->str:
        """This function returns all data as csv string

        Returns:
            str: CSV representation of the data
        """
        return "nr" + self.data_frame.to_csv().replace("\n", ",")

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script

    res = ResMgr("MyResourceManager")
    print(res.get_object_name())
    res.print_all_values()
    print("Last data set:")
    print(f"date: {res.get_last_date()}")
    print(f"gas: {res.get_last_gas()}")
    print(f"power: {res.get_last_power()}")
    print(f"water: {res.get_last_water()}")
    print("-----------------------")
    print(f"Is data set new modified? {res.is_data_unsaved()}")
    res.set_new_gas("4200")
    res.set_new_power("55000")
    res.set_new_water("52")
    print(f"Is data set new modified? {res.is_data_unsaved()}")
    res.save_new_data()
    print("-----------------------")
    print(f"Is data set new modified? {res.is_data_unsaved()}")
    print("Last data set:")
    print(f"date: {res.get_last_date()}")
    print(f"gas: {res.get_last_gas()}")
    print(f"power: {res.get_last_power()}")
    print(f"water: {res.get_last_water()}")
    print("-----------------------")
