import sys
import os
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px

# Pfad zur Datenquelle
csv_ordner = r"C:\DataCraft\11_Datenvisualisierung\Projekt-Emission-Dashboard\data\raw"

# CSV-Dateien einlesen
data_sources = {}
for dateiname in os.listdir(csv_ordner):
    if dateiname.endswith(".csv"):
        dateipfad = os.path.join(csv_ordner, dateiname)
        df = pd.read_csv(dateipfad)
        key = os.path.splitext(dateiname)[0]
        data_sources[key] = df

default_key = list(data_sources.keys())[0]
df_coal = data_sources[default_key]

# Kontinent-Länder Mapping
sys.path.append(r"C:\DataCraft\11_Datenvisualisierung\Projekt-Emission-Dashboard\data")
from kontinente_laender_liste import country_to_continent_map

kontinente = sorted(set(country_to_continent_map.values()))

app = Dash(__name__)

kontinent_options = [{'label': k, 'value': k} for k in kontinente]

def get_countries_by_continent(continent):
    return sorted([country for country, cont in country_to_continent_map.items() if cont == continent])

app.layout = html.Div([
    # Sidebar
    html.Div([
        html.H2("Emission auswählen", style={'padding': '10px', 'color': 'white'}),
        html.Div([
            dcc.RadioItems(
                id='emission-dropdown',
                options=[{'label': key, 'value': key} for key in data_sources.keys()],
                value=default_key,
                labelStyle={'display': 'block', 'padding': '8px', 'fontSize': '16px', 'color': 'white'},
                inputStyle={"margin-right": "8px"}
            )
        ], style={'padding': '0 15px'}),
        html.Button("Schließen", id='close-sidebar', n_clicks=0,
                    style={'margin': '20px', 'padding': '10px', 'fontSize': '16px', 'cursor': 'pointer'})
    ],
    id='sidebar',
    style={
        'position': 'fixed',
        'top': 0,
        'left': '-250px',
        'width': '250px',
        'height': '100%',
        'background-color': '#111',
        'overflow-x': 'hidden',
        'transition': '0.3s',
        'padding-top': '20px',
        'zIndex': 1000
    }),

    # Button zum Öffnen der Sidebar
    html.Button('☰ Emission wählen', id='open-sidebar', n_clicks=0,
                style={
                    'position': 'fixed',
                    'top': '10px',
                    'left': '10px',
                    'fontSize': '20px',
                    'zIndex': 1100,
                    'cursor': 'pointer'
                }),

    # Hauptinhalt
    html.Div([
        # Dropdowns und Slider
        html.Div([
            html.Div("Hinweis: Es können bis zu alle Kontinente ausgewählt werden.", style={'margin-bottom': '10px'}),
            dcc.Dropdown(
                id='kontinent-dropdown',
                options=kontinent_options,
                value=kontinente[:1],
                multi=True,
                clearable=False,
                style={'margin-bottom': '15px'}
            ),

            html.Div("Hinweis: Es können maximal fünf Länder ausgewählt werden.", style={'margin-bottom': '10px'}),
            dcc.Dropdown(
                id='country-dropdown',
                multi=True,
                clearable=False,
                style={'margin-bottom': '30px'}
            ),

            dcc.RangeSlider(
                id='year-slider',
                min=int(df_coal['Year'].min()),
                max=int(df_coal['Year'].max()),
                value=[int(df_coal['Year'].min()), int(df_coal['Year'].max())],
                marks={str(year): str(year) for year in range(int(df_coal['Year'].min()), int(df_coal['Year'].max()) + 1, 5)},
                step=1,
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ], style={'width': '70%', 'margin': 'auto', 'padding': '30px 0'}),

        # Graph Grid 2x2
        html.Div([
            dcc.Graph(id='graph-1'),
            dcc.Graph(id='graph-2'),
            dcc.Graph(id='graph-3'),
            dcc.Graph(id='graph-4'),
        ], style={
            'display': 'grid',
            'gridTemplateColumns': '50% 50%',
            'gridGap': '15px',
            'padding': '10px 50px 50px 50px'
        }),
    ], id='main-content', style={'margin-left': '0', 'transition': 'margin-left 0.3s'})

])


# Sidebar Öffnen/Schließen
@app.callback(
    Output('sidebar', 'style'),
    Output('main-content', 'style'),
    Input('open-sidebar', 'n_clicks'),
    Input('close-sidebar', 'n_clicks'),
    State('sidebar', 'style'),
    State('main-content', 'style'),
)
def toggle_sidebar(open_clicks, close_clicks, sidebar_style, main_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return sidebar_style, main_style
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'open-sidebar':
        sidebar_style['left'] = '0'
    elif button_id == 'close-sidebar':
        sidebar_style['left'] = '-250px'
    return sidebar_style, main_style


# Länder Dropdown aktualisieren
@app.callback(
    Output('country-dropdown', 'options'),
    Output('country-dropdown', 'value'),
    Input('kontinent-dropdown', 'value'),
)
def update_countries(kontinente_auswahl):
    if not kontinente_auswahl:
        return [], []
    if isinstance(kontinente_auswahl, str):
        kontinente_auswahl = [kontinente_auswahl]
    länder = []
    for k in kontinente_auswahl:
        länder.extend(get_countries_by_continent(k))
    länder = sorted(set(länder))[:5]  # max 5 Länder
    options = [{'label': land, 'value': land} for land in länder]
    values = länder[:5] if länder else []
    return options, values


# Graphen und Slider aktualisieren
@app.callback(
    Output('graph-1', 'figure'),
    Output('graph-2', 'figure'),
    Output('graph-3', 'figure'),
    Output('graph-4', 'figure'),
    Output('year-slider', 'min'),
    Output('year-slider', 'max'),
    Output('year-slider', 'value'),
    Input('emission-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_graphs(emission_key, selected_countries, selected_years):
    if not emission_key or not selected_countries or not selected_years:
        return {}, {}, {}, {}, 0, 0, [0, 0]

    df = data_sources[emission_key]

    jahr_min, jahr_max = selected_years

    if isinstance(selected_countries, str):
        selected_countries = [selected_countries]

    df_filtered = df[
        (df['Entity'].isin(selected_countries)) &
        (df['Year'] >= jahr_min) &
        (df['Year'] <= jahr_max)
    ]

    value_col = df.columns[2]

    fig1 = px.line(df_filtered, x='Year', y=value_col, color='Entity',
                   title=f"Line Plot: {value_col}")

    fig2 = px.bar(df_filtered, x='Year', y=value_col, color='Entity',
                  title=f"Bar Plot: {value_col}")

    df_pie = df_filtered[df_filtered['Year'] == jahr_min]
    if not df_pie.empty:
        fig3 = px.pie(df_pie, names='Entity', values=value_col,
                      title=f"Pie Chart {jahr_min}: {value_col}")
    else:
        fig3 = {}

    fig4 = px.scatter(df_filtered, x='Year', y=value_col, color='Entity',
                      title=f"Scatter Plot: {value_col}")

    # Slider limits anpassen, falls Daten anders
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    slider_val = [max(jahr_min, min_year), min(jahr_max, max_year)]

    return fig1, fig2, fig3, fig4, min_year, max_year, slider_val


if __name__ == '__main__':
    app.run(debug=True)