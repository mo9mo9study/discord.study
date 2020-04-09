import discord
import os
import setting
from discord.ext import tasks, commands
from datetime import datetime, timedelta

client = discord.Client()
pretime_dict = {}

SERVER_ID = setting.dServer 


@client.event
async def on_voice_state_update(member, before, after):
    if member.name != 'ブレーメン音楽隊':
        if member.guild.id == SERVER_ID and (before.channel != after.channel):
            guild = client.get_guild(SERVER_ID)
            lounge_channel_role = guild.get_role(684959750236143639)
            if before.channel is None:
                if after.channel.name == '作業部屋用チャット':
                    await member.add_roles(lounge_channel_role)
            elif after.channel is None:
                if before.channel.name == '作業部屋用チャット':
                    await member.remove_roles(lounge_channel_role)

client.run(setting.dToken)
