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
from . import dataframe, capstone_files, metadata, geoview

from utils import to_list

with open("data/geoview/geofile.json") as gf:
    geofile = json.load(gf)

# build geopandas.geodataframe.GeoDataFrame (to start with geoview to preserve data type for plotly map)
# join geoview shape files, geoview metadata, capstone json to anumber mapping, and aggregated event statistics
df = geoview.merge(metadata, on='anumber').merge(capstone_files, on='anumber').merge(
    dataframe.groupby('filename')['label'].sum().reset_index(), on='filename')
df['commodity_list'] = df['commodity'].apply(lambda x : to_list(x, sep=';', default='NO TARGET COMMODITY'))  # expand string separated strings to list
#df['geometry'] = df['geometry'].map(yaml.safe_load)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# one hot encoding - can pre-compute if required
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
mlb.fit(df['commodity_list'])
commodities = pd.DataFrame(mlb.transform(df['commodity_list']), columns=mlb.classes_, index=df.index)
default_commodities = ['GOLD']

# timeline 
df['epoch'] = df.report_year.astype(np.int64).divide(1e9).astype(np.int64)
date_range = pd.date_range(df.report_year.min(), pd.to_datetime('2021-01-01'), freq="AS", name='year')
decades = [date for i, date in enumerate(date_range[::-1]) if i % 10 == 0][::-1]  # datetime for each decade
epochs = pd.Series(decades).astype(np.int64).divide(1e9).astype(np.int64)  # convert to unix time


options = [{'label': commodity, 'value': commodity} for commodity in commodities.columns.unique()]

seconds_per_year = 31536000
marks = {epoch: str(decade.year) for epoch, decade in zip(epochs, decades)}

# specify order of dataframe to display
hide_columns = ["geometry", "commodity_list", 'epoch']  # we dont want to display these 
show_columns = [
    'anumber', 'report_type','report_year','title','project',
    'commodity','keywords','filename','label']
df = df[show_columns + hide_columns]
df['report_year'] = df['report_year'].dt.strftime('%Y')


# specify an html layout for this app's page
layout = html.Div([
    html.H3('Mineral Exploration Map'),  # header name
    dcc.Dropdown(
        id='report-commodity-dropdown',
        options=options,
        value=default_commodities,
        multi=True
    ),
    dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
    dcc.RangeSlider(
        id='year-slider',
        min=df.epoch.min(),
        max=df.epoch.max(),
        value=[df.epoch.min(), df.epoch.max()],
        marks=marks,
        #marks={0 : '1970', seconds_per_year*10 : '1980', -seconds_per_year*10: '1960'},
        step=seconds_per_year,  # 31536000 seconds in a year
        persistence=True,
    ),
    html.Div([
                dcc.Markdown("""
                    **Selection Data**

                    Choose the lasso or rectangle tool in the map's label
                    bar and then select points in the map.
                """),
                #html.Div(id='selected-data'), #style=styles['pre']
                dash_table.DataTable(
                    id='selected-table',
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    },
                    #fixed_rows={'headers': True},
                    #style_table={'height': 800},  # defaults to 500
                    columns=[{"name": col, "id": col} for col in show_columns],
                )
            ]),#, className='three columns'),
        ]
    )

@app.callback(
    Output("graph","figure"),
    [Input('report-commodity-dropdown', 'value'),  # selected
    Input('year-slider', 'value')])  # epoch_range
def make_map(selected, epoch_range):
    
    # create data view subset on rangelslider year and commodity type
    # view = gpd.GeoDataFrame(df.loc[
    #     (commodities.loc[:,commodities.columns.isin(selected)].any(axis=1)) & # boolean logic applied on one hot encoding dataframe
    #     (df["epoch"] >= epoch_range[0]) & 
    #     (df["epoch"] <= epoch_range[1])
    # ])
    
    view = df.loc[
        commodities.loc[:,commodities.columns.isin(selected)].any(axis=1),
        ['anumber','title','label','report_type','report_year','project','commodity','keywords']]
    
    return px.choropleth_mapbox(
        view, geojson=geofile, locations='anumber',
        color='label',
        featureidkey="properties.anumber",
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=3, 
        center = {"lat": -27, "lon": 121.5},
        opacity=0.5,
        labels={'label':'# of near miss events'},
     #  hover_name = 'title',
        hover_data=['report_type','report_year','project','commodity',]
        )

@app.callback(
    Output('selected-table', 'data'),
    [Input('graph', 'selectedData')])
def display_selected_data(selectedData):
    if selectedData is not None:
        selectedANumbers = pd.DataFrame({"anumber": [selectedData['points'][i]['location'] for i in range(len(selectedData['points']))]})
        metadf = df.loc[:, ~df.columns.isin(hide_columns)] # remove the geometry info to get only the metadata
        return metadf.merge(selectedANumbers,on="anumber").to_dict("records")
    else:
        return None
# want to return all the events in the selected region by timeline.