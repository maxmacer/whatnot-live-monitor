from ui.EmbedFactory import create_embed
from discord.ext import commands
import discord

class SlashCog(commands.Cog):
    def __init__(self,bot: discord.Client):
        self.bot = bot

    @discord.app_commands.command(name='monitor_new_user',description='Add a new Whatnot user to the monitor')
    async def add_user_to_monitor(self, interaction: discord.Interaction, user: str):
        result = await self.bot.monitor.add_user_to_monitoring(user)
        if result:
            embed = create_embed(title='Added User to Monitor',description=f'Added `{user}` to the monitor!')
        else:
            embed = create_embed(title='Failed to Add User to Monitor',description=f'`{user}` is already being monitored!')
        await interaction.response.send_message(embed=embed,ephemeral=True)
    
    @discord.app_commands.command(name='monitor_remove_user',description='Remove a Whatnot user from the monitor')
    async def remove_user_from_monitor(self, interaction: discord.Interaction, user: str):
        result = await self.bot.monitor.remove_user_from_monitoring(user)
        if result:
            embed = create_embed(title='Removed User to Monitor',description=f'Removed `{user}` from the monitor!')
        else:
            embed = create_embed(title='Failed to Remove User to Monitor',description=f'`{user}` is not being monitored!')
        await interaction.response.send_message(embed=embed,ephemeral=True)
        
    @discord.app_commands.command(name='monitor_check_active',description='Check actively monitored users')
    async def check_users_monitored(self,interaction: discord.Interaction):
        active_monitor = self.bot.monitor.currently_monitoring
        users = '\n'.join(user for user in active_monitor)

        description = f'Currently monitoring:\n```\n{users}```'
        embed = create_embed(title='Actively Monitoring',description=description)
        
        await interaction.response.send_message(embed=embed,ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashCog(bot))