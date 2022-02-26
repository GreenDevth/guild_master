from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config

db = read_db_config()


def players_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_mission(mission_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT mission_name FROM scum_mission_name WHERE mission_id = %s', (mission_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def hunter_mission():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_mission WHERE MISSION_AWARD = 1000;')
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def fishing_mission():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_mission WHERE MISSION_AWARD = 1500;')
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def famer_mission():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_mission WHERE MISSION_AWARD = 500;')
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def mission_check(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT MISSION FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def players_mission(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT MISSION_NAME FROM scum_players_mission WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def players_mission_channel(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT MISSION_CHANNEL FROM scum_players_mission WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def players_new_mission(discord_id, discord_name, mission_name, mission_award):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO scum_players_mission(DISCORD_ID, DISCORD_NAME, MISSION_NAME, MISSION_STATUS, MISSION_AWARD) '
            'VALUES (%s,%s,%s,%s,%s)',
            (discord_id, discord_name, mission_name, 1, mission_award,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def players_update_report_misson(mission_channel, discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players_mission SET MISSION_CHANNEL = %s WHERE DISCORD_ID = %s ',
                    (mission_channel, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def check_players_mission(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_players_mission WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_players_mission(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_players_mission WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)


def get_img_from_mission(mission_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT MISSION_IMG FROM scum_mission WHERE MISSION_NAME =%s', (mission_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
