""" This module handles the plotting of diagrams

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
    col_set = [["date", "Datum"], ["gas", "Gas"], ["power", "Strom"], ["water", "Wasser"]]
    fig = plot_x_graphs_scatter(data_frame, col_set)
    return convert_figure_to_json(fig)

def plot_consumption_to_json() -> str:
    """Generates a plot of consumption and return it as json format

    Returns:
        str: json representation of a figure showing consumptions
    """
    data_frame = data_handler.load_actuals_data()
    diff_cols = ['gas', 'power', 'water']
    data_frame[diff_cols] = data_frame[diff_cols].diff()
    col_set = [["date", "Datum"], ["gas", "Gas"], ["power", "Strom"], ["water", "Wasser"]]
    fig = plot_x_graphs_bar(data_frame, col_set)
    return convert_figure_to_json(fig)

def plot_historical_to_json() -> str:
    """Generates a plot of historical and return it as json format

    Returns:
        str: json representation of a figure showing consumptions
    """
    data_frame = data_handler.load_historical_data()
    col_set = [["year", "Jahr"], ["gas", "Gas"], ["power", "Strom"], ["water", "Wasser"]]
    fig = plot_x_graphs_vertical_bar(data_frame, col_set)
    return convert_figure_to_json(fig)

def plot_x_graphs_scatter(data_frame:pd.DataFrame, df_cols:list) -> go.Figure:
    """Plots the dataframe to x graph plots

    Args:
        data_frame (pd.DataFrame): data frame
        df_cols (list): list to identify columns in data frame

    Returns:
        go.Figure: three graph bar
    """
    if data_frame.shape[1] < len(df_cols):
        raise ValueError("Data frame doesn't have enough columns")
    if len(df_cols) < 2:
        raise ValueError("Column list doesn't have at least two columns")
    
    graph_columns = len(df_cols) - 1 # includes y axis at 0
    fig = make_subplots(rows=1, cols=graph_columns)


    for i in range(1,len(df_cols)):
        fig.add_trace(
            go.Scatter(x=data_frame[df_cols[0][0]].tolist(), y=data_frame[df_cols[i][0]].tolist(), name=df_cols[i][1]),
            row=1, col=i)

    return fig

def plot_x_graphs_bar(data_frame:pd.DataFrame, df_cols:list) -> go.Figure:
    """Plots the dataframe to x graph plots

    Args:
        data_frame (pd.DataFrame): data frame
        df_cols (list): list to identify columns in data frame

    Returns:
        go.Figure: three graph bar
    """
    if data_frame.shape[1] < len(df_cols):
        raise ValueError("Data frame doesn't have enough columns")
    if len(df_cols) < 2:
        raise ValueError("Column list doesn't have at least two columns")
    
    graph_columns = len(df_cols) - 1 # includes y axis at 0
    fig = make_subplots(rows=1, cols=graph_columns)

    for i in range(1,len(df_cols)):
        fig.add_trace(
            go.Bar(x=data_frame[df_cols[0][0]].tolist(), y=data_frame[df_cols[i][0]].tolist(), name=df_cols[i][1]),
            row=1, col=i)

    return fig

def plot_x_graphs_vertical_bar(data_frame:pd.DataFrame, df_cols:list) -> go.Figure:
    """Plots the dataframe to x graph plots vertical

    Args:
        data_frame (pd.DataFrame): data frame
        df_cols (list): list to identify columns in data frame

    Returns:
        go.Figure: three graph bar
    """
    if data_frame.shape[1] < len(df_cols):
        raise ValueError("Data frame doesn't have enough columns")
    if len(df_cols) < 2:
        raise ValueError("Column list doesn't have at least two columns")
    
    graph_columns = len(df_cols) - 1 # includes y axis at 0
    fig = make_subplots(rows=graph_columns, cols=1)

    for i in range(1, len(df_cols)):
        fig.add_trace(
            go.Bar(x=data_frame[df_cols[0][0]].tolist(), y=data_frame[df_cols[i][0]].tolist(), name=df_cols[i][1]),
            row=i, col=1)

    return fig

def direct_plot_consumption():
    """This function directly plot the consumption
    """
    data_frame = data_handler.load_actuals_data()
    col_set = [["date", "Datum"], ["gas", "Gas"], ["power", "Strom"], ["water", "Wasser"]]
    fig = plot_x_graphs_scatter(data_frame, col_set)
    fig.show()

def convert_figure_to_json(figure:go.Figure) -> str:
    """Convert a figure into a json string

    Args:
        figure (go.Figure): figure to be converted

    Returns:
        str: json representation of the figure
    """
    return json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
