import discord
import random
from discord.ext import commands
from discord_components import Button, ButtonStyle


class GuildSpecialEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        event_btn = interaction.component.custom_id

        if event_btn == 'event_1':
            await interaction.respond(content='ok')

    @commands.command(name='special_event')
    async def special_event_command(self, ctx):
        code = random.randint(9, 99999)
        await ctx.send(
            f'**ภารกิจพิเศษหมายเลข {code}**'
            f'\nเงินรางวัล **4000** ค่าประสบการณ์ **10000** exp'
            f'\nMission Expire in 15 February 2022'
        )
        await ctx.send(
            file=discord.File('./img/events/special_event.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='รับภารกิจ', emoji='⚔', custom_id='event_1'),
                    Button(style=ButtonStyle.blue, label='ส่งภารกิจ', emoji='📩', custom_id='report_event_1'),
                    Button(style=ButtonStyle.gray, label='รายละเอียดภารกิจ', emoji='📃', custom_id='detail_event_1')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(GuildSpecialEventCommand(bot))
