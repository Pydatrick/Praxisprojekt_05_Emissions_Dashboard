from dash import html
# from layout.header import header
# from layout.sidebar import sidebar

def create_layout():
    return html.Div([
        # header,
        # sidebar,
        html.Div(id="page-content")  # Platz für dynamischen Content
    ])

