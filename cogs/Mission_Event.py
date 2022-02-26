from discord.ext import commands
from mission.Mission_db import hunter_mission, famer_mission, fishing_mission, mission_check


class MissionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        mission_status = mission_check(member.id)

def setup(bot):
    bot.add_cog(MissionEvent(bot))
