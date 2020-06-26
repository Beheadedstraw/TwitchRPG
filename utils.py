# utils.py
# A bunch of utility functions

import cfg
import urllib2, json
import time, thread
from time import sleep


# Function: chat
# Send a chat message to the server.
#    Parameters:
#      sock -- the socket over which to send the message
#      msg  -- the message to send

def chat(slack_client, msg, DMMode, user, chan, image=False):
    if DMMode:
        response = slack_client.api_call(
            "conversations.open",
            users=user,
            return_im=0
        )

        print "CHANNEL_ID: " + response["channel"]["id"]
        if image:
            image_response = slack_client.api_call(
                "chat.postMessage",
                channel=response["channel"]["id"],
                blocks=[{"type": "image",
                         "title": {
                             "type": "plain_text",
                             "text": "Your Location"
                         },
                        "block_id": "location",
                        "image_url": image,
                        "alt_text": "Your Location"
                        }]
            )
            print "IMAGE_RESPONSE: "
            print image_response

        slack_client.api_call(
            "chat.postMessage",
            channel=response["channel"]["id"],
            text=msg,
            link_names=1
        )

    else:
        slack_client.api_call(
            "chat.postMessage",
            channel=chan,
            text=msg,
            link_names = 1
        )



# Function: ban
# Ban a user from the channel
#   Parameters:
#       sock -- the socket over which to send the ban command
#       user -- the user to be banned
def ban(sock, user):
    chat(sock, ".ban {}".format(user))


# Function: timeout
# Timeout a user for a set period of time
#   Parameters:
#       sock -- the socket over which to send the timeout command
#       user -- the user to be timed out
#       seconds -- the length of the timeout in seconds (default 600)
def timeout(sock, user, seconds=600):
    chat(sock, ".timeout {}".format(user, seconds))


# Function: threadFillOpList
# In a separate thread, fill up the op list
def threadFillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/beheadedstraw/chatters"
            req = urllib2.Request(url, headers={"accept": "*/*"})
            response = urllib2.urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                cfg.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"]["moderators"]:
                    cfg.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    cfg.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    cfg.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    cfg.oplist[p] = "staff"
        except:
            'do nothing'
        sleep(5)


def isOp(user):
    if user in cfg.oplist:
        return True
    else:
        return False