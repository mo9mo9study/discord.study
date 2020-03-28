import discord
import os
import setting
from discord.ext import tasks, commands
from datetime import datetime, timedelta

client = discord.Client()
pretime_dict = {}

SERVER = setting.dServer 


@client.event
async def on_voice_state_update(member, before, after):
    if member.name != 'ブレーメン音楽隊':
        if member.guild.id == SERVER and (before.channel != after.channel):
            if before.channel is None:
                if after.channel.name == 'リモートワーク用':
                    discord.unils.get(message
            elif after.channel is None:
                if before.channel.name == 'リモートワーク用':
            

client.run(setting.dToken)
