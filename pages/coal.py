from dash import html, dcc

def layout_coal():
    return html.Div([
        html.H3("Kohleemission nach Land"),
        dcc.Dropdown(id="country-dropdown", options=[], placeholder="Land wählen"),
        dcc.Dropdown(id="country-dropdown2", options=[], placeholder="Land wählennjoaegjnbiaeghoun"),
        dcc.Graph(id="total-graph"),
        dcc.Graph(id="total-graph2")
    ])