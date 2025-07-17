from app import app
from dash import Output, Input
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from data.data_loader import load_data_annual, get_countries, get_countries_by_group
from functions.set_color_map import generate_color_map
import pandas as pd

#callback continent/country
@app.callback(
    Output('total-entity-dropdown', 'options'),
    Input('total-preselection-dropdown', 'value'),
)
def update_countries(preselection):
    
    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions.csv'
    country_list = get_countries(PATHTOCSV)

    if preselection:

        if isinstance(preselection, str):
            preselection = [preselection]

        return get_countries_by_group(country_list, preselection)
    
    else:
        return country_list

# callback total line plot
@app.callback(
    Output('total-emission-line-plot', 'figure'),
    Input('total-entity-dropdown', 'value'),
    Input('total-year-slider', 'value')
)
def update_graph(selected_entities, year_range):
    # Überprüfen, ob mindestens eine Auswahl da ist
    if not selected_entities:
        return px.line(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions.csv'
    df = load_data_annual(PATHTOCSV)

    min_year, max_year = year_range
    filtered_df = df[df['country'].isin(selected_entities) & (df['year'] >= min_year) & (df['year'] <= max_year)].copy()

    # color map
    color_map = generate_color_map(selected_entities)

    fig = px.line(
        filtered_df,
        x='year',
        y='value',
        color='country',
        color_discrete_map=color_map,
        title=f'CO₂-Emissionen (Fossile) [t]: {", ".join(selected_entities)}',
        labels={'value': 'CO₂-Emissionen (Tonnen)', 'year' : 'Jahre', 'country' : 'Entität'}
    )

    fig.update_layout(legend_title_text="Entitäten")

    return fig

#callback contribute line plot
@app.callback(
    Output('total-contribution-line-plot', 'figure'),
    Input('total-entity-dropdown', 'value'),
    Input('total-year-slider', 'value')
)
def update_bar_plot(selected_entities, year_range):
    if not selected_entities:
        return px.bar(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'contribution-to-global-mean-surface-temperature-rise-from-fossil-sources.csv'
    df = load_data_annual(PATHTOCSV)

    min_year, max_year = year_range
    df_filtered = df[df["country"].isin(selected_entities) & (df["year"].between(min_year, max_year))]

    # color map
    color_map = generate_color_map(selected_entities)

    fig = px.line(
        df_filtered,
        x='year',
        y='value',
        color='country',
        color_discrete_map=color_map,
        title=f'Beitrag zur Erderwärmung: {", ".join(selected_entities)}',
        labels={'value': 'Beitrag zur Erderwärmung [C°]', 'year' : 'Jahre', 'country' : 'Entität'}
    )

    fig.update_layout(legend_title_text="Entitäten")

    return fig

#callback temperature line plot
@app.callback(
    Output('temperature-line-plot', 'figure'),
    Input('total-year-slider', 'value')
)
def update_bar_plot(year_range):

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'temperature-anomaly' / 'temperature-anomaly.csv'
    df = pd.read_csv(PATHTOCSV)

    df = df.rename(columns={
    "Global average temperature anomaly relative to 1961-1990": "anomaly",
    "Upper bound of the annual temperature anomaly (95% confidence interval)": "upper",
    "Lower bound of the annual temperature anomaly (95% confidence interval)": "lower",
    'Year' : 'year'
    })

    min_year, max_year = year_range
    df_filtered = df[(df["Entity"] == "Global") & (df["year"].between(min_year, max_year))].copy()

    fig = go.Figure()

    # 1. Untere Grenze (für Füllfläche – startet hier)
    fig.add_trace(go.Scatter(
        x=df_filtered["year"],
        y=df_filtered["lower"],
        line=dict(color='rgba(255, 0, 0, 0)'),  # Transparent
        name='95% Konfidenzintervall',
        showlegend=True
    ))

    # 2. Obere Grenze (endet hier, Füllung von "tonexty")
    fig.add_trace(go.Scatter(
        x=df_filtered["year"],
        y=df_filtered["upper"],
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.2)',  # Rote transparente Fläche
        line=dict(color='rgba(255, 0, 0, 0)'),
        name=None,
        showlegend=False
    ))

    # 3. Mittelwert
    fig.add_trace(go.Scatter(
        x=df_filtered["year"],
        y=df_filtered["anomaly"],
        line=dict(color='crimson', width=2),
        name='Temperatur-Anomalie'
    ))

    fig.update_layout(
        title="Globale Temperatur-Anomalie (mit 95 %-Konfidenzintervall)",
        xaxis_title="Jahr",
        yaxis_title="Temperaturabweichung [°C]",
        legend_title="Legende",
        template="plotly"
    )

    return fig
