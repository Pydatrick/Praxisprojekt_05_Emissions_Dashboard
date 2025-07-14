import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table # <<< HIER WURDE 'dash_table' HINZUGEFÜGT
from pathlib import Path
from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name, country_name_to_country_alpha2

# --- 1. Daten laden und vorbereiten ---
# Dein angegebener Pfad zur merged_final.csv
CSV_FILE_PATH = Path(r"C:\Users\Admin\Desktop\Vorlesungen\1.11 Datenvisualisierung mit Python\20250714 Projekt\Projekt-Emission-Dashboard\data\merged_final.csv")

try:
    df = pd.read_csv(CSV_FILE_PATH)
    print("CSV-Datei erfolgreich geladen.")
except FileNotFoundError:
    print(f"FEHLER: Die Datei wurde unter '{CSV_FILE_PATH}' nicht gefunden. Bitte überprüfe den Pfad.")
    exit() # Beendet das Skript, wenn die Datei nicht gefunden wird

# Liste der bekannten Kontinente (aus deiner bereitgestellten Liste von Entities)
# Diese werden als separate Kontinent-Filteroptionen behandelt.
KNOWN_CONTINENTS = [
    'Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'
]

# Liste von Aggregaten/Regionen, die wir nicht als einzelne Länder behandeln möchten
# und die bei der Kontinentfilterung ignoriert werden sollen.
AGGREGATE_REGIONS = [
    'World', 'European Union (27)', 'European Union (28)', 'High-income countries',
    'Low-income countries', 'Lower-middle-income countries', 'Upper-middle-income countries',
    'International aviation', 'International shipping', 'Least developed countries (Jones et al.)',
    'Non-OECD (GCP)', 'OECD (GCP)', 'OECD (Jones et al.)', 'Central America (GCP)',
    'Middle East (GCP)', 'Ryukyu Islands (GCP)', 'Kuwaiti Oil Fires (GCP)',
    'Africa (GCP)', 'Asia (GCP)', 'Europe (GCP)', 'North America (GCP)', 'Oceania (GCP)', 'South America (GCP)',
    'Asia (excl. China and India)', 'Europe (excl. EU-27)', 'Europe (excl. EU-28)',
    'Christmas Island', 'Cocos Islands', 'Cook Islands', 'Falkland Islands', 'Faroe Islands',
    'French Polynesia', 'Gibraltar', 'Greenland', 'Guam', 'Guernsey', 'Hong Kong',
    'Isle of Man', 'Jersey', 'Kiribati', 'Macao', 'Malta', 'Marshall Islands',
    'Micronesia (country)', 'Monaco', 'Montserrat', 'Nauru', 'New Caledonia', 'Niue',
    'Norfolk Island', 'Northern Mariana Islands', 'Palau', 'Palestine', 'Pitcairn',
    'Puerto Rico', 'Ryukyu Islands', 'Saint Helena', 'Saint Pierre and Miquelon',
    'San Marino', 'Sint Maarten (Dutch part)', 'Solomon Islands', 'Timor', 'Tokelau',
    'Tonga', 'Tuvalu', 'Vatican', 'Wallis and Futuna', 'Western Sahara', 'Bermuda',
    'British Virgin Islands', 'Bonaire Sint Eustatius and Saba', 'Curacao', 'Sint Maarten (Dutch part)',
    'Turks and Caicos Islands', 'United States Virgin Islands', # Weitere spezifische Gebiete, die oft nicht zu einem Kontinent zugeordnet werden oder Regionen sind
    'Kuwaiti Oil Fires' # Separate von (GCP) Version
]

def get_continent_for_entity(entity_name):
    """Versucht, den Kontinent für eine gegebene Entität zu ermitteln."""
    # 1. Bekannte Kontinente direkt zuordnen
    if entity_name in KNOWN_CONTINENTS:
        return entity_name
    # 2. Aggregate/Regionen markieren
    if entity_name in AGGREGATE_REGIONS or "(GCP)" in entity_name or "excl." in entity_name or "income countries" in entity_name:
        return "Aggregate / Region" # Eine spezielle Kategorie für Aggregationen
    # 3. Länder zuordnen
    try:
        # Versuche, den Ländercode (Alpha-2) zu bekommen
        country_code = country_name_to_country_alpha2(entity_name, cn_name_format="DEFAULT")
        # Wandle den Ländercode in den Kontinentcode um
        continent_code = country_alpha2_to_continent_code(country_code)
        # Wandle den Kontinentcode in den Kontinentnamen um
        continent_name = convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except KeyError:
        # Falls das Land nicht gefunden wird oder es eine unbekannte Region ist
        return "Unbekannt / Andere"

