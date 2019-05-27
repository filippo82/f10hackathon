# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 02:02:08 2018

@author: Filippo Broggini
"""
import datetime
import io

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my-application")

# ============== back end python ===================

# Create Geolocation Function =================================================
def geolocate(city=None, country=None):
    '''
    Inputs city and country, or just country. Returns the lat/long coordinates of
    either the city if possible, if not, then returns lat/long of the center of the country.
    '''

    # If the city exists,
    if city != None:
        # Try
        try:
            # To geolocate the city and country
            loc = geolocator.geocode(str(city + ',' + country))
            # And return latitude and longitude
            return (loc.latitude, loc.longitude)
        # Otherwise
        except:
            # Return missing value
            return np.nan
    # If the city doesn't exist
    else:
        # Try
        try:
            # Geolocate the center of the country
            loc = geolocator.geocode(country)
            # And return latitude and longitude
            return (loc.latitude, loc.longitude)
        # Otherwise
        except:
            # Return missing value
            return np.nan

# ============== back end python ===================

grade_dict = {
    'A+': 12,
    'A': 11,
    'A-': 10,
    'B+': 9,
    'B': 8,
    'B-': 7,
    'C+': 6,
    'C': 5,
    'C-': 4,
    'D+': 3,
    'D': 2,
    'D-': 1,
}

ex_in = [
    "Tobacco",
    "Alcohol",
    "Gambling",
    "Adult Entertainment",
    "Genetic",
    "Defense",
    "Nuclear",
    "Water",
    "Low-Carbon",
    "Women Empowerment",
    "Renewable Energy",
    "Circular Economy",
    "Education"
]

#df_countries = pd.read_csv('data/Countries.csv')

df_ratings = pd.read_csv('data/Ratings_latlon_v1.csv')

#df_funds = pd.read_csv('data/Funds_v1.csv')

df_funds_small = pd.read_csv('data/Funds_small_v1.csv')

data = go.Scattermapbox(
    lat = df_ratings['Lat'],
    lon = df_ratings['Lon'],
    name = 'Company',
    marker = dict(size = 15, opacity = 0.5, color = 'green')
)

mapbox_access_token='pk.eyJ1IjoiZmlsaXBwbzgyIiwiYSI6ImNqdGx1cHc0bTBodXM0NHBoMWI4aW5zdHQifQ.88J4ReUaoz8Zu0AxsQjS_w'

layout = dict(
    height = 600,
    # top, bottom, left and right margins
    margin = dict(t = 0, b = 0, l = 0, r = 0),
    #font = dict(color = '#FFFFFF', size = 11),
    #paper_bgcolor = '#000000',
    mapbox = dict(
        # here you need the token from Mapbox
        accesstoken = mapbox_access_token,
        #bearing = 0,
        # where we want the map to be centered
        center = dict(
            lat= 36.7985624,
			lon= 8.2319736
        ),
        # we want the map to be "parallel" to our screen, with no angle
        pitch = 0,
        # default level of zoom
        zoom = 1.5,
        # default map style
        style = 'light'
    )
)

# ============== back end python ===================

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Fit for Future Funds",
    brand_href="#",
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                html.H1("Fit for Future Funds")
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
                dbc.Alert(html.H3("Transparent fund selection based on accurate sustainability ratings"), color="success"),
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
                dbc.Col(
                    [

                    ],
                    md=1,
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.H2("Sectors"),
                                dbc.Checklist(
                                    options=[
                                        {"label": "Consumer Discretionary & Staples", "value": 0},
                                        {"label": "Energy", "value": 1},
                                        {"label": "Financials", "value": 2},
                                        {"label": "Health Care", "value": 3},
                                        {"label": "Industrials", "value": 4},
                                        {"label": "Information Technology", "value": 5},
                                        {"label": "Materials", "value": 6},
                                        {"label": "Real Estate", "value": 7},
                                        {"label": "Telecommunication Services", "value": 8},
                                        {"label": "Utlities", "value": 9},
                                    ],
                                    values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                    id="checklist-sectors",
                                ),
                            ]
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.H2("Exclusions"),
                                dbc.Checklist(
                                    options=[
                                        {"label": "Tobacco", "value": 0},
                                        {"label": "Alcohol", "value": 1},
                                        {"label": "Gambling", "value": 2},
                                        {"label": "Adult Entertainment", "value": 3},
                                        {"label": "Genetic", "value": 4},
                                        {"label": "Defense", "value": 5},
                                        {"label": "Nuclear", "value": 6},
                                    ],
                                    values=[],
                                    id="checklist-exclusions",
                                ),
                            ]
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.H2("Inclusions"),
                                dbc.Checklist(
                                    options=[
                                        {"label": "Water", "value": 0},
                                        {"label": "Low-Carbon", "value": 1},
                                        {"label": "Women Empowerment", "value": 2},
                                        {"label": "Renewable Energy", "value": 3},
                                        {"label": "Circular Economy", "value": 4},
                                        {"label": "Education", "value": 5},
                                    ],
                                    values=[],
                                    id="checklist-inclusions",
                                ),
                            ]
                        ),
                    ],
                    md=3,
                ),
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Regions"),
                    ],
                    md=12,
                    className=["text-center "],
                ),
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='graph-with-slider',
                            figure=go.Figure(
                                data=[data,],
                                layout=layout
                            )
                        )
                    ],
                    md=12,
                ),
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
              html.Hr()
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button("Show results", color="secondary", id='show_results'),
                    ],
                    md=4,
                    className=["text-center"]
                ),
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
              html.Hr()
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in df_funds_small.columns],
                            data=[],
                            style_cell={'textAlign': 'left'},
                            style_as_list_view=True,
                            style_data_conditional=[
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "A+"'
                                    },
                                    'backgroundColor': 'DarkGreen',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "A"'
                                    },
                                    'backgroundColor': 'DarkGreen',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "A-"'
                                    },
                                    'backgroundColor': 'DarkGreen',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "B+"'
                                    },
                                    'backgroundColor': 'LimeGreen',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "B"'
                                    },
                                    'backgroundColor': 'LimeGreen',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "B-"'
                                    },
                                    'backgroundColor': 'LimeGreen',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "C+"'
                                    },
                                    'backgroundColor': 'Red',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "C"'
                                    },
                                    'backgroundColor': 'Red',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "C-"'
                                    },
                                    'backgroundColor': 'Red',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "D+"'
                                    },
                                    'backgroundColor': 'DarkRed',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "D"'
                                    },
                                    'backgroundColor': 'DarkRed',
                                    'color': 'white',
                                },
                                {
                                    'if': {
                                        'column_id': 'Rating',
                                        'filter': 'Rating eq "D-"'
                                    },
                                    'backgroundColor': 'DarkRed',
                                    'color': 'white',
                                },
                            ]
                        )
                    ],
                    md=8,
                ),
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
              html.Hr()
            ],
        ),
    ],
    className="mt-4",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[body])

# ---------------
# End of html
# ---------------



# ---------------------------------
# Callbacks
# ---------------------------------

# @app.callback(
#     Output(component_id='my-div', component_property='children'),
#     [Input(component_id='checklist-sectors', component_property='values')]
# )
# def update_output_div(input_value):
#     return 'You\'ve entered "{}"'.format(input_value)

@app.callback(
    Output(component_id='table', component_property='data'),
    [Input(component_id='show_results', component_property='n_clicks')]
)
def on_button_click(n):
    if n is None:
        return []
    else:
        return df_funds_small.to_dict("rows")

# df_funds_small.to_dict("rows")

# ---------------------------------
# Callbacks
# ---------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

