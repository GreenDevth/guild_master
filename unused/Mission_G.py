import asyncio
import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from mission.mission_db import *
from mission.mission_list import animal, guild_master_img


class MissionTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id

        if btn == "green":
            await interaction.respond(content='Green Colors')
        if btn == "gray":
            await interaction.respond(content='Gray Colors')
        if btn == "red":
            await interaction.respond(content='Red Colors')
        if btn == "blue":
            await interaction.respond(content='Blue Colors')

    @commands.command(name='mission_g')
    async def mission_g_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/mission_center.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='Green', custom_id='green'),
                    Button(style=ButtonStyle.gray, label='Gray', custom_id='gray'),
                    Button(style=ButtonStyle.red, label='Red', custom_id='red'),
                    Button(style=ButtonStyle.blue, label='Blue', custom_id='blue')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(MissionTest(bot))
