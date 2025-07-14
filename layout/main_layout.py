import pandas as pd
from dash import html, dcc
from dash import dcc, html, dash_table 
from pathlib import Path
from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name, country_name_to_country_alpha2

# from layout.header import header
# from layout.sidebar import sidebar

def create_layout():

    ROOT = Path(__file__).resolve().parent.parent
    DATA = ROOT / 'data'
    CSV_FILE_PATH = DATA / 'merged_final.csv'

    try:
        df = pd.read_csv(CSV_FILE_PATH)
        print("CSV-Datei erfolgreich geladen.")
    except FileNotFoundError:
        print(f"FEHLER2: Die Datei wurde unter '{CSV_FILE_PATH}' nicht gefunden. Bitte überprüfe den Pfad.")
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

    return html.Div([
        html.H1("CO₂ Emissions Dashboard", style={'textAlign': 'center'}),

        html.Div([
            html.Div([
                html.Label("Kontinent auswählen:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='continent-dropdown',
                    options=continent_options,
                    value='All',
                    clearable=False
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'margin-right': '4%'}),

            html.Div([
                html.Label("Länder auswählen (optional):", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[],
                    multi=True,
                    placeholder="Wähle ein oder mehrere Länder"
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),
        ], style={'padding': 10, 'display': 'flex'}),

        html.Div([
            html.Label("Emissions-Typ auswählen:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='emission-type-dropdown',
                options=[{'label': col, 'value': col} for col in emission_cols],
                value='Annual CO₂ emissions',
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
                marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1, 50)},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'padding': 10, 'margin-top': 20}),

        dcc.Graph(id='emission-graph', style={'height': '600px'}),

        html.Div([
            html.H3("Ausgewählte Daten (Tabelle)", style={'textAlign': 'center', 'marginTop': '30px'}),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                page_size=10,
                style_table={'overflowX': 'auto'}
            )
        ], style={'padding': 10, 'margin-top': 20})
    ])