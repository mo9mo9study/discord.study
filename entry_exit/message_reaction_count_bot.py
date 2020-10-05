import discord
import setting
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DATETIME, exc
from sqlalchemy.orm import sessionmaker
from datetime import datetime

TOKEN = setting.cToken
Base = declarative_base()

client = discord.Client()
engine = sqlalchemy.create_engine('sqlite:///sample_db.sqlite3', echo=True)

@client.event
async def on_ready():
    print(client.emojis)

    Base.metadata.create_all(bind=engine, checkfirst=True)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    """
    リアクション追加
    :param payload:
    :return:
    """
    # 2020/10/05 今回unicodeの絵文字はカウントしない。
    if payload.emoji.is_unicode_emoji():
        return

    save_message_reaction(payload)


def save_message_reaction(payload):
    """
    message_reaction 登録
    :param payload:
    :return:
    """
    session = sessionmaker(bind=engine)()
    try:
        message_reaction = MessageReaction()
        message_reaction.message_id = payload.message_id
        message_reaction.user_id = payload.user_id
        message_reaction.emoji_id = payload.emoji.id
        message_reaction.created_at = datetime.now()
        session.add(instance=message_reaction)
        session.commit()
    except exc.SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


class MessageReaction(Base):
    """
    message_reaction テーブル定義
    TODO: テーブル定義は別ファイルに分離したい。
    """
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    emoji_id = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    __tablename__ = 'message_reaction'


client.run(TOKEN)
