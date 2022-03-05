from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config
from db.Players_db import players_info
from db.Bank_db import minus_coins, plus_coins

db = read_db_config()


def mission_status(discord_id):
    """ ตรวจสอบว่า ผู้เล่นมีภารกิจพิเศษ เป็น 0 หรือ 1 """
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


def mission_exists(discord_id):
    """ ตรวจสอบว่า ผู้เล่น มีภารกิจอยู่แล้วหรือไม่ เป็น 0 และ 1"""
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM scum_players_mission WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchone()
        res = list(row)
        return res[0]
    except Error as e:
        print(e)


def players_mission(discord_id):
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


def mission_img(mission_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT MISSION_IMG FROM scum_mission WHERE MISSION_NAME = %s', (mission_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def mission(award):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_mission WHERE MISSION_AWARD = %s', (award,))
        row = cur.fetchall()
        return row
    except Error as e:
        print(e)


def create_new_mission(discord_id, discord_name, mission_name, mission_award):
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


def update_report_mission(discord_id, channel_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players_mission SET MISSION_CHANNEL = %s WHERE DISCORD_ID = %s',
                    (channel_id, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def new_mission(discord_id, discord_name, mission_name, mission_award):
    create_new_mission(discord_id, discord_name, mission_name, mission_award)
    msg = players_mission(discord_id)
    return msg


def update_mission_status(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players_mission SET MISSION_STATUS = 0 WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def delete_player_mission(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('DELETE FROM scum_players_mission WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def hard_reset(discord_id, coins):
    player = players_info(discord_id)
    coin = player[5]
    if coins <= coin:
        minus_coins(discord_id, coins)
        delete_player_mission(discord_id)
        player = players_info(discord_id)
        coin = player[5]
        msg = f'ระบบทำการหักค่าบริการรีเซ็ตภารกิจจำนวน {coins} เป็นที่เรียบร้อย : ยอดเงินคงเหลือของคุณคือ {coin}'
        return msg
    elif coin < coins:
        player = players_info(discord_id)
        coin = player[5]
        msg = f'ขออภัยยอดเงินของคุณไม่เพียงพอ : ยอดเงินของคุณทั้งหมดคือ {coin}'
        return msg


def solf_reset(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('DELETE FROM scum_players_mission WHERE DISCORD_ID = %s', (discord_id,))
        conn.commit()
        cur.close()
        msg = "🎉 ทำการรีเซ็ตภารกิจใหม่ให้กับคุณเรียบร้อย : ระบบจะทำการปิดห้องส่งภารกิจใน 10 วินาที"
        return msg
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def reset_mission(discord_id, btn):
    msg = None
    if btn == 'yes_reset':
        fine = 100
        hard = hard_reset(discord_id, fine)
        msg = hard
    elif btn == 'yes_self_reset':
        solf = solf_reset(discord_id)
        msg = solf
    return msg


def update_mission(discord_id):
    update_mission_status(discord_id)  # Set mission status to 0


def update_report(discord_id, channel_id):
    update_report_mission(discord_id, channel_id)


def system_pay(discord_id, coins):
    plus_coins(discord_id, coins)


def level_update(discord_id, level):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update scum_players set LEVEL = %s where DISCORD_ID = %s', (level, discord_id,))
        conn.commit()
        print('Level update successfull.')
        cur.close()
        return
    except Error as e:
        print(e)
        return
    finally:
        if conn.is_connected():
            conn.close()
            return
        return


def update_exp(discord_id, exp):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update scum_players set EXP = %s where DISCORD_ID = %s', (exp, discord_id,))
        conn.commit()
        print('Exp update successfull.')
        cur.close()
        return
    except Error as e:
        print(e)
        return
    finally:
        if conn.is_connected():
            conn.close()
            return
        return


def exp_update(discord_id, exp):
    player = players_info(discord_id)
    player_level = player[6]
    player_exp = player[7]
    exp_plus = player_exp + exp
    default_level = 100000
    msg = None
    if default_level <= exp_plus:
        exp_after = exp_plus - default_level
        level_update(discord_id, player_level + 1)
        update_exp(discord_id, exp_after)
        level = players_info(discord_id)
        msg = f'Congratulation Your Level up! {level[6]}'
    elif exp_plus < default_level:
        update_exp(discord_id, exp_plus)
        exp = players_info(discord_id)
        msg = exp[7]
    return msg


def update_mission_img(discord_id, status):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players_mission SET MISSION_IMG = %s WHERE DISCORD_ID = %s', (status, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