# Wende die Funktion an, um die neue 'Continent'-Spalte zu erstellen
df['Continent'] = df['Entity'].apply(get_continent_for_entity)

# Filtere Daten, um nur Länder und echte Kontinente (nicht Aggregate) zu behalten für die Auswahl
# Dies stellt sicher, dass Dropdowns nur sinnvolle Einträge enthalten
valid_entities_df = df[~df['Continent'].isin(["Aggregate / Region", "Unbekannt / Andere"])].copy()

# Hole alle einzigartigen Kontinente für das Dropdown
all_continents = sorted(valid_entities_df['Continent'].unique().tolist())
# Füge "Alle Kontinente" als Option hinzu
continent_options = [{'label': 'Alle Kontinente', 'value': 'All'}] + [{'label': c, 'value': c} for c in all_continents]

# Emissionsspalten identifizieren (alle, die mit 'Annual CO₂ emissions' beginnen, außer 'Annual CO₂ emissions including land-use change')
emission_cols = [
    col for col in df.columns
    if 'Annual CO₂ emissions' in col and
       'Annual CO₂ emissions including land-use change' not in col and
       'Annual CO₂ emissions (per capita)' not in col # Falls Per Capita separat ist
]
# Füge 'Annual CO₂ emissions' (Gesamt) explizit hinzu, falls es nicht erfasst wurde
if 'Annual CO₂ emissions' not in emission_cols:
    emission_cols.append('Annual CO₂ emissions')
# Füge auch die Per-Capita-Werte hinzu, wenn sie visualisiert werden sollen
emission_cols.append('Annual CO₂ emissions (per capita)')
emission_cols.append('Per capita greenhouse gas emissions in CO₂ equivalents')
emission_cols.append('Per capita methane emissions in CO₂ equivalents')
emission_cols.append('Per capita nitrous oxide emissions in CO₂ equivalents')


# --- 2. Dash App initialisieren ---
app = Dash(__name__)

# --- 3. Layout der App definieren ---
app.layout = html.Div([
    html.H1("CO₂ Emissions Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Label("Kontinent auswählen:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='continent-dropdown',
                options=continent_options,
                value='All', # Standardwert
                clearable=False
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'margin-right': '4%'}),

        html.Div([
            html.Label("Länder auswählen (optional):", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[], # Wird dynamisch gefüllt
                multi=True, # Mehrfachauswahl erlauben
                placeholder="Wähle ein oder mehrere Länder"
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'padding': 10, 'display': 'flex'}),

    html.Div([
        html.Label("Emissions-Typ auswählen:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='emission-type-dropdown',
            options=[{'label': col, 'value': col} for col in emission_cols],
            value='Annual CO₂ emissions', # Standardwert
            clearable=False
        ),
    ], style={'padding': 10}),

    html.Div([
        html.Label("Jahresbereich auswählen:", style={'fontWeight': 'bold'}),
        dcc.RangeSlider(
            id='year-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=[df['Year'].min(), df['Year'].max()],
            marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max()+1, 50)}, # Alle 50 Jahre
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    ], style={'padding': 10, 'margin-top': 20}),

    dcc.Graph(id='emission-graph', style={'height': '600px'}),

    html.Div([
        html.H3("Ausgewählte Daten (Tabelle)", style={'textAlign': 'center', 'marginTop': '30px'}),
        dash_table.DataTable( # <<< HIER WIRD dash_table VERWENDET
            id='data-table',
            columns=[{"name": i, "id": i} for i in df.columns], # Alle Spalten anzeigen
            page_size=10, # 10 Zeilen pro Seite
            style_table={'overflowX': 'auto'}
        )
    ], style={'padding': 10, 'margin-top': 20})
])


# --- 4. Callbacks für Interaktivität ---

