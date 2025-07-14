# callback def

### imports ###
from dash import Input, Output
from app import app

### callbacks ###
@app.callback(
    Output('output-id', 'children'),
    Input('input-id', 'value')
)
def update_output(value):
    return f"Du hast eingegeben: {value}"