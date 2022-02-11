import discord
import random
from discord.ext import commands
from discord_components import Button, ButtonStyle
from db.players_db import player_mission, mission_up, players_bank_id
from db.special_event import events_recode, expire_date, get_channel_id, channel_id_update


class GuildSpecialEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        event_btn = interaction.component.custom_id
        check = player_mission(member.id)
        channel_id = get_channel_id(member.id)
        channel_name = interaction.guild.get_channel(channel_id)
        if event_btn == 'event_1':
            if check == 0:
                coin = 4000
                exp = 10000
                ex_date = '2020-02-15'
                events_recode(member.id, coin, exp, ex_date)
                mission_up(member.id)
                await interaction.respond(content=f'บันทึกข้อมูลเรียบร้อย กรุณาส่งภารกิจภายใน **{ex_date}**')
            if check == 1:
                await interaction.respond(content='คุณได้กดรับภารกิจนี้เรียบร้อยแล้ว')
            await interaction.respond(content='ไมพบหมายเลข Steam id ของคุณในระบบ')

        if event_btn == 'report_event_1':
            category = discord.utils.get(interaction.guild.categories, name='EVENT')
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                member: discord.PermissionOverwrite(read_messages=True)
            }
            if check == 1:

                new_channel_name = f'ภารกิจพิเศษ-{players_bank_id(member.id)}'
                if channel_name is None:
                    await category.edit(overwrites=overwrites)
                    await interaction.guild.create_text_channel(new_channel_name, category=category)
                    channel = discord.utils.get(interaction.guild.channels, name=str(new_channel_name))
                    channel_send = interaction.guild.get_channel(channel.id)
                    channel_id_update(member.id, channel.id)
                    await interaction.respond(content=f'ไปยังห้องส่งภารกิจของคุณ <#{channel_id}>')
                await interaction.respond(content=f'ไปยังห้องส่งภารกิจของคุณ <#{channel_id}>')

            if check == 0:
                await interaction.respond(content='คุณไม่มีภารกิจพิเศษที่ต้องส่ง')
            await interaction.respond(content='ไมพบหมายเลข Steam id ของคุณในระบบ')

        if event_btn == 'detail_event_1':
            await interaction.respond(
                content='**นำส่งเซ็ตอาวุธปืน SDASS 12M** ซึ่งประกอบด้วย '
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
