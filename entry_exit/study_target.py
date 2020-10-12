# import mimetypes
import magic
import os
import sys
import setting
from datetime import date, datetime, timedelta
from pprint import pprint
import re
import emoji

import discord
from discord.ext import tasks, commands

client = discord.Client()
bot = commands.Bot(command_prefix='¥')

TOKEN = setting.dToken
CHANNEL = setting.wChannel
SERVER = setting.dServer
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timelog")
USER_SETTINGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userSettings")
MAX_SEND_MESSAGE_LENGTH = 2000
ALLOWED_REACTION_LIST = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']
MAX_STUDY_TARGET_NUM_PER_USER = len(ALLOWED_REACTION_LIST)

def __print_trace_message(ctx, caller):
    print(os.path.basename(__file__), '->', caller)
    print("-----------")
    pprint(vars(ctx))
    print("===========")

# debugスイッチ周り、どうすっかな。
def dprint(msg):
    if not __debug__:
        pprint(msg)

#=======================
# select studing target
#=======================
def __build_study_list_message(user_name, targetList):
    if (len(targetList) > 0):
        selectedTarget = __getSelectedTarget(user_name)
        cnt = 0
        options = ''
        for target in targetList:
            options += '> ' + ALLOWED_REACTION_LIST[cnt] + ' : ' + target.rstrip('\n')
            if (target.rstrip('\n') == selectedTarget):
                options += ' :point_left: これ選択中' # :yoshi-3: にしたいがカスタム絵文字の登録されているサーバでないとテストはできない
            options += '\n'
            cnt+=1
        options = options.rstrip("\n")
        message = '''
> ====================
> [ 勉強する対象を選んでね。このメッセージに勉強したいアイテムの番号のリアクションをつければok。*複数対象にリアクションを付けても１つしか選択されません。結果は¥sで確認してね ]
{options}   
> ====================
        '''.format(options=options).strip()

    else:
        message = '''
> ====================
> 勉強中のものはなかったよ。追加する？
> 追加するなら ¥s add で追加してね。
> ====================
        '''
    return message

# ファイルが存在しない場合、初期化として空ファイルを作成する
def __init_file(file):
    if not os.path.isfile(file):
        open(file,"w", encoding="utf-8").close

# 勉強対象一覧をlistで返す
def __list_study_target(user_name):
    # 初回実行ならユーザ用勉強対象設定ファイルを作成するよ
    listFile = USER_SETTINGS_DIR + '/' + user_name
    __init_file(listFile)
    targetList = open(listFile, "r", encoding="utf-8").readlines()
    return targetList

# 勉強対象を追加します
def __add_study_target(user_name, item=None):
    message = ''
    if (item is None):
        message = '''
> 追加する勉強対象を指定してください。 e.g) ¥s add AWS-SAA
        '''
        return message

    targetListFile = USER_SETTINGS_DIR + '/' + user_name
    __init_file(targetListFile)

    with open(targetListFile, "r", encoding="utf-8") as f:
        if len(f.readlines()) >= MAX_STUDY_TARGET_NUM_PER_USER:
            message = '''
> 登録できる勉強対象は{max_item_num}件までです。不要なものを削除してから追加してください。
> 削除コマンドはこちら ¥s delete
            '''.format(max_item_num=MAX_STUDY_TARGET_NUM_PER_USER).strip()
            return message
        f.close

    with open(targetListFile, "a", encoding="utf-8") as f:
        f.write(item)
        f.write('\n')
        f.close
    message = '''
> {item}を追加しました。
    '''.format(item=item).strip()
    return message

