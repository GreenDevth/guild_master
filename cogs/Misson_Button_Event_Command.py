import asyncio
import random

import discord
from discord.ext import commands
from mission.mission_db import *
from mission.mission_list import foods, fishing, animal, guild_master_img
from discord_components import Button, ButtonStyle


class MissionButtonEventCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        mission_check = mission_exists(member.id)
        current_mission = get_mission_name(member.id)
        channel_id = get_channel_id(member.id)
        channel_name = interaction.guild.get_channel(channel_id)
        in_progress = self.bot.get_channel(911285052204257371)
        success = self.bot.get_channel(936149260540461106)
        image_check = get_image_status(member.id)
        player_exp = players_exp(member.id)
        player_coin = players_coins(member.id)


        if interaction.component.custom_id == 'mission_hunter':
            img = random.choice(animal)
            award = 1000
            embed = discord.Embed(
                title=f'ภารกิจหมายเลข {random.randint(9, 99999)}',
                description=f'ผู้เล่นต้องนำสินค้าภารกิจมาส่งที่ ตำแหน่ง C3N1 พื้นที่ของ Guild Master เท่านั้น ',
                colour=discord.Colour.red()
            )
            embed.set_thumbnail(url=guild_master_img)
            embed.set_image(url=img)
            embed.add_field(name='👨‍🌾 ผู้รับภารกิจ', value=member.mention, inline=False)
            embed.add_field(name='💰 รางวัลสำหรับภารกิจ', value="${:d} เหรียญ".format(award))
            embed.add_field(name="🎖 exp", value=f"{award}")
            embed.set_footer(text="ต้องส่งภารกิจก่อนทุกครั้งผู้เล่นถึงจะสามารถรับภารกิจใหม่ได้")

            if mission_check == 0:
                """ Create New Misson """
                new_mission(member.id, member.name, get_mission(2), award)
                print(f'New Mission recode by {member.id}')
                await in_progress.send(embed=embed)
            else:
                await interaction.respond(content=f'คุณยังทำ **{current_mission}** ไม่สำเร็จ ')

            await interaction.respond(content='ขอให้สนุกกับการทำภารกิจในครั้งนี้ ภารกิจของคุณคือ ', embed=embed)

        if interaction.component.custom_id == 'mission_report':
            print(mission_check)
            if mission_check == 1:
                if channel_name is None:
                    print('Create new text_channel')
                    """ Create text_channel """
                    category = discord.utils.get(interaction.guild.categories, name='MISSION')
                    overwrites = {
                        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
                        member: discord.PermissionOverwrite(read_messages=True)
                    }
                    await category.edit(overwrites=overwrites)
                    new_channel_name = f'ห้องส่งภารกิจ-{mission_id(member.id)}'
                    await interaction.guild.create_text_channel(new_channel_name, category=category)
                    channel = discord.utils.get(interaction.guild.channels, name=str(new_channel_name))
                    include_channel = self.bot.get_channel(channel.id)
                    await interaction.respond(content=f'ไปยังห้องส่งภารกิจ <#{channel.id}>')
                    await include_channel.send(
                        '**ขั้นตอนการส่งภารกิจ** '
                        '\nผู้เล่นต้องนำสินค้ามาส่งให้กับ Guild Master ที่ตำแหน่ง C3N1 ที่โรงนาชั้น 2 ให้ผู้เล่นนำสินค้าใส่ไว้ในตู้\nและล็อคกุญแจตู้ '
                        'หลังจากนั้นให้ผู้เล่นถ่ายภาพสินค้าข้างในตู้ และกดที่ปุ่มสีฟ้า (SEND MISSION)\nเพื่ออัพโหลดภาพและส่งให้แอดมิน'
                        '\n\n**คำอธิบายสำหรับปุ่มคำสั่ง** '
                        '\n- ปุ่ม SEND MISSION กดเพื่อส่งภาพภารกิจให้ทีมงานแอดมิน '
                        '\n- ปุ่ม RESET เพื่อรีเซ็ตภารกิจ และปิดระบบส่งภารกิจ '
                    )
                    await include_channel.send(
                        file=discord.File('./img/mission/mission_center.png'),
                        components=[
                            [
                                Button(style=ButtonStyle.green, label='SHOPPING CART', emoji='🛒',
                                       custom_id='shopping_cart', disabled=True),
                                Button(style=ButtonStyle.blue, label='SEND MISSION', emoji='📧',
                                       custom_id='upload_image_mission'),
                                Button(style=ButtonStyle.red, label='RESET', emoji='⏱',
                                       custom_id='self_reset_mission')
                            ]
                        ]
                    )
                    channel_id_update(member.id, channel.id)

                if channel_name is not None:
                    await interaction.respond(content=f'ไปยังห้องส่งภารกิจ <#{channel_id}>')
            await interaction.respond(content='⚠ คุณยังไม่มีภารกิจที่ต้องส่ง')

        if interaction.component.custom_id == 'mission_reset':
            if mission_check == 1:
                print('continue reset')
                coin = player_coin - 100
                if player_coin < 100:
                    await interaction.respond(content='ขออภัยทำรายการไม่สำเหร็จ : ยอดเงินของคุณไม่เพียงพอ')
                else:
                    update_coin(member.id, coin)
                    mission_solf_reset(member.id)
                    await interaction.respond(content='รีเซ็ตภารกิจใหม่เรียบร้อย ระบบกำลังจะทำการปิดใน 10 วินาที ')
                    await discord.DMChannel.send(member, f'ระบบทำการหักเงินจำนวน 100 จาก {player_coin} จำนวนเงินคงเหลือของคุณคือ {coin}')
                    await asyncio.sleep(9)
                    delete_channel = self.bot.get_channel(channel_id)
                    await delete_channel.delete()

            await interaction.respond(content='⚠ คุณยังไม่มีภารกิจให้รีเซ็ต')

        if interaction.component.custom_id == 'upload_image_mission':
            if image_check == 0:
                award = mission_award(member.id)
                print('continue upload image and update image status to 1')
                await interaction.respond(content='กรุณาอัพโหลดภาพถ่ายสินค้าภารกิจของคุณ')

                def check(message):
                    attachments = message.attachments
                    if len(attachments) == 0:
                        return False
                    attachment = attachments[0]
                    return attachment.filename.endswith(('.jpg', '.png'))

                msg = await self.bot.wait_for('message', check=check)
                if msg is not None:
                    update_image_status(member.id)
                    exp = player_exp + award
                    exp_up(member.id, exp)
                    await interaction.channel.send(
                        f'🎉 ยินดีด้วยคุณได้รับค่า 🎖exp จำนวน {award} ในภารกิจนี้\nโปรดรอการตรวจสอบและจ่ายรางวัลจากทีมงานในเวลาต่อไป')
                image = msg.attachments[0]
                embed = discord.Embed(
                    title=f'ส่งภารกิจโดย {member.name}',
                    description='ขอแสดงความยินดีกับรางวัลความสำเร็จของภารกิจในครั้งนี้ ',
                    color=discord.Colour.green()
                )
                embed.set_image(url=image)
                embed.add_field(name='ผู้ส่งภารกิจ', value=member.mention, inline=False)
                embed.add_field(name='💰 รางวัลที่ได้รับ', value='${:d}'.format(award), inline=True)
                embed.add_field(name='🎚 EXP ที่ได้รับ', value=f"{award}", inline=True)
                # embed.add_field(name='🏆 Level ปัจจุบัน', value=f'{player_info[6]}')
                # embed.add_field(name='🎚 EXP ปัจจุบัน', value=f'{player_info[8]}')
                msg = await success.send(embed=embed)
                await msg.add_reaction("❔")
            await interaction.respond(content='⚠ คุณยังไม่มีภารกิจที่ต้องส่งในตอนนี้')

        if interaction.component.custom_id == 'self_reset_mission':
            if image_check == 1:
                print('continue for reset player mission')
                mission_solf_reset(member.id)
                await interaction.respond(content='รีเซ็ตภารกิจใหม่เรียบร้อย ระบบกำลังจะทำการปิดใน 10 วินาที ')
                await asyncio.sleep(9)
                await interaction.channel.delete()
            await interaction.respond(
                content='⚠ คุณยังไม่ส่งภารกิจให้สำเร็จ การรีเซ็ตนี้จะไม่ทำงาน โปรดส่งภารกิจให้เรียบร้อย')


def setup(bot):
    bot.add_cog(MissionButtonEventCommand(bot))
