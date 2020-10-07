from datetime import datetime

import discord
from discord.ext import commands
import setting
import sqlalchemy
from sqlalchemy import Table, MetaData, DATETIME, Column, Integer, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_views import CreateView, DropView
TOKEN = setting.cToken
Base = declarative_base()
bot = commands.Bot(command_prefix='¥')

engine = sqlalchemy.create_engine('sqlite:///sample_db.sqlite3', echo=True)


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

Base.metadata.create_all(bind=engine, checkfirst=True)

@bot.event
async def on_ready():
    # View追加
    if not engine.dialect.has_table(engine, 'reaction_count'):
        view = Table('reaction_count', MetaData())
        definition = text("SELECT emoji_id, count(emoji_id) as count FROM message_reaction GROUP BY emoji_id")
        create_view = CreateView(view, definition)
        print(str(create_view.compile()).strip())
        engine.execute(create_view)
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_raw_reaction_add(payload):
    """
    リアクション追加
    :param payload:
    :return:
    """
    # 2020/10/05 今回unicodeの絵文字はカウントしない。
    if payload.emoji.is_unicode_emoji():
        return

    # ギルド外の絵文字はカウントしない
    if bot.get_emoji(payload.emoji.id) is None:
        return

    __save_message_reaction(payload)


@bot.event
async def on_raw_reaction_remove(payload):
    """
    リアクション削除
    :param payload:
    :return:
    """
    # 2020/10/05 今回unicodeの絵文字は登録しないめ、不要
    if payload.emoji.is_unicode_emoji():
        return

    # ギルド外の絵文字は登録しないので終了
    if bot.get_emoji(payload.emoji.id) is None:
        return

    __delete_message_reaction(payload)


@bot.command(pass_context=True)
async def rr(ctx):
    embed = discord.Embed(title="リアクションランキング")

    reaction_count = __get_reaction_count()
    reaction = ""
    count_text = ""
    rank = 1
    for row in reaction_count:
        reaction += str(rank) + '. ' + str(bot.get_emoji(id=row.emoji_id)) + "\n"
        rank = rank + 1
        count_text += str(row.count) + "回\n"

    embed.add_field(name="リアクション", value=reaction)
    embed.add_field(name="回数", value=count_text)
    await ctx.send(embed=embed)


def __save_message_reaction(payload):
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


def __delete_message_reaction(payload):
    """
    message_reaction 物理削除
    :param payload:
    :return:
    """
    session = sessionmaker(bind=engine)()
    try:
        session.query(MessageReaction)\
            .filter(
            MessageReaction.message_id == payload.message_id,
            MessageReaction.user_id == payload.user_id,
            MessageReaction.emoji_id == payload.emoji.id
        ).delete()
        session.commit()
    except exc.SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def __get_reaction_count():
    session = sessionmaker(bind=engine)()
    return session.execute("select emoji_id, count from reaction_count order by count desc")


bot.run(TOKEN)
