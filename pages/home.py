from dash import html

def layout_home():
    return html.Div([
        html.H3("Willkommen auf dem Emissions-Dashboard"),
        html.P("Bitte wähle eine Kategorie in der Sidebar.")
    ])