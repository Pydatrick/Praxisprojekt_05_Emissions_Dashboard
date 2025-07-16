from dash import html, dcc

def layout_kuhpups():
    return html.Div([
        html.H3("kuhpups nach Land"),
        dcc.Dropdown(id="country-dropdown", options=[], placeholder="Land wählen"),
        dcc.Dropdown(id="country-dropdown2", options=[], placeholder="Land wählennjoaegjnbiaeghoun"),
        dcc.Graph(id="kuhpups_graph"),
        dcc.Graph(id="kuhpups_linelot")
    ])