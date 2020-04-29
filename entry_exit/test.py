import os
import setting
import discord

TOKEN = cToken

#print("abs",os.path.dirname(os.path.abspath(__file__)))
#fistfile=os.path.dirname(os.path.abspath(__file__))
#str = "timelog"
#strf = fistfile + "/" + str
#print(strf)
#print("dirname" + os.path.dirname())
#print("abs" + os.path.abspath())

client = discord.Client()
@client.event
#async def on_voice_state_update(member, before, after):
#    print(member)
async def on_message(message):
    print('~~~~~~~~~~~~~~~~~~~')
    print(message)
    print('~~~~~~~~~~~~~~~~~~~')
    print(message.guild.member.users)
client.run(TOKEN)