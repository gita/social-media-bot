from asyncio.tasks import sleep
import discord
import random
import requests
import json
import os
from discord.ext import tasks

TOKEN = os.environ.get("TOKEN")  # token saved in environment variable locally
Rapidapi=os.environ.get("RAPIDAPI")  # Api-key saved in environment variable locally
client = discord.Client()
def get_verse(x,y):
    url = f"https://bhagavad-gita3.p.rapidapi.com/v2/chapters/{x}/verses/{y}/"
    headers = {
        'x-rapidapi-key': Rapidapi,
        'x-rapidapi-host': "bhagavad-gita3.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers).text
    # print(response.text)
    json_data = json.loads(response)
    verse = json_data["translations"][1]['description']
    # print(response)
    return(verse)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# will the change the loop time according to requirements
@tasks.loop(seconds=2, count=5) #here seconds needs to be changed to hours=24 for daily scheduled messaged
async def slow_count(message):
    await message.channel.send(f'this is in loop!')


@slow_count.after_loop
async def after_slow_count(message):
    await message.channel.send('done!')


@client.event
async def on_message(message):  # basic setup done below to respond to messages
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}:{user_message} ({channel})')

    if message.author == client.user:
        return
    if message.channel.name == 'bot-testing':  # in specific channel only
        if user_message.lower() == 'hello':
            await message.channel.send(f'Jai Shree Krishna {username}!')
        elif user_message.lower() == 'bye':
            await message.channel.send(f'Radhe Radhe {username}!')
            return
        elif user_message.lower() == 'random':  # checking random function
            x = random.randrange(18)
            l = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 35, 27, 20, 24, 28, 78]
            y=random.randrange(l[x-1])
            verse = get_verse(x, y)
            await message.channel.send(f'Here is random verse for you \n{verse}')
            return
        elif user_message.lower() == 'looped':  # sending messages in loop
            slow_count.start(message)
            return

    if user_message.lower() == 'anywhere':  # anywhere
        await message.channel.send('This message can be used anywhere')
        return
    if user_message.startswith('verse'):
        sliced=user_message[5:]
        x = sliced.split('.')[0]
        y = sliced.split('.')[1]
        verse = get_verse(x, y)
        # print(verse)
        await message.channel.send(verse)
        return

client.run(TOKEN)
