import pandas as pd
import os
from laender import get_unique_countries  # Dein externes Skript mit der Funktion



# Pfad zum Ordner mit den CSV-Dateien
csv_ordner = r"C:\DataCraft\11_Datenvisualisierung\Projekt-Emission-Dashboard\data\raw"

data_sources = {}  # Muss vor Nutzung initialisiert sein

def clean_columns(df):
    rename_map = {
        'Entity': 'Country',
        'Year': 'Year',
        'Annual CO₂ emissions from coal': 'CO2_Coal_Emissions',
        'Annual CO₂ emissions from oil': 'CO2_Oil_Emissions',
        'Annual CO₂ emissions from gas': 'CO2_Gas_Emissions',
        # Weitere Spalten hier ergänzen falls nötig
    }
    cols_to_rename = {k:v for k,v in rename_map.items() if k in df.columns}
    return df.rename(columns=cols_to_rename)

# 1) Lade alle CSVs in data_sources dict
for dateiname in os.listdir(csv_ordner):
    if dateiname.endswith(".csv"):
        dateipfad = os.path.join(csv_ordner, dateiname)
        df = pd.read_csv(dateipfad)
        df = clean_columns(df)

        # Konvertiere wichtige Spalten in numerisch (falls vorhanden)
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        for col in ['CO2_Coal_Emissions', 'CO2_Oil_Emissions', 'CO2_Gas_Emissions']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        critical_cols = ['Country', 'Year']
        critical_cols += [c for c in ['CO2_Coal_Emissions', 'CO2_Oil_Emissions', 'CO2_Gas_Emissions'] if c in df.columns]
        df.dropna(subset=critical_cols, inplace=True)

        key = os.path.splitext(dateiname)[0]
        data_sources[key] = df

def get_all_unique_countries(data_sources):
    countries = set()
    for df in data_sources.values():
        countries.update(df['Country'].unique())
    return sorted(countries)

# 2) Nun alle Länder aus allen CSVs holen
all_countries = get_all_unique_countries(data_sources)
print(f"Länder in allen CSVs: {len(all_countries)}")

# 3) Optional: Beispiel, wie du Länder aus einer repräsentativen CSV liest
repr_csv = None
for fname in os.listdir(csv_ordner):
    if fname.endswith(".csv"):
        repr_csv = os.path.join(csv_ordner, fname)
        break

if repr_csv:
    countries_in_data = get_unique_countries(repr_csv)
else:
    countries_in_data = []

print(f"Länder in der CSV-Datenquelle (repräsentative Datei): {len(countries_in_data)} Länder gefunden.")