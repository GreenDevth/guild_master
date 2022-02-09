from discord.ext import commands
from discord_components import Button, ButtonStyle
from mission.mission_db import get_mission


class MissionButtonEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author

        mission_btn = interaction.component.custom_id

        if mission_btn == 'mission_famer':
            await interaction.respond(content=f'{member.name} Clicked.')

        if mission_btn == 'mission_hunter':
            await interaction.respond(content=f'{member.name} Clicked.')

        if mission_btn == 'mission_fishing':
            await interaction.respond(content=f'{member.name} Clicked.')


def setup(bot):
    bot.add_cog(MissionButtonEventCommand(bot))
