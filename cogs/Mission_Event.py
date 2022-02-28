import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from mission.Mission_db import *


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
        check_mission = check_players_mission(member.id)
        scum_player = get_scum_players(member.id)
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
                if check_mission == 0:
                    players_new_mission(member.id, member.name, data[1], data[2])
                elif player_mission == 0:
                    update_mission(member.id, data[1], data[2])
                elif player_mission == 1:
                    player = get_players_mission(member.id)
                    await interaction.respond(content='⚠ Error: Mission inprogress !'
                                                      '\nคุณยังนำสั่งภารกิจ **{}** ไม่สำเร็จ'.format(player[3]))
                    return

            elif mission_btn == 'mission_fishing':
                number = random.randint(0, 11)
                mission_btn = fishing_mission()  # type list
                data = mission_btn[number]  # type tuple
                player_mission = players_mission(member.id)
                if check_mission == 0:
                    players_new_mission(member.id, member.name, data[1], data[2])
                elif player_mission == 0:
                    update_mission(member.id, data[1], data[2])
                elif player_mission == 1:
                    player = get_players_mission(member.id)
                    await interaction.respond(content='⚠ Error: Mission inprogress !'
                                                      '\nคุณยังนำสั่งภารกิจ **{}** ไม่สำเร็จ'.format(player[3]))
                    return

            elif mission_btn == 'mission_famer':
                number = random.randint(0, 21)
                mission_btn = famer_mission()  # type list
                data = mission_btn[number]  # type tuple
                player_mission = players_mission(member.id)
                if check_mission == 0:
                    players_new_mission(member.id, member.name, data[1], data[2])
                elif player_mission == 0:
                    update_mission(member.id, data[1], data[2])
                elif player_mission == 1:
                    player = get_players_mission(member.id)
                    await interaction.respond(content='⚠ Error: Mission inprogress !'
                                                      '\nคุณยังนำสั่งภารกิจ **{}** ไม่สำเร็จ'.format(player[3]))
                    return
            elif mission_btn == 'mission_report':
                check_report = players_mission(member.id)
                if check_report == 1:
                    mission_id = get_players_mission(member.id)
                    room = str(mission_id[0])
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
                        player = get_players_mission(member.id)
                        img = get_img_from_mission(player[3])
                        print(player)
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
                        await interaction.channel.send(content=f'ไปยังห้องส่งภารกิจของคุณ <#{channel.id}>',
                                                       delete_after=5)
                    else:
                        channel = players_mission_channel(member.id)
                        await interaction.respond(content=f'ไปยังห้องส่งภารกิจของคุณ <#{channel}>')
                        return
                else:
                    message = '⚠ Error, คุยยังไม่มีภารกิจที่ต้องส่งในตอนนี้'
                    await interaction.respond(content=message)
                    return
                return
            elif mission_btn == 'mission_reset':
                check = check_players_mission(member.id)
                if check == 1:
                    fine = 100
                    if fine <= scum_player[5]:
                        update = scum_player[5] - fine
                        total = update_coins(member.id, update)
                        reset_mission(member.id)
                        message = f'ระบบได้หักค่าปรับจำนวน $100 สำเร็จ : ยอดเงินคงเหลือของคุณคือ : {total}' \
                                  f'\nคุณสามารถกดรับภารกิจใหม่ได้แล้ว'
                        # await discord.DMChannel.send(member, message)

                    elif scum_player[5] < fine:
                        message = '⚠ Error, ยอดเงินของคุณไม่เพียงพอสำหรับการจ่ายค่ารีเซ็ตภารกิจ'
                    await interaction.respond(content=message)
                    return
                else:
                    await interaction.respond(content='คุณไม่มีภารกิจที่ต้อง รีเซ็ตใหม่')
                    return
            elif mission_btn == 'upload_image_mission':
                player = get_players_mission(member.id)
                coins = '${:,d}'.format(player[7])
                check = check_players_mission(member.id)
                if check == 1:
                    await interaction.edit_origin(
                        components=[
                            [
                                Button(style=ButtonStyle.gray, label=f'AWORD {coins}', emoji='💵',
                                       custom_id='shopping_cart', disabled=True),
                                Button(style=ButtonStyle.green, label='DISABLE', emoji='📷',
                                       custom_id='upload_image_mission', disabled=True),
                                Button(style=ButtonStyle.red, label='RESET MISSION', emoji='⏱',
                                       custom_id='self_reset_mission', disabled=False)
                            ]
                        ]
                    )
                    msg_send = await interaction.channel.send(
                        '🖼 กรุณาอัพโหลดภาพสินค้าของคุณ สำหรับให้ทีมงานตรวจสอบและดำเนินการจ่ายรางวัลสำหรับภารกิจนี้'
                    )

                    def check(res):
                        attachments = res.attachments
                        if len(attachments) == 0:
                            return False
                        attachment = attachments[0]
                        return attachment.filename.endswith(('.jpg', '.png', '.jpeg'))

                    msg = await self.bot.wait_for('message', check=check)
                    if msg is not None:
                        image = msg.attachments[0]
                        update_mission_img(member.id)
                        exp = int(player[7])
                        update = exp + scum_player[7]
                        update_player_exp(member.id, update)

                        message = f"🎉 ยินดีด้วยคุณได้รับ 🎖 {exp} exp" \
                                  f" โปรดรอการตรวจสอบความถูกต้องของสินค้าเพื่อจ่ายรางวัลจำนวน {exp} จากทีมงานนะครับ"
                        embed = discord.Embed(
                            title=f'ภารกิจ {player[3]} สำเร็จ โดย {player[2]}',
                            colour=discord.Colour.green()
                        )
                        embed.set_author(name=member.name, icon_url=member.avatar_url)
                        embed.set_thumbnail(url=member.avatar_url)
                        embed.set_image(url=image)
                        embed.add_field(name='ผู้ส่งภารกิจ', value=member.mention)
                        embed.add_field(name='รางวันภารกิจ', value=f'💵 {exp}')
                        embed.add_field(name='รางวัล exp', value=f'🎖 {exp}')
                        embed.set_footer(text='รางวันภารกิจจะได้รับหลังจากทีมงานได้ตรวจสอบสินค้าเป็นที่เรียบร้อย')
                        success_channel = self.bot.get_channel(936149260540461106)
                        await success_channel.send(member.mention, embed=embed)
                        await discord.DMChannel.send(
                            member,
                            f"🎉 ส่งภารกิจเรียบร้อย คุณได้รับ 🎖{exp} exp ค่าประสบการณ์ของคุณตอนนี้คือ 🎖 {update} exp"
                        )
                    await interaction.channel.send(message, delete_after=5)
                    await asyncio.sleep(5.5)
                    # await msg.delete()
                    await msg_send.delete()
                    return
                else:
                    await interaction.respond(content='คุณไม่มีภารกิจที่ต้อง รีเซ็ตใหม่')
                    return
            elif mission_btn == 'self_reset_mission':
                player = get_players_mission(member.id)
                if player[5] == 0:
                    message = "⚠ Error, คุณยังไม่ได้ส่งภารกิจ"
                    await interaction.respond(content=message)
                    return
                elif player[5] == 1:
                    reset_mission(member.id)
                    message = 'ระบบได้ทำการรีเซ็ตภารกิจให้คุณแล้ว ระบบจะทำการปิดห้องให้คุณ' \
                              'หลังจากทีมงานได้ตอบสอบความถูกต้องของสินค้าเรียบร้อยแล้ว'
                    await interaction.edit_origin(
                            components=[]
                        )
                await interaction.channel.send(content=message)
                return
            elif mission_btn == 'mission_check':
                check = check_players_mission(member.id)
                if check == 1:
                    player = get_players_mission(member.id)
                    img = get_img_from_mission(player[3])
                    embed = discord.Embed(
                        title=f'ภารกิจ {player[3]} โดย {player[2]}'
                    )
                    embed.set_author(name=member.name, icon_url=member.avatar_url)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_image(url=img)
                    await interaction.respond(content=embed)
                    return
                else:
                    await interaction.respond(content='คุณยังไม่ได้กดรับภารกิจ')
                    return

            else:
                pass
            embed = discord.Embed(
                title=f'🥃 **{data[1]}**',
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
            inprogress = self.bot.get_channel(911285052204257371)
            await interaction.respond(embed=embed)
            await discord.DMChannel.send(member, embed=embed)
        elif mission_status == 1:
            await interaction.respond(content='คุณกำลังรับภารกิจพิเศษอยู่ กรุณาส่งภารกิจก่อนเพื่อรับภารกิจทั่วไป')


def setup(bot):
    bot.add_cog(MissionEvent(bot))
