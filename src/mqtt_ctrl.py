#!/usr/bin/env python
""" This script handles the mqtt publishing

This script will:
This script uses my_secrets variables to connect to the MQTT broker and
publishes the data.

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
from time import sleep

import my_secrets

################################################################################
# Variables

################################################################################
# Functions
def publish_data(topic, payload = ""):
    '''
    this function publishes data to the mqtt broker

    Parameters
    ----------
    topic : str
        This is the topic of the publication
    payload : str, optional
        This is the payload of the publication
    '''
    publish.single(topic, payload, hostname=my_secrets.hostname,
                    port=my_secrets.port, client_id=my_secrets.client_id,
                    auth=my_secrets.auth)

def mqtt_ctrl_test():
    '''
    this function publishes test data to the mqtt broker
    the data is a counter incrementing to 100 and the cycle time is 2secs.

    '''
    for i in range(0,100):
        publish_data("std/dev301/s/mqtt_test/", f"{i}")
        sleep(2)

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    # execute only if run as a script
    mqtt_ctrl_test()
    