import discord
from discord.ext import commands
from db.config import get_token, config_cogs
from discord_components import DiscordComponents
bot = commands.Bot(command_prefix='$')
DiscordComponents(bot)

token = get_token(7)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Discod Guild'))

config_cogs(bot)
bot.run(token)
