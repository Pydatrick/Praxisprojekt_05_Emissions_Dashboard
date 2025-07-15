import pandas as pd

def get_unique_countries(file_path):
    """
    Liest eine CSV-Datei ein und gibt alle einzigartigen Ländernamen
    aus der Spalte 'Entity' zurück.

    Args:
        file_path (str): Der Pfad zur CSV-Datei.

    Returns:
        list: Eine Liste von einzigartigen Ländernamen.
              Gibt eine leere Liste zurück, wenn die Datei nicht gefunden wird
              oder die Spalte 'Entity' nicht existiert.
    """
    try:
        df = pd.read_csv(file_path)

        # Überprüfen, ob die Spalte 'Entity' existiert
        if 'Entity' in df.columns:
            unique_countries = df['Entity'].unique().tolist()
            # Sortieren der Liste für eine bessere Lesbarkeit
            unique_countries.sort()
            return unique_countries
        else:
            print(f"Fehler: Die Spalte 'Entity' wurde in der Datei '{file_path}' nicht gefunden.")
            return []
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden.")
        return []
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return []

# Dateipfad zur CSV-Datei
file_path = 'C:/DataCraft/11 Datenvisualisierung/Projekt-Emission-Dashboard/Entwicklung_chris/annual-co-emissions-from-oil_copy.csv'

# Unique Ländernamen abrufen und ausgeben
unique_countries_list = get_unique_countries(file_path)

if unique_countries_list:
    print("Einzigartige Ländernamen (Entities):")
    for country in unique_countries_list:
        print(country)