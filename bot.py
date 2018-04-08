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


def loadCharacters():
    # Load up all of the characters
    print "--------------------------"
    print "--- LOADING CHARACTERS ---"
    print "--------------------------"
    tempChar = sql.getCharacters()
    for c in tempChar:
        character.characterStore[c["name"]] = character.Characters()
        character.characterStore[c["name"]].name = c["name"]
        character.characterStore[c["name"]].level = c["level"]
        character.characterStore[c["name"]].skillPoints = c["skillPoints"]
        character.characterStore[c["name"]].currentXP = c["currentXP"]
        character.characterStore[c["name"]].levelXP = c["levelXP"]
        character.characterStore[c["name"]].hp = c["hp"]
        character.characterStore[c["name"]].maxHP = c["maxHP"]
        character.characterStore[c["name"]].mana = c["mana"]
        character.characterStore[c["name"]].str = c["str"]
        character.characterStore[c["name"]].wis = c["wis"]
        character.characterStore[c["name"]].vit = c["vit"]
        character.characterStore[c["name"]].weapon = c["weapon"]
        character.characterStore[c["name"]].armor = c["armor"]
        character.characterStore[c["name"]].shield = c["shield"]
        character.characterStore[c["name"]].location = c["location"]
        print character.characterStore[c["name"]]
        print "--- Loaded Character: " + c["name"]



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
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    # Decode chat message from IRC format.
    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "The portals have opened to another land in the Twitch realm! For more information, type !help.")

    loadCharacters()
    loadLocations()
    loadMonsters()

    # load up the oplist for admin commands
    thread.start_new_thread(utils.threadFillOpList, ())

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
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)
            if message.strip() == "!help":
                utils.chat(s, "Hey "+ username + "!, some commands you can use are !joingame, !showstats, !location, !movenorth, !movesouth, !moveeast, !movewest, !addstrength, !addwisdom, !addvitality, !hunt and !rest.")

            # this creates a new character for the account. Only one character is allowed per account.
            if message.strip() == "!joingame":
                    if username in character.characterStore:  # check and see if the character is already made
                        utils.chat(s, username + ", you already have a character!")
                    else:
                        # create the character and add it to the DB
                        character.characterStore[username] = character.Characters()
                        if character.characterStore[username].createCharacter(username):
                            if sql.createCharacter(character.characterStore[username]):
                                utils.chat(s, username + ", You've now created a character. Some commands you can use are !showstats, !location, !movenorth, !movesouth, !moveeast, !movewest")
                            else:
                                utils.chat(s, username + ", there was an error saving you to the database, please contact the channel admin or join the Discord for TC_RPG")

            # Obviously shows the stats for the character. Twitch doesn't have linebreaks thanks to broke ass IRC code. So wall of text it is.
            if message.strip() == "!showstats":
                # We try this, if it throws an error, most likely they don't have a character. Need to clean this up a bit.
                try:
                    utils.chat(s, "Hey " + username + ". Your stats are *** Level: " + str(character.characterStore[username].mana) + " --- XP: " + str(character.characterStore[username].currentXP) + "/" + str(character.characterStore[username].levelXP) + " --- Health: " + str(character.characterStore[username].hp) + " --- Mana: " + str(character.characterStore[username].mana) + " --- Location: " + str(location.locationStore[character.characterStore[username].location].name) + " ***")
                    print character.characterStore[username].name
                except:
                    utils.chat(s, "Hey " + username + ", you don't currently have a character registered. Type !joingame to have us create one for you!")

            if message.strip() == "!movesouth":
                if location.locationStore[character.characterStore[username].location].south > 0:
                    character.characterStore[username].location = location.locationStore[character.characterStore[username].location].south
                    utils.chat(s, username + " decides to go to the south, now you're at " + location.locationStore[character.characterStore[username].location].name)
                else:
                    utils.chat(s, username + " looks to the south but there's no where to go!")

            if message.strip() == "!movenorth":
                if location.locationStore[character.characterStore[username].location].north > 0:
                    character.characterStore[username].location = location.locationStore[character.characterStore[username].location].north
                    utils.chat(s, "You decide you want to head to the north, now you're at " + location.locationStore[character.characterStore[username].location].name)
                else:
                    utils.chat(s, username + " looks to the north but there's no where to go!")

            if message.strip() == "!moveeast":
                if location.locationStore[character.characterStore[username].location].east > 0:
                    character.characterStore[username].location = location.locationStore[
                        character.characterStore[username].location].east
                    utils.chat(s, "You decide you want to head to the north, now you're at " + location.locationStore[
                        character.characterStore[username].location].name)
                else:
                    utils.chat(s, username + " shifts their glance to the east, but there's no where to go!")

            if message.strip() == "!movewest":
                if location.locationStore[character.characterStore[username].location].west > 0:
                    character.characterStore[username].location = location.locationStore[
                        character.characterStore[username].location].west
                    utils.chat(s, "You decide you want to head to the north, now you're at " + location.locationStore[
                        character.characterStore[username].location].name)
                else:
                    utils.chat(s, username + " glances to the west, but there's no where to go!")

            if message.strip() == "!location":
                if location.locationStore[character.characterStore[username].location].location_id > 0:
                    utils.chat(s, username + " looks at their surroundings. " + location.locationStore[
                        character.characterStore[username].location].description)
                else:
                    utils.chat(s, username + " stares into the nether, seeing nothing but darkness.")

            # Players rest to heal in places without monsters
            if message.strip() == "!rest":
                if location.locationStore[character.characterStore[username].location].hasMonsters:
                    utils.chat(s, username + " looks around but think it's not exactly the best idea to rest with monsters roaming around.")
                else:
                    utils.chat(s, username + " takes a break from the burden of adventuring and gains some health.")
                    character.characterStore[username].hp += 20
                    if character.characterStore[username].hp > character.characterStore[username].maxHP:
                        character.characterStore[username].hp = character.characterStore[username].maxHP

            # Starts combat against creatures
            if message.strip() == "!hunt":
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
                        outcome = combat.fightMonster(s, monsterToFight, character.characterStore[username], username)
                        print outcome
                        utils.chat(s, outcome)

                else:
                    utils.chat(s, username + " there doesn't seem to be anything here to kill.")

            # Adds strength using a skill point
            # TODO: add option to add more than just 1 str to minimize duplicate message block
            if message.strip() == "!addstrength":
                if character.characterStore[username].skillPoints > 0:
                    character.characterStore[username].str += 1
                    character.characterStore[username].skillPoints -= 1
                    utils.chat(s, username + " just gained some strength to more easily defeat his foes.")
                else:
                    utils.chat(s, username + " just tried to gain some strength, but failed miserably due to not having enough skill.")

            # Adds wisdom using a skill point
            # TODO: add option to add more than just 1 wis to minimize duplicate message block
            if message.strip() == "!addwisdom":
                if character.characterStore[username].skillPoints > 0:
                    character.characterStore[username].wis += 1
                    character.characterStore[username].skillPoints -= 1
                    utils.chat(s, username + " just got slightly less dumb and gained some hard earned wisdom.")
                else:
                    utils.chat(s, username + " just tried to gain some wisdom, but his brain just couldn't handle it.")

            # Adds vitality using a skill point
            # TODO: add option to add more than just 1 vit to minimize duplicate message block
            if message.strip() == "!addvitality":
                if character.characterStore[username].skillPoints > 0:
                    character.characterStore[username].vit += 1
                    character.characterStore[username].skillPoints -= 1
                    utils.chat(s, username + " just gained some vitality to take some more hits like the mythical Rocky Balboa that he read about in some timetravel mages apartment.")
                else:
                    utils.chat(s, username + " just tried to be more of a meat shield, but is just too scrawny and weak.")
        sleep(1)
    utils.chat(s, "Bye everyone :)");


if __name__ == "__main__":
    main()