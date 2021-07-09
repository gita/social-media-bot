import discord
import random
import requests
import json
import os
from discord.ext import tasks

TOKEN = os.environ.get("TOKEN") #token saved in environment variable locally
client = discord.Client()
x=random.randrange(18) #random generation of x and y(soon)
l=[25,23,21,20] #change the array soon
def get_verse():
    response=requests.get("https://bhagavadgita.io/chapter/x/verse/y/").text
    #will recieve json here
    return(response)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@tasks.loop(hours=24,count=5) #will the change the loop time according to requirements
async def slow_count(message):
    await message.channel.send(f'this is in loop!')

@slow_count.after_loop
async def after_slow_count(message):
    await message.channel.send('done!')

@client.event
async def on_message(message): #basic setup done below to respond to mesages
    username=str(message.author).split('#')[0]
    user_message=str(message.content)
    channel = str(message.channel.name)
    print(f'{username}:{user_message} ({channel})')

    if message.author == client.user:
        return
    if message.channel.name=='bot-testing': #in specific channel only
        if user_message.lower()=='hello':
            await message.channel.send(f'Jai Shree Krishna {username}!')
        elif user_message.lower()=='bye':
            await message.channel.send(f'Radhe Radhe {username}!')
            return
        elif user_message.lower()=='!random': #checking random function
            response = f'This is your random number:{random.randrange(100)}'
            await message.channel.send(response)
            return
        elif user_message.lower()=='looped': #sending messages in loop
            slow_count.start(message)
            return 
           
    if user_message.lower()=='anywhere': #anywhere
        await message.channel.send('This message can be used anywhere')
        return
    # if user_message.lower()=='verse':
    #     verse = get_verse()
    #     await message.channel.send(verse)
    #     return
    #not yet implemented

client.run(TOKEN)