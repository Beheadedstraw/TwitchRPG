# bot.py
# Main loop for the bot.

import cfg
import utils
import sql
import socket
import re
import time, thread
from time import sleep
import characters as character
import locations as location
import monsters as monsters
import random
import combat
import commands as command
import items as item


class Command(object):
    cmd = ""
    response = ""
    description = ""
    op = 0

    def __init__(self, cmd, response, description, op):
        self.cmd = cmd
        self.response = response
        self.description = description
        self.op = op


# Loads up all of the monsters from the DB
def loadMonsters():
    # Load up all of the monsters
    print "--------------------------"
    print "---  LOADING MONSTERS  ---"
    print "--------------------------"

    tempMonsters = sql.getMonsters()

    for m in tempMonsters:
        monsters.monsterStore[m["name"]] = monsters.Monsters()
        monsters.monsterStore[m["name"]].name = m["name"]
        monsters.monsterStore[m["name"]].level = m["level"]
        monsters.monsterStore[m["name"]].hp = m["hp"]
        monsters.monsterStore[m["name"]].damage = m["damage"]
        monsters.monsterStore[m["name"]].xp = m["xp"]
        print "--- Loaded Monster: " + m["name"]


# Removes energy after an action
def removeEnergy(energy, user):

    character.characterStore[user].energy -= energy
    if character.characterStore[user].energy < 0:
        character.characterStore[user].energy = 0

    print "-- Removed " + str(energy) + " energy from " + user


# Load up all of the characters from the DB
def loadCharacters():

    print "--------------------------"
    print "--- LOADING CHARACTERS ---"
    print "--------------------------"
    tempChar = sql.getCharacters()
    for c in tempChar:
        character.characterStore[c["name"]] = character.Characters()
        character.characterStore[c["name"]].name = c["name"]
        character.characterStore[c["name"]].level = c["level"]
        character.characterStore[c["name"]].energy = c["energy"]
        character.characterStore[c["name"]].skillPoints = c["skillPoints"]
        character.characterStore[c["name"]].currentXP = c["currentXP"]
        character.characterStore[c["name"]].levelXP = c["levelXP"]
        character.characterStore[c["name"]].hp = c["hp"]
        character.characterStore[c["name"]].maxHP = c["maxHP"]
        character.characterStore[c["name"]].mana = c["mana"]
        character.characterStore[c["name"]].maxMana = c["maxMana"]
        character.characterStore[c["name"]].str = c["str"]
        character.characterStore[c["name"]].wis = c["wis"]
        character.characterStore[c["name"]].vit = c["vit"]
        character.characterStore[c["name"]].weapon = c["weapon"]
        character.characterStore[c["name"]].armor = c["armor"]
        character.characterStore[c["name"]].shield = c["shield"]
        character.characterStore[c["name"]].location = c["location"]
        character.characterStore[c["name"]].whisperMode = c["whisperMode"]
        character.characterStore[c["name"]].inventory = c["inventory"]
        print character.characterStore[c["name"]].inventory
        print character.characterStore[c["name"]]
        print "--- Loaded Character: " + c["name"]


def loadItems():
    print "--------------------------"
    print "---    LOADING ITEMS   ---"
    print "--------------------------"
    tempItems = sql.getItems()
    for i in tempItems:
        item.itemStore[i["id"]] = item.Items()
        item.itemStore[i["id"]].id = i["id"]
        item.itemStore[i["id"]].name = i["name"]
        item.itemStore[i["id"]].desc = i["description"]
        item.itemStore[i["id"]].type = i["type"]
        item.itemStore[i["id"]].damage = i["damage"]
        item.itemStore[i["id"]].armor = i["armor"]
        item.itemStore[i["id"]].str = i["str"]
        item.itemStore[i["id"]].vit = i["vit"]
        item.itemStore[i["id"]].wis = i["wis"]
        print "--- LOADED ITEM: " + item.itemStore[i["id"]].name


