from db.players_db import *


def new_mission(discord_id, discord_name, mission_name, image_status, channel_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_guild_mission(discord_id, discord_name, mission_name, image_status, channel_id)' \
              'VALUES (%s,%s,%s,%s,%s)'
        cur.execute(sql, (discord_id, discord_name, mission_name, image_status, channel_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def image_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT image_status FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def channel_id(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT channel_id FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
