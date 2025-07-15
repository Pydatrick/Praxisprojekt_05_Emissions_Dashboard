import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os # Nützlich, um Dateinamen zu extrahieren oder mit Pfaden zu arbeiten

# --- 1. Datenbereitstellung (Ihr Projektmitglied Daten) ---
# Importieren der Datenquellen aus der separaten Datei data_loader.py
from data_loader import data_sources

# --- Dash App Initialisierung ---
app = dash.Dash(__name__)

# --- 2. Dashboard Layout (Ihre Blanko Dashboardseite) ---
app.layout = html.Div(className="container mx-auto p-4", children=[
    html.H1(
        id='dashboard-title',
        className="text-4xl font-extrabold text-gray-800 mb-8 text-center",
        children="Dynamisches Emissions-Dashboard"
    ),

    html.Div(className="mb-6 flex flex-col sm:flex-row items-center justify-center gap-4", children=[
        html.Label("Datenquelle auswählen:", className="text-lg font-semibold text-gray-700"),
        dcc.Dropdown(
            id='data-source-selector',
            options=[
                {'label': key, 'value': key} for key in data_sources.keys()
            ],
            value=list(data_sources.keys())[0], # Standardauswahl: die erste Quelle
            clearable=False,
            className="flex-grow p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700 w-full sm:w-auto"
        )
    ]),

    # Platzhalter für den Zeitstrahl (dcc.RangeSlider)
    html.Div(className="mb-6", children=[
        html.Label("Zeitbereich auswählen:", className="text-lg font-semibold text-gray-700"),
        dcc.RangeSlider(
            id='year-slider',
            min=2000,       # aus der csv holen
            max=2025,
            step=1,
            value=[2000, 2025], # Standardbereich
            marks={i: str(i) for i in range(2000, 2026, 5)},
            className="mt-2"
        )
    ]),

    # Platzhalter für die Sidebar (könnte weitere Filter oder Infos enthalten)
    html.Div(className="flex flex-col lg:flex-row gap-4", children=[
        html.Div(className="lg:w-1/4 p-4 bg-gray-50 rounded-lg shadow-inner", children=[
            html.H2("Sidebar", className="text-2xl font-bold text-gray-700 mb-4"),
            html.P("Hier könnten weitere Filter, Legenden oder Informationen platziert werden.", className="text-gray-600")
        ]),
        # Hauptbereich für die Grafik
        html.Div(className="lg:w-3/4 bg-white p-6 rounded-lg shadow-md", children=[
            dcc.Graph(
                id='main-graph',
                className="w-full h-96" # Stellt sicher, dass die Grafik den verfügbaren Platz nutzt
            )
        ])
    ]),

    html.Div(className="mt-8 text-center text-gray-600 text-sm", children=[
        html.P("Dieses Dashboard demonstriert die dynamische Auswahl von Datenquellen und Grafiken."),
        html.P("Die Daten sind beispielhaft und dienen nur zu Demonstrationszwecken.")
    ])
])

# --- 3. Rückrufe (Callbacks) ---
# Dieser Callback aktualisiert die Grafik basierend auf der Auswahl der Datenquelle
@app.callback(
    Output('main-graph', 'figure'),
    Output('dashboard-title', 'children'), # Aktualisiert auch die Überschrift
    Input('data-source-selector', 'value'),
    Input('year-slider', 'value')
)
def update_graph_and_title(selected_source_key, selected_years):
    # --- 4. Grafik-Erstellung (Ihr Projektmitglied Grafiken) ---
    if selected_source_key not in data_sources:
        # Fallback, falls der Schlüssel nicht gefunden wird (sollte nicht passieren bei Dropdown)
        return px.scatter(title="Datenquelle nicht gefunden"), "Fehler: Datenquelle nicht gefunden"

    df_selected = data_sources[selected_source_key]

    # Filtern der Daten basierend auf dem Zeitstrahl
    filtered_df = df_selected[
        (df_selected['Year'] >= selected_years[0]) &
        (df_selected['Year'] <= selected_years[1])
    ]

    # Erstellen der Grafik 1
    # Hier könnten Sie je nach Quelle unterschiedliche Diagrammtypen wählen
    fig = px.line(
        filtered_df,
        # von hier an einen Platzhalter schaffen für die Grafiken
        x='Year',
        y=filtered_df.columns[2],
        # bis hier
        title=f'{selected_source_key} über die Jahre',
        labels={'Year': 'Year', filtered_df.columns[2]: filtered_df.columns[2]}
    )
    fig.update_layout(transition_duration=500) # Sanfte Übergänge beim Aktualisieren

    # Aktualisieren der Hauptüberschrift basierend auf der Auswahl
    new_title = f"Dashboard: {selected_source_key}"

    return fig, new_title

# Erstellen der Grafik 2
    # Hier könnten Sie je nach Quelle unterschiedliche Diagrammtypen wählen
    fig = px.line(
        filtered_df,
        # von hier an einen Platzhalter schaffen für die Grafiken
        x='Year',
        y=filtered_df.columns[2],
        # bis hier
        title=f'{selected_source_key} über die Jahre',
        labels={'Year': 'Year', filtered_df.columns[2]: filtered_df.columns[2]}
    )
    fig.update_layout(transition_duration=500) # Sanfte Übergänge beim Aktualisieren

    # Aktualisieren der Hauptüberschrift basierend auf der Auswahl
    new_title = f"Dashboard: {selected_source_key}"

    return fig, new_title





# --- App starten ---
if __name__ == '__main__':
    app.run(debug=True)