# Loads all locations from the DB
def loadLocations():
    # Load up all of the locations
    print "--------------------------"
    print "--- LOADING LOCATIONS  ---"
    print "--------------------------"

    tempLocations = sql.getLocations()

    for l in tempLocations:
        location.locationStore[l["location_id"]] = location.Locations()
        location.locationStore[l["location_id"]].name = l["name"]
        location.locationStore[l["location_id"]].location_id = l["location_id"]
        location.locationStore[l["location_id"]].description = l["description"]
        location.locationStore[l["location_id"]].hasMonsters = l["hasMonsters"]
        location.locationStore[l["location_id"]].maxMonsterLevel = l["maxMonsterLevel"]
        location.locationStore[l["location_id"]].north = l["north"]
        location.locationStore[l["location_id"]].south = l["south"]
        location.locationStore[l["location_id"]].east = l["east"]
        location.locationStore[l["location_id"]].west = l["west"]
        print "--- Loaded location: " + l["name"]


# Gives energy to players at a regular interval
def giveEnergy(s):
    while True:
        print "--------------------------"
        print "---   GIVING ENERGY    ---"
        print "--------------------------"

        for key, value in character.characterStore.iteritems():
            value.energy += 1
            if value.energy > 10:
                value.energy = 10
            print "--- Giving Energy to Character: " + value.name
        for i in cfg.CHAN:
            utils.chat(s, "Adventurers in the realm feel a little more energetic!", False, None, i)
        sleep (60)


# Parses through the IRC message
def parse(c, s):
    if c.response.find("~") > -1:
        list = c.response.split("~")
        for item in list:
            if item.find("{") > -1:
                code = item.split("{")[1].split("}")[0]
                utils.chat(s, item.split("{")[0] + eval(code))
            else:
                utils.chat(s, item)
    else:

        if c.response.find("{") > -1:
            code = c.response.split("{")[1].split("}")[0]
            utils.chat(s, c.response.split("{")[0] + eval(code))
        else:
            utils.chat(s, c.response)


