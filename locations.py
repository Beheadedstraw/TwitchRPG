# locations.py
# This will load all of the locations into memory so were not bashing the DB every time we want to go somewhere.

locationStore = {}


class Locations:
    def __init__(self):
        self.location_id = 0
        self.description = ""
        self.name = ""
        self.hasMonsters = 0
        self.maxMonsterLevel = 0
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0
