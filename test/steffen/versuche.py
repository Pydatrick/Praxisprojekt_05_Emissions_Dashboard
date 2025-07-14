import pandas as pd
from pathlib import Path # Importiere Path für die Pfadmanipulation

def get_unique_entities(file_path):
    """
    Liest eine CSV-Datei, extrahiert die 'Entity'-Spalte
    und gibt eine sortierte Liste der einzigartigen Einträge zurück.
    """
    try:
        df = pd.read_csv(file_path)

        if 'Entity' in df.columns:
            unique_entities = df['Entity'].unique().tolist()
            unique_entities.sort() # Sortiere die Liste alphabetisch für bessere Lesbarkeit
            return unique_entities
        else:
            print("Fehler: Die Spalte 'Entity' wurde in der CSV-Datei nicht gefunden.")
            return []
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden. Überprüfe den Pfad.")
        return []
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return []

if __name__ == "__main__":
    # Basisverzeichnis des aktuellen Skripts
    script_dir = Path(__file__).resolve().parent

    # Navigiere zum Datenordner basierend auf deiner Struktur
    # Annahme: Das Skript ist in einem Unterordner von 'projekt_root/src'
    # und die Daten sind in 'projekt_root/data/raw/merged_final.csv'
    # Du musst diesen Pfad an deine tatsächliche Ordnerstruktur anpassen!
    # Beispiel: Wenn dein Skript in 'my_project/scripts/' liegt und die Daten in 'my_project/data/raw/'
    # dann müsstest du vielleicht 'parents[1]' oder 'parents[0]' verwenden, je nachdem wo dein Skript liegt.
    # Hier ist ein generischer Ansatz basierend auf deinem Beispiel:
    # Annahme: Dein Skript liegt irgendwo unterhalb des Projekt-Root-Ordners.
    # Wir gehen 2 Ebenen hoch (parents[2]), um zum 'projekt_root' zu gelangen.
    # Von dort aus gehen wir dann zu 'data/raw/merged_final.csv'.
    project_root = script_dir.parents[2] # Passe diese Zahl an deine Ordnerstruktur an!
    csv_file_path = project_root / "data" / "raw" / "merged_final.csv"

    print(f"Versuche, die Datei zu laden von: {csv_file_path}")

    unique_list = get_unique_entities(csv_file_path)

    if unique_list:
        print("\nEinzigartige Einträge in der 'Entity'-Spalte:")
        for entity in unique_list:
            print(entity)