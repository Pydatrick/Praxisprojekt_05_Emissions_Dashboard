from dash import Input, Output, State
from app import app

@app.callback(
    Output("sidebar", "className"),
    Input("toggle-button", "n_clicks"),
    State("sidebar", "className")
)
def toggle_sidebar(n, current_class):
    if n is None:
        return current_class
    if "collapsed" in current_class:
        return "sidebar expanded"
    else:
        return "sidebar collapsed"