# Callback zur Aktualisierung des Länder-Dropdowns basierend auf der Kontinent-Auswahl
@app.callback(
    Output('country-dropdown', 'options'),
    Input('continent-dropdown', 'value')
)
def set_countries_options(selected_continent):
    dff = df[~df['Continent'].isin(["Aggregate / Region", "Unbekannt / Andere"])].copy() # Nur echte Länder/Kontinente

    if selected_continent == 'All':
        countries_in_continent = sorted(dff['Entity'].unique().tolist())
    else:
        # Filter nach ausgewähltem Kontinent
        dff_continent = dff[dff['Continent'] == selected_continent]
        # Filtern Sie hier auch die Kontinentsnamen selbst aus, um nur Länder zu zeigen
        countries_in_continent = sorted([
            entity for entity in dff_continent['Entity'].unique().tolist()
            if entity not in KNOWN_CONTINENTS # Stelle sicher, dass Kontinentnamen nicht in der Länderliste erscheinen
        ])

    return [{'label': country, 'value': country} for country in countries_in_continent]

# Callback zur Aktualisierung des Graphen und der Tabelle
@app.callback(
    Output('emission-graph', 'figure'),
    Output('data-table', 'data'),
    Input('continent-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('emission-type-dropdown', 'value')
)
def update_graph(selected_continent, selected_countries, year_range, emission_type):
    min_year, max_year = year_range

    # Filtern nach Jahresbereich
    filtered_df = df[(df['Year'] >= min_year) & (df['Year'] <= max_year)].copy()

    # Filtern nach Kontinent und/oder Land
    if selected_continent == 'All':
        # Wenn "Alle Kontinente" gewählt ist, zeige standardmäßig alle echten Länder
        # Aber nicht die Aggregat-Regionen
        filtered_df = filtered_df[~filtered_df['Continent'].isin(["Aggregate / Region", "Unbekannt / Andere"])]
    else:
        # Wenn ein spezifischer Kontinent gewählt ist, filtere danach
        filtered_df = filtered_df[filtered_df['Continent'] == selected_continent]
        # Und wenn dieser Kontinent auch als Entity existiert, nimm ihn auch auf, falls keine Länder gewählt sind
        # (Dies ist wichtig, da einige Entitäten sowohl Kontinent als auch Land sein können, aber hier explizit getrennt werden)
        # Wenn der ausgewählte Kontinent selbst eine Entity ist, stelle sicher, dass er nicht gefiltert wird, wenn Länder ausgewählt werden.

    # Wenn spezifische Länder ausgewählt wurden, überschreibe die Kontinent-Filterung für diese Länder
    if selected_countries:
        # Sicherstellen, dass nur die ausgewählten Länder angezeigt werden
        filtered_df = filtered_df[filtered_df['Entity'].isin(selected_countries)]
    else:
        # Wenn keine spezifischen Länder ausgewählt sind, aber ein Kontinent,
        # dann zeige alle Länder dieses Kontinents, aber NICHT den Kontinent als Entity selbst
        # (es sei denn, der Kontinent ist die einzige Auswahl)
        if selected_continent != 'All':
            filtered_df = filtered_df[~filtered_df['Entity'].isin(KNOWN_CONTINENTS + AGGREGATE_REGIONS)]


    # Sortiere die Daten für das Diagramm
    filtered_df = filtered_df.sort_values(by=['Year', 'Entity'])

    # Sicherstellen, dass der Emissionstyp numerisch ist und NaN Werte handhaben
    # Plotly kann NaN handhaben, aber es ist gut, dies zu wissen.
    # Eventuell die Daten vor dem Plotten in einen numerischen Typ umwandeln
    filtered_df[emission_type] = pd.to_numeric(filtered_df[emission_type], errors='coerce')


    # Diagramm erstellen
    fig = px.line(
        filtered_df,
        x='Year',
        y=emission_type,
        color='Entity', # Zeigt verschiedene Linien für verschiedene Entitäten
        title=f'{emission_type} by Entity ({min_year}-{max_year})',
        labels={'Year': 'Jahr', emission_type: emission_type, 'Entity': 'Entität'},
        hover_name='Entity', # Zeigt den Entitätsnamen beim Hovern an
        line_shape="linear" # Verbindet Punkte mit geraden Linien
    )
    fig.update_layout(transition_duration=500) # Sanfter Übergang bei Updates

    # Daten für die Tabelle (nur relevante Spalten für die Anzeige)
    table_data = filtered_df[['Entity', 'Year', 'Continent', emission_type]].to_dict('records')

    return fig, table_data

# --- 5. App starten ---
if __name__ == '__main__':
    # Standardmäßig wird die App auf http://127.0.0.1:8050/ gestartet
    app.run(debug=True)