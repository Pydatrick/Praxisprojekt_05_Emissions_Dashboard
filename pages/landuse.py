from dash import html, dcc
from pathlib import Path
from data.data_loader import get_countries, get_year_range, get_preselection

def layout_landuse():

    ROOT = Path(__file__).resolve().parent.parent
    PATH_TO_CSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-land-use-change.csv'

    entities = get_countries(PATH_TO_CSV)
    preselection_options = get_preselection(PATH_TO_CSV)
    year_min, year_max = get_year_range(PATH_TO_CSV)

    return html.Div([
        html.H1("CO₂-Emissionen aus Landwirtschaft nach Ländern"),
        dcc.Dropdown(
            id='landuse-preselection-dropdown',
            options=preselection_options,
            placeholder = 'Treffe eine Vorauswahl',
            multi=True,
            clearable=False,
            style={'margin-bottom': '15px'}
        ),
        dcc.Dropdown(
            id='landuse-entity-dropdown',
            options=[{'label': entity, 'value': entity} for entity in entities],
            placeholder="Wähle eine oder mehrere Entität(en)",
            multi=True,
            searchable=True,
            clearable=False
        ),

        html.Div([
        html.Label("Jahresbereich auswählen:", style = {'fontWeight' : 'bold'}),
        dcc.RangeSlider(
            id='landuse-year-slider',
            min=year_min,
            max=year_max,
            value=[year_min, year_max],
            marks={str(year): str(year) for year in range(year_min, year_max + 1, 5)}, # Alle 5 Jahre
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}),
                  ], style={'padding': 10, 'margin-top': 20}
                 ),
        
        html.Div([
            dcc.Graph(id='landuse-line-plot'),
            dcc.Graph(id='landuse-bar-plot'),
        ], style={
            'display': 'grid',
            'gridTemplateColumns': '50% 50%',
            'gridGap': '15px',
            'padding': '10px 50px 50px 50px'
        }),
        html.Div([
            dcc.Graph(id='landuse-map'),
        ], style={'margin_left' : 'auto', 'margin_right' : 'auto'})
    ], id='main-content', style={'margin-left': '0', 'transition': 'margin-left 0.3s'})

    