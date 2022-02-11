from db.players_db import db, MySQLConnection, Error


def new_event_recode(discord_id, discord_name, event_name, coin, exp, expire_date):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'INSERT INTO scum_special_event(discord_id, discord_name, event_name, coin, exp, expire_date) VALUES (' \
              '%s,%s,%s,%s,%s,%s) '
        cur.execute(sql, (discord_id, discord_name, event_name, coin, exp, expire_date,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
