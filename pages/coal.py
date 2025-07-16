from dash import html, dcc
from pathlib import Path
from data.data_loader import get_countries, get_year_range

def layout_coal():

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-coal.csv'

    entities = get_countries(PATHTOCSV)
    year_min, year_max = get_year_range(PATHTOCSV)

    return html.Div([
        html.H1("CO₂-Emissionen aus Kohle nach Ländern"),
        
        dcc.Dropdown(
            id='coal-entity-dropdown',
            options=[{'label': entity, 'value': entity} for entity in entities],
            placeholder="Wähle ein oder mehrere Länder",
            multi=True,
            searchable=True,
            clearable=False
        ),

        html.Div([
        html.Label("Jahresbereich auswählen:", style={'fontWeight': 'bold'}),
        dcc.RangeSlider(
            id='coal-year-slider',
            min=year_min,
            max=year_max,
            value=[year_min, year_max],
            marks={str(year): str(year) for year in range(year_min, year_max +1, 50)}, # Alle 50 Jahre
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}),
                  ], style={'padding': 10, 'margin-top': 20}
                 ),
        
        dcc.Graph(id='coal-line-plot')
    ])