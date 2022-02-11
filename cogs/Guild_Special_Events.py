import discord
import random
from discord.ext import commands
from discord_components import Button, ButtonStyle


class GuildSpecialEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='special_event')
    async def special_event_command(self, ctx):
        code = random.randint(9, 99999)
        await ctx.send(
            f'**ภารกิจพิเศษหมายเลข {code}**'
            f'\nเงินรางวัล **4000** ค่าประสบการณ์ **10000** exp'
            f'\nโดยให้ผู้เล่นตามหาและนำส่งอาวุธปืน ซึ่งจะประกอบด้วย '
            '\n- ปืน SDASS 12M 1 กระบอก'
            '\n- Improvised Flashlight 1 อัน '
            '\n- OKP-7 Holographic 1 อัน '
            '\n- Bridshot 1 กล่อง (สีเขียว) '
            '\n- Buckshot 1 กล่อง (สีแดง) '
            '\n- Slug 1 กล่อง (สีดำ) '
        )
        await ctx.send(
            file=discord.File('./img/events/special_event.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET MISSION', emoji='⚔', custom_id='event_1'),
                    Button(style=ButtonStyle.blue, label='SEND MISSION', emoji='📩', custom_id='report_event_1'),
                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱', disabled=True)
                ]
            ]
        )


def setup(bot):
    bot.add_cog(GuildSpecialEventCommand(bot))
