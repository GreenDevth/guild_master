import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from db.Mission_db import mission_status, mission, mission_exists, players_mission, mission_img, new_mission, \
    update_report_mission, update_mission_img, exp_update, reset_mission
from db.Players_db import players_info
from db.Bank_db import plus_coins


class GetMission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        btn_list = ["1000", "1500", "500"]
        check = mission_status(member.id)  # return 0 or 1 for special events.
        in_mission_channel = self.bot.get_channel(951453790316404797)

        if btn in btn_list:
            in_mission = mission_exists(member.id)  # check mission already exisits retur 0 or 1
            get_mission = mission(btn)  # select mission by custom_id
            lenght = len(get_mission)  # count list lenght
            mission_id = random.randint(0, lenght - 1)  # get mission id from random function
            data = get_mission[mission_id]  # result mission from random fuction
            embed = discord.Embed(
                title='⚔ ภารกิจของคุณ คือ **{}**'.format(data[1]),
                description='{} ที่ Guild Master ตำแหน่ง C3N1 (ทะเลสาบ)'.format(data[1]),
                timestamp=datetime.datetime.utcnow(),
                color=discord.Colour.orange(),
            )
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_image(url=data[4])
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='ผู้รับภารกิจ', value=member.mention)
            embed.add_field(name='รางวัลภารกิจ', value=f"{data[2]} 💵")
            embed.add_field(name='ค่าประสบการณ์', value=f"{data[3]} 🎖")
            embed.set_footer(text='กรุณานำส่งภารกิจให้เสร็จก่อนรับภารกิจใหม่')
            message = None  # set golbal variable
            if check == 1:  # check (if) for player in special mission is TRUE
                message = await interaction.respond(content='you have a pending mission')
            elif check == 0:  # check (if) for player in special mission is FALSE
                if in_mission == 0:
                    message = await interaction.respond(embed=embed)
                    new_mission(member.id, member.name, data[1], data[2])
                elif in_mission == 1:
                    player = players_mission(member.id)
                    embed = discord.Embed(
                        title='คุณยังไม่ได้ส่งภารกิจ {}'.format(player[3]),
                        color=discord.Color.red(),
                    )
                    embed.set_image(url=mission_img(player[3]))
                    message = await interaction.respond(embed=embed)
                    await in_mission_channel.send(embed=embed)
                else:
                    pass
            else:
                pass
            return


