import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import reports, event_table, event_details, report_map, sidebar

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

# current page content
content = html.Div(id='page-content', style=CONTENT_STYLE)

# the "current" layout - content changes depending on pathname
app.layout = html.Div(
        [dcc.Location(id="url", refresh=False),
         sidebar.layout,
     #    navbar.layout,
         content,
])

# "complete" layout
# multi-page layout needs to be informed of all layouts to be displayed but no loaded
app.validation_layout = html.Div([
    sidebar.layout,
   # navbar.layout,
    reports.layout,
    event_table.layout,
    event_details.layout,
    report_map.layout,
])

pages = ['map','reports', 'events']

# callback that handles the sidebar hover highlight - hardcoded for three pills only?
@app.callback(
        [Output(f"{page}-link", "active") for page in pages],
        [Input("url", "pathname")])
def toggle_active_links(pathname):
    if pathname in ["/", "/home"]:
        return True, False, False
    return [pathname == f"/{page}" if page != 'event-details' else pathname == f"/events" for page in pages]

# callback for URL routing
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname in ["/", "/home"]:
        return report_map.layout
    elif pathname == '/events':
        return event_table.layout
    elif pathname == '/event-details':
        return event_details.layout
    elif pathname == '/map':
        return report_map.layout
    elif pathname =='/reports':
        return reports.layout
    else:
        return error(pathname)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)