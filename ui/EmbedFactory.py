import discord
from datetime import datetime
from config import EMBED_COLOUR

def create_embed(title: str, description: str = None, stream_thumb: str = None, user_pic: str = None):
    embed = discord.Embed()
    
    embed.title = title
    embed.description = description
    embed.set_image(url=stream_thumb)
    embed.set_thumbnail(url=user_pic)

    embed.colour = EMBED_COLOUR
    embed.timestamp = datetime.now()
    
    return embed