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

# Laden der "Datenquellen" in ein Dictionary
# Die Schlüssel des Dictionaries werden später die Optionen im Dropdown sein
# In einer echten Anwendung würden Sie hier pd.read_csv verwenden
# und die tatsächlichen Pfade zu Ihren CSV-Dateien angeben.
data_sources = {
    "öl_emissionen": pd.read_csv("C:/DataCraft/11 Datenvisualisierung/Projekt-Emission-Dashboard/data/raw/annual-co-emissions-from-coal.csv"),
    "gas_emissionen": pd.read_csv("C:/DataCraft/11 Datenvisualisierung/Projekt-Emission-Dashboard/data/raw/annual-co-emissions-from-gas.csv"),
    "kohle_emissionen": pd.read_csv("C:/DataCraft/11 Datenvisualisierung/Projekt-Emission-Dashboard/data/raw/annual-co-emissions-from-oil.csv"),
    # ... und so weiter für Ihre 10 CSVs
}

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