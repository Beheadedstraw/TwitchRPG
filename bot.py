# -*- coding: utf-8 -*-
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
import monsters as monster
import random
import combat
import commands as command
import items as item
from slackclient import SlackClient, im
import logging, sys
reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig()
# SlackRPG token
#slack_client = SlackClient("xoxb-1181626063335-1191204522711-RyTDywZOmBn1nFkDz39uVypz")

#Peak6 Token
slack_client = SlackClient("xoxb-2471115697-1199711534550-CiE97XRiy8hg7Kzp0SWY2kOy")
starterbot_id = None
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


# Loads up all of the monsters from the DB
def loadMonsters():
    # Load up all of the monsters
    print "--------------------------"
    print "---  LOADING MONSTERS  ---"
    print "--------------------------"

    tempMonsters = sql.getMonsters()

    for m in tempMonsters:
        monster.monsterStore[m["name"]] = monster.Monsters()
        monster.monsterStore[m["name"]].name = m["name"]
        monster.monsterStore[m["name"]].level = m["level"]
        monster.monsterStore[m["name"]].hp = m["hp"]
        monster.monsterStore[m["name"]].damage = m["damage"]
        monster.monsterStore[m["name"]].xp = m["xp"]
        monster.monsterStore[m["name"]].money = m["money"]
        monster.monsterStore[m["name"]].loot = m["loot"]
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
        character.characterStore[c["name"]].money = c["money"]
        character.characterStore[c["name"]].recalculateStats(item.itemStore)
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
        item.itemStore[i["id"]].trade_value = i["trade_value"]
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
        location.locationStore[l["location_id"]].image = l["image"]
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
        #for channel in cfg.CHAN:
            #utils.chat(s, "Adventurers in the realm feel a little more energetic!", False, None, channel)
        sleep(60)


