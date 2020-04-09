# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

"""==============================
Bot credential
# BOT TOKEN
=============================="""
# プール監視員
dToken = os.environ.get("DISCORD_BOT_TOKEN")
# Cron
cToken = os.environ.get("CRON_BOT_TOKEN")
# テスト007
tToken = os.environ.get("TEST_BOT_TOKEN")


"""==============================
Discord Guild
# SERVER ID
## CHANNEL ID
=============================="""
# もくもくOnline勉強会
dServer = int(os.environ.get("DISCORD_SEVER_ID"))
## 勉強記録
dChannel = int(os.environ.get("DISCORD_CHANNEL_ID"))
## 勉強スロット当選者
sChannel = int(os.environ.get("SLOT_RESULT_CHANNEL_ID"))

# role
tServer = int(os.environ.get("TEST_SEVER_ID"))
## supleiadesの実験場
tChannel = int(os.environ.get("TEST_CHANNEL_ID"))

