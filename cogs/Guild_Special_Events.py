import discord
import random
from discord.ext import commands
from discord_components import Button, ButtonStyle
from db.players_db import player_mission, mission_up

class GuildSpecialEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        event_btn = interaction.component.custom_id
        check = player_mission(member.id)
        if event_btn == 'event_1':
            if check == 0:
                await interaction.respond(content='Continue get new event mission')
            if check == 1:
                await interaction.respond(content='event mission already exists')
            await interaction.respond(content='Your steam id not found.')

        if event_btn == 'report_event_1':
            await interaction.respond(content='ok')

        if event_btn == 'detail_event_1':
            await interaction.respond(
                '**นำส่งเซ็ตอาวุธปืน SDASS 12M** ซึ่งประกอบด้วย '
                '\n- ปืน SDASS 12M 1 กระบอก'
                '\n- Improvised Flashlight 1 อัน '
                '\n- OKP-7 Holographic 1 อัน '
                '\n- Bridshot 1 กล่อง (สีเขียว) '
                '\n- Buckshot 1 กล่อง (สีแดง) '
                '\n- Slug 1 กล่อง (สีดำ) ',
            )

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
