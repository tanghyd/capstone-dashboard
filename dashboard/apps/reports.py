import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import map_data

dataframe = map_data.nlargest(100,'score')[['anumber', 'title','report_year', 'score']]
cols = ['A Number', 'Report Title','Year','Score']
dataframe.columns = cols

def Table():
    rows = []
    for i in range(len(dataframe)):
        row = []
        for col in cols:
            value = dataframe.iloc[i][col]
            cell = html.Td(children=value)
            row.append(cell)
        rows.append(html.Tr(row))

    table = [html.Thead(html.Tr([html.Th(col) for col in cols])), html.Tbody(rows)]
    return dbc.Table(table,
                     bordered=True,
                     dark=True,
                     hover=True,
                     responsive=True,
                     striped=True)


layout = html.Div(children=[
    html.H2(children='Top 100 Reports'),
    Table()
])