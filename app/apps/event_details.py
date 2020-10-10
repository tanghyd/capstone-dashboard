import sys
from urllib.parse import urlparse, parse_qs

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_lg')

from app import app

from . import dataframe

dataframe = dataframe.rename(columns={'trigger_words_in_event': 'Trigger Words'})

cols = ['Trigger Words', 'STRAT', 'ROCK', 'LOCATION', 'MINERAL', 'ORE_DEPOSIT', 'TIMESCALE']


@app.callback(
        Output('event-details', 'children'),
        [Input('url', 'search')]
)
def event_details(search):
    idx = parse_qs(urlparse(search).query)['row']
    row = dataframe.iloc[idx]
    event_text = row['event_text'].values[0]


    table = dbc.Table(
            html.Tbody([html.Tr([html.Td(col), html.Td(val)]) for col, val in zip(cols, row[cols].values[0])]),
            bordered=True,
            dark=True,
            hover=True,
            responsive=True,
            striped=True,
    )

    return html.Div([
        html.H2(row['event_id'].values[0]),
        html.Br(),
        html.H4('Event Text:'),
        html.Iframe(sandbox='', srcDoc=displacy.render(nlp(event_text), style="ent"), width="100%"),
        html.Br(),
        table
    ])


layout = html.Div([
    html.Div(id='event-details', style={'margin': '0 auto'})
])
