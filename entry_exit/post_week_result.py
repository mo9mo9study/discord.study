# import mimetypes
import magic
import os
import setting
from datetime import date, datetime, timedelta
from pprint import pprint
import re

import discord
from discord.ext import tasks
from discord.ext import commands

bot = commands.Bot(command_prefix='¥')
## testroleiギルドの[テストBOT007]にて起動
#TOKEN = setting.tToken
#CHANNEL = setting.tChannel
#SERVER = setting.tServer

TOKEN = setting.dToken
CHANNEL = setting.wChannel
SERVER = setting.dServer
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timelog")
MAX_SEND_MESSAGE_LENGTH = 2000


def minutes2time(m):
    hour = m // 60
    minute = m % 60
    result_study_time = str(hour) + "時間" + str(minute) + "分"
    return result_study_time

##[検討]ここをいつ起動しても先週の月〜日を指す方法に変更するのもあり
## 現在は、1日前から遡って7日分取得する方法
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
    #ex) 配列内の[04-20]月-日の文字列を[20]0埋めしない日に変換
    studyDay = []
    for item in studyWeekday:
        item_mod = re.sub(r'(^[0-9]{2})-0?([1-9]?[0-9]$)',r'\2',item)
        studyDay.append(item_mod)
    #ex) [04-20]
    #userWeekResult += serialize_log("　勉強した日付：", str(studyWeekday))
    userWeekResult += serialize_log("　勉強した日付：", str(studyDay))
    userWeekResult += serialize_log("　合計勉強時間：", str(minutes2time(sum_study_time)))
    return userWeekResult


def compose_user_records(strtoday, days, users_log):
    code_block = "```"
    separate = "====================\n"
    start_message = serialize_log("@everyone ")
    start_message += code_block + "\n"
    start_message += serialize_log("今日の日付：", strtoday)
    start_message += serialize_log("先週の日付：", days[0], "~", days[-1])
    week_result = [start_message]
    for user_log in users_log:
        if len(week_result[-1] + (separate + user_log)) >= MAX_SEND_MESSAGE_LENGTH - len(code_block):
            week_result[-1] += code_block # end code_block
            week_result.append(code_block) # start code_block
        week_result[-1] += separate + user_log
    week_result[-1] += code_block # end code_block
    return week_result

def compose_user_record(name, day, studytime):
    code_block = "```"
    separate = "====================\n"
    start_message = code_block
    start_message += separate
    start_message += "[ 今日( " + day + " )の勉強時間 ]\n"
    start_message += "  --->" + name  + " さんの勉強時間は[ " + minutes2time(studytime) + " ]です\n"
    start_message += separate
    start_message += "#もくもくオンライン勉強会\n"
    start_message += "#もくもく勉強机\n"
    start_message += "#今日の積み上げ\n"
    start_message += code_block
    day_result = start_message
    return day_result

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
    memberStudytime = []
    users_record = []
    obj = {}
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
        memberStudytime.append({"username": user_name, "studydays": study_days, "sumstudytime": sum_study_time})
    memberStudytime.sort(key=lambda x: x["sumstudytime"], reverse=True)
    for studytime in memberStudytime :
        user_record = construct_user_record(studytime["username"], studytime["studydays"], studytime["sumstudytime"])
        users_record.append(user_record)
    print("~< ソート済整形データ >~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(memberStudytime)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return users_record


def create_week_result():
    today = datetime.today()
    strtoday = datetime.strftime(today, '%Y-%m-%d')
    days = arr_days(today)
    user_records = aggregate_users_record(days)
    print(user_records[0])
    week_result = compose_user_records(strtoday, days, user_records)
    return week_result

# (確認用)実行された時に出力されるデータの想定
##str_weekResult = create_week_result()
##print(str_weekResult)
##print(len(str_weekResult))
##for strR in str_weekResult:
##    print(strR)
##    print("文字数: ",len(strR))


#週間と被るが、一旦日次分の処理を追加
#今後、統一していってほしい
#関数名がxxxになっている集計
def xxx(name, day):
    user_log = LOG_DIR + '/' + name
    # ログファイル読み込み
    lines_strip = read_file(user_log)
    # １週間以内に勉強した日の学習ログのみ抜き出す
    study_logs = []
    for line in lines_strip:
        if day in line:
            if "Study time" in line:
                print(line)
                study_logs.append(line)
    # 学習ログから合計勉強時間を算出する
    sum_study_time = 0
    for log in study_logs:
        sum_study_time += int(log.split(",")[-1])
    return sum_study_time


client = discord.Client()
@bot.group(invoke_without_command=True)
async def result_d(ctx):
    #当日分の日次集計
    print("-----------")
    pprint(vars(ctx))
    print("===========")
    if ctx.subcommand_passed is None:
        name = ctx.author.name
        today = datetime.today()
        strtoday = datetime.strftime(today, '%Y-%m-%d')
        sum_study_time = xxx(name, strtoday)
        await ctx.send(compose_user_record(name, strtoday, sum_study_time))
    else:
        await ctx.send("[ " + ctx.subcommand_passed + " ]は無効な引数です")

@result_d.command()
async def ago(ctx):
    #前日分の日次集計
    print("-----------")
    pprint(vars(ctx))
    print("===========")
    name = ctx.author.name
    today = datetime.today()
    day = today - timedelta(1)
    print("day :", day)
    strday = datetime.strftime(day, '%Y-%m-%d')
    print("strday :",strday)
    sum_study_time = xxx(name, strday)
    await ctx.send(compose_user_record(name, strday, sum_study_time))

@bot.command()
async def joined(ctx,member : discord.Member):
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
    print(ctx)

@bot.command()
async def Week_Result(ctx):
    message = ctx.message
    print('Used Command :' + ctx.invoked_with + ' (User) ' + message.author.name)
    if message.author.id != 603567991132782592:
        print('管理者(SuPleiades)以外のメンバーが実行しました')
        return
    print(f'手動週間集計実行日: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    channel = bot.get_channel(CHANNEL)
    week_results = create_week_result()
    for week_result in week_results:
        await channel.send(week_result)

@tasks.loop(seconds=60)
async def post_week_result():
    if datetime.now().strftime('%H:%M') == "07:30":
        if date.today().weekday() == 0:
            print(f'週間集計実行日: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
            channel = client.get_channel(CHANNEL)
            week_results = create_week_result()
            for week_result in week_results:
                await channel.send(week_result)

post_week_result.start()
#client.run(TOKEN)
bot.run(TOKEN)
