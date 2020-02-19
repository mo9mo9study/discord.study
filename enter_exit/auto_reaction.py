import discord
from discord.ext import commands
import datetime
import random
import asyncio
import setting

TOKEN = setting.cToken
client = discord.Client()

notOutputNum = list(range(1,5))
intUnder30 = list(range(5,30))
intOver30Under60 = list(range(30,60))
intOver60Under120 = list(range(60,120))

listUnder30 = [':good:625010272641351722',':suteki:636821501085220874']
listOver30Under60 = [':erai:656158893185040395',':sasuga:653986373900173328']
listOver60Under120 = [':sugoi:625014719920472084',':verygood:625010299413725242']
listOver120 = [':subarasii:665583710602526730','exce_llent:665583224646402069']

async def addReaction(message,l):
    i = random.randrange(2)
    reactionId = l[i]
    await message.add_reaction(reactionId)

@client.event
async def on_message(message):
    if 'Study time' in message.content:
        await message.add_reaction(":otukaresama:625009696213958666")
        for i in range(500):
            strjudge = ' ' + str(i) + '/分'
            if strjudge in message.content:
                result = i
                break 
        if result in notOutputNum: 
            print('@1i')
        elif result in intUnder30:
            await addReaction(message,listUnder30)
        elif result in intOver30Under60: 
            await addReaction(message,listUnder30)
            await addReaction(message,listOver30Under60)
        elif result in intOver60Under120: 
            await addReaction(message,listUnder30)
            await addReaction(message,listOver30Under60)
            await addReaction(message,listOver60Under120)
        else:
            await addReaction(message,listUnder30)
            await addReaction(message,listOver30Under60)
            await addReaction(message,listOver60Under120)
            await addReaction(message,listOver120)

client.run(TOKEN)
