import magic
import os
import setting
import discord
from datetime import date, datetime, timedelta
from discord.ext import tasks
from dateutil.relativedelta import relativedelta

# testroleiギルドの[テストBOT007]にて起動
#TOKEN = setting.tToken
#CHANNEL = setting.tChannel
#SERVER = setting.tServer

TOKEN = setting.dToken
CHANNEL = setting.mChannel
SERVER = setting.dServer
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timelog")
MAX_SEND_MESSAGE_LENGTH = 2000

## 今後使えそうだから残してみる、不要なら削除
##def getCalender(y, m, d):
##    weekDay = ['日', '月', '火', '水', '木', '金', '土']
##    wd = getWeekday(y, m, 1)
##    print('-' * 37)
##    for wds in weekDay:
##        print('  ',wds, end='')
##    print()
##    print('-' * 37)
##    print('     ' * wd, end='')
##    for day in range(d):
##        if wd % 7 == 0 and wd >= 7:
##            print()
##        print('{:5d}'.format(day + 1), end='')
##        wd += 1
##    print()
##    print('-' * 37)
##def getWeekday(y, m, d):
##    if m == 1 or m == 2:
##        y -= 1
##        m += 12
##    wd = (d + y // 4 - y // 100 + y // 400 + y + (13 * m + 8) // 5) % 7
##    return wd

def getMonth(y, m):
    if m in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    elif m in {4, 6, 9, 11}:
        return 30
    elif m in 2:
        if y % 4 in 0 and y % 100 != 0 or y % 400:
            return 29
        else:
            return 28
    else:
        return 0

def getLastMonthValiable(request):
    thisMonth_YMFirstday = datetime(int(datetime.strftime(datetime.today(),'%Y')), int(datetime.strftime(datetime.today(),'%m')), 1) #ex)2020-03
    lastMonth_Y = int(datetime.strftime(datetime.today() - relativedelta(months=1), '%Y')) #ex)2020
    lastMonth_M = int(datetime.strftime(datetime.today() - relativedelta(months=1), '%m')) #ex)3
    lastMonth_YMFirstday = date(lastMonth_Y, lastMonth_M , 1) #ex)2020-03-01
    lastMonth_Days = getMonth(lastMonth_Y, lastMonth_M)
#    print('-----> debug')
#    print('lastMonth_Y: ',lastMonth_Y)
#    print('lastMonth_M: ',lastMonth_M)
#    print('lastMonth_YMFirstday: ',lastMonth_YMFirstday)
#    print('-----> debug')
    if request == 'thisMonth_YMFirstday':
        return thisMonth_YMFirstday
    if request == 'lastMonth_YMFirstday':
        return lastMonth_YMFirstday
    if request == 'D':
        return lastMonth_Days


def minutes2time(m):
    hour = m // 60
    minute = m % 60
    result_study_time = str(hour) + "時間" + str(minute) + "分"
    return result_study_time


def arr_days(today): #対象月の日付を日数分配列に格納
    days = []
    for i in reversed(range(1, getLastMonthValiable('D')+1)):
        day = getLastMonthValiable('thisMonth_YMFirstday') - relativedelta(days=i)
        print(day)
        days.append(datetime.strftime(day, '%Y-%m-%d'))
    return days


def serialize_log(*args, end="\n"):
    context = "".join(map(str, args)) + end
    return context


def construct_user_record(user_name, studyMonth_day, sum_study_time):
    userMonthResult = serialize_log("Name：", user_name)
    #userMonthResult += serialize_log("　勉強した日付：", str(studyMonth_day))
    print("(",user_name,")","　勉強した日付：", str(studyMonth_day))
    userMonthResult += serialize_log("　合計勉強時間：", str(minutes2time(sum_study_time)),"(勉強日数：",len(studyMonth_day),")")
    return userMonthResult


def compose_user_records(strtoday, days, users_log):
    code_block = "```"
    separate = "====================\n"

    start_message = serialize_log("@everyone ")
    start_message += code_block + "\n"
    start_message += serialize_log("取得日：", strtoday)
    start_message += serialize_log("先月の日付：", getLastMonthValiable('lastMonth_YMFirstday'),"~", days[-1])

    month_result = [start_message]

    for user_log in users_log:
        if len(month_result[-1] + (separate + user_log)) >= MAX_SEND_MESSAGE_LENGTH - len(code_block):
              month_result[-1] += code_block # end code_block
              month_result.append(code_block) # start code_block
        month_result[-1] += separate + user_log
    month_result[-1] += code_block # end code_block
    return month_result


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines_strip = [line.strip() for line in lines]
    return lines_strip


def exclude_non_txt(file_list):
    file_list_result = list(file_list)
    print('対象ファイル数 : ',len(file_list))
    print('--- 対象ファイルの[名前/ファイルタイプ]と[対象から除外か否か]の処理結果を出力 ---')
    for file in file_list:
        file_type = magic.from_file(file, mime=True)
        print(f'\n python-magic: {file_type} --> [file]: {file}',end='') # 確認用
        if file_type != 'text/plain':
            print('-->  [ remove ]',end='') # 確認用
            file_list_result.remove(file)
    print('\n--- (除外対象)ファイルタイプが[text/plain]でない対象 --- ')
    result = list(set(file_list) - set(file_list_result))
    for x in result:
        print(x)
    print('--- end --- ')
    return file_list_result



def aggregate_users_record(days):
    """
    各ユーザーの１週間の学習時間と日数を集計する
    """
    user_list = [os.path.join(LOG_DIR, txt) for txt in os.listdir(LOG_DIR)]
    user_list = exclude_non_txt(user_list)

    users_record = []

    for user_log in user_list:
        # ログファイル読み込み
        lines_strip = read_file(user_log)

        # １週間以内に勉強した日の学習ログのみ抜き出す
        study_logs = []
        for line in lines_strip:
            if "Study time" in line:
                study_logs += [line for day in days if day in line]
        # 勉強した日がないユーザーは処理をスキップする
        if study_logs == []:
            print(f'{user_log}: 学習記録がありません')
            continue

        # 学習ログから勉強した日付を抜き出す
        study_days = []
        for log in study_logs:
            study_days += [day[-5:] for day in days if day in log]
        study_days = sorted(set(study_days), key=study_days.index)

        # 学習ログから合計勉強時間を算出する
        sum_study_time = 0
        for log in study_logs:
            sum_study_time += int(log.split(",")[-1])

        user_name = os.path.splitext(os.path.basename(user_log))[0]
        user_record = construct_user_record(user_name, study_days, sum_study_time)
        users_record.append(user_record)
    return users_record


def create_month_result():
    today = datetime.today()
    strtoday = datetime.strftime(today, '%Y-%m-%d')
    days = arr_days(today)
    user_records = aggregate_users_record(days)
    month_result = compose_user_records(strtoday, days, user_records)
    return month_result


print(create_month_result())
client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith("¥Month_Result"):
        if message.author.id != 603567991132782592:
            print('管理者(SuPleiades)以外のメンバーが実行しました')
            return
        print(f'手動月間集計実行日: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        channel = client.get_channel(CHANNEL)
        month_results = create_month_result()
        for month_result in month_results:
            await channel.send(month_result)


@tasks.loop(seconds=60)
async def post_month_result():
    if datetime.now().strftime('%H:%M') == "07:35":
        if datetime.now().strftime('%d') == '01':
            print('実行日: ', datetime.now().strftime('%d'))
            print(f'月間集計実行日: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
            channel = client.get_channel(CHANNEL)
            month_results = create_month_result()
            for month_result in month_results:
                await channel.send(month_result)


post_month_result.start()

client.run(TOKEN)
