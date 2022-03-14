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
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img
from datetime import timedelta

import my_secrets
from energy_log import EnergyLog

################################################################################
# Variables
logo = img(src='./static/img/logo.png', height="50", width="50", style="margin-top:-15px")
topbar = Navbar(logo,
                View('Login', 'get_login'),
                View('Zählerstände', 'get_power'),
                View('Historie', 'get_hist'),
                View('Logout', 'get_logout')
                )

# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)
Bootstrap(app)

nav.init_app(app)

################################################################################
# Functions
@app.route("/", methods = ["POST", "GET"])
def get_login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["pwd"]
        if user in my_secrets.users.keys():
            if my_secrets.users[user] == pwd:
                session["user"] = user
                session.permanent = True
                flash(f"{user} sucessful logged in.", "info")
                return redirect(url_for("get_power"))
            else:
                flash(f"wrong password for user: {user}", "info")
                return redirect(url_for("get_login")) 
        else:
            flash(f"unknown user: {user}", "info")
            return redirect(url_for("get_login"))    

    else:   
        if "user" in session:
            user = session["user"]
            flash(f"{user} already logged in", "info")
            return redirect(url_for("get_power")) 
 
    return render_template("login.html")


@app.route("/power", methods = ["POST", "GET"])
def get_power():
    if "user" in session:
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
            return render_template("power.html")
    else:
        flash(f"You are not logged in", "info")
        return redirect(url_for("get_login"))


@app.route("/hist", methods = ["GET"])
def get_hist():
    if "user" in session:
        power = EnergyLog()
        pwr_dict = power.get_history()
        print(f"Datum, Gas, Strom, Wasser")
        for key, val in pwr_dict.items():
            print(f"{key}, {val['gas']}, {val['power']}, {val['water']}")
        return render_template("history.html", pwr_dict=pwr_dict)
    else:
        flash(f"You are not logged in", "info")
        return redirect(url_for("get_login"))


@app.route("/logout")
def get_logout():
    if "user" in session:
        user = session["user"]
        flash(f"{user} have been logged out.", "info")
        session.pop("user", None)
    else:
        flash("You are not privisously logged in.")
    return redirect(url_for("get_login"))

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

