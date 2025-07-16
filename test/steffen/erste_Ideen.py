import pandas as pd

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
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden. Stelle sicher, dass die Datei im selben Verzeichnis wie dein Python-Skript ist oder gib den vollständigen Pfad an.")
        return []
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return []

if __name__ == "__main__":
    csv_file = 'merged_final.csv' # Stelle sicher, dass dies der korrekte Dateiname ist
    unique_list = get_unique_entities(csv_file)

    if unique_list:
        print("Einzigartige Einträge in der 'Entity'-Spalte:")
        for entity in unique_list:
            print(entity)