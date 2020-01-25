import discord
import os
import setting
from discord.ext import tasks, commands
from datetime import datetime, timedelta

client = discord.Client()
pretime_dict = {}
botScriptPath = os.path.dirname(os.path.abspath(__file__))
logsDirectory = 'timelog'

##
logsPath = botScriptPath +"/"+ logsDirectory +"/"

##


def writeLog(time,name,m,mdta=''):
    if not os.path.isdir(logsPaht):
        os.mkdir(logsPaht)
    filePath = f'{logsPaht}{name}'
    if os.path.isfile(filePath):
        with open(filePath, "a", encoding="utf-8") as f:
            f.write(str(time) + ',' + name + ',' + m + ',' + mdta + '\n')
    else:
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(str(time) + ',' + name + ',' + m + ',' + mdta + '\n')

def splitTime(name):
    filePath = f'{logsPaht}{name}'
    with open(filePath) as f:
        arrAlllog = f.readlines()
        strReadlog = arrAlllog[-1]
        arrSplitlog = strReadlog.split(',')
        result = arrSplitlog[0]
        dtResult = datetime.strptime(result, '%Y-%m-%d %H:%M:%S.%f')
        return dtResult


@client.event
async def on_voice_state_update(member, before, after):
    if member.name != 'ブレーメン音楽隊':
        if member.guild.id == setting.dServer and (before.channel != after.channel):
            now = datetime.utcnow() + timedelta(hours=9)
            alert_channel = client.get_channel(setting.dChannel)

            if before.channel is None:
                pretime_dict['beforetime'] = datetime.now()
                msg = f'{now:%m/%d %H:%M} 　 {member.name}   joined the  {after.channel.name}'
                writeLog(datetime.now(),member.name,msg)
                await alert_channel.send(msg)
            elif after.channel is None:
                msg = f'[{now:%m/%d %H:%M} ]  {member.name}  joined  {before.channel.name} '
                dtBefortime = splitTime(member.name)
                try:
                    duration_time = dtBefortime - datetime.now()
                    duration_time_adjust = int(duration_time.total_seconds()) * -1
                    if duration_time_adjust >= 60:
                        minute_duration_time_adjust = int(duration_time_adjust) // 60
                        msg = "-->[" + member.name + "]   Study time： " + str(minute_duration_time_adjust) + "/分"
                        writeLog(datetime.now(),member.name,msg,str(minute_duration_time_adjust))
                        if duration_time_adjust >= 300:
                            await alert_channel.send(msg)
                except KeyError:
                    pass

client.run(setting.dToken)
