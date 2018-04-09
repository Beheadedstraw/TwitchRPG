# items.py
# manages items in the world
itemStore = {}


class Items:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.type = 0
        self.damage = 0
        self.armor = 0
        self.str = 0
        self.vit = 0
        self.wis = 0
