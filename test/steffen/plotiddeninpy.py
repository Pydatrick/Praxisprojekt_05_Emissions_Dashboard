import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Daten laden
file_path = r"C:\Users\Admin\Desktop\Vorlesungen\1.11 Datenvisualisierung mit Python\20250714 Projekt\Projekt-Emission-Dashboard\data\raw\annual-co-emissions-from-coal.csv"
df = pd.read_csv(file_path)

entities = sorted(df['Entity'].unique())

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("CO₂-Emissionen aus Kohle nach Ländern"),
    
    dcc.Dropdown(
        id='entity-dropdown',
        options=[{'label': entity, 'value': entity} for entity in entities],
        value=[entities[0]],  # Liste! → wegen multi=True
        multi=True,
        searchable=True,
        clearable=False
    ),
    
    dcc.Graph(id='line-plot')
])

@app.callback(
    Output('line-plot', 'figure'),
    Input('entity-dropdown', 'value')
)
def update_graph(selected_entities):
    # Überprüfen, ob mindestens eine Auswahl da ist
    if not selected_entities:
        return px.line(title="Keine Auswahl")

    filtered_df = df[df['Entity'].isin(selected_entities)]
    fig = px.line(
        filtered_df,
        x='Year',
        y='Annual CO₂ emissions from coal',
        color='Entity',  # Automatisch unterschiedliche Farben je Land
        title=f'CO₂-Emissionen aus Kohle: {", ".join(selected_entities)}',
        labels={'Annual CO₂ emissions from coal': 'CO₂-Emissionen (Tonnen)'}
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
