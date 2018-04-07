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


def saveCharacters(c):
            print c.name

            try:
                connection = connect()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO Characters (name, level, hp, mana, str, wis, vit, weapon, shield, armor, inCombat, inCombatID) VALUES ('" \
                        + str(c.name) + "'," \
                        + str(c.level) + "'," \
                        + str(c.hp) + "," \
                        + str(c.mana) + "," \
                        + str(c.str) + "," \
                        + str(c.wis) + "," \
                        + str(c.vit) + "," \
                        + str(c.weapon) + "," \
                        + str(c.shield) + "," \
                        + str(c.armor) + "," \
                        + str(c.inCombat) + "," \
                        + str(c.inCombatID) + ");"
                    print sql
                    cursor.execute(sql)

            finally:
                connection.close()
                return True


def saveCharacters(c):
    print c.name

    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "UPDATE Characters SET " \
                  + "name='" + str(c.name) + "'," \
                  + "level=" + str(c.level) + "," \
                  + "hp=" +str(c.hp) + "," \
                  + "mana=" + str(c.mana) + "," \
                  + "str=" + str(c.str) + "," \
                  + "wis=" + str(c.wis) + "," \
                  + "vit=" + str(c.vit) + "," \
                  + "weapon=" + str(c.weapon) + "," \
                  + "shield=" + str(c.shield) + "," \
                  + "armor=" + str(c.armor) + "," \
                  + "inCombat=" + str(c.inCombat) + "," \
                  + "inCombatID=" + str(c.inCombatID) + ");"
            print sql
            cursor.execute(sql)

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
            sleep(60)
    except:
        pass


