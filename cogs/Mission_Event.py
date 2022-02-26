from discord.ext import commands
from mission.Mission_db import hunter_mission, famer_mission, fishing_mission, mission_check


class MissionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        mission_status = mission_check(member.id)
        mission_btn = interaction.component.custom_id

        if mission_btn == 'mission_hunter':
            message = f"{member.name} click {mission_btn}"
        elif mission_btn == 'mission_fishing':
            message = f"{member.name} click {mission_btn}"
        elif mission_btn == 'mission_famer':
            message = f"{member.name} click {mission_btn}"
        await interaction.respond(content=message)

def setup(bot):
    bot.add_cog(MissionEvent(bot))
