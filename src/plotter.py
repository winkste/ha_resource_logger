""" This module handles the plotting of diagrams

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

import json
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import data_handler

################################################################################
# Functions

def plot_overall_counters_to_json() -> str:
    """Generates a plot of all counters and return it as json format

    Returns:
        str: json representation of a figure showing the overall counters
    """
    data_frame = data_handler.load_actuals_data()
    fig = plot_three_graphs_scatter(data_frame)
    return convert_figure_to_json(fig)

def plot_consumption_to_json() -> str:
    """Generates a plot of consumption and return it as json format

    Returns:
        str: json representation of a figure showing consumptions
    """
    data_frame = data_handler.load_actuals_data()
    diff_cols = ['gas', 'power', 'water']
    data_frame[diff_cols] = data_frame[diff_cols].diff()
    fig = plot_three_graphs_bar(data_frame)
    return convert_figure_to_json(fig)

def plot_three_graphs_scatter(data_frame:pd.DataFrame) -> go.Figure:
    """Plots the dataframe to three scatter graphs

    Args:
        data_frame (pd.DataFrame): data set for three data sets

    Returns:
        go.Figure: returns a plot with three graphs
    """
    fig = make_subplots(rows=1, cols=3)
    # plot gas in column 1 means left
    fig.add_trace(
        go.Scatter(x=data_frame['date'].tolist(), y=data_frame['gas'].tolist(), name="GAS"),
        row=1, col=1)
    # plot power in column 2 means middle
    fig.add_trace(
        go.Scatter(x=data_frame['date'].tolist(), y=data_frame['power'].tolist(), name="POWER"),
        row=1, col=2)
    # plot water in column 3 means right
    fig.add_trace(
        go.Scatter(x=data_frame['date'].tolist(), y=data_frame['water'].tolist(), name="WATER"),
        row=1, col=3)
    return fig

def plot_three_graphs_bar(data_frame:pd.DataFrame) -> go.Figure:
    """Plots the dataframe to three block graphs

    Args:
        data_frame (pd.DataFrame): data set for three data sets

    Returns:
        go.Figure: returns a plot with three graphs
    """
    fig = make_subplots(rows=1, cols=3)
        # plot gas in column 1 means left
    fig.add_trace(
        go.Bar(x=data_frame['date'].tolist(), y=data_frame['gas'].tolist(), name="GAS"),
        row=1, col=1)
    # plot power in column 2 means middle
    fig.add_trace(
        go.Bar(x=data_frame['date'].tolist(), y=data_frame['power'].tolist(), name="POWER"),
        row=1, col=2)
    # plot water in column 3 means right
    fig.add_trace(
        go.Bar(x=data_frame['date'].tolist(), y=data_frame['water'].tolist(), name="WATER"),
        row=1, col=3)
    return fig

def direct_plot_consumption():
    """This function directly plot the consumption
    """
    data_frame = data_handler.load_actuals_data()
    fig = plot_three_graphs_scatter(data_frame)
    fig.show()

def convert_figure_to_json(figure:go.Figure) -> str:
    """Convert a figure into a json string

    Args:
        figure (go.Figure): figure to be converted

    Returns:
        str: json representation of the figure
    """
    return json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
