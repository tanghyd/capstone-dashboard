import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import reports, event_table, event_details, report_map
from apps.navbar import navbar
from apps.sidebar import sidebar, CONTENT_STYLE

pages = ['reports', 'events']


def error(pathname):
    return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised...")
            ]
    )


content = html.Div(id='page-content', style=CONTENT_STYLE)

app.layout = html.Div(
        [dcc.Location(id="url", refresh=False),
         sidebar,
         navbar,
         content,
         html.Div(id='intermediate-value', style={'display': 'none'})
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
