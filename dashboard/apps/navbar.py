# import sys

# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate

# # import app
# from app import app

# # import data
# from app import capstone_files

# NAVBAR_STYLE = {
#     'position': 'relative',
#     'left': 0,
#     'right': 12,
#     'margin-left': '16rem', # left margin starts at 16rem width of sidebar
#     'padding': '1rem 1rem',
# }

# options = [{'label': str(anumber), 'value': idx} for idx, anumber in capstone_files[['anumber']].drop_duplicates()['anumber'].to_dict().items()]

# layout = dbc.Navbar(
#         [
#             html.Div(
#                     [
#                         dbc.Row(
#                                 [
#                                     dbc.Col(
#                                             dbc.NavbarBrand("Search WAMEX Reports", className="ml-2",
#                                                             style={'height': '30px', 'width': '200px'}),
#                                             align="center"),
#                                     dbc.Col(
#                                             dcc.Dropdown(
#                                                     id='navbar-dropdown',
#                                                     options=options,
#                                                     style={'height': '30px', 'width': '600px'},
#                                                     # className="ml-auto flex-nowrap mt-3 mt-md-0"
#                                             ),
#                                             align="center"),
#                                 #     dbc.Col(
#                                 #             html.Div(id='navbar-display-report', style={'width': '600px'}),
#                                 #             width="auto",
#                                 #             align="center"),
#                                 ],
#                                 no_gutters=True
#                         ),
#                     ]
#             )
#         ],
#         sticky="top",
#         color="dark",
#         dark=True,
#         style=NAVBAR_STYLE
# )

# # add callback for search value in list for dropdown
# @app.callback(
#         Output("navbar-dropdown", "options"),
#         [Input("navbar-dropdown", "search_value")], )
# def update_options(search_value):
#     if not search_value:
#         raise PreventUpdate
#     elif search_value == None:  # key error of none will error
#         raise PreventUpdate
#     return [o for o in options if search_value in o["value"]]

# # add callback for toggling the collapse on small screens
# @app.callback(
#         Output("navbar-collapse", "is_open"),
#         [Input("navbar-toggler", "n_clicks")],
#         [State("navbar-collapse", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
