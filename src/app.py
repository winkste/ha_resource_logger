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
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from dominate.tags import img

import my_secrets
import mqtt_ctrl
#from energy_log import EnergyLog
import data_analysis as da
import plotter
import parameter


################################################################################
# Variables
port_number:int = parameter.PORT_NUMBER
logo = img(src='./static/img/logo.png', height="50", width="50", style="margin-top:-15px")
topbar = Navbar(logo,
                View('Login', 'get_login'),
                View('Eingabe Zählerstände', 'get_new_data_entry_page'),
                View('Eingabe Jahresverbräuche', 'get_new_history_entry_page'),
                View('Ansicht Jahresverbräuche', 'get_historical'),
                View('Tabelle Zähler', 'get_actuals_view'),
                View('Tabelle Jahresverbräuche', 'get_historical_view'),
                View('Statistiken', 'get_statistics_view'),
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
        if user in my_secrets.USERS.keys():
            if my_secrets.USERS[user] == pwd:
                session["user"] = user
                session.permanent = True
                flash(f"{user} sucessful logged in.", "info")
                return redirect(url_for("get_new_data_entry_page"))
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
            return redirect(url_for("get_new_data_entry_page"))
    return render_template("login.html")


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


@app.route('/newyear', methods = ["GET", "POST"])
def get_new_data_entry_page():
    """
    Generates the new data entry page
    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        if request.method == "POST":
            # get the data from the page
            data_set = request.get_json()
            new_data = data_set['values']
            # store the data
            da.set_new_counter_data_set(new_data)
            #TODO: publish data via mqtt
            flash("data successfully stored and published")
            return jsonify({'message': 'Values updated successfully'})
        return render_template('new_data.html', jumpPage='/newyear', page_name="Zählerstände",
                               ccolumn_names=da.get_counter_column_names(),
                               initial_data=da.get_last_counter_row_as_list())
    flash("You are not logged in", "info")
    return redirect(url_for("get_login"))


@app.route('/newhist', methods = ["GET", "POST"])
def get_new_history_entry_page():
    """
    Generates the new history entry page
    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        if request.method == "POST":
            # get the data from the page
            data_set = request.get_json()
            new_data = data_set['values']
            # store the data
            da.set_history_from_list(new_data)
            #TODO: publish data via mqtt
            flash("data successfully stored and published")
            return jsonify({'message': 'Values updated successfully'})
        return render_template('new_data.html', jumpPage='/newyear', page_name="Verbräuche",
                               ccolumn_names=da.get_history_column_names(), initial_data=da.get_last_history_row_as_list())
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


@app.route("/viewhist", methods = ["GET"])
def get_historical_view():
    """
    Generates the historical page for flask
    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        return render_template('view_history.html', page_name="Verbräuche",
                               ccolumn_names=da.get_history_column_names(),
                               initial_data=da.get_history_as_list())

    flash("You are not logged in", "info")
    return redirect(url_for("get_login"))


@app.route("/viewactuals", methods = ["GET"])
def get_actuals_view():
    """
    Generates the actuals page for flask
    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        return render_template('view_history.html', page_name="Zählerstände",
                               ccolumn_names=da.get_counter_column_names(),
                               initial_data=da.get_counters_as_list())
    flash("You are not logged in", "info")
    return redirect(url_for("get_login"))


@app.route("/viewstats", methods = ["GET"])
def get_statistics_view():
    """
    Generates the statistics page for flask
    Return
    --------
    obj : returns a page that is displayed in the browser
    """
    if "user" in session:
        stats_data = da.get_statistics(2023)
        # Zipping the data before passing it to the template
        zipped_data = zip(list(stats_data.keys()), list(stats_data.values()))
        return render_template('view_stats.html', page_name="Statistiken", stats_data=zipped_data)
    flash("You are not logged in", "info")
    return redirect(url_for("get_login"))


@app.route('/api/hist')
def get_history_api():
    """
    Get the history API
    Return
    --------
    obj : returns a string of data or redirects to the login display
    """
    if "user" in session:
        return da.get_historical_as_string()
    flash("You are not logged in", "info")
    return redirect(url_for("get_login"))


@app.route('/api/actuals')
def data_func():
    """
    Get the actuals API
    Return
    --------
    obj : returns a string of data or redirects to the login display
    """
    if "user" in session:
        return da.get_counters_as_string()
    flash("You are not logged in", "info")
    return redirect(url_for("get_login"))

################################################################################
# Classes

################################################################################
# Scripts
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port_number)
