import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from mission.Mission_db import get_mission
from events.Get_mission import GetMission, ReportMission


class GuildMasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='group_mission')
    async def group_mission_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/mission/mission_ban.png')
        )
        await ctx.send(
            '\nผู้เล่นจะต้องนำส่งสินค้าที่ได้จากการกดรับภารกิจมาส่ง ที่ '
            '\nGuild Master ตำแหน่ง C3N1 (ทะเลสาบ)'
            '\nโดยจำนวนสินค้า ชนิด และรางวัลประจำภารกิจจะถูกระบุไว้'
            '\nในภาพที่ได้จากการกดรับภารกิจ '
            '\n\n📋 **คำอธิบายสำหรับปุ่มคำสั่ง** '
            '\n- กดปุ่ม REPORT เพื่อเปิดห้องส่งภารกิจ '
            '\n- กดปุ่ม RESET เพื่อรีเซ็ตภารกิจ มีค่าบริการ $100'
            '\n- กดปุ่ม YOU MISSION เพื่อแสดงภารกิจของคุณ'
        )
        await ctx.send(
            file=discord.File('./img/mission/mission_2.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, label='HUNTING', emoji='🥩', custom_id='1000'),
                    Button(style=ButtonStyle.gray, label='FISHERMAN', emoji='🎣', custom_id='1500'),
                    Button(style=ButtonStyle.gray, label='FAMER', emoji='👨‍🌾', custom_id='500')
                ],
                [
                    Button(style=ButtonStyle.blue, label=' REPORT', emoji='✉', custom_id='mission_report'),
                    Button(style=ButtonStyle.red, label=' RESET', emoji='⏱', custom_id='mission_reset'),
                    Button(style=ButtonStyle.blue, label='YOU MISSION', emoji='📃', custom_id='mission_check')
                ]

            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(GuildMasterCommand(bot))
    bot.add_cog(GetMission(bot))
    bot.add_cog(ReportMission(bot))
