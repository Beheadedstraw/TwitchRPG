# Dictionary containing the character instances loaded.
characterStore = {}


class Characters:
    def __init__(self):
        self.name = ""
        self.level = 1
        self.energy = 10
        self.skillPoints = 0
        self.currentXP = 0
        self.levelXP = 20
        self.hp = 0
        self.maxHP = 0
        self.mana = 0
        self.maxMana = 0
        self.str = 0
        self.wis = 0
        self.vit = 0
        self.weapon = 2
        self.shield = 3
        self.armor = 1
        self.inCombat = 0
        self.inCombatID = 0
        self.location = 1
        self.whisperMode = 0
        self.inventory = "1,2,3"

    def createCharacter(self, name):
        self.name = name
        self.str = 1
        self.wis = 1
        self.vit = 1
        self.hp = self.vit * 20
        self.maxHP = self.vit * 20 * self.level
        self.mana = self.wis * 5 * self.level
        self.maxMana = self.wis * 5 * self.level
        return True




