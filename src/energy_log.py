#!/usr/bin/env python
""" This script handles the power logging as class

This script will:
- generate an object for Gas, Electricity and Water as attributes
- allows to read out the last values
- stores new values in RAM
- checks if data has been changed and gives a feedback
- supports storage of the data to log file and mqtt broker

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
import pprint
import datetime

import log
import my_secrets
import mqtt_ctrl
import inspect


################################################################################
# Variables

################################################################################
# Functions

################################################################################
# Classes
class EnergyLog:
    """
    A class to represent the power logging functions

    ...

    Attributes
    ----------
    object_name : str
        a formatted string of the objects name
    last_entry : list
        the last entry in the log file
    new_time : str
        the new editing time also used to identify data changes
    data_dict : dictionary
        the complete data log which is stored to the log file


    Methods
    -------
    get_object_name()
        Returns the name of the object

    set_object_name(object_name = "DefaultObject")
        Sets the name of the object

    get_last_gas()
        Returns the last gas value

    set_new_gas(gas)
        Sets the new gas value

    get_last_power()
        Returns the last power value

    set_new_power(power)
        Sets the new gas value

    get_last_water()
        Returns the last water value

    set_new_water(water)
        Sets the new water value

    is_data_unsaved()
        Returns true if there is unsaved data

    save_new_data()
        Saves the new data set to log
    """

    ############################################################################
    # Member Variables
    obj_name = "ObjectNameDefault"
    last_entry = {}
    new_entry = {}
    new_time = None
    data_dict = {}

    ############################################################################
    # Member Functions
    def __init__(self, name = "DefaultObject"):
        self.obj_name = name
        self.data_dict = log.data_dict
        self.last_entry = self.data_dict[list(self.data_dict.keys())[-1]]
        self.new_entry["gas"] = self.get_last_gas()
        self.new_entry["power"] = self.get_last_power()
        self.new_entry["water"] = self.get_last_water()
        self.new_time = None

    def get_object_name(self):
        """Returns the object name

        Return
        ------
        str : Name of the object
        """
        return self.obj_name

    def set_object_name(self, object_name = "DefaultObject"):
        """Sets the object name

        Parameters
        ----------
        object_name : str, optional
            The new name of the object
        """
        self.obj_name = object_name

    def get_last_gas(self):
        """Returns the last gas value

        Return
        ------
        int : Last gas value
        """
        return self.last_entry["gas"]

    def set_new_gas(self, gas):
        """Sets the new gas value

        Parameters
        ----------
        gas : int
            The new gas value
        """
        self.new_entry["gas"] = gas
        self.new_time = datetime.datetime.now().strftime("%Y-%m-%d")

    def get_last_power(self):
        """Returns the last power value

        Return
        ------
        int : Last power value
        """
        return self.last_entry["power"]

    def set_new_power(self, power):
        """Sets the new gas value

        Parameters
        ----------
        power : int
            The new power value
        """
        self.new_entry["power"] = power
        self.new_time = datetime.datetime.now().strftime("%Y-%m-%d")

    def set_new_water(self, water):
        """Sets the new water value

        Parameters
        ----------
        gas : int
            The new water value
        """
        self.new_entry["water"] = water
        self.new_time = datetime.datetime.now().strftime("%Y-%m-%d")

    def get_last_water(self):
        """Returns the last water value

        Return
        ------
        int : Last water value
        """
        return self.last_entry["water"]

    def is_data_unsaved(self):
        """Returns true if there is unsaved data

        Return
        ------
        bool : True if unsaved data exists
        """
        return(self.new_time != None)

    def save_new_data(self):
        """Saves the new data set to log

        Return
        ------
        bool : True if save was successful
        """
        if self.is_data_unsaved():
            self._save_data_in_log_file()
            self._send_data_via_mqtt()
            self.new_time = None
    
    def _save_data_in_log_file(self):
        """Saves the new data set to log
        """
        #file = open("log" + '.py', 'w')
        file = open(inspect.getfile(log), "w")
        self.data_dict[self.new_time] = self.new_entry
        file.write('data_dict =' + pprint.pformat(self.data_dict))
        file.close()
    
    def _send_data_via_mqtt(self):
        """Sends the new data set to mqtt broker
        """
        val = self.new_entry["gas"] - my_secrets.gas_last_year
        mqtt_ctrl.publish_data("std/dev301/s/ener_wat/gas", val)
        val = self.new_entry["power"] - my_secrets.power_last_year
        mqtt_ctrl.publish_data("std/dev301/s/ener_wat/power", val)
        val = self.new_entry["water"] - my_secrets.water_last_year
        mqtt_ctrl.publish_data("std/dev301/s/ener_wat/water", val)
        val = self.new_time
        mqtt_ctrl.publish_data("std/dev301/s/ener_wat/date", val)
    
    def get_history(self):
        """Returns the dictionary with all history

        Return
        ------
        dict : history
        """
        return(self.data_dict)

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    pass
