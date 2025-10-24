import pandas as pd

room_priority = "Fill" #Optionen (Großschreibung beachten!): "Fill", "Make"
type_priority = "Wish" #Optionen "Wish", "Experience"
free_speakers_priority = "Fill" #Optionen "Fill", "Spread"

min_rooms = 2
max_rooms = 5
ironman_threshold = 15 #Minimum an kumulativer Erfahrung, um dritten Teamplatz frei zu erlauben

class Room:
    def __init__(self, ID: int, Team1: list[tuple[str, int]], Team2: list[tuple[str, int]], ):
        self.ID = ID
        self.Team1 = Team1
        self.Team2 = Team2

Rooms: list[Room] = []

def validate_data():
    pass

def calculate_bounds():
    pass

def initialize_rooms():
    if room_priority == "Fill":
        pass
    elif room_priority == "Make":
        pass

def fill_rooms():
    pass

def fill_free_speakers():
    pass

def print_rooms():
    pass

def main():
    validate_data()
    calculate_bounds()
    initialize_rooms()

    fill_rooms()

    fill_free_speakers()

    print_rooms()

    print("Done :)")

if __name__ == "__main__":
    main()