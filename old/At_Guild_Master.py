import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle


class AtGuildMasterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='guild', invoke_without_command=True)
    @commands.has_role('Admin')
    async def guild_command(self, ctx):
        await ctx.reply('This command only used in admin role.')
        await ctx.message.delete()

    @guild_command.command(name='at_guild')
    async def at_guild_sub_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/mission/mission_center.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='เรียกใช้บริการ taxi', emoji='🚘', custom_id='taxi_to_guild'),
                    Button(style=ButtonStyle.gray, label='ค่าบริการ 100 เหรียญ', emoji='💵', disabled=True)
                ]
            ]
        )


def setup(bot):
    bot.add_cog(AtGuildMasterCommand(bot))
