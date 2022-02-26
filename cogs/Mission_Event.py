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

        if mission_status == 0:

            if mission_btn == 'mission_hunter':
                hunter = hunter_mission()
                test = hunter[5]
                print(type(test))
                message = f"{member.name} mission {hunter[5]}"
            elif mission_btn == 'mission_fishing':
                message = f"{member.name} click {mission_btn}"
            elif mission_btn == 'mission_famer':
                message = f"{member.name} click {mission_btn}"
            else:
                message = 'something went wrong.'

            await interaction.respond(content=message)
        elif mission_status == 1:
            await interaction.respond(content='mission already exists')

def setup(bot):
    bot.add_cog(MissionEvent(bot))
