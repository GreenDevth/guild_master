import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from db.players_db import players_exists


class MissionV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mission Vegetable online')

    @commands.command(name='mission_v')
    async def mission_v_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/mission/vegetable_1.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET MISSION', emoji='⚔', custom_id='mission_v'),
                    Button(style=ButtonStyle.blue, label='REPORT MISSION', emoji='📩', custom_id='mission_v_report'),
                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱', custom_id='mission_v_reset')
                ]
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        v_btn = interaction.component.custome_id

        if v_btn == 'mission_v':
            """ Check register players """
            check = players_exists(member.id)
            if check == 1:
                await interaction.respond(content=f'I found a player {member.name}')
                return True
            else:
                await interaction.respond(content=f'Status {check} : your informaion is not found!')


def setup(bot):
    bot.add_cog(MissionV(bot))
