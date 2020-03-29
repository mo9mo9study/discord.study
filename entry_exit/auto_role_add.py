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
            guild = client.get_guild('') # FIXME: guild_id
            roles = guild.get_role('') # FIXME: role_id（ `ラウンジ用チャット` の表示/非表示を切り替える）
            if before.channel is None:
                if after.channel.name == 'ラウンジ（会話有）':
                    await member.add_roles(roles)
            elif after.channel is None:
                if before.channel.name == 'ラウンジ（会話有）':
                    await member.remove_roles(roles)
            

client.run(setting.dToken)
