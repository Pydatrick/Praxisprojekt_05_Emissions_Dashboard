import pandas as pd
import numpy as np
from pandas import DataFrame
import csv

eingabe_datei = r'11 Datenvisualisierung/Projekt-Emission-Dashboard/data/raw/annual-co-emissions-from-oil.csv'
ausgabe_datei = r'11 Datenvisualisierung/Projekt-Emission-Dashboard/Entwicklung_chris/annual-co-emissions-from-oil_copy.csv'

def schreibe_csv_neu(eingabe_datei, ausgabe_datei):
    try:
        with open(eingabe_datei, "r", newline="", encoding="utf-8") as infile, \
             open(ausgabe_datei, "w", newline="", encoding="utf-8") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow(row)
                print(f"Die Datei {eingabe_datei} wurde erfolgreich in {ausgabe_datei} geschrieben.")
    except FileNotFoundError:
        print(f"Fehler: Die Datei {eingabe_datei} wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

schreibe_csv_neu(eingabe_datei, ausgabe_datei)

"""

# Der Pfad zur Datei (das ist immer noch korrekt als String)
dateipfad = r"11 Datenvisualisierung/Projekt-Emission-Dashboard/Entwicklung_chris/annual-co-emissions-from-oil_normalisiert.csv"

try:
    # Lese die CSV-Datei in ein Pandas DataFrame ein
    df_annual_oil_n = pd.read_csv(dateipfad)

    # Jetzt kannst du die .head()-Methode auf das DataFrame anwenden
    print(df_annual_oil_n.head())

except FileNotFoundError:
    print(f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden. Überprüfe den Pfad.")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

print(df_annual_oil_n_df.head())
# Entity / Year / Annual CO₂ emissions from oil

# print(df_annual_oil_n.dtypes)
# Entity                            object
# Year                               int64
# Annual CO₂ emissions from oil    float64

# print(df_annual_oil_n.shape)
# (25218, 3)

emissions_column = "Annual CO₂ emissions from oil"

# if emissions_column in df_annual_oil_n.columns:
#     min_emission = df_annual_oil_n[emissions_column].min()
#     max_emission = df_annual_oil_n[emissions_column].max()

#     print(f"Minimaler Emissionswert (vor Normalisierung): {min_emission}")
#     print(f"Maximaler Emissionswert (vor Normalisierung): {max_emission}")
# else:
#     print(f"Fehler: Spalte '{emissions_column}' wurde im DataFrame nicht gefunden. Verfügbare Spalten: {df_annual_oil_n.columns.tolist()}")


# Ab hier tatsächliche Durchführung der Normalisierung

#df_annual_oil_n.dropna(subset=[emissions_column], inplace=True)

df_annual_oil_n.dropna(): Diese Methode entfernt Zeilen oder Spalten mit fehlenden Werten.

subset=['emissions_column_name']: Dieser Parameter stellt sicher, dass nur die Zeilen 
entfernt werden, die in der angegebenen Spalte ('emissions_column_name') einen NaN-Wert 
haben. Andere NaN-Werte in anderen Spalten bleiben unberührt.

## Schritt 1: Zeilen mit NaN-Werten in der Emissionsspalte entfernen
# 'inplace=True' ändert das DataFrame direkt
#df_annual_oil_n.dropna(subset=[emissions_column], inplace=True)

# Der aktuelle, "alte" Spaltenname
alter_spaltenname = "Annual CO₂ emissions from oil"

# Der gewünschte, "neue" Spaltenname
# Hier ersetzen wir Leerzeichen und das CO2-Sonderzeichen
neuer_spaltenname = alter_spaltenname.replace(' ', '_').replace('CO₂', 'CO2')

# Spalte umbenennen
df_annual_oil_n.rename(columns={alter_spaltenname: neuer_spaltenname}, inplace=True)

print("\n--- DataFrame mit neuem Spaltennamen ---")
print(df_annual_oil_n.columns)
print("-" * 30)

# print(df_annual_oil_n.shape)
"""