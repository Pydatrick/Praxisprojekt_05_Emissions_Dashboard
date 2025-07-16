from dash import Dash
from dash.dependencies import Input, Output

def register_sidebar_toggle(app: Dash):
    @app.callback(
        Output("sidebar", "className"),
        Input("toggle-button", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_sidebar(n_clicks):
        if n_clicks % 2 == 1:
            return "sidebar collapsed"
        return "sidebar expanded"
