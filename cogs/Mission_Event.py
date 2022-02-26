import datetime
import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from mission.Mission_db import hunter_mission, famer_mission, \
    fishing_mission, mission_check, players_mission, \
    players_mission_channel, players_new_mission, \
    players_update_report_misson, get_players_mission, check_players_mission, get_img_from_mission


class MissionEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        mission_status = mission_check(member.id)
        mission_btn = interaction.component.custom_id
        channel_id = players_mission_channel(member.id)
        channel_name = interaction.guild.get_channel(channel_id)
        in_mission = self.bot.get_channel(911285052204257371)
        success_mission = self.bot.get_channel(936149260540461106)
        create_channel = 'ระบบกำลังสร้างห้องส่งภารกิจให้กับคุณ กรุณารอสักครู่'
        code = random.randint(0, 99999)
        room = str(code)

        if mission_status == 0:
            data = None
            embed = None
            message = None
            channel = None
            if mission_btn == 'mission_hunter':
                number = random.randint(0, 11)
                mission_btn = hunter_mission()  # type list
                data = mission_btn[number]  # type tuple
                player_mission = players_mission(member.id)

                if player_mission is None:
                    print(player_mission)
                    players_new_mission(member.id, member.name, data[1], data[2])
                elif player_mission is not None:
                    player = get_players_mission(member.id)
                    await interaction.respond(content='⚠ Error: Mission inprogress !'
                                                      '\nคุณยังนำสั่งภารกิจ **{}** ไม่สำเร็จ'.format(player[3]))
                    return

            elif mission_btn == 'mission_fishing':
                number = random.randint(0, 11)
                mission_btn = fishing_mission()  # type list
                data = mission_btn[number]  # type tuple
                player_mission = players_mission(member.id)
                if player_mission is None:
                    print(player_mission)
                    players_new_mission(member.id, member.name, data[1], data[2])
                elif player_mission is not None:
                    player = get_players_mission(member.id)
                    await interaction.respond(content='⚠ Error: Mission inprogress !'
                                                      '\nคุณยังนำสั่งภารกิจ **{}** ไม่สำเร็จ'.format(player[3]))
                    return

            elif mission_btn == 'mission_famer':
                number = random.randint(0, 21)
                mission_btn = famer_mission()  # type list
                data = mission_btn[number]  # type tuple
                player_mission = players_mission(member.id)
                if player_mission is None:
                    print(player_mission)
                    players_new_mission(member.id, member.name, data[1], data[2])
                elif player_mission is not None:
                    player = get_players_mission(member.id)
                    await interaction.respond(content='⚠ Error: Mission inprogress !'
                                                      '\nคุณยังนำสั่งภารกิจ **{}** ไม่สำเร็จ'.format(player[3]))
                    return
            elif mission_btn == 'mission_report':
                print(channel_name)
                if channel_name is None:
                    print('Create new text channel')
                    await interaction.respond(content=create_channel)
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
                    include = self.bot.get_channel(channel.id)
                    name = players_mission(member.id)
                    img = get_img_from_mission(name)
                    player = get_players_mission(member.id)
                    embed = discord.Embed(
                        title=f'ภารกิจ {player[3]} โดย {player[2]}'
                    )
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_image(url=img)
                    await include.send(
                        f'{member.mention}',
                        file=discord.File('./img/mission/mission_center.png')
                    )
                    await include.send(
                        '**📃 ขั้นตอนการส่งภารกิจ** '
                        '\nผู้เล่นต้องนำสินค้ามาส่งให้กับ Guild Master ที่ตำแหน่ง '
                        'C3N1 ที่โรงนาชั้น 2 ให้ผู้เล่นนำสินค้าใส่ไว้ในตู้ และล็อคกุญแจตู้ให้เรียบร้อย '
                        'หลังจากนั้นให้ผู้เล่นถ่ายภาพสินค้าข้างในตู้ และกดที่ปุ่มสีฟ้า 🟦 (UPLOAD IMAGE) '
                        'เพื่ออัพโหลดภาพ หลังระบบจะส่งขอมูลภารกิจให้แอดมินเพื่อแจ้งให้ทีมงานจ่ายรางวัล '
                        'และเมื่อผู้เล่นอัพโหลดภาพสินเค้าเรียบร้อย ปุ่มรีเซ็ตภารกิจใหม่จะทำงาน 🟥 (RESET) '
                        'ให้ผู้เล่นกดที่ปุ่ม RESET เพื่อปิดห้องส่งภารกิจ และจะสามารถกดรับภารกิจใหม่ได้'
                    )
                    coins = '${:,d}'.format(player[7])
                    await include.send(

                        embed=embed,
                        components=[
                            [
                                Button(style=ButtonStyle.gray, label=f'AWORD {coins}', emoji='💵',
                                       custom_id='shopping_cart', disabled=True),
                                Button(style=ButtonStyle.blue, label='UPLOAD IMAGE', emoji='📷',
                                       custom_id='upload_image_mission'),
                                Button(style=ButtonStyle.red, emoji='⏱',
                                       custom_id='self_reset_mission', disabled=True)
                            ]
                        ]
                    )
                    players_update_report_misson(channel.id, member.id)
                    await interaction.channel.send(content=f'ไปยังห้องส่งภารกิจของคุณ <#{channel.id}>', delete_after=5)
                else:
                    channel = players_mission_channel(member.id)
                    await interaction.respond(content=f'ไปยังห้องส่งภารกิจของคุณ <#{channel}>')
                    return
                return
            elif mission_btn == 'mission_reset':
                check = check_players_mission(member.id)
                if check == 1:
                    await interaction.respond(content='คุณเสียค่าปรับจำนวน $100 สำหรับการรีเซ็ตภารกิจในครั้งนี้')
                    return
                else:
                    await interaction.respond(content='คุณไม่มีภารกิจที่ต้อง รีเซ็ตใหม่')
                    return
            elif mission_btn == 'upload_image_mission':
                check = check_players_mission(member.id)
                if check == 1:
                    await interaction.respond(content='upload image')

                    def check(res):
                        attachments = res.attachments
                        if len(attachments) == 0:
                            return False
                        attachment = attachments[0]
                        return attachment.filename.endswith(('.jpg', '.png'))

                    msg = await self.bot.wait_for('message', check=check)
                    if msg is not None:

                        await interaction.channel.send(
                            f'🎉 ยินดีด้วยคุณได้รับค่า 🎖exp จำนวน ในภารกิจนี้\n'
                            f'โปรดรอการตรวจสอบและจ่ายรางวัลจากทีมงานในเวลาต่อไป')
                    return
                else:
                    await interaction.respond(content='คุณไม่มีภารกิจที่ต้อง รีเซ็ตใหม่')
                    return
            elif mission_btn == 'self_mission_reset':
                return
            elif mission_btn == 'mission_check':
                check = check_players_mission(member.id)
                if check == 1:
                    player = get_players_mission(member.id)
                    print(player)
                    if player[4] == 1:
                        message = "INPROGRESS"
                    msg = f'MISSION OWN : {player[2]}\n'
                    f'MISSION NAME : {player[3]}\n'
                    f'MISSION STATUS : {message}\n'
                    f'AWARD : {player[7]}'
                    await interaction.respond(
                        content=msg

                    )
                    return
                else:
                    await interaction.respond(content='คุณยังไม่ได้กดรับภารกิจ')
                    return

            else:
                pass
            embed = discord.Embed(
                title=f'🥩 **{data[1]}**',
                description=f'{data[1]} ที่ Guild Master ตำแหน่ง C1N3 (ทะเลสาบ)',
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

            await interaction.respond(embed=embed)

        elif mission_status == 1:
            await interaction.respond(content='mission already exists')


def setup(bot):
    bot.add_cog(MissionEvent(bot))
