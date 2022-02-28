import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from mission.Mission_db import get_mission


class GuildMasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='group_mission')
    async def group_mission_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/mission/mission_ban.png')
        )
        await ctx.send(
            '\nผู้เล่นจะต้องนำส่งสินค้าที่ได้จากการกดรับภารกิจมาส่ง ที่ Guild Master ตำแหน่ง C3N1 (ทะเลสาบ)'
            '\nโดยจำนวนสินค้า ชนิด และรางวัลประจำภารกิจจะถูกระบุไวในภาพที่ได้จากการกดรับภารกิจ '
            '\n\n📋 **คำอธิบายสำหรับปุ่มคำสั่ง** '
            '\n- ปุ่ม REPORT MISSION กดเพื่อเปิดห้องส่งภารกิจ '
            '\n- ปุ่ม RESET MISSION เพื่อรีเซ็ตภารกิจ ระบบจะหักค่าปรับจำนวน $100 จากบัญชีของคุณ'
        )
        await ctx.send(
            file=discord.File('./img/mission/mission.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, label='HUNTING QUEST', emoji='🥩', custom_id='mission_hunter'),
                    Button(style=ButtonStyle.gray, label='FISHING QUEST', emoji='🎣', custom_id='mission_fishing'),
                    Button(style=ButtonStyle.gray, label='FAMER QUEST', emoji='👨‍🌾', custom_id='mission_famer')
                ],
                [
                    Button(style=ButtonStyle.blue, label=' REPORT MISSION ', emoji='✉', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label=' RESET MISSION', emoji='⏱', custom_id='mission_reset'),
                    Button(style=ButtonStyle.blue, label=' YOUR MISSION', emoji='📃', custom_id='mission_check')
                ]

            ]
        )
        await ctx.message.delete()

    @commands.command(name='hunter')
    async def hunter_command(self, ctx):
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
            file=discord.File('./img/mission/animal_1.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET MISSION', emoji='⚔', custom_id='mission_hunter'),
                    Button(style=ButtonStyle.blue, label='REPORT MISSION', emoji='📩', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱', custom_id='mission_reset')
                ]
            ]
        )

    @commands.command(name='fishing')
    async def fishing_command(self, ctx):
        await ctx.send(
            f'**🦈 {get_mission(3)}** '
            '\nผู้เล่นจะต้องนำส่งสินค้าที่ได้จากการกดรับภารกิจมาส่ง ที่ Guild Master ตำแหน่ง C1N3 (ทะเลสาบ)'
            '\nโดยจำนวนสินค้า ชนิด และรางวัลประจำภารกิจจะถูกระบุไวในภาพที่ได้จากการกดรับภารกิจ '
            '\n\n**คำอธิบายปุ่มต่าง ๆ** '
            '\nGET MISSION ปุ่มสำหรับรับภารกิจ '
            '\nREPORT MISSION ปุ่มสำหรับเปิดห้องเพื่อส่งมอบสินค้า '
            '\nRESET ปุ่มสำหรับรีเซ็ตภารกิจโดยต้องเสียค่าปรับ **100** เหรียญ'
        )
        await ctx.send(
            file=discord.File('./img/mission/fishing.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET MISSION', emoji='⚔', custom_id='mission_fishing'),
                    Button(style=ButtonStyle.blue, label='REPORT MISSION', emoji='📩', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱', custom_id='mission_reset')
                ]
            ]
        )

    @commands.command(name='famer')
    async def famer_command(self, ctx):
        await ctx.send(
            f'**🍅 {get_mission(1)}** '
            '\nผู้เล่นจะต้องนำส่งสินค้าที่ได้จากการกดรับภารกิจมาส่ง ที่ Guild Master ตำแหน่ง C3N1 (ทะเลสาบ)'
            '\nโดยจำนวนสินค้า ชนิด และรางวัลประจำภารกิจจะถูกระบุไวในภาพที่ได้จากการกดรับภารกิจ '
            '\n\n**คำอธิบายปุ่มต่าง ๆ** '
            '\nGET MISSION ปุ่มสำหรับรับภารกิจ '
            '\nREPORT MISSION ปุ่มสำหรับเปิดห้องเพื่อส่งมอบสินค้า '
            '\nRESET ปุ่มสำหรับรีเซ็ตภารกิจโดยต้องเสียค่าปรับ **100** เหรียญ'
        )
        await ctx.send(
            file=discord.File('./img/mission/vegetable.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GET MISSION', emoji='⚔', custom_id='mission_famer'),
                    Button(style=ButtonStyle.blue, label='REPORT MISSION', emoji='📩', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label='RESET', emoji='⏱', custom_id='mission_reset')
                ]
            ]
        )


def setup(bot):
    bot.add_cog(GuildMasterCommand(bot))
