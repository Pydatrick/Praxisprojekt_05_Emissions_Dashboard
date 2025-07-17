from dash import html

def create_sidebar():
    return html.Div([
        html.Button("☰", id="toggle-button", n_clicks=0, className="toggle-btn"),
        html.Div([
            html.H2("Navigation"),
            html.A("Übersicht Emission ", href="/total"),
            html.Br(),
            html.A("Emission Coal", href="/coal"),
            html.Br(),
            html.A("Emission Gas", href="/gas"),
            html.Br(),
            html.A("Emission Oil", href="/oil"),
            html.Br(),
            html.A("Emission landuse", href="/landuse"),
            html.Br(),
            html.A("Emission pro Kopf", href="/per_capita"),
        ], id="sidebar-content"),
    ], id="sidebar", className="sidebar expanded")
