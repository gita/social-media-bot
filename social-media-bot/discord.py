from asyncio.tasks import sleep
import discord
import random
import requests
import json
import os
from datetime import datetime, time, timedelta
import asyncio
from discord.ext import tasks, commands
from requests.api import get

TOKEN = os.environ.get("TOKEN")  # token saved in environment variable locally
# Api-key saved in environment variable locally
Rapidapi = os.environ.get("RAPIDAPI")
client = discord.Client()


def get_verse(x, y):
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
    channel = client.get_channel(channel_id)
    await background_task(channel)


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
            l = [47, 72, 43, 42, 29, 47, 30, 28, 34,
                 42, 55, 20, 35, 27, 20, 24, 28, 78]
            y = random.randrange(l[x-1])
            verse = get_verse(x, y)
            await message.channel.send(f'Here is random verse for you \n{verse}')
            return
    if user_message.lower() == 'help':  # anywhere
        embedVar = discord.Embed(title="Bhagavad Gita Bot",name="BhagavadGita.io",url="https://bhagavadgita.io/",description="Click to visit site",color=0x00ff00)
        embedVar.add_field(name="hello, bye", value="The bot responds to hello and bye in any case", inline=False)
        embedVar.add_field(name="random", value="Use this command to generate random verse", inline=False)
        embedVar.add_field(name="verse <x>.<y>", value="Use this command to get specific verse where `<x>` is chapter number and `<y>` verse number", inline=False)
        await message.channel.send(embed=embedVar)
        return

    if user_message.startswith('verse'):
        sliced = user_message[5:]
        x = sliced.split('.')[0]
        y = sliced.split('.')[1]
        verse = get_verse(x, y)
        if verse=="":
            await message.channel.send("Please check your chapter number or verse number")
        await message.channel.send(verse)
        return
WHEN = time(3, 30, 0)  # 3:30 AM UTC = 9:00 AM IST
channel_id = 865245003885576232


async def called_once_a_day(channel):  # Fired every day
    await client.wait_until_ready()
    # print(channel)
    await channel.send("scheduled")


@tasks.loop(seconds=1)
async def background_task(channel):
    now = datetime.utcnow()
    # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # Seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # Sleep until tomorrow and then the loop will start
        await asyncio.sleep(seconds)
    while True:
        # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        now = datetime.utcnow()
        target_time = datetime.combine(
            now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        # Sleep until we hit the target time
        await asyncio.sleep(seconds_until_target)
        # Call the helper function that sends the message
        await called_once_a_day(channel)
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # Seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # Sleep until tomorrow and then the loop will start a new iteration
        await asyncio.sleep(seconds)

client.run(TOKEN)
