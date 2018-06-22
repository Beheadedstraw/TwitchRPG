# combat.py
# Combat functions for general fighting

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


def fightMonster(s, monster, character, username, weapon, armor, shield, items):
    combatText = ""

    # variables to store story mode combat description
    characterTotalDamage = 0
    monsterTotalDamage = 0
    characterDied = 0
    characterLeveled = 0
    monsterDroppedLoot = ""

    # Check if we have armor equipped, set variables accordingly
    if armor == 0:
        character_armor = 0
    else:
        print "-- Armor: " + armor.name
        character_armor = armor.armor

    if weapon == 0:
        character_weaponDamage = 0
    else:
        print "-- Weapon: " + weapon.name
        character_weaponDamage = weapon.damage

    if shield == 0:
        character_shieldArmor = 0
    else:
        print "-- Shield: " + shield.name
        character_shieldArmor = shield.armor

    # --- combat loop start ---
    while monster['hp'] > 0 and character.hp > 0:
        # Append the combat text so we can shove it out to Twitch in one big wall of text, should make for some interesting channels LOL
        characterDamage = character.str + character_weaponDamage
        monsterDamage = (monster['damage'] + monster['level'] + random.randint(0,5)) - (character_armor + character_shieldArmor) * 2

        # Stop negative numbers, negative numbers bad, very bad.
        if monsterDamage < 0:
            monsterDamage = 0

        monsterTotalDamage += monsterDamage
        characterTotalDamage += characterDamage

        monster['hp'] -= characterDamage
        character.hp -= monsterDamage



        print "--- Monster HP is " + str(monster['hp'])

        # They lost, so we send them back to the Inn and set the HP to 1
        # TODO: Send them to boound location if it's set.
        if character.hp <= 0:
            print "--- Lost the fight!"
            character.hp = 1
            character.location = 1
            characterDied = 1

        # The monster died before we did.
        elif monster['hp'] <= 0:
            print "--- Won the fight!"
            character.money += monster['money']

            # begin inventory handling
            monsterLoot = monster['loot'].split(',')
            monsterDroppedLoot = ""
            characterInventory = character.inventory.split(',')

            for l in monsterLoot:
                print l
                if int(l) >= 1000 and int(l) <= 1999:
                    print "--- added to inventory: " + l
                    if random.randint(0, 100) > 20:
                        list.append(characterInventory, l)
                        if monsterDroppedLoot == "":
                            monsterDroppedLoot += items[int(l)].name
                        else:
                            monsterDroppedLoot += "," + items[int(l)].name

            print "---- char inventory: "
            print characterInventory
            print "---- char imploded inventory"
            print ','.join(characterInventory)
            print "---- dropped loot: "
            print monsterDroppedLoot
            character.inventory = ','.join(characterInventory)
            print character.inventory

            # Level check to prevent easy leveling by killing low level monsters
            if not (character.level - 5) > monster['level']:
                character.currentXP += monster['xp']
            else:
                # didn't earn experience
                pass

            # Level up the character if they break the levelXP cap
            if character.currentXP >= character.levelXP:
                # combatText += " *** " + username + " JUST LEVELED UP!!! You gained 2 skillpoints! ***"
                characterLeveled = 1
                character.level += 1
                character.currentXP = character.currentXP - character.levelXP
                character.skillPoints += 2
                character.hp = character.maxHP

        combatText = "You went valiantly into battle against " + monster['name'] + ". You did a number on them, doing " + str(characterTotalDamage) + " damage to them while they did " + str(monsterTotalDamage) + "."
        if characterDied:
            combatText += " Unfortunately, while being the brave adventurer you are, you died."
        else:
            combatText += " At the end of the battle though, you slayed " + monster['name'] + " and gained " + str(monster['xp']) + " experience. You looted coin from the corpse totaling " + str(monster['money']) + " copper."

            if monsterDroppedLoot == "":
                pass
            else:
                combatText += " You also looted items " + monsterDroppedLoot + "."

            if characterLeveled:
                combatText += " You gained a level!"
    return combatText

'''
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

        round += 1 '''
