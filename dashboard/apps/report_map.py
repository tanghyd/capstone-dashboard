import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import plotly.express as px
import numpy as np
import pandas as pd
import geopandas as gpd

from datetime import datetime
import json

# import our main dash app variable from the app.py file
from app import app

# import data
from app import map_data, map_geometry

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

#default_commodities = ['GOLD']

#date_range = pd.date_range(map_data.report_year.min(), pd.to_datetime('2021-01-01'), freq="AS", name='year')
#decades = [date for i, date in enumerate(date_range[::-1]) if i % 10 == 0][::-1]  # datetime for each decade
#epochs = pd.Series(decades).astype(np.int64).divide(1e9).astype(np.int64)  # convert to unix time

#options = [{'label': commodity, 'value': commodity} for commodity in commodities.columns.unique()]

#seconds_per_year = 31536000
#marks = {epoch: str(decade.year) for epoch, decade in zip(epochs, decades)}

# specify order of data frame to display
hide_columns = ["geometry", 'epoch']  # we dont want to display these 
show_columns = [
    'anumber','title','report_type','report_year','date_from','date_to','project',
   'commodity','keywords','score']
#map_data = map_data[show_columns + hide_columns]


#event_columns = ['anumber','event_text','date_from','date_to','label']
import json
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
    width=600
)

# specify an html layout for this app's page
layout = html.Div([
    html.H3('Mineral Exploration Map'),  # header name
    # dcc.Dropdown(
    #     id='report-commodity-dropdown',
    #     options=options,
    #     value=default_commodities,
    #     multi=True
    # ),
    dcc.Graph(
        id="map", 
        figure=fig,
        style={"width": "80%", "display": "inline-block"}),
    # dcc.RangeSlider(
    #     id='year-slider',
    #     min=map_data['epoch'].min(),
    #     max=map_data['epoch'].max(),
    #     value=[map_data['epoch'].min(), map_data['epoch'].max()],
    #     marks=marks,
    #     #marks={0 : '1970', seconds_per_year*10 : '1980', -seconds_per_year*10: '1960'},
    #     step=seconds_per_year,  # 31536000 seconds in a year
    #     persistence=True,
    # ),
    html.Div([
                dcc.Markdown("""
                    **Selection Data**

                    Choose the lasso or rectangle tool in the map's label
                    bar and then select points in the map.
                """),
                html.Div(id='selected-data'), #style=styles['pre']
                dash_table.DataTable(
                    id='selected-table',
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '250px',
                        'width': '250px',
                        'maxWidth': '250px'
                    },
                    #fixed_rows={'headers': True},
                    #style_table={'height': 800},  # defaults to 500
                    columns=[{"name": col, "id": col} for col in show_columns],
                ),
                #dcc.Graph(id="selected-timeline", style={"width": "100%", "display": "inline-block"})
            ]),#, className='three columns'),
        ]
    )

# @app.callback(
#     Output("map","figure"),
#     [Input('report-commodity-dropdown', 'value'),  # selected
#     Input('year-slider', 'value')])  # epoch_range
# def make_map(selected, epoch_range):
    
#     # create data view subset on rangelslider year and commodity type
#     # view = gpd.GeoDataFrame(df.loc[
#     #     (commodities.loc[:,commodities.columns.isin(selected)].any(axis=1)) & # boolean logic applied on one hot encoding dataframe
#     #     (df["epoch"] >= epoch_range[0]) & 
#     #     (df["epoch"] <= epoch_range[1])
#     # ])
    
#     view = map_data.loc[:,['anumber','title','label','report_type','report_year','project','commodity','keywords']]
    
#     return px.choropleth_mapbox(
#         view, geojson=geofile, locations='anumber',
#         color='label',
#         featureidkey="properties.anumber",
#         color_continuous_scale="Viridis",
#         mapbox_style="carto-positron",
#         zoom=3, 
#         center = {"lat": -27, "lon": 121.5},
#         opacity=0.5,
#         labels={'label':'# of near miss events'},
#      #  hover_name = 'title',
#         hover_data=['report_type','report_year','project','commodity',]
#         )

@app.callback(
    Output('selected-table','data'),
    # Output('selected-timeline', 'figure'),
    [Input('map', 'selectedData')])
def display_selected_data(selectedData):
    if selectedData is not None:
        selectedANumbers = pd.DataFrame({"anumber": [selectedData['points'][i]['location'] for i in range(len(selectedData['points']))]})
        metadf = map_data.loc[:, ~map_data.columns.isin(hide_columns)] # remove the geometry info to get only the metadata
        return metadf.merge(selectedANumbers,on="anumber").to_dict("records")
    else:
        return []


# @app.callback(
#     Output('selected-table','data'),
#     # Output('selected-timeline', 'figure'),
#     [Input('map', 'selectedData')])
# def display_selected_data(selectedData):
#     if selectedData is not None:
#         selectedANumbers = pd.DataFrame({"anumber": [selectedData['points'][i]['location'] for i in range(len(selectedData['points']))]})
#         metadf = map_data.loc[:, ~map_data.columns.isin(hide_columns)] # remove the geometry info to get only the metadata

#         report_dates = map_data.loc[:, ['anumber','report_year','date_from','date_to']]
#         events_timeline_df = events.merge(selectedANumbers,on="anumber")
#         events_timeline_df = events_timeline_df.merge(report_dates,on="anumber")
#         events_timeline_df = events_timeline_df.loc[:, event_columns]
#         return metadf.merge(selectedANumbers,on="anumber").to_dict("records"), px.timeline(events_timeline_df, x_start="date_from", x_end="date_to", y="anumber", color="label")
#     else:
#         return [], {}

#add something which displays the event selected from the timeline




###################
# THIS CODE WORKS #
###################

# # specify an html layout for this app's page
# layout = html.Div([
#     html.H3('Mineral Exploration Map'),  # header name
#     # dcc.Dropdown(
#     #     id='report-commodity-dropdown',
#     #     options=options,
#     #     value=default_commodities,
#     #     multi=True
#     # ),
#     dcc.Graph(
#         id="map", 
#         figure=fig,
#         style={"width": "100%", "display": "inline-block"}),
#     # dcc.RangeSlider(
#     #     id='year-slider',
#     #     min=map_data['epoch'].min(),
#     #     max=map_data['epoch'].max(),
#     #     value=[map_data['epoch'].min(), map_data['epoch'].max()],
#     #     marks=marks,
#     #     #marks={0 : '1970', seconds_per_year*10 : '1980', -seconds_per_year*10: '1960'},
#     #     step=seconds_per_year,  # 31536000 seconds in a year
#     #     persistence=True,
#     # ),
#     html.Div([
#                 dcc.Markdown("""
#                     **Selection Data**

#                     Choose the lasso or rectangle tool in the map's label
#                     bar and then select points in the map.
#                 """),
#                 html.Div(id='selected-data'), #style=styles['pre']
#                 dash_table.DataTable(
#                     id='selected-table',
#                     style_cell={
#                         'whiteSpace': 'normal',
#                         'height': 'auto',
#                         'minWidth': '250px',
#                         'width': '250px',
#                         'maxWidth': '250px'
#                     },
#                     #fixed_rows={'headers': True},
#                     #style_table={'height': 800},  # defaults to 500
#                     columns=[{"name": col, "id": col} for col in show_columns],
#                 ),
#                 #dcc.Graph(id="selected-timeline", style={"width": "100%", "display": "inline-block"})
#             ]),#, className='three columns'),
#         ]
#     )