# 勉強対象を削除します
def __delete_study_target(user_name, targetNo=None):
    message = ''
    if (targetNo is None) \
        or (not isinstance(targetNo, int)) \
        or (not (1 <= targetNo <= MAX_STUDY_TARGET_NUM_PER_USER)):
        message = '''
> 削除する勉強対象を1-{max_item_num}で指定してください。 e.g) ¥s delete 7
> 勉強対象の数字は ¥s で確認できます。
        '''.format(max_item_num=MAX_STUDY_TARGET_NUM_PER_USER).strip()
        return message

    targetListFile = USER_SETTINGS_DIR + '/' + user_name

    # 勉強対象リストが存在しないor削除対象が未登録の場合
    isTargetExists = os.path.isfile(targetListFile)
    studyTargetNum = 0
    if (isTargetExists):
        with open(targetListFile, "r", encoding="utf-8") as f:
            studyTargetNum = len(f.readlines())
            f.close
    # この辺のロジックはPandas時代の名残り
    if (not isTargetExists) or (studyTargetNum < targetNo):
        message = '''
> 削除対象が存在しませんでした。¥s で削除対象の数字を確認し、再実行してください。
        '''
        return message

    # ここ、2ファイルにまたがって削除処理をおこなうのでトランザクションを張りたいけどファイルだしあきらめ😩
    # targetListFileから削除対象を読み取っておき、-selectedのものなら-selectedからも削除する
    deleteTarget = ''
    with open(targetListFile, "r", encoding="utf-8") as f:
        deleteTarget = f.readlines()[targetNo-1]
        f.close

    selectedStudyTargetFile = USER_SETTINGS_DIR + '/' + user_name + '-selected'
    if (os.path.isfile(selectedStudyTargetFile)):
        with open(selectedStudyTargetFile, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line.rstrip('\n') == deleteTarget.rstrip('\n'):
                    # 削除対象が選択中の勉強対象なら、-selectedファイルを初期化する
                    open(selectedStudyTargetFile, 'w').close()
            f.close

    # targetListFileから削除対象を除いたものを書き戻す    
    with open(targetListFile, "r", encoding="utf-8") as f:
        targetList = f.readlines()
    with open(targetListFile, "w", encoding="utf-8") as f:
        cnt = 1
        for target in targetList:
            if cnt != targetNo:
                f.write(target)
            cnt += 1
        f.close
                
    message = '''
> {item}を削除しました。
    '''.format(item=deleteTarget).strip()
    return message

# アクティブな勉強対象をセットする
def __selectStudyTarget(user_name, selected):
    studyTargetFile = USER_SETTINGS_DIR + '/' + user_name + '-selected'
    # 初回実行ならユーザ用勉強対象設定ファイルを作成するよ
    __init_file(studyTargetFile)
    with open(studyTargetFile, "w", encoding="utf-8") as f:
        f.write(selected)
        f.close

# アクティブな勉強対象を取得する
def __getSelectedTarget(user_name):
    studyTargetFile = USER_SETTINGS_DIR + '/' + user_name + '-selected'
    # 初回実行ならユーザ用勉強対象設定ファイルを作成するよ
    __init_file(studyTargetFile)
    selected = ""
    if os.path.getsize(studyTargetFile) > 0:
        selected = open(studyTargetFile, "r", encoding="utf-8").readlines()[0]
    return selected

@bot.group(invoke_without_command=True)
async def s(ctx):
    __print_trace_message(ctx, sys._getframe().f_code.co_name)
    targetList = __list_study_target(ctx.author.name)
    message = __build_study_list_message(ctx.author.name, targetList)
    await ctx.send(message)    

@bot.group(invoke_without_command=True)
async def study(ctx):
    __print_trace_message(ctx, sys._getframe().f_code.co_name)
    targetList = __list_study_target(ctx.author.name)
    message = __build_study_list_message(ctx.author.name, targetList)
    await ctx.send(message)    

@s.command()
async def add(ctx, item=None):
    message = __add_study_target(ctx.author.name, item)
    await ctx.send(message)

@s.command()
async def delete(ctx, targetNo=None):
    _targetNo = int(targetNo)
    message = __delete_study_target(ctx.author.name, _targetNo)
    await ctx.send(message)


@bot.event
async def on_reaction_add(reaction, user):
    userReaction = emoji.demojize(reaction.emoji, use_aliases=True)
    # リアクションが勉強アイテムに対応するものかを判定する
    targetList = __list_study_target(user.name)
    studyOptions = ALLOWED_REACTION_LIST[0:len(targetList)]
    if (userReaction in studyOptions):
        selectedStudyTarget = __list_study_target(user.name)[studyOptions.index(userReaction)].rstrip("\n")
        __selectStudyTarget(user.name, selectedStudyTarget)


@bot.event
async def on_raw_reaction_add(payload):
    # botがオフライン時のメッセージに対応する必要はないので、このイベントは使わなくてOK
    pass

bot.run(TOKEN)
