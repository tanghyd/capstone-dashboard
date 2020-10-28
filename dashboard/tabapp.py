# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output

import plotly.express as px
import numpy as np
import pandas as pd
import geopandas as gpd

from datetime import datetime
import json

# import our main dash app variable from the app.py file
from app import app
from apps import event_table, event_details

# import data
from app import map_data, map_geometry, events

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# specify order of data frame to display in table
hide_columns = ["geometry", 'epoch']  # we dont want to display these 
show_columns = ['anumber','title','report_type','report_year','project',
'commodity','keywords','score']

geofile = json.loads(map_geometry.set_index('anumber').to_json())

fig = px.choropleth_mapbox(
    map_data, geojson=geofile,
    locations='anumber_str',
    color='score',
    featureidkey="id",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    zoom=4, 
    center={"lat": -25, "lon": 121.5},
    opacity=0.5,
    height=800,
    width=580
)

frontpage_map_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '64rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
}

frontpage_map = html.Div([
    html.H3('Mineral Exploration Map'),  # header name
    dcc.Graph(
        id="map", 
        figure=fig,  # thisis where choropleth mapbox figure is inserted
        style={"width": "100%", "display": "inline-block"}
    )]
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Map Tab', children=[
            frontpage_map
        ]),
        dcc.Tab(label='Table Tab', children=[
            dash_table.DataTable(
                    id='selected-table',
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        # 'minWidth': '25px',
                        # 'width': '150px',
                        # 'maxWidth': '200px'
                    },
                    style_table={'height': '700px', 'overflowY': 'auto', 'width': '1400px'},
                    #fixed_rows={'headers': True},
                    #style_table={'height': 800},  # defaults to 500
                    columns=[{"name": col, "id": col} for col in show_columns],
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    selected_rows=[],
                    style_cell_conditional=[
                        {'if': {'column_id': 'anumber'},
                        'width': '8%'},
                        {'if': {'column_id': 'title'},
                        'width': '25%'},
                        {'if': {'column_id': 'report_type'},
                        'width': '8%'},  
                        {'if': {'column_id': 'report_year'},
                        'width': '8%'},  
                         {'if': {'column_id': 'project'},
                        'width': '8%'},  
                        {'if': {'column_id': 'commodity'},
                        'width': '10%'},  
                        {'if': {'column_id': 'keywords'},
                        'width': '20%'},  
                        {'if': {'column_id': 'score'},
                        'width': '8%'},  
                        # {'if': {'column_id': 'count'},
                        # 'width': '5%'}, 
                        # {'if': {'column_id': 'total'},
                        # 'width': '2%'}, 
                        # {'if': {'column_id': 'prop'},
                        # 'width': '2%'},  
                        ],
                ),
        ]),
        dcc.Tab(label='Event Details', children=[
            event_table.layout
        ]),
    ])
])

@app.callback(
    Output('selected-table','data'),
    [Input('map', 'selectedData')])
def display_selected_data(selectedData):
    if selectedData is not None:
        selectedANumbers = pd.DataFrame({"anumber": [selectedData['points'][i]['location'] for i in range(len(selectedData['points']))]})
        metadf = map_data.loc[:, ~map_data.columns.isin(hide_columns)] # remove the geometry info to get only the metadata
        return metadf.merge(selectedANumbers,on="anumber").to_dict("records")
    else:
        return []

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)

