import dash
import dash_bootstrap_components as dbc

# load data frames
from database import events, map_data, map_geometry

app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True
)
server = app.server