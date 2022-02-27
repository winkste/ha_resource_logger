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

import my_secrets
import cls_screen
from energy_log import EnergyLog



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

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    launch_menu()
    