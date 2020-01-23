# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

dServer = int(os.environ.get("DISCORD_SEVER_ID"))
dChannel = int(os.environ.get("DISCORD_CHANNEL_ID"))
dToken = os.environ.get("DISCORD_BOT_TOKEN")
