# main app

### imports ###
from dash import Dash

# app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server