import discord
import random
from discord.ext import commands
from discord_components import Button, ButtonStyle
from db.players_db import *
from db.special_event import *


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
        check_img = event_image_upload_status(member.id)
        event_award = get_event_exp(member.id)
        event_coins = get_event_coin(member.id)
        player_exp = players_exp(member.id)
        success = self.bot.get_channel(936149260540461106)
        if event_btn == 'event_1':
            if check == 0:
                coin = 4000
                exp = 10000
                ex_date = '2020-02-15'
                await interaction.respond(content=f'บันทึกข้อมูลเรียบร้อย กรุณาส่งภารกิจภายใน **{ex_date}**')
                events_recode(member.id, coin, exp, ex_date)
                mission_up(member.id)
            if check == 1:
                await interaction.respond(content='คุณได้กดรับภารกิจนี้เรียบร้อยแล้ว')
            await interaction.respond(content='ไมพบหมายเลข Steam id ของคุณในระบบ')

        if event_btn == 'report_event_1':
            expire = expire_date('2022-02-15')
            if expire == 0:
                await interaction.respond(content='⚠ Mission Expire : ไว้รอภารกิจพิเศษในครั้งต่อไปนะครับ')
            if channel_name is None:
                await interaction.respond(content=f'ระบบกำลังสร้างห้องสำหรับส่งภารกิจพิเศษให้คุณกรุณารอสักครู่')
                category = discord.utils.get(interaction.guild.categories, name='EVENT')
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                new_channel_name = f'ภารกิจพิเศษ-{players_bank_id(member.id)}'
                await category.edit(overwrites=overwrites)
                await interaction.guild.create_text_channel(new_channel_name, category=category)
                channel = discord.utils.get(interaction.guild.channels, name=str(new_channel_name))
                channel_send = interaction.guild.get_channel(channel.id)
                channel_id_update(member.id, channel.id)
                await channel_send.send(
                    f'{member.mention}\n '
                    f'นำสินค้ามาส่งยัง C3N1 ตำแหน่งที่ตั้ง Guild Master เพื่อทำการส่งสินค้า '
                    f'โดยให้ผู้เล่นนำสินค้าใส่ไว้ในตู้และล็อคกุญแจตู้ หลังจากนั้นให้ผู้เล่นถ่ายภาพสินค้าข้างในตู้ '
                    f'และกดที่ปุ่มสีฟ้า (SEND MISSION)เพื่ออัพโหลดภาพและส่งให้แอดมิน ',
                    file=discord.File('./img/mission_center.png'),
                    components=[
                        [
                            Button(
                                style=ButtonStyle.blue,
                                label='อัพโหลดสินค้าเพื่อส่งให้แอดมินตรวจสอบ',
                                emoji='📷',
                                custom_id='event_upload'),
                            Button(
                                style=ButtonStyle.red,
                                label='ปิดภารกิจ',
                                emoji='❌',
                                custom_id='event_reset'
                            )
                        ]
                    ]
                )

                await interaction.channel.send(f'ไปยังห้องส่งภารกิจ <#{channel.id}>', delete_after=10)
            if channel_name is not None:
                await interaction.respond(content=f'ไปยังห้องส่งภารกิจ <#{channel_id}>')

        if event_btn == 'event_upload':
            if check_img == 0:
                update_image_status(member.id)
                await interaction.respond(content='กรุณาอัพโหลดภาพสินค้าที่คุณนำมาส่ง')
                #
                # def check(message):
                #     attachments = message.attachments
                #     if len(attachments) == 0:
                #         return False
                #     attachment = attachments[0]
                #     return attachment.filename.endswith(('.jpg', '.png'))
                #
                # msg = await self.bot.wait_for('message', check=check)
                # if msg is not None:
                #     update_image_status(member.id)
                #     exp = player_exp + event_award
                #     exp_up(member.id, exp)
                #     await interaction.channel.send(
                #         f'🎉 ยินดีด้วยคุณได้รับค่า 🎖exp จำนวน {event_award} ในภารกิจนี้\n'
                #         f'โปรดรอการตรวจสอบและจ่ายรางวัลจากทีมงานในเวลาต่อไป')
                # image = msg.attachments[0]
                # embed = discord.Embed(
                #     title=f'ส่งภารกิจโดย {member.name}',
                #     description='ขอแสดงความยินดีกับรางวัลความสำเร็จของภารกิจในครั้งนี้ ',
                #     color=discord.Colour.green()
                # )
                # embed.set_image(url=image)
                # embed.add_field(name='ผู้ส่งภารกิจ', value=member.mention, inline=False)
                # embed.add_field(name='💰 รางวัลที่ได้รับ', value='${:d}'.format(event_coins), inline=True)
                # embed.add_field(name='🎚 EXP ที่ได้รับ', value=f"{event_award}", inline=True)
                # msg = await success.send(embed=embed)
                # await msg.add_reaction("❔")
            await interaction.respond(content='⚠ คุณยังไม่มีภารกิจที่ต้องส่งในตอนนี้')

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
