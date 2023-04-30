from gpt import gptbot
import discord
from discord.ext import commands
import toml
import re
import sys
import copy
import time
ids ={"#general": "1081639868423221278"}
intents = discord.Intents.all()
# client = discord.BotIntegration(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)

with open('config.toml', 'r') as f:
    data = toml.load(f)
serverkey = data["serverkey"]

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))



@bot.event
async def on_message(message):
    message_content = copy.copy(message.content)
    if message.author == bot.user:
        return
    if message_content.lower().startswith("/summarize "):
        history = ""
        content = message_content.removeprefix("/summarize ")
        content = content.split()
        r = re.search("\<\#(\d+)\>", content[0])
        try:
            channel_id = r.group(1)
        except:
            message.channel.send("You did not input a channel that exists in this server.") #todo test if this works

        channel = bot.get_channel(int(channel_id))

        print(channel)

        messages = channel.history(limit=20)
        print(messages)
        async for i in messages:
            history += str(i.content)

            #print(i.content)
        print(history)
        ask = "Summarize these messages: " + history
        await message.channel.send(gptbot(ask))

    if message_content.lower().startswith("/chatbot "):
        #async with message.typing(): #todo make bot type in real time or show that bot is typing
            content = message_content.removeprefix("/chatbot ")

            if content:
                await message.channel.send(gptbot(content))
            else:
                message.channel.send("You have to ask me a question!")


    if message.author == bot.user:
        return
    if not message.guild:
        if message_content.lower().startswith("/exit " + data["exitKey"]):
            try:
                await message.channel.send("Shutting down!")
                sys.exit("Recieved shutdown command.")
            except discord.errors.Forbidden:
                pass
    else:
        pass


bot.run(serverkey)