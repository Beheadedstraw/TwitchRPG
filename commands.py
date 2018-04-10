# commands.py
# Commands get processed here.
import utils


def toggleWhisper(s, username, character, chan):
    if character.whisperMode == 0:
        character.whisperMode = 1
        utils.chat(s,
                    username + " whisper mode has been enabled.",
                    character.whisperMode, username, chan)

    else:
        character.whisperMode = 0
        utils.chat(s,
                    username + " whisper mode has been disabled.",
                    character.whisperMode, username, chan)


def showEquipment(s, user, character, items, chan):
    print items
    if character.weapon == 0:
        weapon = "Nothing."
    else:
        weapon = items[character.weapon].name

    if character.armor == 0:
        armor = "Nothing."
    else:
        armor = items[character.armor].name

    if character.shield == 0:
        shield = "Nothing."
    else:
        shield = items[character.shield].name

    utils.chat(s,
               user + " your equipment you're using is -- Weapon: " + weapon + " || Armor: " + armor + " || Shield: " + shield + "--.",
               character.whisperMode, user, chan)


def showWeapon(s, username, character, items, chan):
    print items
    utils.chat(s,
               username + " Weapon Info: --- Name:  " + items[character.weapon].name + " -- Description: " + items[character.weapon].desc + " -- Damage: " + str(items[character.weapon].damage) + " ---.",
               character.whisperMode, username, chan)


def showArmor(s, username, character, items, chan):
    print items
    utils.chat(s,
               username + " Armor Info: --- Name:  " + items[character.armor].name + " -- Description: " + items[character.armor].desc + " -- Armor Rating: " + str(items[character.armor].armor) + " ---.",
               character.whisperMode, username, chan)


def showShield(s, username, character, items, chan):
    print items
    utils.chat(s,
               username + " Shield Info: --- Name:  " + items[character.shield].name + " -- Description: " + items[character.shield].desc + " -- Armor Rating: " + str(items[character.shield].armor) + "---",
               character.whisperMode, username, chan)


def showInventory(s, username, character, items, chan):
    print items
    inventoryText = ""
    tempInv = str(character.inventory).split(',')
    print tempInv

    for i in tempInv:
        if items[int(i)].id == character.weapon or items[int(i)].id == character.armor or items[int(i)].id == character.shield:
            inventoryText += "|| (" + str(i) +")(Equipped)" + items[int(i)].name + " "
        else:
            inventoryText += "|| (" + str(i) + ")" + items[int(i)].name + " "

    utils.chat(s,
               username + " --- Inventory:  " + inventoryText,
               character.whisperMode, username, chan)


def unequipWeapon(s, username, character, chan):

    if character.weapon == 0:
        utils.chat(s, username + " you already don't have a weapon equipped!",character.whisperMode, username, chan)
    else:
        character.weapon = 0
        utils.chat(s, username + " you take your weapon and you stash it in your magical semi-bottomless bag.",character.whisperMode, username, chan)


def unequipArmor(s, username, character, chan):
    if character.armor == 0:
        utils.chat(s, username + " you already don't have any armor equipped!", character.whisperMode, username, chan)
    else:
        character.armor = 0
        utils.chat(s, username + " you take your armor and you somehow manage to fit the whole bulk of it in your bottomless bad, you're basically naked now you dirty dog you!", character.whisperMode, username, chan)


def unequipShield(s, username, character, chan):
    if character.shield == 0:
        utils.chat(s, username + " you already don't have a shield equipped!", character.whisperMode, username, chan)
    else:
        character.shield = 0
        utils.chat(s, username + " you take your shield and shove it in your bottomless bag.", character.whisperMode, username, chan)


def equipItem(s, username, character, items, itemToEquip, chan):
    inventory = character.inventory.split(',')

    print inventory
    print itemToEquip

    try:
        if str(itemToEquip) in inventory and int(items[itemToEquip].type) == 2:  # is an weapon
            if character.weapon == 0:
                character.weapon = itemToEquip
                utils.chat(s, username + " you equipped the " + items[itemToEquip].name + "!", character.whisperMode, username, chan)
            else:
                utils.chat(s, username + " you already have a weapon equipped!", character.whisperMode, username, chan)

        elif str(itemToEquip)in inventory and int(items[itemToEquip].type) == 1:  # is a armor
            if character.armor == 0:
                character.armor = itemToEquip
                utils.chat(s, username + " you equipped the " + items[itemToEquip].name + "!", character.whisperMode, username, chan)
            else:
                utils.chat(s, username + " you already have armor equipped!", character.whisperMode, username, chan)

        elif str(itemToEquip) in inventory and int(items[itemToEquip].type) == 3:  # is a shield
            if character.shield == 0:
                utils.chat(s, username + " you equipped the " + items[itemToEquip].name + "!", character.whisperMode, username, chan)
                character.shield = itemToEquip
            else:
                utils.chat(s, username + " you already have a shield equipped!", character.whisperMode, username, chan)

        elif int(items[itemToEquip].type) > 3:
            utils.chat(s, username + " you can't equip that item!", character.whisperMode, username, chan)

    except KeyError:
        utils.chat(s, username + " that item isn't in your inventory!", character.whisperMode, username, chan)


