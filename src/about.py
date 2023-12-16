#!/usr/bin/env python
""" This script handles the version and identification of the program

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
__status__ = "BETA"
__software_name__ = "ha_resource_log"
__description__ = """This Software stores and analysis home consumables like
gas consumption, water consumption and power consumption. Additional it handles
power generation."""

__version__ = "0.0.4"
__version_log__ = """
v0.0.1      01.01.2023      SWI     initial version
v0.0.2      27.11.2023      SWI     reworked version to new look and feel using table style
v0.0.3      02.12.2023      SWI     reworked html pages to simplify code
                                    introduced input validation
v0.0.4      15.12.2023      SWI     updated the statistics calculation
"""
################################################################################
# Imports

################################################################################
# Variables

################################################################################
# Functions

def get_software_full_identification()->str:
    """Returns software name and version combined to one string.
    Returns:
        str: version identification string
    """
    return __software_name__ + __version__

def get_software_status()->str:
    """Returns software type
    Returns:
        str: software type
    """
    return __status__

def get_software_version()->str:
    """This function returns the version of the software
    Returns:
        str: version of software
    """
    return __version__

def get_software_description()->str:
    """This function returns the software description.
    Returns:
        str: software descpription as string.
    """
    return __description__

def get_software_version_log()->str:
    """Returns a dictionary with keys for the version

    Returns:
        dict: a dictionary with the version log
    """
    return __version_log__

def get_complete_story_of_program()->str:
    """This function returns in a string the full information of the program

    Returns:
        str: string with all information about the program
    """
    story:str = ""

    story = story + f"Program: {__software_name__} \n"
    story = story + f"Status of Program: {__status__}\n"
    story = story + f"License: {__license__}\n"
    story = story + f"Actual version: {__version__}\n\n"
    story = story + f"Description: {__description__}\n\n"
    story = story + "Version Log:"
    story = story + f"{__version_log__}\n"
    return story

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    print(get_complete_story_of_program())
