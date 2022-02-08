from mysql.connector import MySQLConnection, Error

from db.db_config import read_db_config

db = read_db_config()


def players_exists(discord_id):
    """ Check register players """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COUNT(*) FROM scum_players WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def player(discord_id):
    """ Get player information """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT * FROM scum_players WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res
    except Error as e:
        print(e)


def exp_up(discord_id, exp):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET EXP = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (exp, discord_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def level_up(discord_id, level):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET LEVEL = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (level, discord_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def coin_up(discord_id, coin):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (coin, discord_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def coin_down(discord_id, coin):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (coin, discord_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def mission_up(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET MISSION = 1 WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def mission_reset(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET MISSION = 0 WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()