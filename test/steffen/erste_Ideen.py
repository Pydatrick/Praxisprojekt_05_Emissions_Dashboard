import pandas as pd
from pathlib import Path

# Basisverzeichnis = zwei Ebenen hoch vom aktuellen Skript
basis_pfad = Path(__file__).resolve().parents[2]

# Pfad zu den CSV-Dateien im Unterordner data/raw
daten_ordner = basis_pfad / "data" / "raw"

# CSV-Dateien suchen
csv_files = list(daten_ordner.glob("*.csv"))

"""print(f"{len(csv_files)} Dateien gefunden:")
for file in csv_files:
    print(file.relative_to(basis_pfad))"""

# Dateien einlesen und zusammenführen
dfs = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(dfs, ignore_index=True)

# Schritt 1: Duplikate prüfen
print(merged_df.duplicated(subset=["Entity", "Year"]).sum(), "Duplikate vor dem Aufräumen")

# Schritt 2: Gruppieren und den vollständigsten Datensatz je Entity + Year wählen
def wähle_vollständigsten_eintrag(gruppe):
    # Zählt pro Zeile die nicht-leeren Werte (nicht-NaN)
    anzahl_wertvoller_werte = gruppe.notna().sum(axis=1)
    # Nimmt die Zeile mit den meisten gefüllten Werten
    return gruppe.loc[anzahl_wertvoller_werte.idxmax()]

bereinigt_df = merged_df.groupby(["Entity", "Year"], as_index=False).apply(wähle_vollständigsten_eintrag)

# Schritt 3: Überprüfen
print(bereinigt_df.shape)
print(bereinigt_df.duplicated(subset=["Entity", "Year"]).sum(), "Duplikate nach dem Aufräumen")

# Ergebnis speichern z. B. nach data/merged.csv
output_pfad = basis_pfad / "data" / "merged.csv"
merged_df.to_csv(output_pfad, index=False)

print(f"Zusammengeführte Datei gespeichert unter: {output_pfad.relative_to(basis_pfad)}")