def main():
    print "Connecting to Slack as SlackRPG"
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        print "STARTER BOT ID: " + starterbot_id
        s = slack_client
        '''
        # Networking functions
        
        s.connect((cfg.HOST, cfg.PORT))
        s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
        s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
        s.send("JOIN #{}\r\n".format(cfg.CHAN[0]).encode("utf-8"))
        s.send("JOIN #{}\r\n".format(cfg.CHAN[1]).encode("utf-8"))
    
        # Decode chat message from IRC format.
        
        for i in cfg.CHAN:
            utils.chat(s, "The portals have opened to another land in the Slack realm! For more information, type @SlackRPG !help.", False, None, i)
        '''
        for channel in cfg.CHAN:
            utils.chat(s,
                       "The portals have opened to another land in the Twitch realm! For more information, type !help.",
                       False, None, channel)

        loadLocations()
        loadItems()
        loadCharacters()
        loadMonsters()

        # load up the oplist for admin commands
        thread.start_new_thread(utils.threadFillOpList, ())

        # start the thread to give energy every 60 seconds
        thread.start_new_thread(giveEnergy, (s,))

        # Start the autosaving thread to save characters to DB every 60 seconds
        thread.start_new_thread(sql.autosaveCharacters, (character.characterStore,))

        # Main logic loop
        while True:
            CHAT_MSG, chan, username = parse_bot_commands(slack_client.rtm_read())
            response = CHAT_MSG
            # Respond to ping request to stay alive on the server
            if response:
                # Here we process the different commands
                print "COMMAND WAS MESSAGE:" + CHAT_MSG + " CHANNEL:" + chan + " USER:" + username


                message = CHAT_MSG
                print "--- MESSAGE NOT STRIPPED: " + message
                print "--- MESSAGE NOT STRIPPED: " + message.strip()

                # splits the message so we can detect if there's a number to add for certain commands.
                message = message.split(" ")

                try:
                    char = character.characterStore[username]
                except:
                    pass

                if message[0].strip() == "!help":
                    utils.chat(s, "Hey <@" + username + ">!, some commands you can use are !joingame, !stats, !location [additional], !north, !south, !east, !west, !addstrength, !addwisdom, !addvitality, !hunt, !toggleWhisper, !rest, !inventory, !equipment, !equip [inventory slot number], !unequip [weapon/armor/shield]", True, username, chan)
                    # TODO: Flesh out the help command to take additional argument for per command usage.
                # this creates a new character for the account. Only one character is allowed per account.
                if message[0].strip() == "!joingame":
                        if username in character.characterStore:  # check and see if the character is already made
                            utils.chat(s, "<@" + username + ">, you already have a character!", True, username, chan)
                        else:
                            # create the character and add it to the DB
                            character.characterStore[username] = character.Characters()
                            if character.characterStore[username].createCharacter(username):
                                if sql.createCharacter(character.characterStore[username]):
                                    utils.chat(s, "<@" + username + ">, You've now created a character. Some commands you can use are !help ,!stats, !location, !north, !south, !east, !west", True, username, chan)
                                else:
                                    utils.chat(s, "<@" + username + ">, there was an error saving you to the database, please contact the channel admin or join the Discord for TC_RPG", True, username, chan)

                # Obviously shows the stats for the character. Twitch doesn't have linebreaks thanks to broke ass IRC code. So wall of text it is.
                if message[0].strip() == "!stats":
                    # We try this, if it throws an error, most likely they don't have a character. Need to clean this up a bit.
                    try:
                        print
                        utils.chat(s, "Hey <@" + username + ">. Your stats are:"\
                                     "\n• Level: " + str(character.characterStore[username].level) \
                                   + "\n• XP: " + str(character.characterStore[username].currentXP) + "/" + str(character.characterStore[username].levelXP) \
                                   + "\n• Health: " + str(character.characterStore[username].hp) + "/" + str(character.characterStore[username].maxHP) \
                                   + "\n• Mana: " + str(character.characterStore[username].mana) + "/" + str(character.characterStore[username].mana) \
                                   + "\n• Energy: " + str(character.characterStore[username].energy) \
                                   + "\n• Money: " + str(character.characterStore[username].money) \
                                   + "\n• Skill Points: " + str(character.characterStore[username].skillPoints) \
                                   + "\n• Location: " + str(location.locationStore[character.characterStore[username].location].name) \
                                   + ".", True, username, chan)
                        print character.characterStore[username].name
                    except:
                        utils.chat(s, "Hey " + username + ", you don't currently have a character registered. Type !joingame to have us create one for you!", True, username, chan)

                if message[0].strip() == "!south":
                    if location.locationStore[character.characterStore[username].location].south > 0:
                        character.characterStore[username].location = location.locationStore[character.characterStore[username].location].south
                        utils.chat(s, "<@" + username + "> decides to go to the south, now you're at " + location.locationStore[character.characterStore[username].location].name, True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> looks to the south but there's no where to go!", True, username, chan)

                if message[0].strip() == "!north":
                    if location.locationStore[character.characterStore[username].location].north > 0:
                        character.characterStore[username].location = location.locationStore[character.characterStore[username].location].north
                        utils.chat(s, "You decide you want to head to the north, now you're at " + location.locationStore[character.characterStore[username].location].name, True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> looks to the north but there's no where to go!", True, username, chan)

                if message[0].strip() == "!east":
                    if location.locationStore[character.characterStore[username].location].east > 0:
                        character.characterStore[username].location = location.locationStore[
                            character.characterStore[username].location].east
                        utils.chat(s, "You decide you want to head to the east, now you're at " + location.locationStore[character.characterStore[username].location].name, True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> shifts their glance to the east, but there's no where to go!", True, username, chan)

                if message[0].strip() == "!west":
                    if location.locationStore[character.characterStore[username].location].west > 0:
                        character.characterStore[username].location = location.locationStore[
                            character.characterStore[username].location].west
                        utils.chat(s, "You decide you want to head to the west, now you're at " + location.locationStore[
                            character.characterStore[username].location].name, True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> glances to the west, but there's no where to go!", True, username, chan)

                if message[0].strip() in ('!location', '!look'):
                    text = ""
                    if len(message) > 1:
                        print message
                        if message[1].strip() == "players":
                            playersAtLocation = sql.getPlayersAtLocation(character.characterStore[username].location)
                            print playersAtLocation
                            if len(playersAtLocation) > 1:
                                for p in playersAtLocation:
                                    text += "• <@" + p["name"] + "> \n "
                                utils.chat(s, "<@" + username + "> the current players in the same location are:\n " + text, True, username, chan)
                            else:
                                utils.chat(s, "<@" + username + "> you're all alone...", True, username, chan)
                        else:
                            utils.chat(s, "<@" + username + "> I didn't quite understand that.", True, username, chan)
                    else:
                        if location.locationStore[character.characterStore[username].location].location_id > 0:
                            utils.chat(s, "<@" + username + "> looks at their surroundings. " + location.locationStore[char.location].description, True, username, chan, image=location.locationStore[char.location].image)
                        else:
                            utils.chat(s, "<@" + username + "> stares into the nether, seeing nothing but darkness.", True, username, chan)

                # Players rest to heal in places without monsters
                if message[0].strip() == "!rest":
                    if location.locationStore[character.characterStore[username].location].hasMonsters:
                        utils.chat(s, "<@" + username + "> looks around but think it's not exactly the best idea to rest with monsters roaming around.", True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> takes a break from the burden of adventuring and gains some health.", True, username, chan)
                        character.characterStore[username].hp += 20
                        if character.characterStore[username].hp > character.characterStore[username].maxHP:
                            character.characterStore[username].hp = character.characterStore[username].maxHP

                # Starts combat against creatures
                if message[0].strip() == "!hunt":
                    print character.characterStore[username].energy
                    char = character.characterStore[username]
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

                                if char.weapon == 0:
                                    weapon = 0
                                else:
                                    weapon = item.itemStore[char.weapon]

                                if char.armor == 0:
                                    armor = 0
                                else:
                                    armor = item.itemStore[char.armor]

                                if char.shield == 0:
                                    shield = 0
                                else:
                                    shield = item.itemStore[char.shield]

                                outcome = combat.fightMonster(s, monsterToFight, char, username, weapon, armor, shield, item.itemStore)
                                # print outcome
                                utils.chat(s, outcome, True, username, chan)
                                removeEnergy(1, username)
                        else:
                            utils.chat(s, "<@" + username + "> there doesn't seem to be anything here to kill.", True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> tries to go and kill stuff, but takes a nap instead due to being completely out of of energy.", True, username, chan)

                # Adds strength using a skill point
                if message[0].strip() == "!addstrength":
                    if character.characterStore[username].skillPoints > 0:
                        try:
                            if len(message) > 1:
                                message_amount = int(message[1])

                                if message_amount <= character.characterStore[username].skillPoints:
                                    character.characterStore[username].skillPoints -= message_amount
                                    utils.chat(s, "<@" + username + "> just gained some strength to more easily defeat his foes.", True, username, chan)
                                else:
                                     utils.chat(s, "<@" + username + "> you don't have enough skillpoints!", True, username, chan)
                            else:
                                utils.chat(s, "<@" + username + "> looks like you wanted to add some strength, but wasn't quite sure how much. Please use !addstrength amount (ex: !addstrength 5).", True, username, chan)
                        except ValueError:
                            utils.chat(s, "<@" + username + "> you entered a wrong value, please make sure it's a number.", True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> just tried to gain some strength, but failed miserably due to not having enough skill.", True, username, chan)

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

                # Sells and item
                if message[0].strip() == "!sell":
                    print location.locationStore[char.location].hasMonsters
                    if location.locationStore[char.location].hasMonsters == 0:
                        try:
                            if len(message[1]) >= 1:
                                command.sellItem(s, username, character.characterStore[username], item.itemStore, int(message[1].strip()), chan)
                            else:
                                utils.chat(s, "<@" + username + "> we didn't quite catch what you wanted to sell. Use the item number in () when using !inventory to sell that item to the merchant.", char.whisperMode, username, chan)
                        except ValueError as e:
                            utils.chat(s, "<@" + username + "> you entered a wrong value, please make sure it's a number and that you actually, you know, have the item.", True, username, chan)
                            print e
                        except IndexError as e:
                            utils.chat(s,"<@" + username + "> you entered a wrong value, please make sure it's a number and that you actually, you know, have the item.",True, username, chan)
                    else:
                        utils.chat(s, "<@" + username + "> there isn't a merchant at this location.", True, username, chan)

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
                                        utils.chat(s, "<@" + username + "> just got slightly less dumb and gained some hard earned wisdom.", True, username, chan)
                                    else:
                                        utils.chat(s, "<@" + username + "> you don't have enough skillpoints!", True, username, chan)
                                else:
                                    utils.chat(s, "<@" + username + "> you need to specify how many you wan to add!", True, username, chan)
                            finally:
                                pass
                        else:
                            utils.chat(s, "<@" + username + "> just tried to gain some wisdom, but his brain just couldn't handle it.", True, username, chan)
                    except ValueError:
                        utils.chat(s, "<@" + username + "> you entered a wrong value, please make sure it's a number.", True, username, chan)

                # Adds vitality using a skill point
                if message[0].strip() == "!addvitality":
                    try:
                        if character.characterStore[username].skillPoints > 0:
                                if len(message) > 1:
                                    message_amount = int(message[1])
                                    if message_amount <= character.characterStore[username].skillPoints:
                                        character.characterStore[username].vit += 1
                                        character.characterStore[username].skillPoints -= 1
                                        character.Characters.recalculateStats()
                                        utils.chat(s, "<@" + username + "> just gained some vitality to take some more hits like the mythical Rocky Balboa that he read about in some timetravel mages apartment.", True, username, chan)
                                    else:
                                        utils.chat(s, "<@" + username + "> you don't have enough skillpoints!", True, username, chan)
                                else:
                                    utils.chat(s, "<@" + username + "> you need to specify how many.", True, username, chan)
                        else:
                            utils.chat(s, "<@" + username + "> just tried to be more of a meat shield, but is just too scrawny and weak.", True, username, chan)
                    except ValueError:
                        utils.chat(s, "<@" + username + "> you entered a wrong value, please make sure it's a number.", True, username, chan)

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
                                utils.chat(s, "<@" + username + "> we didn't quite catch what you wanted to unequip. Did you want to !unequip your weapon, armor, or shield?", True, username, chan)
                        else:
                            utils.chat(s, "<@" + username + "> we didn't quite catch what you wanted to unequip. Did you want to !unequip your weapon, armor, or shield?", True, username, chan)
                    except ValueError:
                        utils.chat(s, "<@" + username + "> you entered a wrong value, please make sure it's a number.", True, username, chan)

                if message[0].strip() == "!equip":
                    try:
                        if len(message) > 1 and int(message[1]):
                            command.equipItem(s, username, character.characterStore[username], item.itemStore, int(message[1].strip()), chan)
                        else:
                            utils.chat(s, "<@" + username + "> we didn't quite catch what you wanted to equip. Use the item number in () when using !inventory to equip that item.", char.whisperMode, username, chan)
                    except ValueError:
                        utils.chat(s, "<@" + username + "> you entered a wrong value, please make sure it's a number.", True, username, chan)

                if message[0].strip() == "!reload":
                    try:
                        if len(message) > 1:
                            if message[1].strip() == "characters":
                                character.characterStore.clear()
                                loadCharacters()
                                utils.chat(s, "<@" + username + "> all characters have been reloaded.", False, username, chan)

                            if message[1].strip() == "items":
                                item.itemStore.clear()
                                loadItems()
                                utils.chat(s, "<@" + username + "> all items have been reloaded.", False, username, chan)

                            if message[1].strip() == "monsters":
                                monster.monsterStore.clear()
                                loadMonsters()
                                utils.chat(s, "<@" + username + "> all monsters have been reloaded.", False, username, chan)

                            if message[1].strip() == "locations":
                                location.locationStore.clear()
                                loadLocations()
                                utils.chat(s, "<@" + username + "> all locations have been reloaded.", False, username, chan)
                        else:
                            utils.chat(s, "<@" + username + "> we didn't quite catch what you wanted to reload master.", False, username, chan)
                    except ValueError:
                        utils.chat(s, "<@" + username + "> you entered a wrong value, please make sure it's either characters, locations, items, or monsters.", True, username, chan)
            sleep(0.5)
        utils.chat(s, "Bye everyone :)");

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    #print slack_events
    for event in slack_events:
        #print event
        if event["type"] == "message" and not "subtype" in event:
            #user_id, message = parse_direct_mention(event["text"])
            #if user_id == starterbot_id:
            return event['text'], event["channel"], event["user"]
    return None, None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    #return (matches.group(1), matches.group(2).strip()) if matches else (None, None)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

if __name__ == "__main__":
      main()