class ReportMission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        btn_list = ["mission_report", "mission_check", "mission_reset", "yes_reset"]

        if btn in btn_list:
            in_mission = mission_exists(member.id)
            if in_mission == 1:
                if btn == 'mission_check':
                    player = players_mission(member.id)

                    embed = discord.Embed(
                        title='ภารกิจของคุณคือ {}'.format(player[3]),
                        color=discord.Color.red(),
                    )
                    embed.set_image(url=mission_img(player[3]))
                    message = await interaction.respond(embed=embed)
                    return False

                elif btn == 'mission_reset':
                    await interaction.respond(
                        content='การรีเซ็ตภารกิจมีค่าบริการ $100 ยืนยันกดที่ปุ่ม YES',
                        components=[Button(style=ButtonStyle.red, label='YES', custom_id='yes_reset')]
                    )
                    return False
                elif btn == 'yes_reset':
                    hard = reset_mission(member.id, btn)
                    message = await interaction.respond(content=hard)
                    await discord.DMChannel.send(member, '```css\nคุณจ่ายค่าบริการรีเซ็ตภารกิจจำนวน $100 : ยอดเงินในบัญชีปัจจุบันคือ ${:,d}\n```'.format(players_info(member.id)[5]))
                    return

                channel_name = interaction.guild.get_channel(players_mission(member.id)[6])  # get channel name by id
                mission_id = players_mission(member.id)[0]  # get mission id
                room = str(mission_id)  # create room number
                channel_id = players_mission(member.id)[6]  # get channel id
                if channel_name is None:
                    print('Create new report channel')
                    msg = await interaction.respond(content='โปรดรอสักครู่ ระบบกำลังสร้างห้องส่งภารกิจให้กับคุณ')
                    categorys = discord.utils.get(interaction.guild.categories,
                                                  name='MISSION')  # get Category by name MISSION.
                    overwrites = {
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                        member: discord.PermissionOverwrite(read_messages=True)
                    }
                    await categorys.edit(overwrites=overwrites)
                    new_channel = f'ห้องส่งภารกิจ-{room}'
                    create = await interaction.guild.create_text_channel(new_channel, category=categorys)
                    channel = discord.utils.get(interaction.guild.channels, name=str(new_channel))
                    update_report_mission(member.id, channel.id)
                    include = self.bot.get_channel(channel.id)
                    embed = discord.Embed(
                        title='ภารกิจของ {}'.format(players_mission(member.id)[2]),
                        description='ภารกิจ {} ผู้เล่นต้องนำสินค้าใส่ไว้ในตู้ที่จัดเตรียมไว้'
                                    'ให้และล็อคกุญแจให้เรียบร้อย หากเกิดกรณีไม่พบสินค้าผู้เล่นอาจ'
                                    'จะเสียสิทธิ์ในการรับเงินรางวัล และยึดค่าประสบการณ์คืน'.format(
                            players_mission(member.id)[3]),
                        color=discord.Colour.green()
                    )
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_image(url=mission_img(players_mission(member.id)[3]))
                    embed.set_footer(text='หากพบการทุจริตในการส่งสินค้า ต้องรับโทษปรับสูงสุด')
                    await include.send(
                        '{}\nศึกษาคู่มือการใช้งานได้ที่ <#932164700479828008>'.format(member.mention),
                    )
                    await include.send(
                        embed=embed,
                        components=[
                            [
                                Button(style=ButtonStyle.green,
                                       label='MISSION AWARD ${:,d}'.format(players_mission(member.id)[7]), emoji='💵',
                                       disabled=True),
                                Button(style=ButtonStyle.blue, label='UPLOAD MISSION IMAGE', emoji='📷',
                                       custom_id='upload_img')
                            ]
                        ]
                    )
                    message = await interaction.channel.send('🛣 ไปยังห้องส่งภารกิจของคุณที่ <#{}>'.format(channel.id),
                                                             delete_after=5)
                    return
                elif channel_name is not None:
                    message = await interaction.respond(
                        content='🛣 ไปยังห้องส่งภารกิจของคุณที่ <#{}>'.format(players_mission(member.id)[6]))
                return

            else:
                message = await interaction.respond(content="⚠ คุณไม่มีข้อมูลภารกิจในระบบ กรุณากดรับภารกิจ.")
            return

        elif btn == 'upload_img':
            if players_mission(member.id)[5] == 0:
                await interaction.respond(
                    content='📷 กรุณาอัพโหลดภาพสินค้าของคุณ เพื่อให้ทีมงานตรวจสอบความถูกต้อง')

                def check(res):
                    attachments = res.attachments
                    if len(attachments) == 0:
                        return False
                    attachment = attachments[0]
                    file_type = attachment.filename.endswith(('.jpg', '.png', 'jpeg'))
                    return res.author == interaction.author and res.channel == interaction.channel and file_type
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60)
                    if msg is not None:
                        update_mission_img(member.id, 1)
                        award = players_mission(member.id)[7]
                        img = msg.attachments[0]
                        embed = discord.Embed(
                            title='ภารกิจ {} สำเร็จ โดย {}'.format(players_mission(member.id)[3],
                                                                   players_mission(member.id)[2]),
                            colour=discord.Colour.green()
                        )
                        embed.set_author(name=member.name, icon_url=member.avatar_url)
                        embed.set_thumbnail(url=member.avatar_url)
                        embed.set_image(url=img)
                        embed.add_field(name='ผู้ส่งภารกิจ', value=member.mention)
                        embed.add_field(name='รางวันภารกิจ', value='💵 ${:,d}'.format(award))
                        embed.add_field(name='รางวัล exp', value=f'🎖 {award}')
                        embed.set_footer(text='หากตรวจพบการทุจริต จะทำการยึดเงินและค่าประสบการณ์ทั้งหมดทันที')
                        award = players_mission(member.id)[7]
                        coins = players_info(member.id)[5]
                        exp = exp_update(member.id, award)
                        y_int = isinstance(exp, int)
                        total_coins = plus_coins(member.id, award)

                        await discord.DMChannel.send(member, 'คุณได้รับรางวัลภารกิจจำนวน ${:,d}'
                                                             ' : จำนวนเงินปัจจุบันของคุณคือ ${:,d}'.format(award,
                                                                                                           total_coins))
                        if y_int is True:
                            await discord.DMChannel.send(member, f'คุณได้รับค่าประสบการณ์จำนวน {award}exp'
                                                                 f' : ค่าประสบการณ์ปัจจุบันของคุณคือ {exp}exp')
                        else:
                            await discord.DMChannel.send(member, exp)

                        statement = self.bot.get_channel(949609279277633536)
                        await statement.send(
                            "📃 **Mission Statement {}**\n"
                            "```=====================================\n"
                            "ผู้ทำภารกิจ : {}\n"
                            "ภารกิจ : {}\n"
                            "เงินรางวัล : {}\n"
                            "ค่าประสบการณ์ : ${:,d}\n"
                            "สถานะ : จ่ายแล้ว ✅\n"
                            "=====================================\n```".format(member.display_name, member.display_name,
                                                                                players_mission(member.id)[3], award, award)
                        )
                        await self.bot.get_channel(936149260540461106).send(embed=embed)
                        await interaction.channel.send(
                            embed=embed,
                            components=[Button(style=ButtonStyle.red, label='CLOSE THIS CHANNEL', emoji='⛔', custom_id='yes_self_reset')]
                        )
                        await msg.delete()
                except asyncio.TimeoutError:
                    pass
                return

            elif players_mission(member.id)[5] == 1:
                await interaction.respond(content='คุณได้ส่งรายงานภารกิจของภารกิจนี้แล้ว')
                return False
            return

        elif btn == 'yes_self_reset':
            solf = reset_mission(member.id, btn)
            message = solf
            await interaction.respond(content=message)
            await asyncio.sleep(10)
            await interaction.channel.delete()
            return

