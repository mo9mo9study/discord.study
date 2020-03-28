import os
from datetime import datetime,timedelta

dirListName = os.listdir(path='/home/ec2-user/discords/enter_exit/timelog')
### 例外
dirListName.remove("lesson.py")
dirListName.remove("test.py")
dirListName.remove(".lesson.py.swp")
# 対象ファイル（ユーザー）一覧
print(dirListName)

strWeekResult = ""
today = datetime.today()
def arrWeeklist(today):
    arrMonthday = []
    global strWeekResult
    strtoday = datetime.strftime(today, '%Y-%m-%d')
    strWeekResult += "今日の日付：" + str(strtoday) + "\n"
    for i in range(8):
        if i == 0:
            arrMonthday.append(strtoday)
        else:
            td = timedelta(days=i)
            strselectday = today - td
            arrMonthday.append(datetime.strftime(strselectday, '%Y-%m-%d'))
    arrMonthday.remove(strtoday)
    strWeekResult += "先週の日付：" + arrMonthday[0] + "~" + arrMonthday[-1] + "\n"
    arrMonthday.sort()
    return arrMonthday

for dirUserName in dirListName:
    arrMonthday = []
    arrMonthday = arrWeeklist(today)

    print(str(len(arrMonthday)))
    print("@@@@" + dirUserName + "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
    with open(dirUserName) as f:
        lines = f.readlines()
    lines_strip = [ line.strip() for line in lines]

    #print(lines) 
    
    l_day = [lineS for lineS in lines_strip if "Study time" in lineS]
    for i in l_day:
        print(i)

    arrDay = []

    print("@@@arrMonthday@@@")
    print(arrMonthday)
    print("@@@arrMonthday@@@")
    for lineD in l_day:
        #arrDay += [line for line in l_day if i in line]
        for sMon in arrMonthday:
            if sMon in lineD:
                arrDay.append(lineD)
        print(lineD)
        
    #print("---" + dirUserName)
    #print(arrDay)
    #print("---end---")
    # 勉強時間のログを全て出力する
    #print('-----勉強ログ---------')
    #print(l_day)
    #print('--------------')

    if arrDay == []:
        continue
    strWeekResult += "====================================================\n"
    strWeekResult += "Name：" + dirUserName + "\n"
    
    studyWeekday = arrMonthday
    for i in arrMonthday:
        strarrDay = map(str, arrDay)
        strarrDay = ','.join(strarrDay)
        if i not in strarrDay:
            studyWeekday.remove(i)
    strWeekResult += "　勉強した日付：" + str(studyWeekday) + "\n"
    strWeekResult += "　勉強した日数：" + str(len(studyWeekday)) + "\n"
    
    checkWeekDay = []
    for i in arrMonthday:
        for j in arrDay:
            if i in j:
                checkWeekDay.append(i)
            else:
                continue
    countCheckWeekDay = len(checkWeekDay)
    
    
    strWeekResult += "　座席着席回数：" + str(len(arrDay)) + "回\n"
    sumTime = 0
    for i in arrDay:
        i_split = i.split(",")
        sumTime += int(i_split[-1])
    def calTime(m):
        hour = m // 60
        minute = m % 60
        resultStudyTime = str(hour) + "時間" + str(minute) + "分\n"
        return resultStudyTime
    strWeekResult += "　合計勉強時間：" + str(calTime(sumTime) + "\n")
    
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#print(strWeekResult)
