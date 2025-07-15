from dash import html, dcc

def layout_oil():
    return html.Div([
        html.H3("Ölemissionen nach Land"),
        dcc.Dropdown(id="country-dropdown", options=[], placeholder="Land wählen"),
        dcc.Graph(id="total-graph")
    ])