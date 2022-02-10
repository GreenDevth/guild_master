import random

import discord
from discord.ext import commands
from mission.mission_db import *
from mission.mission_list import foods, fishing, animal, guild_master_img


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

        if interaction.component.custom_id == 'mission_hunter':
            img = random.choice(animal)
            award = 1000
            embed = discord.Embed(
                title=f'ภารกิจหมายเลข {random.randint(9,99999)}',
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
                await interaction.respond(content=f'Your current mission is a **{current_mission}**')

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
                    await include_channel.send('ok')
                    channel_id_update(member.id, channel.id)
                if channel_name is not None:
                    await interaction.respond(content=f'goto your report mission channel <#{channel_id}>')
                channel_id = get_channel_id(member.id)
                await interaction.respond(content=f' goto your report mission channel <#{channel_id}> {round(self.bot.latency*1000)}ms')
                # await interaction.respond(content='⚠ คุณยังไม่มีภารกิจที่ต้องส่ง')
            await interaction.respond(content='⚠ คุณยังไม่มีภารกิจที่ต้องส่ง')

        if interaction.component.custom_id == 'mission_reset':
            if mission_check == 1:
                print('continue reset')
                await interaction.respond(content='continue reset command')
            await interaction.respond(content='⚠ คุณยังไม่มีภารกิจให้รีเซ็ต')



def setup(bot):
    bot.add_cog(MissionButtonEventCommand(bot))
