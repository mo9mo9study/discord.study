import discord
import os
import setting
from discord.ext import tasks, commands
from datetime import datetime, timedelta

client = discord.Client()
pretime_dict = {}
logDir = 'timelog'

##
lD = logDir

##


def writeLog(time,name,m,mdta=''):
    if not os.path.isdir(lD):
        os.mkdir(lD)
    filePath = f'{lD}/{name}'
    if os.path.isfile(filePath):
        with open(filePath, "a", encoding="utf-8") as f:
            f.write(str(time) + ',' + name + ',' + m + ',' + mdta + '\n')
    else:
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(str(time) + ',' + name + ',' + m + ',' + mdta + '\n')

def splitTime(name):
    filePath = f'{lD}/{name}'
    with open(filePath) as f:
        arrAlllog = f.readlines()
        strReadlog = arrAlllog[-1]
        arrSplitlog = strReadlog.split(',')
        result = arrSplitlog[0]
        dtResult = datetime.strptime(result, '%Y-%m-%d %H:%M:%S.%f')
        return dtResult

###########################
#@tasks.loop(seconds=60)
#async def loop():
#    now = datetime.now().strftime('%H:%M')
#    weekday = datetime.now().weekday()
#    if now == '00:38' and weekday == 0:   
#        alert_channel = client.get_channel(setting.dChannel)
#        dirListName = os.listdir(path='/home/ec2-user/discords/enter_exit/timelog')
#        ### 例外
#        dirListName.remove("lesson.py")
#        # 対象ファイル（ユーザー）一覧
#        #print(dirListName)
#        
#        strWeekResult = ""
#        arrMonthday = []
#        today = datetime.today()
#        def arrWeeklist(today):
#            global strWeekResult
#            strtoday = datetime.strftime(today, '%Y-%m-%d')
#            strWeekResult += "今日の日付：" + str(strtoday) + "\n"
#            for i in range(8):
#                if i == 0:
#                    arrMonthday.append(strtoday)
#                else:
#                    td = timedelta(days=i)
#                    strselectday = today - td
#                    arrMonthday.append(datetime.strftime(strselectday, '%Y-%m-%d'))
#            arrMonthday.remove(strtoday)
#            arrMonthday.sort()
#        arrWeeklist(today)
#        
#        strWeekResult += "先週の日付：" + arrMonthday[0] + "~" + arrMonthday[-1] + "\n"
#        
#        for dirUserName in dirListName:
#            with open(dirUserName) as f:
#                lines = f.readlines()
#            lines_strip = [ line.strip() for line in lines]
#            
#            
#            l_day = [line for line in lines_strip if "Study time" in line]
#        
#            arrDay = []
#            for i in arrMonthday:
#                arrDay += [line for line in l_day if i in line]
#            # 勉強時間のログを全て出力する
#            #print('-----勉強ログ---------')
#            #print(arrDay)
#            #print('--------------')
#            
#            if arrDay == []:
#                continue
#            strWeekResult += "====================================================\n"
#            strWeekResult += "Name：" + dirUserName + "\n"
#            
#            studyWeekday = arrMonthday
#            for i in arrMonthday:
#                strarrDay = map(str, arrDay)
#                strarrDay = ','.join(strarrDay)
#                if i not in strarrDay:
#                    studyWeekday.remove(i)
#            strWeekResult += "　勉強した日付：" + str(studyWeekday) + "\n"
#            strWeekResult += "　勉強した日数：" + str(len(studyWeekday)) + "\n"
#            
#            checkWeekDay = []
#            for i in arrMonthday:
#                for j in arrDay:
#                    if i in j:
#                        checkWeekDay.append(i)
#                    else:
#                        continue
#            countCheckWeekDay = len(checkWeekDay)
#            
#            
#            strWeekResult += "　座席着席回数：" + str(len(arrDay)) + "回\n"
#            sumTime = 0
#            for i in arrDay:
#                i_split = i.split(",")
#                sumTime += int(i_split[-1])
#            def calTime(m):
#                hour = m // 60
#                minute = m % 60
#                resultStudyTime = str(hour) + "時間" + str(minute) + "分\n"
#                return resultStudyTime
#            strWeekResult += "　合計勉強時間：" + str(calTime(sumTime) + "\n")
#
#            await alert_channel.send(strWeekResult)
#        
###########################


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
                        await alert_channel.send(msg)
                except KeyError:
                    pass

client.run(setting.dToken)
