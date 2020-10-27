import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# import app
from app import app

# # import data
# from app import capstone_files

NAVBAR_STYLE = {
    'position': 'relative',
    'left': 0,
    'right': 12,
   # 'margin-left': '16rem', # left margin starts at 16rem width of sidebar
    'padding': '2rem 1rem',
}

# options = [{'label': str(anumber), 'value': idx} for idx, anumber in capstone_files[['anumber']].drop_duplicates()['anumber'].to_dict().items()]

# this example has a search bar and button instead of navitems / dropdowns
layout = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("WAMEX", href="/map", className="ml-2",style={'height': '30px', 'width': '200px'}),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavLink("Map", href="/map", id='map-link'),
                        dbc.NavLink("Reports", href="/reports", id="reports-link"),
                        dbc.NavLink("Events", href="/events", id="events-link"),
                    ],
                    pills=True, 
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    sticky="top",
    color="dark",
    dark=True,
    style=NAVBAR_STYLE,
    className="mb-5",
)



# # this example has a search bar and button instead of navitems / dropdowns
# layout = dbc.Navbar(
#     dbc.Container(
#         [
#             dbc.NavbarBrand("Search", href="#"),
#             dbc.NavbarToggler(id="navbar-toggler3"),
#             dbc.Collapse(
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             dbc.Button(type="search", placeholder="Search")
#                         ),
#                         dbc.Col(
#                             dbc.Button(
#                                 "Search", color="primary", className="ml-2"
#                             ),
#                             # set width of button column to auto to allow
#                             # search box to take up remaining space.
#                             width="auto",
#                         ),
#                     ],
#                     no_gutters=True,
#                     # add a top margin to make things look nice when the navbar
#                     # isn't expanded (mt-3) remove the margin on medium or
#                     # larger screens (mt-md-0) when the navbar is expanded.
#                     # keep button and search box on same row (flex-nowrap).
#                     # align everything on the right with left margin (ml-auto).
#                     className="ml-auto flex-nowrap mt-3 mt-md-0",
#                     align="center",
#                 ),
#                 id="navbar-collapse3",
#                 navbar=True,
#             ),
#         ]
#     ),
#     className="mb-5",
# )

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
