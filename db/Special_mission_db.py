from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config

db = read_db_config()


def get_mission(mission_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_special_mission where MISSION_ID = %s', (mission_id,))
        row = cur.fetchone()
        return row
    except Error as e:
        print(e)


def get_mission_id():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select MISSION_ID from scum_special_mission')
        res = [item[0] for item in cur.fetchall()]
        return res
    except Error as e:
        print(e)


def players_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(STEAM_ID) from scum_players where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        return row
    except Error as e:
        print(e)
        return False


def players_mission_ready(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select MISSION from scum_players where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)
        return False


def get_player_mission(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_special_events where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res
    except Error as e:
        print(e)
        return False


def check_mission_ready(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from scum_special_events where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)
        return False


def delete_mission(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_special_events SET MISSION_STATUS = 0 WHERE DISCORD_ID=%s', (discord_id,))
        conn.commit()
        cur.execute('UPDATE scum_players SET MISSION = 0 WHERE DISCORD_ID=%s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return False


def get_players_info(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_players WHERE DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res
    except Error as e:
        print(e)


def get_mission_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select MISSION_STATUS from scum_special_events where DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
