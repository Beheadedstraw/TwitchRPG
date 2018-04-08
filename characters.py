# Dictionary containing the character instances loaded.
characterStore = {}


class Characters:
    def __init__(self):
        self.name = ""
        self.level = 1
        self.hp = 0
        self.mana = 0
        self.str = 0
        self.wis = 0
        self.vit = 0
        self.weapon = 1
        self.shield = 1
        self.armor = 1
        self.inCombat = 0
        self.inCombatID = 0
        self.location = 1

    def createCharacter(self, name):
        self.name = name
        self.str = 1
        self.wis = 1
        self.vit = 1
        self.hp = self.vit * 20
        self.mana = self.wis * 10
        return True




