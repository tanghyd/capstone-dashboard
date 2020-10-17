import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from . import dataframe

options = [{'label': filename, 'value': filename} for filename in dataframe.filename.unique()]

layout = html.Div([
    html.H3('reports'),  # header name
    dcc.Dropdown(
            id='reports-dropdown',
            options=options,
    ),
    html.Div(id='reports-display-value'),  # we will output the result from our dropdown here
])

# handle the user interactivity for our dropdown
@app.callback(
        Output('reports-display-value', 'children'),
        [Input('reports-dropdown', 'value')])
def display_value(value):  # define the function that will compute the output of the dropdown
    return f'You have selected "{value}"'
