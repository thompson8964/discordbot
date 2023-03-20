from gpt import gptbot
import discord
from discord.ext.commands import Bot
import toml
import re

ids ={"#general": "1081639868423221278"}
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

with open('config.toml', 'r') as f:
    data = toml.load(f)
serverkey = data["serverkey"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event

async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith("/summarize "):
        content = message.content.removeprefix("/summarize ")
        content = content.split()
        r = re.search("\<\#(\d+)\>", content[0])
        try:
            channel_id = r.group(1)
        except:
            message.channel.send("You did not input a channel that exists in this server.") #todo test if this works

        channel = client.get_channel(int(channel_id))

        print(channel)

        messages = await channel.history(limit=50).flatten()
        print(messages)
        for i in messages:
            print(i.content)
    if message.content.lower().startswith("/chatbot "):
        #async with message.typing(): #todo make bot type in real time or show that bot is typing
        content = message.content.removeprefix("/chatbot ")
        await message.channel.send(gptbot(content))


client.run(serverkey)