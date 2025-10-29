import pandas as pd
import chardet
from pathlib import Path
import math
from itertools import combinations

inputname = "INPUT/INPUT" #Hier Namen der Datei eintragen, in der im Input die Namen stehen

room_priority = "Make" #Optionen (Großschreibung beachten!): "Fill", "Make"
type_priority = "Experience" #Optionen "Wish", "Experience"
free_speakers_priority = "Spread" #Optionen "Fill", "Spread"

min_rooms = 2
max_rooms = 5
ironman_threshold = 15 #WIP: Minimum an kumulativer Erfahrung, um dritten Teamplatz frei zu erlauben

class Room:
    def __init__(self, ID: int):
        self.ID = ID
        self.Team1 = []
        self.Team2 = []
        self.Frei = []

Rooms: list[Room] = []
data: pd.DataFrame = []

def validate_data(input_name: str) -> pd.DataFrame:
    pfad = Path(input_name)
    if pfad.suffix == "":
        pfad = pfad.with_suffix(".csv")

    if not pfad.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {pfad}")
    
    with open(pfad, "rb") as f:
        result = chardet.detect(f.read(100000))

    print("Erkanntes Encoding:", result["encoding"])

    df = pd.read_csv(pfad, sep=None, encoding=result["encoding"])

    print("Kopfzeile eingelesen als ", df.head())
    print("Info eingelesen als", df.info())

    expected_cols = ["Name", "Redepräferenz", "Erfahrung"]

    if list(df.columns) != expected_cols:
        print("Spaltennamen passen nicht, werden überschrieben:")
        print("Gefunden:", list(df.columns))
        df.columns = expected_cols
    else:
        print("Spalten korrekt.")

    return df


def calculate_bounds(minrooms, maxrooms, data):
    n = len(data)  # Anzahl Zeilen ohne Kopfzeile = Anzahl Personen
    true_min_rooms = math.ceil(n / 9)
    true_max_rooms = math.floor(n / 6)
    if true_max_rooms < maxrooms:
        maxrooms = true_max_rooms
        print("So viele Räume können wir nicht füllen, Raumzahl wurde verringert!")
    if true_min_rooms > minrooms:
        minrooms = true_min_rooms
        print("Plätze reichen nicht, Mindestraumzahl wurde erhöht!")
    return minrooms, maxrooms

def initialize_rooms(Rooms):
    if room_priority == "Fill": #Möglichst wenig Räume zu Anfang bauen und diese dann füllen
        for index in range(min_rooms):
            room = Room(index + 1)
            Rooms.append(room)
    elif room_priority == "Make": #Möglichst viele Räume bauen und flach füllen
        for index in range(max_rooms):
            room = Room(index + 1)
            Rooms.append(room)
    print(f"Initialisiere {len(Rooms)} Räume")
    return Rooms

def first_iteration(data, rooms, type_priority):
    pref_order = {"Team": 0, "Frei": 1} #Numerische Werte an Teamart zuweisen

    if type_priority == "Wish":
        data_sorted = data.sort_values(
            by=["Redepräferenz", "Erfahrung"], 
            key=lambda col: col.map(pref_order) if col.name == "Redepräferenz" else col,
            ascending=[True, False]  # Präferenz aufsteigend (Team oben), Erfahrung absteigend
        ).reset_index(drop=True)
    elif type_priority == "Experience":
        data_sorted = data.sort_values(
            by=["Erfahrung", "Redepräferenz"], 
            key=lambda col: col.map(pref_order) if col.name == "Redepräferenz" else col,
            ascending=[False, True]  # Erfahrung absteigend, Präferenz aufsteigend
        ).reset_index(drop=True)

    for room in rooms:
        participant1 = data_sorted.iloc[0]
        participant2 = data_sorted.iloc[1]
            
        # Teilnehmer in room einsortieren
        room.Team1.append({
            "Name": participant1["Name"],
            "Redepräferenz": participant1["Redepräferenz"],
            "Erfahrung": participant1["Erfahrung"]
        })

        room.Team2.append({
            "Name": participant2["Name"],
            "Redepräferenz": participant2["Redepräferenz"],
            "Erfahrung": participant2["Erfahrung"]
        })
            
        # Personen aus Liste löschen
        data_sorted = data_sorted.drop(0).reset_index(drop=True)
        data_sorted = data_sorted.drop(0).reset_index(drop=True)

    return data_sorted, rooms  # Rückgabe der restlichen Teilnehmer

