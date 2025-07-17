from app import app
from dash import Output, Input
import plotly.express as px
from pathlib import Path
from data.data_loader import load_data_annual, get_countries, get_countries_by_group
from functions.set_color_map import generate_color_map

#callback continent/country
@app.callback(
    Output('landuse-entity-dropdown', 'options'),
    Input('landuse-preselection-dropdown', 'value'),
)
def update_countries(preselection):
    
    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-land-use-change.csv'
    country_list = get_countries(PATHTOCSV)

    if preselection:

        if isinstance(preselection, str):
            preselection = [preselection]

        return get_countries_by_group(country_list, preselection)
    
    else:
        return country_list

# callback land-use line plot
@app.callback(
    Output('landuse-line-plot', 'figure'),
    Input('landuse-entity-dropdown', 'value'),
    Input('landuse-year-slider', 'value')
)
def update_graph(selected_entities, year_range):
    # Überprüfen, ob mindestens eine Auswahl da ist
    if not selected_entities:
        return px.line(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-land-use-change.csv'
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
        title=f'CO₂-Emissionen aus Landnutzung: {", ".join(selected_entities)}',
        labels={'value': 'CO₂-Emissionen [t]', 'year' : 'Jahre', 'country' : 'Entität'}
    )

    fig.update_layout(legend_title_text="Entitäten")

    return fig

#callback land-use comulated bar plot
@app.callback(
    Output('landuse-bar-plot', 'figure'),
    Input('landuse-entity-dropdown', 'value'),
    Input('landuse-year-slider', 'value')
)
def update_bar_plot(selected_entities, year_range):
    if not selected_entities:
        return px.bar(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-land-use-change.csv'
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
        labels={"value": "CO₂-Emissionen [t]", "country": ""},
        title="Kumulierte Emissionen über gewählten Zeitraum"
    )

    fig.update_layout(xaxis_tickangle=-45, legend_title_text="Entitäten")

    return fig

# callback land use map
@app.callback(
    Output("landuse-map", "figure"),
    Input("landuse-year-slider", "value"),
    Input("landuse-entity-dropdown", "value")
)
def update_landuse_map(year_range, selected_countries):
    if not selected_countries:
        return px.choropleth(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-land-use-change.csv'
    df = load_data_annual(PATHTOCSV)

    start_year, end_year = year_range

    filtered_df = df[
        (df["country"].isin(selected_countries)) &
        (df["year"] >= start_year) &
        (df["year"] <= end_year)
    ]

    summed_df = filtered_df.groupby("country", as_index=False)["value"].sum()

    fig = px.choropleth(
        summed_df,
        locations="country",
        locationmode="country names",
        color="value",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Tealgrn,
        labels={"value": "Emissionen", "country": "Entität"},
        title=f"Kumulierte CO₂-Emissionen von {start_year} bis {end_year} (nur ausgewählte Länder)",
        # width=900,  # Breite in Pixel
        # height=600  # Höhe in Pixel
    )
    fig.update_geos(
        projection_type="natural earth",
        showland=True, landcolor="lightgray",
        showocean=True, oceancolor="lightblue",
        showlakes=True, lakecolor="lightblue",
        showrivers=False,
        showcoastlines=True, coastlinecolor="gray",
        fitbounds="locations"
    )
    fig.update_layout(
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        paper_bgcolor="white",
        geo_bgcolor="rgba(0,0,0,0)",
        title_font_size=20
    )
    return fig