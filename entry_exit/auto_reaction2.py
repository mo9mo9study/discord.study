import discord
from discord.ext import commands
import datetime
import random
import asyncio
import setting
import re
from datetime import datetime, timedelta

TOKEN = setting.cToken
client = discord.Client()
CHANNEL = setting.sChannel


slot1 = ['🙈','👹','👾'] 
slot2 = ['🙉','🤡','💀']
slot3 = ['🙊','💩','👻']

notOutputNum = list(range(1,5))

def intRandom(l):
    i = random.randrange(len(l))
    return i

async def addReaction(message,l,i):
    reactionId = l[i]
    await message.add_reaction(reactionId)

@client.event
async def on_message(message):
    if 'Study time' in message.content:
        global slotresult3
        result = re.compile(r'.*Study time： (.*)/分').match(message.content)
        intStudyTime = int(result[1])
        strName = re.compile(r'-->\[(.*)\].*').match(message.content)
        strName = strName[1]
        if intStudyTime in notOutputNum: 
            return
        else:
            # 確認用の大当たりをコード
#            slotresult1 = 0
#            slotresult2 = 0
#            slotresult3 = 0
            slotresult1 = intRandom(slot1)
            await addReaction(message,slot1,slotresult1)
            slotresult2 = intRandom(slot2)
            await addReaction(message,slot2,slotresult2)
            slotresult3 = intRandom(slot3)
            await addReaction(message,slot3,slotresult3)
        if slotresult1 == 0 and slotresult2 == 0 and slotresult3 == 0:
            alert_channel = client.get_channel(CHANNEL)
            now = datetime.utcnow() + timedelta(hours=9)
            # messageと文字列の名前を紐づけてmembers.mentionの取得
            guildMembers = message.guild.members
            intCountLoop = 0
            for member in guildMembers:
                if member.name == strName:
                    break
                intCountLoop += 1
            userMentionId = guildMembers[intCountLoop].mention
            print('userMentionId:',userMentionId)
            print('username:',guildMembers[intCountLoop].name)
        
            msg = userMentionId + " \n"
            msg += f'[{now:%m/%d %H:%M} ] 勉強時間ボーナススロット大当たり！！{intStudyTime}分の勉強お疲れ様！'
            print(msg)
            await alert_channel.send(msg)

client.run(TOKEN)
