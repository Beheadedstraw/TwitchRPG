# combat.py
# Combat functions for general fighting
import utils


def fightMonster(s, monster, character, username):
    combatText = ""
    monsterMaxHP = monster['hp']
    round = 1

    while monster['hp'] > 0 and character.hp > 0:
        # Append the combat text so we can shove it out to Twitch in one big wall of text, should make for some interesting channels LOL
        combatText += "*** COMBAT ROUND: " + str(round)
        characterDamage = character.str + character.level*2
        monsterDamage = monster['damage'] + monster['level']

        combatText += " ***" + username + "(" + str(character.hp) + "/" + str(character.maxHP) + ") " + " ATTACKS " + monster['name'] + " FOR " + str(characterDamage) + "!"
        combatText += " ***" + monster['name'] + "(" + str(monster['hp']) + "/" + str(monsterMaxHP) + ") " + " ATTACKS " + username + " FOR " + str(monsterDamage) + "!"

        monster['hp'] -= characterDamage
        character.hp -= monsterDamage
        print "--- Monster HP is " + str(monster['hp'])

        if monster['hp'] <= 0:
            print "--- Won the fight!"
            combatText += "*** " + username + " DEFEATS " + monster['name'] + "! ***"
            character.currentXP += monster['xp']
            combatText += "*** " + username + " EARNED " + str(monster['xp']) + " experience! ***"
            if character.currentXP >= character.levelXP:
                combatText += "*** " + username + " JUST LEVELED UP!!! You gained 2 skillpoints! ***"
                character.level += 1
                character.currentXP = character.currentXP - character.levelXP
                character.skillPoints += 2

        if character.hp <= 0:
            print "--- Lost the fight!"
            combatText += "*** Oh no " + username + "!, You were killed by " + monster['name'] + "! ***"
            character.hp = 0
            character.location = 1
        round += 1
    return combatText