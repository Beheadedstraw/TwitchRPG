# bot.py
# The code for our bot

import cfg
import utils
import sql
import socket
import re
import time, thread
from time import sleep
import characters as character


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
    utils.chat(s, "Hi everyone!")

    thread.start_new_thread(utils.threadFillOpList, ())

    # Load up all of the characters
    tempChar = sql.getCharacters()
    for c in tempChar:
        character.characterStore[c["name"]] = character.Characters()
        character.characterStore[c["name"]].name = c["name"]
        character.characterStore[c["name"]].level = c["level"]
        character.characterStore[c["name"]].hp = c["hp"]
        character.characterStore[c["name"]].mana = c["mana"]
        character.characterStore[c["name"]].str = c["str"]
        character.characterStore[c["name"]].wis = c["wis"]
        character.characterStore[c["name"]].vit = c["vit"]
        character.characterStore[c["name"]].weapon = c["weapon"]
        character.characterStore[c["name"]].armor = c["armor"]
        character.characterStore[c["name"]].shield = c["shield"]

        print "Loaded Character: " + c["name"]

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
                utils.chat(s, "This is the help command " + username.strip() + ".")

            # this creates a new character for the account. Onnly one characer is allowed per account.
            if message.strip() == "!joingame":
                    if username in character.characterStore:  # check and see if the character is already made
                        utils.chat(s, username + ", you already have a character!")
                    else:
                        # create the character and add it to the DB
                        character.characterStore[username] = character.Characters()
                        if character.characterStore[username].createCharacter(username):
                            c = character.characterStore[username]
                            if sql.saveCharacters(c):
                                utils.chat(s, username + ", You've now created a character. Some commands you can use are '!showstats'")
                            else:
                                utils.chat(s, username + ", there was an error saving you to the database, please contact the channel admin or join the Discord for TC_RPG")

            # Obviously shows the stats for the character. Twitch doesn't have linebreaks thanks to broke ass IRC code. So wall of text it is.
            if message.strip() == "!showstats":
                # We try this, if it throws an error, most likely they don't have a character. Need to clean this up a bit.
                try:
                    utils.chat(s, "Hey " + username + ". Your stats are *** Level: " + str(character.characterStore[username].mana) + " --- Health: " + str(character.characterStore[username].hp) + " --- Mana: " + str(character.characterStore[username].mana) + " ***")
                    print character.characterStore[username].name
                except:
                    utils.chat(s, "Hey " + username + ", you don't currently have a character registered. Type !joingame to have us create one for you!")

        sleep(1)
    utils.chat(s, "Bye everyone :)");


if __name__ == "__main__":
    main()