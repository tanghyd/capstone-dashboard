import dash_bootstrap_components as dbc
import dash_html_components as html

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
}

layout = html.Div(
    [
        html.H2("WAMEX", className="display-4"),  # sidebar header(?)
        html.Hr(),
        html.P(
            "Natural Language Processing Dashboard UWA MDS", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Reports", href="/reports", id="reports-link"),
                dbc.NavLink("Report Map", href="/map", id='report-map-link'),
                dbc.NavLink("Events", href="/events", id="events-link"),
            ],
            vertical=True,  # ?
            pills=True,  # ?
        ),
    ],
    style=SIDEBAR_STYLE
)