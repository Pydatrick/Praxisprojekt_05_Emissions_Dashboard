from dash import html

def create_sidebar():
    return html.Div([
        html.Button("☰", id="toggle-button", n_clicks=0, className="toggle-btn"),
        html.Div(id="sidebar-content", children=[
            html.H2("Navigation"),
            html.A("Emission Coal", href="/coal"),
            html.Br(),
            html.A("Emission Gas", href="/gas"),
            html.Br(),
            html.A("Emission Oil", href="/oil"),
        ])
    ], id="sidebar", className="sidebar expanded")