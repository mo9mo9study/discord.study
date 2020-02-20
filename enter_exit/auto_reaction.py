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

listUnder30 = [':Good:680059967839010841',':suteki:636821501085220874']
listOver30Under60 = [':Great:680059986595807267',':sasuga:653986373900173328']
listOver60Under120 = [':sugoi:625014719920472084',':Verygood:680060008867561533']
listOver120 = [':subarasii:665583710602526730',':Excellent:680060036810145872',':Marvelous:680064313267847186']

async def addReaction(message,l):
    i = random.randrange(len(l))
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
