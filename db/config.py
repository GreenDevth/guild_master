import os
from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config
from datetime import datetime, date

db = read_db_config()


def get_token(token_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT token FROM scum_discord_token WHERE token_id = %s'
        cur.execute(sql, (token_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def config_cogs(client):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


def expire_date(ex_date):
    expire = datetime.strptime(ex_date, "%Y-%m-%d").date()
    now = date.today()
    if expire >= now:
        msg = "Misssion Expire."
        return msg.strip()
