import discord
from discord.ext import tasks

TOKEN = 
CHANNEL = 

client = discord.Client()


import os
from datetime import datetime,timedelta

dirListName = os.listdir(path='/home/ec2-user/discord/enter_exit/timelog')
### 例外
dirListName.remove("lesson.py")
dirListName.remove("test.py")
#dirListName.remove(".test.py.swp")
# 対象ファイル（ユーザー）一覧
#print(dirListName)

strWeekResult = ""
#arrMonthday = []
today = datetime.today()
def arrWeeklist(today):
    global strWeekResult
    arrMonthday = []
    strtoday = datetime.strftime(today, '%Y-%m-%d')
    for i in range(8):
        if i == 0:
            arrMonthday.append(strtoday)
        else:
            td = timedelta(days=i)
            strselectday = today - td
            arrMonthday.append(datetime.strftime(strselectday, '%Y-%m-%d'))
    arrMonthday.remove(strtoday)
    arrMonthday.sort()
    return arrMonthday
arrMonthday = arrWeeklist(today)

strtoday = datetime.strftime(today, '%Y-%m-%d')
strWeekResult += "@everyone \n"
strWeekResult += "```\n"
strWeekResult += "今日の日付：" + str(strtoday) + "\n"
strWeekResult += "先週の日付：" + arrMonthday[0] + "~" + arrMonthday[-1] + "\n"

for dirUserName in dirListName:
    arrMonthday = arrWeeklist(today)
    with open(dirUserName, encoding="utf-8") as f:
        lines = f.readlines()
    lines_strip = [ line.strip() for line in lines]
    
    
    l_day = [line for line in lines_strip if "Study time" in line]

    arrDay = []
    for i in l_day:
        arrDay += [i for line in arrMonthday if line in i]
    # 勉強時間のログを全て出力する
    #print('-----勉強ログ---------')
    #print(arrDay)
    #print('--------------')
    
    if arrDay == []:
        continue
    strWeekResult += "====================\n"
    strWeekResult += "Name：" + dirUserName + "\n"
    
    studyWeekday = [] 
   
    for i in arrMonthday:
        strarrDay = map(str, arrDay)
        strarrDay = ','.join(strarrDay)

        if i in strarrDay:
            a = i[-5:]
            studyWeekday.append(a)
    #print("-修正後の日付---------")
    #print(studyWeekday)
    #print("----------")

    strWeekResult += "　勉強した日付：" + str(studyWeekday) + "\n"
    #strWeekResult += "　勉強した日数：" + str(len(studyWeekday)) + "\n"
    
    checkWeekDay = []
    for i in arrMonthday:
        for j in arrDay:
            if i in j:
                checkWeekDay.append(i)
            else:
                continue
    countCheckWeekDay = len(checkWeekDay)
    
    
    #strWeekResult += "　座席着席回数：" + str(len(arrDay)) + "回\n"
    sumTime = 0
    for i in arrDay:
        i_split = i.split(",")
        sumTime += int(i_split[-1])
    def calTime(m):
        hour = m // 60
        minute = m % 60
        resultStudyTime = str(hour) + "時間" + str(minute) + "分\n"
        return resultStudyTime
    strWeekResult += "　合計勉強時間：" + str(calTime(sumTime))

    
print(strWeekResult)

@client.event
async def on_message(message):
    if message.content.startswith("/Result"):
        global strWeekResult
        channel = client.get_channel(CHANNEL)
        strWeekResult += "\n```"
        await channel.send(strWeekResult)


client.run(TOKEN)

