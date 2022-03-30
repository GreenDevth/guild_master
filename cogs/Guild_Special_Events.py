import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from db.Special_db import *
from db.Special_mission_db import *
from db.special_event import *


class GuildSpecialEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        btn_list = get_mission_id()
        btn_random = random.choice(btn_list)
        btn = interaction.component.custom_id
        member = interaction.author
        channel_id = get_channel_id(member.id)
        ex_date = '2022-04-08'

        if btn == 'event_1':
            check = check_mission_ready(member.id)
            if check != 0:
                await interaction.respond(content="สิทธิ์ในการรับภารกิจของคุณหมดแล้ว กรุณารอกิจกรรมครั้งต่อไปเร็ว ๆ นี้")
            else:
                mission = get_mission(btn_random)
                embed = discord.Embed(
                    title=f"คุณได้รับภารกิจ {mission[1]}",
                    color=discord.Colour.green()
                )
                embed.set_author(name=member.name, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_image(url=f"{mission[5]}")
                embed.add_field(name="Description", value="```\n{}\n```".format(mission[2]), inline=False)
                embed.add_field(name="รางวัลภารกิจ", value="```css\n${:,d}\n```".format(mission[3]))
                embed.add_field(name="ค่าประสบการณ์", value="```css\n{}\n```".format(mission[4]))
                events_recode(member.id, mission[3], mission[4], ex_date, mission[5], mission[1])
                mission_up(member.id)
                await interaction.respond(content=f'บันทึกข้อมูลเรียบร้อย ระบบกำลังส่งข้อมูลภารกิจให้คุณ : กรุณาส่งภารกิจภายใน **{ex_date}**')
                await discord.DMChannel.send(member, embed=embed)
                await interaction.respond(content="สถานะภารกิจเป็น {}".format(check))

        if btn == "detail_event_1":
            check = check_mission_ready(member.id)
            if check == 0:
                await interaction.respond(content="คุณยังไม่มีภารกิจ กรุณากดรับภารกิจ")
            elif check == 1:
                mission = get_mission_status(member.id)
                if mission == 1:
                    # await interaction.respond(content="แสดงรายการภารกิจ")
                    player = get_player_mission(member.id)
                    embed = discord.Embed(
                        title="คุณมีภารกิจ {} ค้างอยู่".format(player[8]),
                        color=discord.Colour.red()
                    )
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_image(url="{}".format(player[7]))
                    embed.set_footer(text="กรุณาส่งภารกิจภายใน {}".format(player[6]))
                    await interaction.respond(embed=embed)
                elif mission == 0:
                    await interaction.respond(content="สิทธิ์ในการรับภารกิจของคุณหมดแล้ว กรุณารอกิจกรรมครั้งต่อไปเร็ว ๆ นี้")

            # check_mission = get_mission_status(member.id)
            # if check == 0 or check_mission == 0:
            # else:
            #     return False

        if btn == 'report_event_1':
            check = check_mission_ready(member.id)
            if check == 0:
                await interaction.respond(content="คุณไม่มีภารกิจที่ต้องส่ง กรุณากดรับภารกิจ")
            elif check == 1:
                mission = get_mission_status(member.id)
                if mission == 1:
                    # await interaction.respond(content='create new report channel')
                    expire = expire_date(ex_date)
                    if expire == 0:
                        await interaction.respond(content='⚠ Mission Expire : ไว้รอภารกิจพิเศษในครั้งต่อไปนะครับ')
                    elif expire != 0:
                        channel_name = interaction.guild.get_channel(channel_id)
                        if channel_name is None:
                            await interaction.respond(content=f'ระบบกำลังสร้างห้องสำหรับส่งภารกิจพิเศษให้คุณกรุณารอสักครู่')
                            category = discord.utils.get(interaction.guild.categories, name='SPECIAL')
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
                                f'นำสินค้ามาส่งยัง A4N3 ตำแหน่งที่ตั้ง สถานนีขนส่ง \nเพื่อทำการส่งสินค้า '
                                f'โดยให้ผู้เล่นนำสินค้าใส่ไว้ในตู้และล็อคกุญแจตู้ \nหลังจากนั้นให้ผู้เล่นถ่ายภาพสินค้าข้างในตู้ '
                                f'และกดที่ปุ่มสีฟ้า \nเพื่ออัพโหลดภาพและส่งให้แอดมิน ',
                                file=discord.File('./img/guild.png'),
                                components=[
                                    Button(style=ButtonStyle.blue, label='UPLOAD IMAGE', emoji='📷', custom_id='event_upload')
                                ]
                            )

                            await interaction.channel.send(f'ไปยังห้องส่งภารกิจ <#{channel.id}>', delete_after=10)
                        if channel_name is not None:
                            await interaction.respond(content=f'ไปยังห้องส่งภารกิจ <#{channel_id}>')
                elif mission == 0:
                    await interaction.respond(content="สิทธิ์ในการรับภารกิจของคุณหมดแล้ว กรุณารอกิจกรรมครั้งต่อไปเร็ว ๆ นี้")

        if btn == 'event_upload':
            await interaction.edit_origin(
                components=[]
            )
            await interaction.channel.send(
                f"{member.mention}\n 📸 กรุณาอัพโหลดภาพสินค้าภารกิจพิเศษของคุณ และรอการนำจ่ายรางวัลให้คุณต่อไป")

            def check(res):
                attachments = res.attachments
                if len(attachments) == 0:
                    return False
                attachment = attachments[0]
                file_type = attachment.filename.endswith(('.jpg', '.png', 'jpeg'))
                return res.author == interaction.author and res.channel == interaction.channel and file_type

            msg = await self.bot.wait_for('message', check=check)
            image = msg.attachments[0]
            player_exp = players_exp(member.id)
            coin = get_event_coin(member.id)
            award = get_event_exp(member.id)
            update_image_status(member.id)
            exp = player_exp + award
            exp_up(member.id, exp)
            embed = discord.Embed(
                title=f'ส่งภารกิจโดย {member.name}',
                description='ขอแสดงความยินดีกับรางวัลความสำเร็จของภารกิจในครั้งนี้ ',
                color=discord.Colour.green()
            )
            embed.set_image(url=image)
            embed.add_field(name='ผู้ส่งภารกิจ', value=member.mention, inline=False)
            embed.add_field(name='💰 รางวัลที่ได้รับ', value='${:,d}'.format(coin), inline=True)
            embed.add_field(name='🎚 EXP ที่ได้รับ', value=f"{award}", inline=True)
            await interaction.channel.send(
                embed=embed,
                components=[
                    Button(style=ButtonStyle.red, label='CLOSE MISSION', emoji='⏱', custom_id='end_special_mission')
                ]
            )
            return False
        if btn == "end_special_mission":
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=False)
            }
            await interaction.edit_origin(
                components=[]
            )
            await interaction.channel.edit(overwrites=overwrites)
            delete_mission(member.id)
            player = get_players_info(member.id)
            message = f"{member.mention}\nยอดเงินปัจจุบันของคุณ **{player[5]}** ค่าประสบการณ์ปัจจุบันของคุณ **{player[7]}**"
            await interaction.channel.send(content="{}\nยอดเงินปัจจุบันของคุณคือ **{}** ค่าประสบการณ์ของคุณคือ **{}**".format(member.mention, player[5], player[7]))
            await discord.DMChannel.send(member, message)
            return

    @commands.command(name='special_event')
    async def special_event_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/events/special_mission_new.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='Get Mission', emoji='⚔', custom_id='event_1'),
                    Button(style=ButtonStyle.blue, label='Send Mission', emoji='📩', custom_id='report_event_1'),
                    Button(style=ButtonStyle.gray, label='You Mission', emoji='📃', custom_id='detail_event_1')
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(GuildSpecialEventCommand(bot))
