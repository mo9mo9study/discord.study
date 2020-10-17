from itertools import islice

import discord
import setting
from discord.ext import commands

TOKEN = setting.dToken

bot = commands.Bot(command_prefix='¥')

# 管理者等、当コマンドを使用可能なロールIDを指定
ALLOWED_ROLES = [
    123456789012345678
]


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(pass_context=True)
async def member_list(ctx):
    """
    ギルド内メンバー一覧取得
    のちにメンバー整理処理が作成されるため、当コマンドは不要になるため削除すること
    :param ctx:
    :return:
    """
    # 許可ロール以外はコマンドを使用できない。
    roles = ctx.author.roles
    is_allowed_user = False
    for role in roles:
        if role.id in ALLOWED_ROLES:
            is_allowed_user = True

    if is_allowed_user is False:
        embed = discord.Embed(title="ERROR", color=0xdc3545)
        embed.add_field(name="REASON", value="使用権限がありません")
        await ctx.send(embed=embed)
        return

    members = []
    for member in bot.get_all_members():
        if member.bot is False:
            row = str(member.name) + ',' + str(member.joined_at.strftime("%Y-%m-%d"))
            members.append(row)

    members = list(split_every(50, members))
    for group in members:
        value = '\n'.join(group)
        embed = discord.Embed(title="メンバー一覧", color=0x28a745)
        embed.add_field(name="name, joined_date", value=value)
        await ctx.send(embed=embed)


def split_every(n, iterable):
    """
    リストをn個ずつ分割リストにする
    :param n:
    :param iterable:
    :return:
    """
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))


bot.run(TOKEN)
