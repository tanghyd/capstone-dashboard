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

# specify order of data frame to display in table
hide_columns = ["geometry", 'epoch']  # we dont want to display these 
show_columns = ['anumber','title','report_type','report_year','project',
'commodity','keywords','score','count'] # ,'total','prop', 'date_from','date_to'

# geofile for choropleth mapbox visualisation
import json
geofile = json.loads(map_geometry.set_index('anumber').to_json())

# build interactive choropleth_mapbox figure
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

# transparent background
# fig.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
# })

# specify an html layout for this app's page
layout = html.Div([
            html.Div([
                html.Div([
                    html.H3('Mineral Exploration Map'),  # header name
                        dcc.Graph(
                            id="map", 
                            figure=fig,  # this is where choropleth mapbox figure is inserted
                            style={"width": "80%", "display": "inline-block"}
                        )],className = "six columns"),  #six columns???

            html.Div([
                html.H3('Data Table'),
                dcc.Markdown("""
                    **Selection Data**

                    Choose the lasso or rectangle tool in the map's label
                    bar and then select points in the map.
                """),
                # html.Div(id='selected-data'), #style=styles['pre']
                dash_table.DataTable(
                    id='selected-table',
                    style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '25px',
                        'width': '150px',
                        'maxWidth': '200px'
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
                        'width': '5%'},
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
                        'width': '5%'},  
                        {'if': {'column_id': 'count'},
                        'width': '5%'}, 
                        # {'if': {'column_id': 'total'},
                        # 'width': '2%'}, 
                        # {'if': {'column_id': 'prop'},
                        # 'width': '2%'},  
                        ],
                ),
            ],className = "six columns"),
        ], className = "row"
    ),
    html.Div(id='datatable-interactivity-container')
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


# @app.callback(
#     Output('datatable-interactivity', 'style_data_conditional'),
#     [Input('datatable-interactivity', 'selected_columns')]
# )
# def update_styles(selected_columns):
#     return [{
#         'if': { 'column_id': i },
#         'background_color': '#D2F3FF'
#     } for i in selected_columns]

# @app.callback(
#     Output('datatable-interactivity-container', "children"),
#     [Input('datatable-interactivity', "derived_virtual_data"),
#      Input('datatable-interactivity', "derived_virtual_selected_rows")])
# def update_graphs(rows, derived_virtual_selected_rows):
#     # When the table is first rendered, `derived_virtual_data` and
#     # `derived_virtual_selected_rows` will be `None`. This is due to an
#     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
#     # calls the dependent callbacks when the component is first rendered).
#     # So, if `rows` is `None`, then the component was just rendered
#     # and its value will be the same as the component's dataframe.
#     # Instead of setting `None` in here, you could also set
#     # `derived_virtual_data=df.to_rows('dict')` when you initialize
#     # the component.
#     if derived_virtual_selected_rows is None:
#         derived_virtual_selected_rows = []

#     dff = df if rows is None else pd.DataFrame(rows)

#     colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
#               for i in range(len(dff))]

#     return [
#         dcc.Graph(
#             id=column,
#             figure={
#                 "data": [
#                     {
#                         "x": dff["country"],
#                         "y": dff[column],
#                         "type": "bar",
#                         "marker": {"color": colors},
#                     }
#                 ],
#                 "layout": {
#                     "xaxis": {"automargin": True},
#                     "yaxis": {
#                         "automargin": True,
#                         "title": {"text": column}
#                     },
#                     "height": 250,
#                     "margin": {"t": 10, "l": 10, "r": 10},
#                 },
#             },
#         )
#         # check if column exists - user may have deleted it
#         # If `column.deletable=False`, then you don't
#         # need to do this check.
#         for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
#     ]

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

