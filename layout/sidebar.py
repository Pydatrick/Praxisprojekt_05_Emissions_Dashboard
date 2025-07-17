from dash import html

def create_sidebar():
    return html.Div([
        html.Button("☰", id="toggle-button", n_clicks=0, className="toggle-btn"),
        html.Div([
            html.H2("Navigation"),
            html.A("Übersicht Emissionen ", href="/total"),
            html.Br(),
            html.A("Emissionen aus Kohle", href="/coal"),
            html.Br(),
            html.A("Emissionen aus Gas", href="/gas"),
            html.Br(),
            html.A("Emissionen aus Öl", href="/oil"),
            html.Br(),
            html.A("Emissionen aus Landwirtschaft", href="/landuse"),
            html.Br(),
            html.A("Emissionen pro Kopf", href="/per_capita"),
        ], id="sidebar-content"),
    ], id="sidebar", className="sidebar expanded")
