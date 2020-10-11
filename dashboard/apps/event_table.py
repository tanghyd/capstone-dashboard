import dash_bootstrap_components as dbc
import dash_html_components as html

from . import dataframe

dataframe = dataframe.copy()[['event_id', 'event_text', 'labels']]
cols = ['Event ID', 'Event Text', 'Label']
dataframe.columns = cols

def Table():
    rows = []
    for i in range(len(dataframe)):
        row = []
        for col in cols:
            value = dataframe.iloc[i][col]
            if col == 'Event ID':
                cell = html.Td(html.A(href=f'/event-details?row={i}', children=value, style={'color': 'white'}))
            else:
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
    html.H2(children='Labelled Events'),
    Table()
])