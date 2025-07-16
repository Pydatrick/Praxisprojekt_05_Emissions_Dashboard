from dash import Dash, html, Input, Output, State

app = Dash(__name__)

app.layout = html.Div([
    # Toggle Button außerhalb der Sidebar, bleibt immer sichtbar
    html.Button("☰", id="toggle-button", n_clicks=0, className="toggle-btn"),

    # Sidebar selbst
    html.Div(id="sidebar", children=[
        html.H2("Navigation"),
        html.A("Emission Coal", href="/coal"),
        html.Br(),
        html.A("Emission Gas", href="/gas"),
        html.Br(),
        html.A("Emission Oil", href="/oil"),
        html.Br(),
        html.A("Emission kuhpups", href="/kuhpups"),
    ], className="sidebar expanded"),

    # Hauptinhalt
    html.Div("Main Content goes here", className="main-content")
])

# Callback zur Steuerung der Sidebar-Klasse
@app.callback(
    Output("sidebar", "className"),
    Input("toggle-button", "n_clicks"),
    State("sidebar", "className"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, current_class):
    if "collapsed" in current_class:
        return "sidebar expanded"
    else:
        return "sidebar collapsed"

if __name__ == "__main__":
    app.run(debug=True)
