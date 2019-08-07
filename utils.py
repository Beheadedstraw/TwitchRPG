# utils.py
# A bunch of utility functions

import cfg
import urllib3, json
import time, _thread
from time import sleep
import discord


class Utils:
    # Function: chat
    # Send a chat message to the server.
    #    Parameters:
    #      sock -- the socket over which to send the message
    #      msg  -- the message to send
    def __init__(self):
        self.client = None
        self.channel = None

    async def chat(self, channel, message):
        # msg = 'Hello {0.author.mention}'.format(channel)
        await channel.send(message)


    # Function: ban
    # Ban a user from the channel
    #   Parameters:
    #       sock -- the socket over which to send the ban command
    #       user -- the user to be banned
    def ban(self, sock, user):
        pass
        #chat(sock, ".ban {}".format(user))


    # Function: timeout
    # Timeout a user for a set period of time
    #   Parameters:
    #       sock -- the socket over which to send the timeout command
    #       user -- the user to be timed out
    #       seconds -- the length of the timeout in seconds (default 600)
    def timeout(self, sock, user, seconds=600):
        pass
        # chat(sock, ".timeout {}".format(user, seconds))


    # Function: threadFillOpList
    # In a separate thread, fill up the op list

    def isOp(self, user):
        if user in cfg.oplist:
            return True
        else:
            return False