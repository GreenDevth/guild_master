from discord.ext import commands

class MissionV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mission Vegetable online')

def setup(bot):
    bot.add_cog(MissionV(bot))