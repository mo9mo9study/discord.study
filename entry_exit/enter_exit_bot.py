import discord
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import setting
from discord.ext import tasks, commands
from datetime import datetime, timedelta

client = discord.Client()
pretime_dict = {}
botScriptPath = os.path.dirname(os.path.abspath(__file__))
logsDirectory = 'timelog'
NotRecordChannels = '時間記録無'

logsPath = botScriptPath +"/"+ logsDirectory +"/"
print(logsPath)


def writeLog(time,name,m,mdta=''):
    print(f'{name} : <ログの書き込み>')
    if not os.path.isdir(logsPath):
        os.mkdir(logsPath)
    filePath = f'{logsPath}{name}'
    if os.path.isfile(filePath):
        with open(filePath, "a", encoding="utf-8") as f:
            f.write(str(time) + ',' + name + ',' + m + ',' + mdta + '\n')
    else:
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(str(time) + ',' + name + ',' + m + ',' + mdta + '\n')

def splitTime(name):
    print(f'{name} : <ログの読み込み>')
    filePath = f'{logsPath}{name}'
    with open(filePath) as f:
        arrAlllog = f.readlines()
        strReadlog = arrAlllog[-1]
        arrSplitlog = strReadlog.split(',')
        result = arrSplitlog[0]
        dtResult = datetime.strptime(result, '%Y-%m-%d %H:%M:%S.%f')
        return dtResult


@client.event
async def on_voice_state_update(member, before, after):
    print(member.name + " : ステータスが変更されました")
    if member.bot:
        print(f'{member.name} : BOTは記録しません')
        return
    if member.guild.id == setting.dServer and (before.channel != after.channel):
        now = datetime.utcnow() + timedelta(hours=9)
        alert_channel = client.get_channel(setting.dChannel)
        if before.channel is None:
            print(f'{member.name} : 入室時の処理')
            pretime_dict['beforetime'] = datetime.now()
            msg = f'{now:%m/%d %H:%M} 　 {member.name}   joined the  {after.channel.name}'
            writeLog(datetime.now(),member.name,msg)
            if  NotRecordChannels in after.channel.name:
                print(f'{member.name} : NotRecordChannelsリストに記載されているので記録しません')
                return
            await alert_channel.send(msg)
        elif after.channel is None:
            print(f'{member.name} : 退室時の処理')
            if NotRecordChannels in before.channel.name:
                print(f'{member.name} : NotRecordChannelsリストに記載されているので記録しません')
                return
            msg = f'[{now:%m/%d %H:%M} ]  {member.name}  joined  {before.channel.name} '
            dtBefortime = splitTime(member.name)
            try:
                duration_time = dtBefortime - datetime.now()
                duration_time_adjust = int(duration_time.total_seconds()) * -1
                if duration_time_adjust >= 60:
                    print(f'{member.name} : 60sec以上')
                    minute_duration_time_adjust = int(duration_time_adjust) // 60
                    msg = "-->[" + member.name + "]   Study time： " + str(minute_duration_time_adjust) + "/分"
                    writeLog(datetime.now(),member.name,msg,str(minute_duration_time_adjust))
                    if duration_time_adjust >= 300:
                        print(f'{member.name} : 退室ログをDiscordに出力')
                        await alert_channel.send(msg)
            except KeyError:
                print(f'{member.name} : except')
                pass
            
client.run(setting.dToken)
