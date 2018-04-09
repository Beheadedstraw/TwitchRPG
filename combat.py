# combat.py
# Combat functions for general fighting
import utils
import random

def levelup(s, character):
    combatText = ""

    character.level += 1
    character.currentXP = character.currentXP - character.levelXP
    character.skillPoints += 2
    character.maxHP = character.vit * 20 * character.level
    character.maxMana = character.wis * 5 * character.level
    character.hp = character.maxHP
    character.mana = character.maxMana


def fightMonster(s, monster, character, username, weapon, armor):
    combatText = ""
    monsterMaxHP = monster['hp']
    round = 1

    print "-- weapon: " + weapon.name
    print "-- Armor: " + armor.name

    while monster['hp'] > 0 and character.hp > 0:
        # Append the combat text so we can shove it out to Twitch in one big wall of text, should make for some interesting channels LOL
        combatText += "*** COMBAT ROUND: " + str(round)
        characterDamage = character.str + character.level + weapon.damage + random.randint(0,5) * 2
        monsterDamage = (monster['damage'] + monster['level'] + random.randint(0,5)) - armor.armor * 2

        combatText += " ***" + username + "(" + str(character.hp) + "/" + str(character.maxHP) + ") " + " ATTACKS " + monster['name'] + " FOR " + str(characterDamage) + "!"
        combatText += " ***" + monster['name'] + "(" + str(monster['hp']) + "/" + str(monsterMaxHP) + ") " + " ATTACKS " + username + " FOR " + str(monsterDamage) + "!"

        monster['hp'] -= characterDamage
        character.hp -= monsterDamage
        print "--- Monster HP is " + str(monster['hp'])

        if monster['hp'] <= 0:
            print "--- Won the fight!"
            combatText += " *** " + username + " DEFEATS " + monster['name'] + "! ***"
            character.currentXP += monster['xp']
            combatText += " *** " + username + " EARNED " + str(monster['xp']) + " experience! ***"
            if character.currentXP >= character.levelXP:
                combatText += " *** " + username + " JUST LEVELED UP!!! You gained 2 skillpoints! ***"
                character.level += 1
                character.currentXP = character.currentXP - character.levelXP
                character.skillPoints += 2
                character.hp = character.maxHP

        if character.hp <= 0:
            print "--- Lost the fight!"
            combatText += " *** Oh no " + username + "!, You were killed by " + monster['name'] + "! ***"
            character.hp = 0
            character.location = 1
        round += 1
    return combatText


def fightPlayer(s, monster, character1, character2, username):
    combatText = ""
    monsterMaxHP = monster['hp']
    round = 1

    while character2.hp > 0 and character1.hp > 0:
        # Append the combat text so we can shove it out to Twitch in one big wall of text, should make for some interesting channels LOL
        combatText += "*** COMBAT ROUND: " + str(round)
        character1Damage = character1.str + character1.level*2
        character2Damage = character2.str + character2.level*2

        combatText += " ***" + username + "(" + str(character1.hp) + "/" + str(character1.maxHP) + ") " + " ATTACKS " + character2.name + " FOR " + str(character1Damage) + "!"
        combatText += " ***" + character2.name + "(" + str(character2.hp) + "/" + str(character2.maxHP) + ") " + " ATTACKS " + username + " FOR " + str(character2Damage) + "!"

        character1.hp -= character2Damage
        character2.hp -= character1Damage

        if character2.hp <= 0:
            print "--- Won the fight!"
            combatText += "*** " + username + " DEFEATS " + character2.name + "! ***"
            # character1.currentXP += monster['xp']
            # combatText += "*** " + username + " EARNED " + str(monster['xp']) + " experience! ***"
            if character1.currentXP >= character1.levelXP:
                combatText += "*** " + username + " JUST LEVELED UP!!! You gained 2 skillpoints! ***"
                character1.level += 1
                character1.currentXP = character1.currentXP - character1.levelXP
                character1.skillPoints += 2
                character1.hp = character1.maxHP

        if character1.hp <= 0:
            print "--- Lost the fight!"
            combatText += "*** Oh no " + username + "!, You were killed by " + character2.name + "! ***"
            character1.hp = 0
            character1.location = 1

        round += 1
    return combatText