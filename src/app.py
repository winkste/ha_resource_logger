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

import collections.abc
import collections
from datetime import timedelta
collections.MutableMapping = collections.abc.MutableMapping
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from dominate.tags import img

import mqtt_secrets
import mqtt_ctrl
#from energy_log import EnergyLog
from resource_mgr import ResMgr
import plotter
import parameter


################################################################################
# Variables
port_number:int = parameter.PORT_NUMBER
logo = img(src='./static/img/logo.png', height="50", width="50", style="margin-top:-15px")
topbar = Navbar(logo,
                View('Login', 'get_login'),
                View('Zählerstände', 'get_power'),
                View('Daten', 'get_datasets'),
                View('Actuals', 'get_actuals'),
                View('Historie', 'get_historical'),
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
    """
    Generates the login page for flask

    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["pwd"]
        if user in mqtt_secrets.USERS.keys():
            if mqtt_secrets.USERS[user] == pwd:
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
    """
    Generates the resource entry page for flask

    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        if request.method == "POST":
            res_mgr = ResMgr()
            new_value = int(request.form["gas"])
            res_mgr.set_new_gas(new_value)
            new_value = int(request.form["ele"])
            res_mgr.set_new_power(new_value)
            new_value = int(request.form["water"])
            res_mgr.set_new_water(new_value)
            res_mgr.save_new_data()
            mqtt_ctrl.publish_data("std/dev301/s/ener_wat/gas",
                                    int(res_mgr.get_gas_year_consum()))
            mqtt_ctrl.publish_data("std/dev301/s/ener_wat/power",
                                    int(res_mgr.get_power_year_consum()))
            mqtt_ctrl.publish_data("std/dev301/s/ener_wat/water",
                                    int(res_mgr.get_water_year_consum()))
            mqtt_ctrl.publish_data("std/dev301/s/ener_wat/date",
                                    res_mgr.get_last_date())
            flash("data successfully stored and published")
            return redirect(url_for("get_analysis"))
        else:
            return render_template("power.html")
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("get_login"))


@app.route("/data", methods = ["GET"])
def get_datasets():
    """
    Generates the history log page for flask

    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        res_mgr = ResMgr()
        res_str = res_mgr.get_history()
        return render_template("datasets.html", res_data=res_str)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("get_login"))

@app.route("/act", methods = ["GET"])
def get_actuals():
    """
    Generates the analysis page for flask

    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        graph_json_count = plotter.plot_overall_counters_to_json()
        graph_json_consum = plotter.plot_consumption_to_json()
        return render_template('actuals.html',
                                graphJSON1=graph_json_count,
                                graphJSON2=graph_json_consum)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("get_login"))

@app.route("/hist", methods = ["GET"])
def get_historical():
    """
    Generates the historical page for flask

    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        graph_json_hist = plotter.plot_historical_to_json()
        return render_template('history.html', graphJSON1=graph_json_hist)
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("get_login"))


@app.route("/logout")
def get_logout():
    """
    Generates the logout page for flask
    
    Return
    --------
    obj : returns a page that is displayed in the browser
    """
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
    app.run(debug=True, host="0.0.0.0", port=port_number)

