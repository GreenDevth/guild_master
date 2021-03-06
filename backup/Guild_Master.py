import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from db.Mission_db import *


class GuildMasster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        check = mission_status(member.id)
        btn = interaction.component.custom_id
        in_mission = mission_exists(member.id)  # check player mission already exists.
        report_list = ["mission_report", "mission_check", "mission_reset", "yes_reset"]
        btn_list = ["1000", "1500", "500"]
        report_mission_list = ["upload_image", "self_reset", "yes_self_reset"]
        message = None
        data = None

        if btn in btn_list:
            if check == 0:
                get_mission = mission(btn)
                list_length = len(get_mission)
                mission_id = random.randint(0, list_length - 1)
                data = get_mission[mission_id]  # แสดง mission data.
                in_mission = mission_exists(member.id)  # check player mission already exists.
                in_mission_channel = self.bot.get_channel(951453790316404797)
                if in_mission == 0:
                    """ ถ้าผู้เล่นยังไม่ได้รับภารกิจ หรือ ภารกิจเป็น 0 """
                    """ Create new mission. """
                    new_mission(member.id, member.name, data[1], data[2])
                    embed = discord.Embed(
                        title=f'⚔ ภารกิจของคุณ คือ **{data[1]}**',
                        description=f'{data[1]} ที่ Guild Master ตำแหน่ง C3N1 (ทะเลสาบ)',
                        timestamp=datetime.datetime.utcnow(),
                        color=discord.Colour.orange()
                    )
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    embed.set_image(url=data[4])
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.add_field(name='ผู้รับภารกิจ', value=member.mention)
                    embed.add_field(name='รางวัลภารกิจ', value=f"{data[2]} 💵")
                    embed.add_field(name='ค่าประสบการณ์', value=f"{data[3]} 🎖")
                    embed.set_footer(text='กรุณานำส่งภารกิจให้เสร็จก่อนรับภารกิจใหม่')
                    message = embed
                    await interaction.respond(embed=message)
                    await in_mission_channel.send(embed=message)
                    return
                elif in_mission == 1:
                    player = players_mission(member.id)
                    img_name = player[3]
                    img = mission_img(img_name)
                    embed = discord.Embed(
                        title=f'คุณยังไม่ส่งภารกิจ {player[3]}',
                        color=discord.Colour.red()
                    )
                    embed.set_image(url=img)
                    await interaction.respond(embed=embed)
                    return
                await interaction.respond(content=message)
            else:
                message = 'คุณกำลังรับภารกิจพิเศษอยู่ กรุณาส่งภารกิจก่อนเพื่อรับภารกิจทั่วไป'
            await interaction.respond(content=message)
            return

        elif btn in report_list:
            if in_mission == 1:
                if btn == 'mission_check':
                    player = players_mission(member.id)
                    img = mission_img(player[3])
                    embed = discord.Embed(
                        title=f'ภารกิจของคุณคือ {player[3]}',
                        color=discord.Color.red()
                    )
                    embed.set_image(url=img)
                    await interaction.respond(embed=embed)
                    return
                elif btn == 'mission_reset':
                    await interaction.respond(content='Are you sure', components=[
                        Button(style=ButtonStyle.red, label='Yes', custom_id='yes_reset')])
                elif btn == 'yes_reset':
                    hard = reset_mission(member.id, btn)
                    message = hard
                else:
                    player = players_mission(member.id)
                    channel_name = interaction.guild.get_channel(player[6])
                    mission_id = player[0]
                    room = str(mission_id)
                    channel_id = player[6]
                    if channel_name is None:
                        print('Create new report channel')
                        """ Update MISSION STATUS TO 0 """
                        await interaction.respond(content='โปรดรอสักครู่ ระบบกำลังสร้างห้องส่งภารกิจให้กับคุณ')
                        category = discord.utils.get(interaction.guild.categories, name='MISSION')
                        overwrites = {
                            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                                        connect=False),
                            member: discord.PermissionOverwrite(read_messages=True)
                        }
                        await category.edit(overwrites=overwrites)
                        new_channel = f'ห้องส่งภารกิจ-{room}'
                        await interaction.guild.create_text_channel(new_channel, category=category)
                        channel = discord.utils.get(interaction.guild.channels, name=str(new_channel))
                        update_report_mission(member.id, channel.id)
                        include = self.bot.get_channel(channel.id)
                        embed = discord.Embed(
                            title=f'ภารกิจของ {player[2]}',
                            description=f'ภารกิจ {player[3]} ผู้เล่นต้องนำสินค้าใส่ไว้ในตู้ที่จัดเตรียมไว้'
                                        f'ให้และล็อคกุญแจให้เรียบร้อย หากเกิดกรณีไม่พบสินค้าผู้เล่นอาจ'
                                        f'จะเสียสิทธิ์ในการรับเงินรางวัล และยึดค่าประสบการณ์คืน',
                            color=discord.Colour.green()
                        )
                        img_name = player[3]
                        img = mission_img(img_name)
                        embed.set_author(name=member.name, icon_url=member.avatar_url)
                        embed.set_thumbnail(url=member.avatar_url)
                        embed.set_image(url=img)
                        embed.set_footer(text='ห้ามโกงการส่งภารกิจโดยเด็ดขาด')
                        await include.send(
                            f'{member.mention}'
                            'ศึกษาคู่การใช้งานได้ที่ <#932164700479828008>'
                        )
                        coins = '${:,d}'.format(player[7])
                        await include.send(
                            embed=embed,
                            components=[
                                [
                                    Button(style=ButtonStyle.green, label=f'MISSION AWARD {coins}', emoji='💵',
                                           custom_id='receipt', disabled=True),
                                    Button(style=ButtonStyle.blue, label='UPLOAD MISSION IMAGE', emoji='📷',
                                           custom_id='upload_image')
                                ]
                            ]
                        )
                        message = 'ไปยังห้องส่งภารกิจของคุณ <#{}>'.format(channel.id)
                        await interaction.channel.send(message, delete_after=5)
                        return

                    elif channel_name is not None:
                        channel = player[6]
                        message = f'ไปยังห้องส่งภารกิจของคุณ <#{channel}>'

            elif in_mission == 0:
                message = 'คุณยังไม่มีภารกิจในระบบ'
            await interaction.respond(content=message)
            return
        elif btn in report_mission_list:
            m_player = players_mission(member.id)
            player = players_info(member.id)

            if btn == 'self_reset':
                if m_player[5] == 2:
                    await interaction.respond(content='Are you sure', components=[
                        Button(style=ButtonStyle.red, label='Yes', custom_id='yes_self_reset')])
                else:
                    message = '⚠ คุณยังไม่ได้กดรับรางวัลภารกิจ โปรดกดรับรางวัลภารกิจของคุณเสียก่อน'
            elif btn == 'yes_self_reset':
                solf = reset_mission(member.id, btn)
                message = solf
                await interaction.respond(content=message)
                await asyncio.sleep(10)
                await interaction.channel.delete()
                return

            else:
                if m_player[5] == 0:
                    award = int(m_player[7])
                    coins = '${:,d}'.format(award)
                    message = '🖼 กรุณาอัพโหลดภาพสินค้าของคุณ ' \
                              'สำหรับให้ทีมงานตรวจสอบความถูกต้องของภารกิจ '
                    await interaction.respond(content=message)

                    def check(res):
                        attachments = res.attachments
                        if len(attachments) == 0:
                            return False
                        attachment = attachments[0]
                        return res.author == interaction.author and res.channel == interaction.channel and attachment.filename.endswith(
                            ('.jpg', '.png', '.jpeg'))

                    msg = await self.bot.wait_for('message', check=check)
                    if msg is not None:
                        award = int(m_player[7])
                        coins = '${:,d}'.format(award)
                        image = msg.attachments[0]
                        message = f"🎉 คุณส่งภาจกิจสำเร็จแล้ว : กดที่ปุ่ม เพื่อรับรางวัลของคุณ"
                        update_mission_img(member.id, 1)
                        embed = discord.Embed(
                            title=f'ภารกิจ {m_player[3]} สำเร็จ โดย {m_player[2]}',
                            colour=discord.Colour.green()
                        )
                        embed.set_author(name=member.name, icon_url=member.avatar_url)
                        embed.set_thumbnail(url=member.avatar_url)
                        embed.set_image(url=image)
                        embed.add_field(name='ผู้ส่งภารกิจ', value=member.mention)
                        embed.add_field(name='รางวันภารกิจ', value=f'💵 {coins}')
                        embed.add_field(name='รางวัล exp', value=f'🎖 {award}')
                        embed.set_footer(text='หากตรวจพบว่าโกงการส่งภารกิจ จะทำการยึดเงินและค่าประสบการณ์ทั้งหมดทันที')
                        success_channel = self.bot.get_channel(936149260540461106)
                        await success_channel.send(member.mention, embed=embed)
                        await interaction.channel.send(
                            f"{message}",
                            components=[
                                [
                                    Button(style=ButtonStyle.green, label=f'GET YOUR MISSION AWORD ', emoji='🎖',
                                           custom_id='receipt'),
                                    Button(style=ButtonStyle.gray, label=f'AWARD {coins}', emoji='💵', disabled=True)
                                ]
                            ]
                        )
                    await interaction.respond(content=message)
                    return

                else:
                    message = '⚠ คุณได้ส่งภารกิจเรียบร้อยแล้ว กรุณากดปุ่ม Close ' \
                              'เพิ่อรีเซ็ตภารกิจและปิดห้องส่งสินค้าของคุณ '
                    await interaction.respond(content=message)
            return
        elif btn == 'receipt':
            if players_mission(member.id)[5] == 2:
                message = '⚠ Error : ระบบจ่ายรางวัลภารกิจให้กับคุณไปแล้ว'
                await interaction.respond(content=message)
            else:
                message = 'กรุณารอสักครู่ระบบกำลังจ่ายรางวัลภารกิจและค่าประสบการณ์ให้กับคุณ'
                await interaction.respond(content=message)
                award = players_mission(member.id)[7]
                coins = players_info(member.id)[5]
                exp = exp_update(member.id, award)
                y_int = isinstance(exp, int)
                total_coins = plus_coins(member.id, award)
                update_mission_img(member.id, 2)

                await discord.DMChannel.send(member, 'คุณได้รับรางวัลภารกิจจำนวน {}'
                                                     ' : จำนวนเงินปัจจุบันของคุณคือ ${:,d}'.format(coins, total_coins))
                if y_int is True:
                    await discord.DMChannel.send(member, f'คุณได้รับค่าประสบการณ์จำนวน {award}exp'
                                                         f' : ค่าประสบการณ์ปัจจุบันของคุณคือ {exp}exp')
                else:
                    await discord.DMChannel.send(member, exp)

                statement = self.bot.get_channel(949609279277633536)
                await statement.send(
                    "📃 **Mission Statement**\n"
                    "```=====================================\n"
                    "ผู้ทำภารกิจ : {}\n"
                    "เงินรางวัล : {}\n"
                    "ค่าประสบการณ์ : ${:,d}\n"
                    "สถานะ : จ่ายแล้ว ✅\n"
                    "=====================================\n```".format(member.display_name, award, award)
                )
                await interaction.channel.send(
                    "⚠ **กดปุ่มเพื่อปิดห้องส่งภารกิจ**",
                    components=[Button(style=ButtonStyle.red, label='CLOSE', emoji='⛔', custom_id='self_reset')]
                )
                return
        return


def setup(bot):
    bot.add_cog(GuildMasster(bot))