def second_iteration(data, rooms): #Selbe Wirkweise, nur dass die unerfahrensten Redenden einsortiert werden
    pref_order = {"Team": 0, "Frei": 1} #Numerische Werte an Teamart zuweisen

    if type_priority == "Wish":
        data_sorted = data.sort_values(
            by=["Redepräferenz", "Erfahrung"], 
            key=lambda col: col.map(pref_order) if col.name == "Redepräferenz" else col,
            ascending=[True, True]  # Präferenz aufsteigend (Team oben), Erfahrung absteigend
        ).reset_index(drop=True)
    elif type_priority == "Experience":
        data_sorted = data.sort_values(
            by=["Erfahrung", "Redepräferenz"], 
            key=lambda col: col.map(pref_order) if col.name == "Redepräferenz" else col,
            ascending=[True, True]  # Erfahrung absteigend, Präferenz aufsteigend
        ).reset_index(drop=True)

    for room in rooms:
        participant1 = data_sorted.iloc[0]
        participant2 = data_sorted.iloc[1]
            
        # Teilnehmer in room einsortieren
        room.Team1.append({
            "Name": participant1["Name"],
            "Redepräferenz": participant1["Redepräferenz"],
            "Erfahrung": participant1["Erfahrung"]
        })

        room.Team2.append({
            "Name": participant2["Name"],
            "Redepräferenz": participant2["Redepräferenz"],
            "Erfahrung": participant2["Erfahrung"]
        })
            
        # Personen aus Liste löschen
        data_sorted = data_sorted.drop(0).reset_index(drop=True)
        data_sorted = data_sorted.drop(0).reset_index(drop=True)

    return data_sorted, rooms  # Rückgabe der restlichen Teilnehmer

def third_iteration(data, rooms):
    for room in rooms:
        if len(data) < 2:
            print("Nicht genügend Teilnehmer übrig.")
            break

        # Summen der bisherigen Erfahrung pro Team
        sum1 = sum(member["Erfahrung"] for member in room.Team1)
        sum2 = sum(member["Erfahrung"] for member in room.Team2)

        best_pair = None #Aktuell optimale Paarung
        min_diff = float('inf')

        # Alle möglichen Paare aus Data
        for i, j in combinations(range(len(data)), 2):
            p1 = data.iloc[i]
            p2 = data.iloc[j]

            # Neue Summen, wenn das Paar hinzugefügt wird
            new_sum1 = sum1 + p1["Erfahrung"]
            new_sum2 = sum2 + p2["Erfahrung"]

            diff = abs(new_sum1 - new_sum2)

            # Prüfen, ob diese Kombination besser (balancierter) ist
            if diff < min_diff:
                min_diff = diff
                best_pair = (i, j)

        if best_pair is None:
            print("FEHLER: Kein passendes Paar gefunden?!")
            continue

        # Bestes Paar einfügen
        i, j = best_pair
        p1 = data.iloc[i]
        p2 = data.iloc[j]

        room.Team1.append({
            "Name": p1["Name"],
            "Redepräferenz": p1["Redepräferenz"],
            "Erfahrung": p1["Erfahrung"]
        })
        room.Team2.append({
            "Name": p2["Name"],
            "Redepräferenz": p2["Redepräferenz"],
            "Erfahrung": p2["Erfahrung"]
        })

        # Entferne beide Redner aus Tabelle
        data = data.drop([i,j]).reset_index(drop=True)

    return data, rooms

