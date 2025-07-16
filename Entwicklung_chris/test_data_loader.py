import pandas as pd
import os

# Beispiel-Daten für Demonstrationszwecke
# Erstellen Sie Dummy-DataFrames, die echten CSV-Daten ähneln könnten
def create_dummy_dataframe(name, start_year=1800, end_year=2030):
    years = list(range(start_year, end_year + 1))
    # Simulieren Sie unterschiedliche Emissionsmuster
    if name == "Öl Emissionen":
        emissions = [1000 + i * 10 + (i % 5) * 50 for i in range(len(years))]
    elif name == "Gas Emissionen":
        emissions = [500 + i * 20 - (i % 3) * 30 for i in range(len(years))]
    elif name == "Kohle Emissionen":
        emissions = [1500 - i * 15 + (i % 4) * 20 for i in range(len(years))]
    else: # Für andere generische Daten
        emissions = [700 + i * 5 + (i % 7) * 10 for i in range(len(years))]

    return pd.DataFrame({
        'Jahr': years,
        'Emissionen': emissions,
        'Quelle': name
    })

# Pfad zu deinen CSV-Dateien - DEFINIERE DIESEN unbedingt!

# Pfad zu CSV-Ordner anpassen
import os
import pandas as pd
from kontinente_laender_liste import country_to_continent_map

# Pfad zum Ordner mit den CSV-Dateien
csv_ordner = r"C:\DataCraft\11_Datenvisualisierung\Projekt-Emission-Dashboard\data\raw"

# Wörterbuch für alle geladenen DataFrames
data_sources = {}

# Einheitliche Spaltennamen
def clean_columns(df):
    rename_map = {
        'Entity': 'Country',
        'Country': 'Country',
        'Year': 'Year',
        'Annual CO₂ emissions from coal': 'CO2_Coal_Emissions',
        'Annual CO₂ emissions from oil': 'CO2_Oil_Emissions',
        'Annual CO₂ emissions from gas': 'CO2_Gas_Emissions',
        # Weitere Emissionstypen ggf. ergänzen
    }
    cols_to_rename = {k: v for k, v in rename_map.items() if k in df.columns}
    return df.rename(columns=cols_to_rename)

# CSV-Dateien laden
for dateiname in os.listdir(csv_ordner):
    if dateiname.endswith(".csv"):
        dateipfad = os.path.join(csv_ordner, dateiname)
        try:
            df = pd.read_csv(dateipfad)
            df = clean_columns(df)

            # Nur Länder behalten, die im Mapping sind
            df = df[df['Country'].isin(country_to_continent_map.keys())]

            # Jahreszahlen als Zahl formatieren
            if 'Year' in df.columns:
                df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

            # CO₂-Werte in numerische Werte umwandeln
            for col in ['CO2_Coal_Emissions', 'CO2_Oil_Emissions', 'CO2_Gas_Emissions']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Nur gültige Einträge behalten
            critical_cols = ['Country', 'Year']
            critical_cols += [c for c in ['CO2_Coal_Emissions', 'CO2_Oil_Emissions', 'CO2_Gas_Emissions'] if c in df.columns]
            df.dropna(subset=critical_cols, inplace=True)

            # In die Datenquelle einfügen
            key = os.path.splitext(dateiname)[0]
            data_sources[key] = df

        except Exception as e:
            print(f"Fehler beim Laden von {dateiname}: {e}")

# Optional: Eine Funktion, um die Spaltennamen anzupassen oder Daten zu bereinigen,
# falls Ihre CSVs unterschiedliche Formate haben.
# def preprocess_dataframe(df, source_name):
#     # Beispiel: Sicherstellen, dass 'Jahr' und 'Emissionen' Spalten existieren
#     # und ggf. umbenennen
#     if 'Year' in df.columns:
#         df = df.rename(columns={'Year': 'Jahr'})
#     if 'CO2_Emissions' in df.columns:
#         df = df.rename(columns={'CO2_Emissions': 'Emissionen'})
#     df['Quelle'] = source_name # Eine Spalte für die Quelle hinzufügen
#     return df

# # Wenn Sie die Preprocessing-Funktion verwenden möchten, würden Sie data_sources so laden:
# data_sources_processed = {
#     key: preprocess_dataframe(pd.read_csv(path), key)
#     for key, path in {
#         "Öl Emissionen (annual-co-emissions-from-oil_copy.csv)": "C:/DataCraft/11 Datenvisualisierung/Projekt-Emission-Dashboard/Entwicklung_chris/annual-co-emissions-from-oil_copy.csv",
#         "Gas Emissionen (annual-co-emissions-from-gas.csv)": "C:/DataCraft/11 Datenvisualisierung/Projekt-Emission-Dashboard/Entwicklung_chris/annual-co-emissions-from-gas.csv",
#         "Kohle Emissionen (annual-co-emissions-from-coal.csv)": "C:/DataCraft/11 Datenvisualisierung/Projekt-Emission-Dashboard/Entwicklung_chris/annual-co-emissions-from-coal.csv",
#         # ... weitere Dateien mit ihren Pfaden
#     }.items()
# }
# data_sources = data_sources_processed # Dann diese Zeile verwenden
