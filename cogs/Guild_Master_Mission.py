import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from mission.mission_db import get_mission


class GuildMasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='famer')
    async def famer_command(self, ctx):
        await ctx.send(
            f'**🥩 {get_mission(2)}** '
            '\nผู้เล่นจะต้องนำส่งสินค้าที่ได้จากการกดรับภารกิจมาส่ง ที่ Guild Master ตำแหน่ง C1N3 (ทะเลสาบ)'
            '\nโดยจำนวนสินค้า ชนิด และรางวัลประจำภารกิจจะถูกระบุไวในภาพที่ได้จากการกดรับภารกิจ '
            '\n\n**คำอธิบายปุ่มต่าง ๆ** '
            '\nGET MISSION ปุ่มสำหรับรับภารกิจ '
            '\nREPORT MISSION ปุ่มสำหรับเปิดห้องเพื่อส่งมอบสินค้า '
            '\nRESET ปุ่มสำหรับรีเซ็ตภารกิจโดยต้องเสียค่าปรับ **100** เหรียญ'
        )
        await ctx.send(
            file=discord.File('./img/mission/animals.jpg'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET MISSION', emoji='⚔', custom_id='mission_hunter'),
                    Button(style=ButtonStyle.blue, label='REPORT MISSION', emoji='📩', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱', custom_id='mission_reset')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(GuildMasterCommand(bot))
