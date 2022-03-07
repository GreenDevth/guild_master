import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from db.Players_db import players_info


class GuildLocation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        guild_location = ["guild_location"]
        btn = interaction.component.custom_id
        if btn in guild_location:
            cmd = self.bot.get_channel(927796274676260944)
            teleport = '.set #Teleport 240610.469 82449.469 26973.654 {}'.format(players_info(member.id)[3])
            message = 'โปรดรอสักครู่ ระบบกำลังส่งคุณไปยังที่ทำการผู้ใหญ่บ้าน'
            await interaction.respond(content=message)
            await cmd.send(teleport)
            return
        return

    @commands.command(name='guild_location')
    async def guild_location(self, ctx):
        await ctx.send(
            file=discord.File('./img/vehicle_zero.png'),
            components=[Button(style=ButtonStyle.blue, label='GUILD', emoji='✈', custom_id='guild_location')]
        )


def setup(bot):
    bot.add_cog(GuildLocation(bot))
