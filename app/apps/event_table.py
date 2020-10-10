import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('data/group_all_labelled.csv',
                 usecols=['group', 'filename', 'Near Miss Event', 'event_text', 'reviewed'], nrows=50)

df['label'] = df['Near Miss Event'].astype(int)
df = df.loc[
    df.reviewed, ['group', 'filename', 'event_text', 'label']]  # only show reviewed events but drop column after subset

layout = html.Div(children=[
    html.H4(children='Extracted Labelled Events'),
    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
])
