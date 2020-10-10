import sys

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps.sidebar import NAVBAR_STYLE
from . import dataframe

filenames = dataframe[['filename']].drop_duplicates()['filename']


options = [{'label': filename, 'value': idx} for idx, filename in filenames.to_dict().items()]

navbar = dbc.Navbar(
        [
            html.Div(
                    [
                        dbc.Row(
                                [
                                    dbc.Col(
                                            dbc.NavbarBrand("Search WAMEX Reports", className="ml-2",
                                                            style={'height': '30px', 'width': '200px'}),
                                            align="center"),
                                    dbc.Col(
                                            dcc.Dropdown(
                                                    id='navbar-dropdown',
                                                    options=options,
                                                    style={'height': '30px', 'width': '600px'},
                                                    # className="ml-auto flex-nowrap mt-3 mt-md-0"
                                            ),
                                            align="center"),
                                    dbc.Col(
                                            html.Div(id='navbar-display-report', style={'width': '600px'}),
                                            width="auto",
                                            align="center"),
                                ],
                                no_gutters=True
                        ),
                    ]
            )
        ],
        sticky="top",
        color="dark",
        dark=True,
        style=NAVBAR_STYLE
)


# output selected report to navbar
@app.callback(
        Output('navbar-display-report', 'children'),
        [Input('navbar-dropdown', 'value')])
def display_value(value):  # define the function that will compute the output of the dropdown
    if value == None:
        return 'No Report selected'
    return f'Displaying information from Report #{value}: {filenames.loc[value]}'


# add callback for search value in list for dropdown
@app.callback(
        Output("navbar-dropdown", "options"),
        [Input("navbar-dropdown", "search_value")], )
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    elif search_value == None:  # key error of none will error
        raise PreventUpdate
    return [o for o in options if search_value in o["value"]]


# add callback for toggling the collapse on small screens
@app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
