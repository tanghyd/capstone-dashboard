# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

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
from apps import event_details

# import data
from app import map_data, map_geometry, events

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

layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Map', children=[
            html.Div(className='two-columns',children=[
                frontpage_map,
                dcc.Graph(id="selected-timeline", style={"width": "100%", "display": "inline-block",'vertical-align': 'middle'})
            ]
            )
        ]),
        dcc.Tab(label='Reports', children=[
            dash_table.DataTable(
                    id='report-table',
                    style_cell={'textAlign': 'left',
                    'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '180px',
                        'width': '180px',
                        'maxWidth': '180px'},                    
                    #fixed_rows={'headers': True},
                    #style_table={'height': 800},  # defaults to 500
                    columns=[{"name": col, "id": col} for col in ['id', 'Report Title','Year','Score']], # this should really be a variable
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    selected_rows=[],
                ),
        ]),
        dcc.Tab(label='Events', children=[
               html.Div(id="event-table")
        ]),
    ])
])

@app.callback(
    Output('report-table','data'),
    Output('selected-timeline', 'figure'),
    [Input('map', 'selectedData')])
def display_selected_data(selectedData):
    if selectedData is not None:
        selectedANumbers = pd.DataFrame({"anumber": [selectedData['points'][i]['location'] for i in range(len(selectedData['points']))]})
        report_df = map_data.loc[:, ~map_data.columns.isin(hide_columns)] # remove the geometry info to get only the metadata

        report_df['id'] = report_df['anumber']
        report_df.set_index('id', inplace=True, drop=False) # need a column that is actually called "id" for the datatable callback to work correctly
        report_df = report_df.merge(selectedANumbers,on="anumber")

        report_df = report_df.sort_values('score',axis=0,ascending=False)[['id', 'title','report_year', 'score']]
        cols = ['id', 'Report Title','Year','Score']
        report_df.columns = cols

        report_dates = map_data.loc[:, ['anumber','report_year','date_from','date_to']]
        events_timeline_df = events.merge(selectedANumbers,on="anumber")	       
        events_timeline_df = events_timeline_df.merge(report_dates,on="anumber")

        report_dict = report_df.to_dict('records')
        return report_dict, px.timeline(events_timeline_df, x_start="date_from", x_end="date_to", y="anumber", color="label")
    else:
        return [], {} # return nothing

@app.callback(
    Output('event-table','children'),
    [Input('report-table', 'selected_row_ids')])
def display_event_details(selectedRows):

    dataframe = events.copy()[['anumber','event_id', 'event_text', 'label']]
    dataframe['idx'] = dataframe.index

    cols = ['anumber','Event ID', 'Event Text', 'Label','idx']
    dataframe.columns = cols

    displaycols = ['Event ID', 'Event Text', 'Label']

    if selectedRows is not None:
        dataframe = dataframe.loc[dataframe['anumber'].isin(selectedRows),:]
        dataframe.drop('anumber',axis=1)

        #dataframe.set_index('Event ID')

        rows = []
        for i in range(len(dataframe)):
            row = []
            idx = dataframe.iloc[i]['idx']
            for col in displaycols:
                value = dataframe.iloc[i][col]
                if col == 'Event ID':
                    cell = html.Td(html.A(href=f'/event-details?row={idx}', children=value, style={'color': 'white'}))
                else:
                    cell = html.Td(children=value)
                row.append(cell)
            rows.append(html.Tr(row))

        table = [html.Thead(html.Tr([html.Th(col) for col in displaycols])), html.Tbody(rows)]
        return dbc.Table(table,
                        bordered=True,
                        dark=True,
                        hover=True,
                        responsive=True,
                        striped=True)
    else:
        return []


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)

