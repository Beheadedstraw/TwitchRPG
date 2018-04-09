# commands.py
# Commands get processed here.
import utils


def toggleWhisper(s, username, character):
    if character.whisperMode == 0:
        character.whisperMode = 1
        utils.chat(s,
                    username + " whisper mode has been enabled.",
                    character.whisperMode, username)

    else:
        character.whisperMode = 0
        utils.chat(s,
                    username + " whisper mode has been disabled.",
                    character.whisperMode, username)


def showEquipment(s, user, character, items):
    print items
    utils.chat(s,
               user + " your equipment you're using is -- Weapon: " + items[character.weapon].name + " --- Armor: " + items[character.armor].name + " --.",
               character.whisperMode, user)


def showWeapon(s, username, character, items):
    print items
    utils.chat(s,
               username + " Weapon Info --- Name:  " + items[character.weapon].name + " -- Description: " + items[character.weapon].desc + " -- Damage: " + str(items[character.weapon].damage) + " --.",
               character.whisperMode, username)


def showArmor(s, username, character, items):
    print items
    utils.chat(s,
               username + " Armor Info --- Name:  " + items[character.armor].name + " -- Description: " + items[character.armor].desc + " -- Armor Rating: " + str(items[character.armor].armor) + " --.",
               character.whisperMode, username)


def showShield(s, username, character, items):
    print items
    utils.chat(s,
               username + " ---Shield Info:--- Name:  " + items[character.shield].name + "``` ```Description: " + items[character.shield].desc + "``` ```Armor Rating: " + str(items[character.shield].armor) + "```",
               character.whisperMode, username)


def showInventory(s, username, character, items):
    print items
    inventoryText = ""
    tempInv = str(character.inventory).split(',')
    print tempInv

    for i in tempInv:
        if items[int(i)].id == character.weapon or items[int(i)].id == character.armor or items[int(i)].id == character.shield:
            inventoryText += "*** (" + str(i) +")(Equipped)" + items[int(i)].name + " "
        else:
            inventoryText += "*** (" + str(i) + ")" + items[int(i)].name + " "

    utils.chat(s,
               username + " --- Inventory:  " + inventoryText,
               character.whisperMode, username)
