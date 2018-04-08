import pymysql.cursors
from pymysql import MySQLError
import cfg
from time import sleep


def connect():
    try:
        connection = pymysql.connect(host=cfg.DBHOST,
                                     user=cfg.DBUSER,
                                     password=cfg.DBPASS,
                                     db=cfg.DB,
                                     cursorclass=pymysql.cursors.DictCursor)
    finally:
        return connection


def getCommands():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "select * from BotCommands"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


def getCharacters():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "select * from Characters"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


def getMonsters():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "select * from monsters"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


def createCharacter(c):
            print c.name

            try:
                connection = connect()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO characters (name, level, energy, skillPoints, hp, maxHP, currentXP, levelXP, mana, maxMana, str, wis, vit, weapon, shield, armor, inCombat, inCombatID, location, whisperMode) VALUES ('" \
                        + str(c.name) + "'," \
                        + str(c.level) + "," \
                        + str(c.energy) + "," \
                        + str(c.skillPoints) + "," \
                        + str(c.hp) + "," \
                        + str(c.maxHP) + "," \
                        + str(c.currentXP) + "," \
                        + str(c.levelXP) + "," \
                        + str(c.mana) + "," \
                        + str(c.maxMana) + "," \
                        + str(c.str) + "," \
                        + str(c.wis) + "," \
                        + str(c.vit) + "," \
                        + str(c.weapon) + "," \
                        + str(c.shield) + "," \
                        + str(c.armor) + "," \
                        + str(c.inCombat) + "," \
                        + str(c.inCombatID) + "," \
                        + str(c.location) + "," \
                        + str(c.whisperMode) + ";)"
                    print sql
                    cursor.execute(sql)

            except MySQLError as e:
                print e;

            finally:
                connection.close()
                return True


def saveCharacters(c):
    print c.name

    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "UPDATE characters SET " \
                  + "name='" + str(c.name) + "'," \
                  + "level=" + str(c.level) + "," \
                  + "energy=" + str(c.energy) + "," \
                  + "skillPoints=" + str(c.skillPoints) + "," \
                  + "currentXP=" + str(c.currentXP) + "," \
                  + "levelXP=" + str(c.levelXP) + "," \
                  + "hp=" + str(c.hp) + "," \
                  + "maxHP=" + str(c.maxHP) + "," \
                  + "mana=" + str(c.mana) + "," \
                  + "maxMana=" + str(c.maxMana) + "," \
                  + "str=" + str(c.str) + "," \
                  + "wis=" + str(c.wis) + "," \
                  + "vit=" + str(c.vit) + "," \
                  + "weapon=" + str(c.weapon) + "," \
                  + "shield=" + str(c.shield) + "," \
                  + "armor=" + str(c.armor) + "," \
                  + "inCombat=" + str(c.inCombat) + "," \
                  + "inCombatID=" + str(c.inCombatID) + "," \
                  + "location=" + str(c.location) + "," \
                  + "whisperMode=" + str(c.whisperMode) + " " \
                  + "WHERE name = '" + str(c.name) + "';"

            cursor.execute(sql)
    except MySQLError as e:
        print e;

    finally:
        connection.close()
        return True

def autosaveCharacters(char):
    try:
        while True:
            for key, value in char.iteritems():
                c = value
                saveCharacters(c)
                print "AutoSaved: " + value.name
            sleep(30)
    except:
        pass

def getLocations():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "select * from Locations"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


def getMonstersByLevel(minLevel, maxLevel):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "select * from monsters WHERE level >= " + str(minLevel) + " AND level <= " + str(maxLevel)
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


def getPlayersAtLocation(location):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "select * from characters WHERE location=" + str(location)
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

