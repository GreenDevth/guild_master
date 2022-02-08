import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from db.players_db import players_exists
from mission.mission_db import new_mission, mission_exists, get_mission_name
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

        if v_btn == 'mission_v':
            """ Check register players """
            order_code = str(member.id)
            convert = order_code[:5]
            gen_code = str(convert)
            img = random.choice(foods)
            in_progress = self.bot.get_channel(926894035707244626)
            check = players_exists(member.id)
            mission_name = "ภารกิจนำส่งผักผลไม้"
            mission_check = mission_exists(member.id)
            award = 500
            if check == 1 and mission_check == 0:
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
                await interaction.respond(content="คุณสามารถดูภารกิจของคุณได้ที่ห้อง <#911285052204257371>", embed=embed)
                await in_progress.send(embed=embed)

                new_mission(member.id, member.name, mission_name, award)

                return True
            elif check == 1 and mission_check == 1:
                your_mission = get_mission_name(member.id)
                await interaction.respond(content=f'⚠ คุณยังทำ ``{your_mission}`` ไม่สำเร็จ')
            else:
                await interaction.respond(content=f'Status {check} : your informaion is not found!')


def setup(bot):
    bot.add_cog(MissionV(bot))
