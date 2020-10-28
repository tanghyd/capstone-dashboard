import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import dash_table

from dash.dependencies import Input, Output

from app import app
from app import map_data

dataframe = map_data.nlargest(100,'score')[['anumber', 'title','report_year', 'score']]
cols = ['A Number', 'Report Title','Year','Score']
dataframe.columns = cols

layout = html.Div(children=[
    html.H2(children='Top 100 Reports'),
    dash_table.DataTable(id='table',
    columns=[{"name": i, "id": i} for i in dataframe.columns],
    data=dataframe.to_dict('records'),
    style_cell={'textAlign': 'left',
    'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'whiteSpace': 'normal',
        'height': 'auto',
        'minWidth': '180px',
        'width': '180px',
        'maxWidth': '180px'},
    )
])