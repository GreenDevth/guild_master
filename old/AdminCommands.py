from discord.ext import commands
from mysql.connector import MySQLConnection, Error
from db.db_config import read_db_config

db = read_db_config()


def reset():
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = "UPDATE scum_players SET MISSION = 0 WHERE PLAYERS_ID > 0"
        cur.execute(sql)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()

def reset_daily_pack():
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = "UPDATE scum_players SET DAILY_PACK = 0 WHERE PLAYERS_ID > 0"
        cur.execute(sql)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()

class AdminCommandEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reset_mission')
    async def reset_mission_command(self, ctx):
        reset()
        await ctx.reply('Set Players Mission to Zero Successfull', mention_author=False)


    @commands.command(name='reset_daily')
    async def reset_daily_command(self, ctx):
        reset_daily_pack()
        await ctx.reply('Set Players Daily Pack to Zero Successfull', mention_author=False)


def setup(bot):
    bot.add_cog(AdminCommandEvent(bot))
