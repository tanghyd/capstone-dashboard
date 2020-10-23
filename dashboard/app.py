import dash
import dash_bootstrap_components as dbc

# load data frames
from pipeline.data import *

app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True
)
server = app.server