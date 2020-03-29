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
            lounge_channel_role = guild.get_role('') # FIXME: role_id（ `ラウンジ用チャット` を表示/非表示させるための権限）
            if before.channel is None:
                if after.channel.name == 'ラウンジ（会話有）':
                    await member.add_roles(lounge_channel_role)
            elif after.channel is None:
                if before.channel.name == 'ラウンジ（会話有）':
                    await member.remove_roles(lounge_channel_role)
            

client.run(setting.dToken)
