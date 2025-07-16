from dash import html, dcc
from layout.header import create_header
from layout.sidebar import create_sidebar


def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        
        create_header(),  # bleibt oben
        
        html.Div([        # flex-container
            create_sidebar(),  # linke spalte
            html.Div(id='main-content', className="main-content")  # rechte spalte
        ], className="content-container")
    ])