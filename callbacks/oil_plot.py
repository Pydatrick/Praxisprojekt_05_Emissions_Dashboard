from app import app
from dash import Output, Input
import plotly.express as px
from pathlib import Path
from data.data_loader import load_data_annual, get_countries, get_countries_by_group
from functions.set_color_map import generate_color_map

#callback continent/country
@app.callback(
    Output('oil-entity-dropdown', 'options'),
    Input('oil-preselection-dropdown', 'value'),
)
def update_countries(preselection):
    
    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-oil.csv'
    country_list = get_countries(PATHTOCSV)

    if preselection:

        if isinstance(preselection, str):
            preselection = [preselection]

        return get_countries_by_group(country_list, preselection)
    
    else:
        return country_list

# callback oil line plot
@app.callback(
    Output('oil-line-plot', 'figure'),
    Input('oil-entity-dropdown', 'value'),
    Input('oil-year-slider', 'value')
)
def update_graph(selected_entities, year_range):
    # Überprüfen, ob mindestens eine Auswahl da ist
    if not selected_entities:
        return px.line(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-oil.csv'
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
        title=f'CO₂-Emissionen aus Oil: {", ".join(selected_entities)}',
        labels={'value': 'CO₂-Emissionen (Tonnen)', 'year' : 'Jahre', 'country' : 'Entität'}
    )

    fig.update_layout(legend_title_text="Entitäten")

    return fig

#callback oil comulated bar plot
@app.callback(
    Output('oil-bar-plot', 'figure'),
    Input('oil-entity-dropdown', 'value'),
    Input('oil-year-slider', 'value')
)
def update_bar_plot(selected_entities, year_range):
    if not selected_entities:
        return px.bar(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-oil.csv'
    df = load_data_annual(PATHTOCSV)

    min_year, max_year = year_range
    df_filtered = df[df["country"].isin(selected_entities) & (df["year"].between(min_year, max_year))]

    df_grouped = (
        df_filtered.groupby("country")["value"]
        .sum()
        .reset_index()
        .sort_values(by="value", ascending=False)
    )

    # color map
    color_map = generate_color_map(selected_entities)

    fig = px.bar(
        df_grouped,
        x="country",
        y="value",
        color = 'country',
        color_discrete_map=color_map,
        labels={"value": "Gesamtemissionen", "country": ""},
        title="Kumulierte Emissionen über gewählten Zeitraum"
    )

    fig.update_layout(xaxis_tickangle=-45)

    return fig
