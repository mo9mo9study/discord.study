import mimetypes
import os
import setting
from datetime import date, datetime, timedelta

import discord
from discord.ext import tasks

TOKEN = setting.tToken
#CHANNEL = setting.tChannel
SERVER = 657225044971356170
CHANNEL = 678977043811270678
#SERVER = setting.tServer
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timelog")


def minutes2time(m):
    print("minutes2time")
    hour = m // 60
    minute = m % 60
    result_study_time = str(hour) + "時間" + str(minute) + "分"
    return result_study_time


def arr_days(today):
    days = []
    for i in reversed(range(1, 8)):
        day = today - timedelta(days=i)
        days.append(datetime.strftime(day, '%Y-%m-%d'))
    return days


def serialize_log(*args, end="\n"):
    print("serialize_log")
    context = "".join(map(str, args)) + end
    return context


def construct_user_record(user_name, studyWeekday, sum_study_time):
    print('construct_user_record')
    userWeekResult = serialize_log("Name：", user_name)
    userWeekResult += serialize_log("　勉強した日付：", str(studyWeekday))
    userWeekResult += serialize_log("　合計勉強時間：", str(minutes2time(sum_study_time)))
    return userWeekResult


def compose_user_records(strtoday, days, users_log):
    print('compose_user_records')
    week_result = serialize_log("@everyone ")
    week_result += "```\n"  # コードブロック始まり
    week_result += serialize_log("今日の日付：", strtoday)
    week_result += serialize_log("先週の日付：", days[0], "~", days[-1])
    for user_log in users_log:
        week_result += "====================\n"
        week_result += user_log
    week_result += "```"  # コードブロック終わり
    return week_result


def read_file(file_path):
    print('read_file')
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines_strip = [line.strip() for line in lines]
    return lines_strip


def exclude_non_txt(file_list):
    print('exclude_non_txt')
    for file in file_list:
        mime = mimetypes.guess_type(file)
        if mime[0] != 'text/plain':
            file_list.remove(file)
    return file_list


def aggregate_users_record(days):
    print('aggregate_users_record')
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
            print("学習記録がありません")
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
        print(user_log)
        user_record = construct_user_record(user_name, study_days, sum_study_time)
        print(user_record)
        users_record.append(user_record)
    return users_record


def create_week_result():
    print(2)
    today = datetime.today()
    strtoday = datetime.strftime(today, '%Y-%m-%d')
    days = arr_days(today)
    user_records = aggregate_users_record(days)
    print(user_records)
    week_result = compose_user_records(strtoday, days, user_records)
    return week_result


client = discord.Client()


@client.event
async def on_message(message):
    if message.content.startswith("/Result"):
        channel = client.get_channel(CHANNEL)
        print(1)
        strResult = create_week_result()
        print(strResult)
        await channel.send(create_week_result())


@tasks.loop(seconds=60)
async def post_week_result():
    print(1)
    print(datetime.now().strftime('%H:%M'))
    if datetime.now().strftime('%H:%M') == "15:18":
        channel = client.get_channel(CHANNEL)
        await channel.send(create_week_result())
        if date.today().weekday() == 0:
            channel = client.get_channel(CHANNEL)
            await channel.send(create_week_result())


post_week_result.start()

client.run(TOKEN)
