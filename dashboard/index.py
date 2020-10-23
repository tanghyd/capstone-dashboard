import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import reports, event_table, event_details, report_map, sidebar, navbar

pages = ['reports', 'events']

def error(pathname):
    return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised...")
            ]
    )

# the styles for the main content position it to the right of the side bar and add some padding
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

content = html.Div(id='page-content', style=CONTENT_STYLE)

app.layout = html.Div(
        [dcc.Location(id="url", refresh=False),
         sidebar.layout,
         navbar.layout,
         content,
         #html.Div(id='intermediate-value', style={'display': 'none'})
         ])

# "complete" layout
app.validation_layout = html.Div([
    sidebar.layout,
    navbar.layout,
    reports.layout,
    event_table.layout,
    event_details.layout,
    report_map.layout,
])

@app.callback(
        [Output(f"{page}-link", "active") for page in pages],
        [Input("url", "pathname")])
def toggle_active_links(pathname):
    if pathname in ["/", '/reports', "/home"]:
        return True, False
    else:
        return False, True


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname in ["/", '/reports', "/home"]:
        return reports.layout
    elif pathname == '/events':
        return event_table.layout
    elif pathname == '/event-details':
        return event_details.layout
    elif pathname == '/map':
        return report_map.layout
    else:
        return error(pathname)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)