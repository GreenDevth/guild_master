import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle


class EventsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='velentine')
    async def valentine_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/events/gift.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='Get Free Gift',  emoji='🎁', custom_id='free_gift'),
                    Button(style=ButtonStyle.blue, label='จำนวนที่เหลือ',  emoji='⌛', disabled=True),
                    Button(style=ButtonStyle.blue, label='จำนวนทั้งหมด',  emoji='📦', disabled=True)
                ]
            ]
        )

def setup(bot):
    bot.add_cog(EventsCommand(bot))