def fill_rooms(data, rooms, type_priority):
    data, rooms = first_iteration(data, rooms, type_priority)
    data, rooms = second_iteration(data, rooms)
    data, rooms = third_iteration(data, rooms)
    return data, rooms

def fill_free_speakers(data, rooms, free_speakers_priority):
    #Räume füllen solange möglich
    if free_speakers_priority == "Fill":
        for room in Rooms:
            while len(data) > 0 and len(getattr(room, "Frei", [])) < 3:
                # Obersten Eintrag nehmen
                speaker = data.iloc[0]
                # Raum bekommt Redner
                getattr(room, "Frei", []).append({
                    "Name": speaker["Name"],
                    "Redepräferenz": speaker["Redepräferenz"],
                    "Erfahrung": speaker["Erfahrung"]
                })
                # Eintrag aus Data löschen
                data = data.drop(0).reset_index(drop=True)
                if data.empty:
                    break

    # Gleichmäßig verteilen solange möglich
    elif free_speakers_priority == "Spread":
        # Bis zu 3 Runden (max. 3 pro Raum)
        for round_num in range(3):
            for room in Rooms:
                if data.empty:
                    break
                # Prüfen, ob Raum schon 3 hat
                current_team = getattr(room, "Frei", [])
                if len(current_team) < 3:
                    speaker = data.iloc[0]
                    current_team.append({
                        "Name": speaker["Name"],
                        "Redepräferenz": speaker["Redepräferenz"],
                        "Erfahrung": speaker["Erfahrung"]
                    })
                    data = data.drop(0).reset_index(drop=True)
                    # Zurückschreiben, falls "Frei" erst jetzt erstellt wurde
                    setattr(room, "Frei", current_team)
            if data.empty:
                break

    else:
        print("Ungültiger prio-Wert. Erlaubt: 'Fill' oder 'Spread'.")

    return data, rooms

def print_rooms(Rooms):
    room_columns = {}

    # Jede Raumspalte aufbauen
    for room in Rooms:
        col_entries = []
        col_entries.append("Team 1")
        col_entries += [f"{m["Name"]} ({m["Redepräferenz"]}, {m["Erfahrung"]})" for m in room.Team1]
        col_entries.append("")  # Leerzeile
        col_entries.append("Team 2")
        col_entries += [f"{m["Name"]} ({m["Redepräferenz"]}, {m["Erfahrung"]})" for m in room.Team2]
        col_entries.append("")  # Leerzeile
        col_entries.append("Frei")
        if hasattr(room, "Frei"):
            col_entries += [f"{m["Name"]} ({m["Redepräferenz"]}, {m["Erfahrung"]})" for m in room.Frei]
        room_columns[f"Raum {room.ID}"] = col_entries

    # Nicht zugeordnete Teilnehmer
    unassigned_entries = []
    if not data.empty:
        unassigned_entries = [f"{row['Name']} ({row['Erfahrung']})" for _, row in data.iterrows()]
    room_columns["Nicht zugeordnet!"] = [""] + unassigned_entries

    # Alle Spalten gleich lang machen
    max_len = max(len(v) for v in room_columns.values())
    for key in room_columns:
        room_columns[key] += [""] * (max_len - len(room_columns[key]))

    # DataFrame erstellen
    result = pd.DataFrame(room_columns)

    # Ausgabe auf Bildschirm
    print(result)

    result.to_csv("OUTPUT/Setzung.csv", index=False, encoding="utf-8-sig", sep =";")
    print(f"Tabelle wurde gespeichert.")

    return result

def main():
    global min_rooms, max_rooms, data, Rooms

    data = validate_data(inputname)
    min_rooms, max_rooms = calculate_bounds(min_rooms, max_rooms, data)
    Rooms = initialize_rooms(Rooms)

    global type_priority
    data, Rooms = fill_rooms(data, Rooms, type_priority)

    global free_speakers_priority
    data, Rooms = fill_free_speakers(data, Rooms, free_speakers_priority)

    result = print_rooms(Rooms)

    print("Fertig! :)")

if __name__ == "__main__":
    main()