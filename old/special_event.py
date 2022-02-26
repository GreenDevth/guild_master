from db.players_db import db, MySQLConnection, Error
from datetime import datetime, date


def events_recode(discord_id, coin, exp, ex_date):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_special_events(DISCORD_ID,COIN, EXP, EXPIRE_DATE) VALUES (%s,%s,%s,%s)'
        cur.execute(sql, (discord_id, coin, exp, ex_date,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def expire_date(ex_date):
    expire = datetime.strptime(ex_date, "%Y-%m-%d").date()
    now = date.today()
    if expire <= now:
        return 0


def get_channel_id(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT CHANNEL_ID FROM scum_special_events WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def channel_id_update(discord_id, ch_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_special_events SET CHANNEL_ID = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (ch_id, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def image_status(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT IMAGE FROM scum_special_events WHERE DISCORD_ID=%s'
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
        sql = 'UPDATE scum_special_events SET IMAGE = 1 WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def get_event_coin(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COIN FROM scum_special_events WHERE DISCORD_ID=%s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def get_event_exp(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT EXP FROM scum_special_events WHERE DISCORD_ID=%s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
