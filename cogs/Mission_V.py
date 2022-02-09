import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from mission.mission_db import *
from mission.mission_list import foods, guild_master_img


class MissionV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Mission Vegetable online')

    @commands.command(name='mission_v')
    async def mission_v_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/mission/vegetable_1.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET MISSION', emoji='⚔', custom_id='mission_v'),
                    Button(style=ButtonStyle.blue, label='REPORT MISSION', emoji='📩', custom_id='mission_v_report'),
                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱', custom_id='mission_v_reset')
                ]
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        v_btn = interaction.component.custom_id
        order_code = str(member.id)
        convert = order_code[:5]
        gen_code = str(convert)
        in_progress = self.bot.get_channel(926894035707244626)
        check = player_mission(member.id)
        mission_check = mission_exists(member.id)

        if v_btn == 'mission_v':
            img = random.choice(foods)
            mission_name = "ภารกิจนำส่งผักผลไม้"
            award = 500

            if check is not None:  # Check player already exists.

                if check == 0 and mission_check == 0:  # Check for mission status and mission exists = 0.
                    mission_up(member.id)
                    new_mission(member.id, member.name, mission_name, award)  # Create new recode.
                    embed = discord.Embed(
                        title=f'ภารกิจหมายเลข {gen_code}',
                        description='คุณจะได้รับคำแนะนำสำหรับการนำส่งสินค้าเมื่อคุณกดที่ปุ่ม REPORT MISSION '
                                    'ของภารกิจที่คุณเลือก',
                        colour=discord.Colour.red()
                    )
                    embed.set_thumbnail(url=guild_master_img)
                    embed.set_image(url=img)
                    embed.add_field(name='👨‍🌾 ผู้รับภารกิจ', value=member.mention, inline=False)
                    embed.add_field(name='💰 รางวัลสำหรับภารกิจ', value="${:d} เหรียญ".format(award))
                    embed.add_field(name="🎖 exp", value=f"{award}")
                    embed.set_footer(text="ต้องส่งภารกิจก่อนทุกครั้งผู้เล่นถึงจะสามารถรับภารกิจใหม่ได้")
                    await interaction.respond(content="คุณสามารถดูภารกิจของคุณได้ที่ห้อง <#911285052204257371>",
                                              embed=embed)
                    await in_progress.send(embed=embed)

                else:
                    your_mission = get_mission_name(member.id)
                    await interaction.respond(content=f'⚠ คุณยังทำ ``{your_mission}`` ไม่สำเร็จ')
            else:
                await interaction.respond(content='⚠ ไม่พบ Steam ID ของคุณในระบบ')

        if v_btn == 'mission_v_report':
            channel = get_channel_id(member.id)
            channel_id = interaction.guild.get_channel(channel)
            room = mission_id(member.id)
            if check is not None:
                if check == 1 and mission_check == 1:  # Check for already mission exists.
                    if channel == 0 or channel_id is None:  # Check for channel or channel id exists.
                        category = discord.utils.get(interaction.guild.categories, name='MISSION')
                        overwrites = {
                            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False,
                                                                                        connect=False),
                            member: discord.PermissionOverwrite(read_messages=True)
                        }
                        await category.edit(overwrites=overwrites)
                        channel_name = f'ห้องส่งภารกิจ-{room}'
                        await interaction.guild.create_text_channel(channel_name, category=category)
                        report_channel = discord.utils.get(interaction.guild.channels, name=str(channel_name))
                        channel_send = interaction.guild.get_channel(report_channel.id)
                        channel_id_update(member.id, report_channel.id)
                        await interaction.respond(content=f'ไปที่ห้องส่งภารกิจของคุณ <#{report_channel.id}>')
                        await channel_send.send(
                            '**ขั้นตอนการส่งภารกิจ** '
                            '\nผู้เล่นต้องนำสินค้ามาส่งให้กับ Guild Master ที่ตำแหน่ง C3N1 '
                            '\nที่โรงนาชั้น 2 ให้ผู้เล่นนำสินค้าใส่ไว้ในตู้ และล็อคกุญแจตู้ '
                            '\nหลังจากนั้นให้ผู้เล่นถ่ายภาพสินค้าข้างในตู้ และกดที่ปุ่มสีฟ้า '
                            '\n(SEND MISSION) เพื่ออัพโหลดภาพและส่งให้แอดมิน'
                            '\n\n**คำอธิบายสำหรับปุ่มคำสั่ง** '
                            '\n- ปุ่ม SEND MISSION กดเพื่อส่งภาพภารกิจให้ทีมงานแอดมิน '
                            '\n- ปุ่ม RESET เพื่อรีเซ็ตภารกิจ และปิดระบบส่งภารกิจ '
                        )
                        await channel_send.send(
                            file=discord.File('./img/mission/mission_center.png'),
                            components=[
                                [
                                    Button(style=ButtonStyle.green, label='SHOPPING CART', emoji='🛒',
                                           custom_id='shopping_cart', disabled=True),
                                    Button(style=ButtonStyle.blue, label='SEND MISSION', emoji='📧',
                                           custom_id='upload_image'),
                                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱',
                                           custom_id='self_reset_mission')
                                ]
                            ]
                        )
                    else:
                        await interaction.respond(content=f'goto <#{channel}>')
                else:
                    await interaction.respond(content='⚠ คุณยังไม่มีภารกิจที่ต้องส่ง')
            else:
                await interaction.respond(content='⚠ ไม่พบ Steam ID ของคุณในระบบ')

        if v_btn == 'upload_image':

            upload_check = get_image_status(member.id)
            if upload_check == 0:
                await interaction.respond(content="อัพโหลดรูปภาพสินค้าเพื่อส่งให้ทีมงานตรวจสอบ")

                def check(message):
                    attachments = message.attachments
                    if len(attachments) == 0:
                        return False
                    attachment = attachments[0]
                    return attachment.filename.endswith(('.jpg', '.png'))

                msg = await self.bot.wait_for('message', check=check)
                image = msg.attachments[0]

                if msg is not None:
                    update_image_status(member.id)
                    await interaction.respond(content='ระบบได้ส่งรายงานภารกิจไปยังทีมงานเป็นที่เรียบร้อยแล้ว')
                else:
                    pass
            else:
                await interaction.respond(
                    content='คุณได้ส่งภารกิจไว้แล้ว กรุณารอทางทีมงานดำเนินการตรวจสอบและจ่ายรางวัลในเวลาต่อไป')


def setup(bot):
    bot.add_cog(MissionV(bot))
