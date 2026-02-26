import discord

class PresenceManager:
    def __init__(self,bot: discord.Client) -> None:
        self.bot = bot
        
    async def set_presence(self, activity: str) -> None:
        game = discord.Game(name=activity)
        await self.bot.change_presence(status=discord.Status.online, activity=game)