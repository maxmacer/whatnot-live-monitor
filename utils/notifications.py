import asyncio
from config import NOTIFICATION_CHANNEL_ID, NOTIFICATION_PING_ROLE_ID
from ui.EmbedFactory import create_embed
import discord

class Notifications:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.notif_channel = None

    async def setup_channel(self):
        if not self.notif_channel:
            self.notif_channel = await self.bot.fetch_channel(NOTIFICATION_CHANNEL_ID)

    async def send_notification(self, live_status: bool, user: str, stream_title: str, stream_id: str, stream_thumbnail: str = None, user_pic: str = None):
        content = f'||<@{NOTIFICATION_PING_ROLE_ID}>||'
        
        if live_status:
            embed_title = f'{user} went live!'
            embed_description = f'**{stream_title}**\n\n[Click Here](https://www.whatnot.com/live/{stream_id})'
        
            embed = create_embed(title=embed_title, description=embed_description, stream_thumb=stream_thumbnail, user_pic=user_pic)
        else:
            embed_title = f'{user} went offline.'
        
            embed = create_embed(title=embed_title, user_pic=user_pic)

        await self.notif_channel.send(content=content if live_status else None, embed=embed)