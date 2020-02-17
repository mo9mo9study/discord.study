# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# mainBOT
dServer = int(os.environ.get("DISCORD_SEVER_ID"))
dChannel = int(os.environ.get("DISCORD_CHANNEL_ID"))
dToken = os.environ.get("DISCORD_BOT_TOKEN")

# testServerBOT
tServer = int(os.environ.get("TEST_SEVER_ID"))
tChannel = int(os.environ.get("TEST_CHANNEL_ID"))
tToken = os.environ.get("TEST_BOT_TOKEN")

# cronBOT
#cServer = int(os.environ.get("CRON_SEVER_ID"))
#cChannel = int(os.environ.get("CRON_CHANNEL_ID"))
#cToken = os.environ.get("CRON_BOT_TOKEN")
