from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

import numpy as np
import pandas as pd 
import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateFormatter, AutoDateLocator
import plotly.graph_objs as go

all_df = pd.read_csv('data/devices1.csv')

columns_todrop = ['current_in','current_out','panel_voltage','state_of_charge_percent','usb_current','voltage']
batt0 = all_df.drop(columns=columns_todrop)

batt0['year'] = pd.DatetimeIndex(batt0['timestamp']).year
batt0['month'] = pd.DatetimeIndex(batt0['timestamp']).month
batt0['date'] = pd.DatetimeIndex(batt0['timestamp']).day
batt0["power"] = batt0["battery_voltage"] * batt0["current"]

app = Dash(__name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [
        html.H2("Visualization for devices1.csv"),
        html.Div(
            [
                dbc.Label("Battery ID"),
                dcc.Dropdown(
                    batt0['battery_id'].unique(),
                    id="battid",
                    
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("year"),
                dcc.Dropdown(
                    batt0['year'].unique(),
                    id="year",
                    value=2021,
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("month"),
                dcc.Dropdown(
                    batt0['month'].unique(),
                    id="month",
                    value=3,
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("date"),
                dcc.Dropdown(
                    batt0['date'].unique(),
                    id="date",
                    value=2,
                ),
            ]
        ),
    ],
    body=True,
)

graph = dbc.Card(
    [
        dcc.Graph(id="plot")
    ],
    body=True,
)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_index = html.Div([
    html.H2('Bbox Challenge'),
    dcc.Link(html.Button('Visualization'), href='/page-1'),
    dcc.Link(html.Button('Insights'), href='/page-2'),
])

layout_page_1 = html.Div([
    dbc.Container(
    [
        html.H1("Visualization"),
        dcc.Link(html.Button('Navigate to home'), href='/'),
        dcc.Link(html.Button('Insights'), href='/page-2'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(graph, md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
),

])

layout_page_2 = html.Div([
    html.H2('Insights'),
    dcc.Link(html.Button('Navigate to home'), href='/'),
    dcc.Link(html.Button('Visualization'), href='/page-1'),
])

# index layout
app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    layout_page_1,
    layout_page_2,
])


# Index callbacks
@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/page-1":
        return layout_page_1
    elif pathname == "/page-2":
        return layout_page_2
    else:
        return layout_index


# Page 1 callbacks
@callback(Output("plot", "figure"),
    [
        Input("battid", "value"),
        Input("year", "value"),
        Input("month", "value"),
        Input("date", "value"),
    ],
)
def make_graph(battid, year, month, date):
    datebatt = batt0.loc[(batt0.battery_id == battid) &(batt0.year == year) & (batt0.month == month) & (batt0.date == date)]

    dates = datebatt.loc[:,"timestamp"]
    current = datebatt.loc[:,"current"]
    voltage = datebatt.loc[:,"battery_voltage"]
    power = datebatt.loc[:,"power"]


    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=dates,
            y=voltage,
            mode="lines",
            marker={"size": 4},
            name='voltage'
        ))

    fig.add_trace(go.Scatter(
            x=dates,
            y=current,
            mode="lines",
            marker={"size": 4},
            name='current'
        ))

    fig.add_trace(go.Scatter(
            x=dates,
            y=power,
            mode="lines",
            marker={"size": 4},
            name='power'
        ))


   
    return fig





# Page 2 callbacks



if __name__ == '__main__':
    app.run_server(debug=True)
