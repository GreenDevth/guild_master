import discord
from discord.ext import commands
from mission.mission_db import *


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
        if interaction.component.custom_id == 'mission_hunter':
            award = 1000
            if mission_check == 0:
                """ Create New Misson """
                new_mission(member.id, member.name, get_mission(2), award)
                print(f'New Mission recode by {member.id}')
            else:
                await interaction.respond(content=f'Your current mission is a **{current_mission}**')

            await interaction.respond(content=f'{member.name} are clicked.')

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
            await interaction.respond('⚠ คุณยังไม่มีภารกิจให้รีเซ็ต')



def setup(bot):
    bot.add_cog(MissionButtonEventCommand(bot))
