# bot.py
# Main loop for the bot.

import cfg
import utils
import sql
import socket
import re
import time, _thread
from time import sleep
import characters as character
import locations as location
import monsters as monster
import random
import combat
import commands as command
import items as item
import discord
import asyncio
from discord.ext.commands import Bot


utils = utils.Utils()

client = discord.Client()
utils.client = client
bot = Bot(command_prefix='!')
background_task_loop = asyncio.new_event_loop()

global channel

@client.event
async def on_ready():
    global channel
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    channel = client.get_channel(328026310209175553)
    utils.channel = channel

    start_threads()
    await utils.chat(channel, "The portals have opened to another land in the slack realm! For more information, type !help.")

@client.event
async def on_message(message):
    if message.author.name == "SlackRPG":
        pass
    else:
        await utils.chat(channel, "Giving Energy now.")

def start_threads():
    # Start the autosaving thread to save characters to DB every 60 seconds
    _thread.start_new_thread(sql.autosaveCharacters, (character.characterStore,))

@client.event
async def on_message(message):
    if message.author.name == "DiscordRPG":
        pass
    else:
        #await utils.chat(channel, "Giving Energy now.")
        # Networking functions\
        i = 1 ## Backwards compat with twitch


        # load up username of message sender
        username = str(message.author.name).lower()
        chan = message.channel

        # Main logic loop
        # splits the message so we can detect if there's a number to add for certain commands.
        message_text = message.content
        print (message_text)
        if " " in message_text:
            message = str(message_text).split(" ")
        else:
            message = []
            message.insert(0,message_text)

        print (message[0].strip())

        if message[0].strip() == "!help":
            await utils.chat(chan, "Hey "+ username + "!, some commands you can use are: \n!joingame, \n!stats, \n!location [additional], \n!north, \n!south, \n!east, \n!west, \n!addstrength, \n!addwisdom, \n!addvitality, \n!hunt, \n!toggleWhisper, \n!rest, \n!inventory, \n!equipment, \n!equip [inventory slot number], \n!unequip [weapon/armor/shield]")
            # TODO: Flesh out the help command to take additional argument for per command usage.
        # this creates a new character for the account. Only one character is allowed per account.
        if message[0].strip() == "!joingame":
                if username in character.characterStore:  # check and see if the character is already made
                    await utils.chat(s, username + ", you already have a character!", character.characterStore[username].whisperMode, username, chan)
                else:
                    # create the character and add it to the DB
                    character.characterStore[username] = character.Characters()
                    if character.characterStore[username].createCharacter(username):
                        if sql.createCharacter(character.characterStore[username]):
                            await utils.chat(s, username + ", You've now created a character. Some commands you can use are !help ,!stats, !location, !north, !south, !east, !west", character.characterStore[username].whisperMode, username, chan)
                        else:
                            await utils.chat(s, username + ", there was an error saving you to the database, please contact the channel admin or join the Discord for TC_RPG", character.characterStore[username].whisperMode, username, chan)


client.run('NTk5NDI5MzA5MDE0MzQzNzAz.XSlE4g.7nE7EzTwf8RWImnEOV9hnnZ9FZg')
s = 0