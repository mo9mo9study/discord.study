# import mimetypes
import magic
import os
import setting
from datetime import date, datetime, timedelta

import discord
from discord.ext import tasks
## testroleiギルドの[テストBOT007]にて起動
#TOKEN = setting.tToken
#CHANNEL = setting.tChannel
#SERVER = setting.tServer
TOKEN = setting.dToken
CHANNEL = setting.wChannel
SERVER = setting.dServer
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timelog")


def minutes2time(m):
    hour = m // 60
    minute = m % 60
    result_study_time = str(hour) + "時間" + str(minute) + "分"
    return result_study_time


def arr_days(today):
    days = []
    for i in reversed(range(1, 8)):
#    for i in reversed(range(2, 9)): # 火曜日用
        day = today - timedelta(days=i)
        days.append(datetime.strftime(day, '%Y-%m-%d'))
    return days

def serialize_log(*args, end="\n"):
    context = "".join(map(str, args)) + end
    return context


def construct_user_record(user_name, studyWeekday, sum_study_time):
    userWeekResult = serialize_log("Name：", user_name)
    userWeekResult += serialize_log("　勉強した日付：", str(studyWeekday))
    userWeekResult += serialize_log("　合計勉強時間：", str(minutes2time(sum_study_time)))
    return userWeekResult


def compose_user_records(strtoday, days, users_log):
    week_result = serialize_log("@everyone ")
#    week_result = serialize_log("<@603567991132782592>") # デバック用にSuPleiades宛にメンション
    week_result += "```\n"  # コードブロック始まり
    week_result += serialize_log("今日の日付：", strtoday)
    week_result += serialize_log("先週の日付：", days[0], "~", days[-1])
    for user_log in users_log:
        week_result += "====================\n"
        week_result += user_log
    week_result += "```"  # コードブロック終わり
    return week_result


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines_strip = [line.strip() for line in lines]
    return lines_strip

# 削除予定
#def exclude_non_txt(file_list):
#    for file in file_list:
#        mime = mimetypes.guess_type(file)
#        if mime[0] != 'text/plain':
#            file_list.remove(file)
#    return file_list

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


def create_week_result():
    today = datetime.today()
    strtoday = datetime.strftime(today, '%Y-%m-%d')
    days = arr_days(today)
    user_records = aggregate_users_record(days)
    week_result = compose_user_records(strtoday, days, user_records)
    return week_result


print(create_week_result())
client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith("/Week_Result"):
        if message.author.id != 603567991132782592:
            print('管理者(SuPleiades)以外のメンバーが実行しました')
            return
        print(f'手動週間集計実行日: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        channel = client.get_channel(CHANNEL)
## デバック用
#        strResult = create_week_result()
#        print(strResult)
        await channel.send(create_week_result())


@tasks.loop(seconds=60)
async def post_week_result():
    if datetime.now().strftime('%H:%M') == "07:30":
        if date.today().weekday() == 0:
            print(f'週間集計実行日: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
            channel = client.get_channel(CHANNEL)
            await channel.send(create_week_result())


post_week_result.start()

client.run(TOKEN)
