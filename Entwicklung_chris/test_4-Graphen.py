import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go

# Initialisiere die Dash App
app = dash.Dash(__name__)

# Definiere das Layout der App
app.layout = html.Div(children=[
    # Bereich für Zeitleiste und Dropdown-Menü
    html.H3("Kohleemission nach Land"),

    html.Div([
        dcc.Graph(id="total-graph"),
        dcc.Graph(id="per-capita-graph")
    ], className="row"),

    html.Div([
        dcc.Graph(id="trend-graph")
    ], className="row")
])


# Starte den Server
if __name__ == '__main__':
    app.run(debug=True)