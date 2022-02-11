from db.players_db import db, MySQLConnection, Error


def events_recode(discord_id, coin, exp, expire_date):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_special_events(DISCORD_ID,COIN, EXP, EXPIRE_DATE) VALUES (%s,%s,%s,%s)'
        cur.execute(sql, (discord_id,coin, exp, expire_date,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
