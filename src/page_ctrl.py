#!/usr/bin/env python
""" This script handles the web page for energy entry

This script will:
- use flask to generate the web page for the data entry of gas, electricity 
    and water
- it generates the EngeryLog object to store the data and publish it to 
    mqtt broker
- some code base on
     https://getbootstrap.com/docs/5.1/getting-started/introduction/
    https://www.w3schools.com/html/html_form_input_types.asp

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
__date__ = "2022/02/27"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "winkste"
__status__ = "Development"
__version__ = "0.0.1"

################################################################################
# Imports
from flask import Flask, redirect, url_for, render_template, request
from energy_log import EnergyLog

################################################################################
# Variables
app = Flask(__name__)

################################################################################
# Functions

# start home page
@app.route("/", methods =["POST", "GET"])
def home():
    if request.method == "POST":
        power = EnergyLog()
        new_value = int(request.form["gas"])
        power.set_new_gas(new_value)
        new_value = int(request.form["ele"])
        power.set_new_power(new_value)
        new_value = int(request.form["water"])
        power.set_new_water(new_value)
        power.save_new_data()
        return f"<h1>data successfully stored</h1>"
    else:    
        return render_template("index.html")

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

