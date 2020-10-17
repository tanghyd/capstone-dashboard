from urllib.parse import urlparse, parse_qs

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import spacy
from dash.dependencies import Input, Output
from lime.lime_text import LimeTextExplainer
from spacy import displacy
from spacy.lang.en import English
from joblib import load

from app import app
from . import dataframe

# load nlp model
#from pipeline.processing import load_spacy_model
from . import nlp

from pipeline.display import display_ent

pipe = load('models/model.pkl')

dataframe = dataframe.rename(columns={'trigger_words_in_event': 'Trigger Words'})

cols = ['Trigger Words', 'STRAT', 'ROCK', 'LOCATION', 'MINERAL', 'ORE_DEPOSIT', 'TIMESCALE']

class_names = ['not_near_miss', 'near_miss']  # just to display instead of 0 and 1
explainer = LimeTextExplainer(class_names=class_names)


def get_exp(sample):
    exp = explainer.explain_instance(sample.item(), pipe.predict_proba, num_features=6)
    fig = exp.as_pyplot_figure()
    return fig


@app.callback(
        Output('event-details', 'children'),
        [Input('url', 'search')]
)
def event_details(search):
    idx = parse_qs(urlparse(search).query)['row']
    row = dataframe.iloc[idx]
    event_text = row['event_text'].values[0]
    label_int = row['label'].values[0]
    label = "Near Miss Event" if label_int else "Not Near Miss Event"
    color = 'green' if label_int else 'red'

    table = dbc.Table(
            html.Tbody([html.Tr([html.Td(col), html.Td(val)]) for col, val in zip(cols, row[cols].values[0])]),
            bordered=True,
            dark=True,
            hover=True,
            responsive=True,
            striped=True,
    )

    exp = explainer.explain_instance(event_text, pipe.predict_proba, num_features=6)
    exp_df = pd.DataFrame(exp.as_list(), columns=['word', 'importance'])
    exp_df['color'] = exp_df['importance'].apply(lambda x: 'green' if x >= 0 else 'red')
    prob = round(pipe.predict_proba(row['event_text'].values)[0, 1] * 100, 1)
    title = f'Probability(Near Miss Event): {prob}%'

    fig = go.Figure(data=[go.Bar(
            x=exp_df.importance,
            y=exp_df.word,
            marker_color=exp_df.color,
            orientation='h',
    )])
    fig.update_layout(title=title, yaxis=dict(autorange="reversed"))

    return html.Div([
        html.H2(row['event_id'].values[0]),
        html.H3(label, style={'color': color}),
        html.Br(),
        html.H4('Event Text:'),
        html.Iframe(sandbox='', srcDoc=display_ent(nlp(event_text), style="ent"), width="100%"),
        html.Br(),
        table,
        dcc.Graph(figure=fig)
    ])


layout = html.Div([
    html.Div(id='event-details', style={'margin': '0 auto'})
])
