#!/usr/bin/env python
""" This script supports user input of power data to log it

This script will:
- support a command line menu to enter gas, power and water counts
- it will store the data into a local dictionary with date as key and
    gas / power / water as sub keys
- it will use the last entry as default if only one or two out of three
    values are updated
- the data can also be pushed to home assistant via mqtt

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
from paho.mqtt import publish
import pprint
import datetime

import my_secrets
import log
import cls_screen



################################################################################
# Variables

################################################################################
# Functions
def launch_menu():
    """ Menu handling and program control
    """
    power = EnergyLog()

    choice = "g"
    while choice in ["g", "p", "w", "s", "q"]:
        cls_screen.clear_screen()
        print("--- Power Log ---")
        print(f" (g) - Gas (Counternr: {my_secrets.gas_nr}, last value: {power.get_last_gas()} qm")
        print(f" (p) - Power (Counternr: {my_secrets.power_nr}, last value: {power.get_last_power()} kWh")
        print(f" (w) - Water (Counternr: {my_secrets.water_nr}, last value: {power.get_last_water()} qm")
        print(f" (s) - save and send to HomeAssistant")
        print(f" (q) - quit")
        choice = input("Select option: ")

        if choice == "g":
            new_value = int(input("Enter value (qm): "))
            power.set_new_gas(new_value)
        if choice == "p":
            new_value = int(input("Enter value (kWh): "))
            power.set_new_power(new_value)
        if choice == "w":
            new_value = int(input("Enter value (qm): "))
            power.set_new_water(new_value)
        if choice == "s":
            power.save_new_data()
            pass
        if choice == "q":
            if power.is_data_unsaved():
                if "y" == input("Unsaved data, do you really want to quit (y/n)? "):
                    return
            else:
                return

def publish_data(topic, payload):
    '''
    this function publishes data to the mqtt broker
    '''
    publish.single(topic, payload, hostname=my_secrets.hostname,
                    port=my_secrets.port, client_id=my_secrets.client_id,
                    auth=my_secrets.auth)

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


    Methods
    -------
    get_object_name()
        Returns the name of the object
    
    set_object_name(object_name = "DefaultObject")
        Sets the name of the object
    
    get_last_gas()
        Returns the last gas value
    
    get_last_power()
        Returns the last power value

    get_last_water()
        Returns the last water value
    """

    ############################################################################
    # Member Variables
    obj_name = "ObjectNameDefault"
    last_entry = []
    new_gas = 0
    new_power = 0
    new_water = 0
    new_time = None
    last_time = None
    data_dict = {}

    ############################################################################
    # Member Functions
    def __init__(self, name = "DefaultObject"):
        self.obj_name = name
        self.data_dict = log.data_dict
        self.last_entry = self.data_dict[list(self.data_dict.keys())[-1]]

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
        self.last_entry["gas"] = gas
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
        self.last_entry["power"] = power
        self.new_time = datetime.datetime.now().strftime("%Y-%m-%d")

    def set_new_water(self, water):
        """Sets the new water value

        Parameters
        ----------
        gas : int
            The new water value
        """
        self.last_entry["water"] = water
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
            file = open("src/log" + '.py', 'w')
            self.data_dict[self.new_time] = self.last_entry
            file.write('data_dict =' + pprint.pformat(self.data_dict))
            file.close()

            val = self.last_entry["gas"] - my_secrets.gas_last_year
            publish_data("std/dev301/s/ener_wat/gas", val)
            val = self.last_entry["power"] - my_secrets.power_last_year
            publish_data("std/dev301/s/ener_wat/power", val)
            val = self.last_entry["water"] - my_secrets.water_last_year
            publish_data("std/dev301/s/ener_wat/water", val)
            val = self.new_time
            publish_data("std/dev301/s/ener_wat/date", val)
            self.new_time = None

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    launch_menu()

# '2022-02-20': {'gas': 3825, 'power': 51661, 'water': 818}}