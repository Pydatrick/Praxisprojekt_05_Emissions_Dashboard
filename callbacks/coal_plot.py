from app import app
from dash import Output, Input
import plotly.express as px
from pathlib import Path
from data.data_loader import load_data_annual


@app.callback(
    Output('coal-line-plot', 'figure'),
    Input('coal-entity-dropdown', 'value'),
    Input('coal-year-slider', 'value')
)
def update_graph(selected_entities, year_range):
    # Überprüfen, ob mindestens eine Auswahl da ist
    if not selected_entities:
        return px.line(title="Keine Auswahl")

    ROOT = Path(__file__).resolve().parent.parent
    PATHTOCSV = ROOT / 'data' / 'raw' / 'annual-co-emissions-from-coal.csv'
    df = load_data_annual(PATHTOCSV)

    min_year, max_year = year_range
    filtered_df = df[df['country'].isin(selected_entities) & (df['year'] >= min_year) & (df['year'] <= max_year)].copy()

    fig = px.line(
        filtered_df,
        x='year',
        y='value',
        color='country',  # Automatisch unterschiedliche Farben je Land
        title=f'CO₂-Emissionen aus Kohle: {", ".join(selected_entities)}',
        labels={'value': 'CO₂-Emissionen (Tonnen)', 'year' : 'Jahre', 'country' : 'Entität'}
    )

    fig.update_layout(legend_title_text="Entitäten")

    return fig