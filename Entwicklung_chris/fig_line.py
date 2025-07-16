import pandas as pd
import plotly.express as px

# Pfad zur CSV-Datei
base_path = r"C:\DataCraft\11_Datenvisualisierung\Projekt-Emission-Dashboard\data\raw"
file_name = "annual-co-emissions-from-coal.csv"
file_path = f"{base_path}\\{file_name}"

# CSV laden
df = pd.read_csv(file_path)

# Plot als Variable speichern (z. B. für Afghanistan)
fig_line = px.line(
    df[df['Entity'] == 'Afghanistan'],  # Nur Afghanistan filtern
    x='Year',
    y='Annual CO₂ emissions from coal',
    title='Jährliche CO₂-Emissionen aus Kohle (Afghanistan)',
    labels={'Annual CO₂ emissions from coal': 'CO₂-Emissionen (Tonnen)'}
)
