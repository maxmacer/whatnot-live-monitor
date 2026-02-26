import discord,sys
from discord.ext import commands
from config import BOT_TOKEN, BOT_PREFIX
from whatnot.monitor import Monitor
from utils.notifications import Notifications
from utils.presence_manager import PresenceManager
from utils.file_manager import FileManager

class MonitorBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None,intents=discord.Intents.all())
        self.remove_command('help')
        self.presence = PresenceManager(self)
        self.notifications = Notifications(self)
        self.fm = FileManager()
        self.monitor = Monitor(self.notifications, self.presence, self.fm)
        
    async def setup_hook(self):
        await self.load_extension('cogs.slash_commands')
        synced = await self.tree.sync()
        print(f'Synced {len(synced)} commands.')

    async def on_ready(self):
        print(f'Bot up and running, under {self.user}')
        
        if self.notifications:
            await self.notifications.setup_channel()
            print("Notifications - All Green.")

        if self.monitor:
            await self.monitor.start_when_ready()
            print("Monitor - All Green.")

bot = MonitorBot()

if __name__ == '__main__':
    bot.run(BOT_TOKEN, log_handler=None)