from dash import html

def create_header():
    return html.Div([
        html.H1("CO₂ Emissionen Dashboard", className="header-title")
    ], className="header")