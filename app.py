# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 02:02:08 2018

@author: Dan
"""
import datetime
import io

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from sklearn.cluster import *
import math
from scipy.stats import norm
from dash.dependencies import Input, Output

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my-application")

from textwrap import dedent

df = pd.read_csv('../Hackathon_Copenhagen_2018/ClusteringWebApp/data/Xu_et_al_2016_dataset.xlsx')
df = df.rename(columns=lambda x: x.strip())
lats=list(df.iloc[0].values)
longs=list(df.iloc[1].values)
sample_names=list(df)   

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

pd_countries = pd.read_csv('data/Countries.csv')

data = go.Scattermapbox(
    lat = pd_countries['Lat'],
    lon = pd_countries['Lon'],
    name = 'Company',
    marker = dict(size = 15, opacity = 0.5)
)

mapbox_access_token='pk.eyJ1IjoiZmlsaXBwbzgyIiwiYSI6ImNqdGx1cHc0bTBodXM0NHBoMWI4aW5zdHQifQ.88J4ReUaoz8Zu0AxsQjS_w'

layout = dict(
    height = 800,
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
            lat= 46.7985624,
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

scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
[0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
[0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]

COLORSCALE = [ [0, "B61F45"], [0.15, "rgb(249,210,41)"], [0.3, "rgb(134,191,118)"],
                [0.45, "rgb(37,180,167)"], [0.6, "rgb(17,123,215)"], [0.85, "716E6B"],[1, "rgb(54,50,153)"] ]
"""
test_df = KDE_df[KDE_df.columns[0]]
traces=[]
traces.append(go.Scatter(
        x=range(len(test_df)),
        y=test_df,
        marker={
            'size': 0,
            'line': {'width': 0.5, 'color': 'black'}
        },
        ))
"""
#=======================

# external_stylesheets = ['']
# external_stylesheets = ['https://github.com/plotly/dash-app-stylesheets/blob/master/dash-analytics-report.css']
# external_stylesheets = ['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
# xternal_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.3.1/flatly/bootstrap.min.css']


# Boostrap CSS.
# app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

html_center = 'left'
# html_border = 'solid'
html_border = 'none'

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
    brand="Sustainability Ratings",
    brand_href="#",
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
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
                                    values=[],
                                    id="checklist-sectors",
                                ),
                            ]
                        ),
                        dbc.Button("View details", color="secondary"),
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
                        dbc.Button("View details", color="secondary"),
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
                        dbc.Button("View details", color="secondary"),
                    ],
                    md=4,
                ),
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
                html.Div(id='my-div')
            ],
            justify="center",
            no_gutters=True
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Regions"), 
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
                dbc.Col(
                    [
                        html.H2("Show results"), 
                        dbc.Button("View details", color="secondary"),
                    ],
                    md=12,
                ),
            ],
            justify="center",
            no_gutters=True
        ),
    ],
    className="mt-4",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[navbar, body])

# ---------------
# End of html
# ---------------



# ---------------------------------
# Callbacks
# ---------------------------------

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='checklist-sectors', component_property='values')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


# ---------------------------------
# Callbacks
# ---------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

#TODO
    # refind missing numbers on slider
    # deploy as web app
    # polish
    # add axis