def main():
    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN[0]).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN[1]).encode("utf-8"))

    # Decode chat message from IRC format.
    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    for i in cfg.CHAN:
        utils.chat(s, "The portals have opened to another land in the Twitch realm! For more information, type !help.", False, None, i)

    loadCharacters()
    loadLocations()
    loadMonsters()
    loadItems()

    # load up the oplist for admin commands
    thread.start_new_thread(utils.threadFillOpList, ())

    # load up the oplist for admin commands
    thread.start_new_thread(giveEnergy, (s,))

    # Start the autosaving thread to save characters to DB every 60 seconds
    thread.start_new_thread(sql.autosaveCharacters, (character.characterStore,))

    # Main logic loop
    while True:
        response = s.recv(1024).decode("utf-8")
        # Respond to ping request to stay alive on the server
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            # Here we process the different commands
            print response
            try:
                username = response
                username = username.split(':')[1]
                username = username.split('!')[0].strip(':')
                char = character.characterStore[username]

                chan = response
                chan = chan.split('#')[1]
                chan = chan.split(':')[0].strip(' ')

                print chan
                print username
            except StandardError as e:
                print e

            message = CHAT_MSG.sub("", response)
            print(response)
            print "--- MESSAGE NOT STRIPPED: " + message
            print "--- MESSAGE NOT STRIPPED: " + message.strip()

            # splits the message so we can detect if there's a number to add for certain commands.
            message = message.split(" ")

            if message[0].strip() == "!help":
                utils.chat(s, "Hey "+ username + "!, some commands you can use are !joingame, !stats, !location [additional], !north, !south, !east, !west, !addstrength, !addwisdom, !addvitality, !hunt, !toggleWhisper, !rest, !inventory, !equipment, !equip [inventory slot number], !unequip [weapon/armor/shield]", character.characterStore[username].whisperMode, username, chan)
                # TODO: Flesh out the help command to take additonal argument for per command usage.
            # this creates a new character for the account. Only one character is allowed per account.
            if message[0].strip() == "!joingame":
                    if username in character.characterStore:  # check and see if the character is already made
                        utils.chat(s, username + ", you already have a character!", character.characterStore[username].whisperMode, username, chan)
                    else:
                        # create the character and add it to the DB
                        character.characterStore[username] = character.Characters()
                        if character.characterStore[username].createCharacter(username):
                            if sql.createCharacter(character.characterStore[username]):
                                utils.chat(s, username + ", You've now created a character. Some commands you can use are !showstats, !location, !movenorth, !movesouth, !moveeast, !movewest", character.characterStore[username].whisperMode, username, chan)
                            else:
                                utils.chat(s, username + ", there was an error saving you to the database, please contact the channel admin or join the Discord for TC_RPG", character.characterStore[username].whisperMode, username, chan)

            # Obviously shows the stats for the character. Twitch doesn't have linebreaks thanks to broke ass IRC code. So wall of text it is.
            if message[0].strip() == "!stats":
                # We try this, if it throws an error, most likely they don't have a character. Need to clean this up a bit.
                try:
                    print
                    utils.chat(s, "Hey " + username + ". Your stats are Level: " + str(character.characterStore[username].mana) \
                               + " || XP: " + str(character.characterStore[username].currentXP) + "/" + str(character.characterStore[username].levelXP) \
                               + " || Health: " + str(character.characterStore[username].hp) + "/" + str(character.characterStore[username].hp) \
                               + " || Mana: " + str(character.characterStore[username].mana) + "/" + str(character.characterStore[username].mana) \
                               + " || Energy: " + str(character.characterStore[username].energy) \
                               + " || Skill Points: " + str(character.characterStore[username].skillPoints) \
                               + " || Location: " + str(location.locationStore[character.characterStore[username].location].name) \
                               + ".", character.characterStore[username].whisperMode, username, chan)
                    print character.characterStore[username].name
                except:
                    utils.chat(s, "Hey " + username + ", you don't currently have a character registered. Type !joingame to have us create one for you!", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!south":
                if location.locationStore[character.characterStore[username].location].south > 0:
                    character.characterStore[username].location = location.locationStore[character.characterStore[username].location].south
                    utils.chat(s, username + " decides to go to the south, now you're at " + location.locationStore[character.characterStore[username].location].name, character.characterStore[username].whisperMode, username, chan)
                else:
                    utils.chat(s, username + " looks to the south but there's no where to go!", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!north":
                if location.locationStore[character.characterStore[username].location].north > 0:
                    character.characterStore[username].location = location.locationStore[character.characterStore[username].location].north
                    utils.chat(s, "You decide you want to head to the north, now you're at " + location.locationStore[character.characterStore[username].location].name, character.characterStore[username].whisperMode, username, chan)
                else:
                    utils.chat(s, username + " looks to the north but there's no where to go!", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!east":
                if location.locationStore[character.characterStore[username].location].east > 0:
                    character.characterStore[username].location = location.locationStore[
                        character.characterStore[username].location].east
                    utils.chat(s, "You decide you want to head to the east, now you're at " + location.locationStore[character.characterStore[username].location].name, character.characterStore[username].whisperMode, username, chan)
                else:
                    utils.chat(s, username + " shifts their glance to the east, but there's no where to go!", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!west":
                if location.locationStore[character.characterStore[username].location].west > 0:
                    character.characterStore[username].location = location.locationStore[
                        character.characterStore[username].location].west
                    utils.chat(s, "You decide you want to head to the west, now you're at " + location.locationStore[
                        character.characterStore[username].location].name, character.characterStore[username].whisperMode, username, chan)
                else:
                    utils.chat(s, username + " glances to the west, but there's no where to go!", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!location":
                text = ""
                if len(message) > 1:
                    print message
                    if message[1].strip() == "players":
                        playersAtLocation = sql.getPlayersAtLocation(character.characterStore[username].location)
                        print playersAtLocation
                        if len(playersAtLocation) > 1:
                            for p in playersAtLocation:
                                text += p["name"] + " -- "
                            utils.chat(s, username + " the current players in the same location are: " + text, character.characterStore[username].whisperMode, username, chan)
                        else:
                            utils.chat(s, username + " you're all alone...", character.characterStore[username].whisperMode, username, chan)
                    else:
                        utils.chat(s, username + " I didn't quite understand that.", character.characterStore[username].whisperMode, username, chan)
                else:
                    if location.locationStore[character.characterStore[username].location].location_id > 0:
                        utils.chat(s, username + " looks at their surroundings. " + location.locationStore[
                            character.characterStore[username].location].description, character.characterStore[username].whisperMode, username, chan)
                    else:
                        utils.chat(s, username + " stares into the nether, seeing nothing but darkness.", character.characterStore[username].whisperMode, username, chan)

            # Players rest to heal in places without monsters
            if message[0].strip() == "!rest":
                if location.locationStore[character.characterStore[username].location].hasMonsters:
                    utils.chat(s, username + " looks around but think it's not exactly the best idea to rest with monsters roaming around.", character.characterStore[username].whisperMode, username, chan)
                else:
                    utils.chat(s, username + " takes a break from the burden of adventuring and gains some health.", character.characterStore[username].whisperMode, username, chan)
                    character.characterStore[username].hp += 20
                    if character.characterStore[username].hp > character.characterStore[username].maxHP:
                        character.characterStore[username].hp = character.characterStore[username].maxHP

            # Starts combat against creatures
            if message[0].strip() == "!hunt":
                print character.characterStore[username].energy
                if character.characterStore[username].energy > 3:
                    maxLevel = location.locationStore[character.characterStore[username].location].maxMonsterLevel
                    if maxLevel > 8:
                        minLevel = maxLevel-5
                    else:
                        minLevel = 1

                    if location.locationStore[character.characterStore[username].location].hasMonsters:
                        monsters = sql.getMonstersByLevel(minLevel, maxLevel)
                        if monsters:
                            print "Total Monsters" + str(len(monsters))
                            indexOfMonster = random.randint(0, len(monsters) - 1)
                            print "Index of Monster " + str(indexOfMonster)
                            monsterToFight = monsters[indexOfMonster]
                            print monsterToFight

                            outcome = combat.fightMonster(s, monsterToFight, character.characterStore[username], username, item.itemStore[character.characterStore[username].weapon], item.itemStore[character.characterStore[username].armor])
                            # print outcome
                            utils.chat(s, outcome, character.characterStore[username].whisperMode, username, chan)
                            removeEnergy(1, username)
                    else:
                        utils.chat(s, username + " there doesn't seem to be anything here to kill.", character.characterStore[username].whisperMode, username, chan)
                else:
                    utils.chat(s, username + " tries to go and kill stuff, but takes a nap instead due to being completely out of of energy!", character.characterStore[username].whisperMode, username, chan)

            # Adds strength using a skill point
            if message[0].strip() == "!addstrength":
                if character.characterStore[username].skillPoints > 0:
                    try:
                        if len(message) > 1:
                            message_amount = int(message[1])

                            if message_amount <= character.characterStore[username].skillPoints:
                                character.characterStore[username].skillPoints -= message_amount
                                utils.chat(s, username + " just gained some strength to more easily defeat his foes.", character.characterStore[username].whisperMode, username, chan)
                            else:
                                 utils.chat(s, username + " you don't have enough skillpoints!", character.characterStore[username].whisperMode, username, chan)
                        else:
                            utils.chat(s, username + " looks like you wanted to add some strength, but wasn't quite sure how much. Please use !addstrength amount (ex: !addstrength 5).", character.characterStore[username].whisperMode, username, chan)
                    except ValueError:
                        utils.chat(s, username + " you entered a wrong value, please make sure it's a number.", character.characterStore[username].whisperMode, username, chan)
                else:
                    utils.chat(s, username + " just tried to gain some strength, but failed miserably due to not having enough skill.", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!toggleWhisper":
                command.toggleWhisper(s, username, character.characterStore[username], chan)

            if message[0].strip() == "!equipment":
                command.showEquipment(s, username, character.characterStore[username], item.itemStore, chan)

            if message[0].strip() == "!weapon":
                command.showWeapon(s, username, character.characterStore[username], item.itemStore, chan)

            if message[0].strip() == "!armor":
                command.showArmor(s, username, character.characterStore[username], item.itemStore, chan)

            if message[0].strip() == "!shield":
                command.showShield(s, username, character.characterStore[username], item.itemStore, chan)

            if message[0].strip() == "!inventory":
                command.showInventory(s, username, character.characterStore[username], item.itemStore, chan)

            # Adds wisdom using a skill point
            if message[0].strip() == "!addwisdom":
                print len(message)
                try:
                    if character.characterStore[username].skillPoints > 0:
                        try:
                            if len(message) > 1:
                                message_amount = int(message[1])

                                if message_amount <= character.characterStore[username].skillPoints:
                                    character.characterStore[username].wis += 1
                                    character.characterStore[username].skillPoints -= 1
                                    utils.chat(s, username + " just got slightly less dumb and gained some hard earned wisdom.", character.characterStore[username].whisperMode, username, chan)
                                else:
                                    utils.chat(s, username + " you don't have enough skillpoints!", character.characterStore[username].whisperMode, username, chan)
                            else:
                                utils.chat(s, username + " you need to specify how many you wan to add!", character.characterStore[username].whisperMode, username, chan)
                        finally:
                            pass
                    else:
                        utils.chat(s, username + " just tried to gain some wisdom, but his brain just couldn't handle it.", character.characterStore[username].whisperMode, username, chan)
                except ValueError:
                    utils.chat(s, username + " you entered a wrong value, please make sure it's a number.", character.characterStore[username].whisperMode, username, chan)

            # Adds vitality using a skill point
            if message[0].strip() == "!addvitality":
                try:
                    if character.characterStore[username].skillPoints > 0:
                            if len(message) > 1:
                                message_amount = int(message[1])
                                if message_amount <= character.characterStore[username].skillPoints:
                                    character.characterStore[username].vit += 1
                                    character.characterStore[username].skillPoints -= 1
                                    utils.chat(s, username + " just gained some vitality to take some more hits like the mythical Rocky Balboa that he read about in some timetravel mages apartment.", character.characterStore[username].whisperMode, username, chan)
                                else:
                                    utils.chat(s, username + " you don't have enough skillpoints!", character.characterStore[username].whisperMode, username, chan)
                            else:
                                utils.chat(s, username + " you need to specify how many.", character.characterStore[username].whisperMode, username, chan)
                    else:
                        utils.chat(s, username + " just tried to be more of a meat shield, but is just too scrawny and weak.", character.characterStore[username].whisperMode, username, chan)
                except ValueError:
                    utils.chat(s, username + " you entered a wrong value, please make sure it's a number.", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!unequip":
                try:
                    if len(message) > 1:
                        if message[1].strip() == "weapon":
                            command.unequipWeapon(s, username, character.characterStore[username], chan)
                        elif message[1].strip() == "armor":
                            command.unequipArmor(s, username, character.characterStore[username], chan)
                        elif message[1].strip() == "shield":
                            command.unequipShield(s, username, character.characterStore[username], chan)
                        else:
                            utils.chat(s, username + " we didn't quite catch what you wanted to unequip. Did you want to !unequip your weapon, armor, or shield?", character.characterStore[username].whisperMode, username, chan)
                    else:
                        utils.chat(s, username + " we didn't quite catch what you wanted to unequip. Did you want to !unequip your weapon, armor, or shield?", character.characterStore[username].whisperMode, username, chan)
                except ValueError:
                    utils.chat(s, username + " you entered a wrong value, please make sure it's a number.", character.characterStore[username].whisperMode, username, chan)

            if message[0].strip() == "!equip":
                try:
                    if len(message) > 1 and int(message[1]):
                        command.equipItem(s, username, character.characterStore[username], item.itemStore, int(message[1].strip()), chan)
                    else:
                        utils.chat(s, username + " we didn't quite catch what you wanted to equip. Use the item number in () when using !inventory to equip that item.", username, chan)
                except ValueError:
                    utils.chat(s, username + " you entered a wrong value, please make sure it's a number.", character.characterStore[username].whisperMode, username, chan)
        sleep(1)

    utils.chat(s, "Bye everyone :)");


if __name__ == "__main__":
    main()