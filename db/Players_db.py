from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config

db = read_db_config()


def players_info(discord_id):
    """ Get player information. """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from scum_players where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
        return False
    except Error as e:
        print(e)
        return None


def coins_update(discord_id, coins):
    """ Update players coins """
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('update scum_players set COINS = %s where DISCORD_ID = %s', (coins, discord_id,))
        conn.commit()
        print('Coins update successfull.')
        cur.close()
        return
    except Error as e:
        print(e)
        return None
    finally:
        if conn.is_connected():
            conn.close()
            print('Database disconnected.')
            return None
        return None


def plus_coins(discord_id, coins):
    player = players_info(discord_id)
    coin = player[5]
    coins_update(discord_id, coin + coins)
    player = players_info(discord_id)
    coin = player[5]
    return coin
