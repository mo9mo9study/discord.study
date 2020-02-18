import discord
from discord.ext import commands
import datetime
import asyncio
import setting

TOKEN = setting.cToken
client = discord.Client()
@client.event
async def on_message(message):
    if "Study time" in message.content :
        await message.add_reaction(":otukaresama:625009696213958666")

client.run(TOKEN)

