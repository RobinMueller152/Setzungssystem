import pandas as pd
import random

def generate_csv(filename: str, n: int = 30):
    """
    Erzeugt eine CSV-Datei mit n zufälligen Personen.
    Spalten:
      - Name: zufälliger deutscher Vor- und Nachname
      - Redepräferenz: 'Team' oder 'Frei'
      - Erfahrung: Zufallszahl zwischen 0 und 10
    """
    
    # Beispielhafte Namenslisten
    first_names = [
        "Lukas", "Anna", "Marie", "Jonas", "Leon", "Mia", "Paul", "Laura",
        "Tim", "Emma", "Noah", "Sophie", "Ben", "Öüaärk", "Lena", "Elias", "Clara"
    ]
    last_names = [
        "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Äöüzé", "Wagner", "Becker",
        "Hoffmann", "Schäfer", "Koch", "Richter", "Klein", "Wolf", "Schröder"
    ]
    
    preferences = ["Team", "Frei"]

    data = []

    for _ in range(n):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        pref = random.choice(preferences)
        exp = random.randint(0, 10)
        data.append([name, pref, exp])
    
    df = pd.DataFrame(data, columns=["Name", "Redepräferenz", "Erfahrung"])
    
    # CSV speichern (UTF-8 mit BOM für Excel-Kompatibilität)
    df.to_csv(filename, index=False, encoding="utf-8-sig", sep=";")
    
    print(f"CSV-Datei '{filename}' mit {n} Einträgen erstellt.")


if __name__ == "__main__":
    # Beispiel: 40 zufällige Einträge erzeugen
    generate_csv("INPUT/TESTINPUT.csv", n=40)
