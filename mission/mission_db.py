from numpy import random

from db.players_db import *


def get_mission(id_mission):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT mission_name FROM scum_mission_name WHERE mission_id =%s', (id_mission,))
        row = cur.fetchall()
        while row is not None:
            res = list(row)
            return res
    except Error as e:
        print(e)


def new_mission(discord_id, discord_name, mission_name, award):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_guild_mission(discord_id, discord_name, mission_name, award) VALUES (%s,%s,%s,%s)'
        cur.execute(sql, (discord_id, discord_name, mission_name, award))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def mission_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COUNT(*) FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_image_status(discord_id):
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


def update_image_status(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_guild_mission SET image_status = 1 WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
        cur.close()
        msg = "ระบบได้ส่งรายงานภารกิจไปยังทีมงานแอดมินเป็นที่เรียบร้อยแล้ว"
        return msg.strip()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def get_channel_id(discord_id):
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


def channel_id_update(discord_id, code):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_guild_mission SET channel_id = %s WHERE discord_id = %s'
        cur.execute(sql, (code, discord_id,))
        conn.commit()
        cur.close()

    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def get_mission_name(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT mission_name FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def generate_code():
    x = random.randint(9, 99999)
    return x


def mission_id(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT mission_id FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def mission_award(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT award FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def mission_solf_reset(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'DELETE FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
        cur.close()
        msg = 'ทำการรีเซ็ตภารกิจของคุณเรียบร้อยแล้ว ขอให้สนุกกับภารกิจใหม่ กำลังทำการปิดระบบใน 10 วินาที'
        return msg.strip()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def mission_hard_reset(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'DELETE FROM scum_guild_mission WHERE discord_id = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
        cur.close()
        msg = 'ทำการรีเซ็ตภารกิจของคุณเรียบร้อยแล้ว ขอให้สนุกกับภารกิจใหม่'
        return msg.strip()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
