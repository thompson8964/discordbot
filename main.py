from gpt import gptbot
import discord
from discord.ext import commands
import toml
import re
import sys
import copy
import mysql.connector
import time


from datetime import datetime


ids ={"#general": "1081639868423221278"}
intents = discord.Intents.all()
# client = discord.BotIntegration(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)




@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

with open('config.toml', 'r') as f:
    data = toml.load(f)
serverkey = data["serverkey"]

passw = data["dbpsword"]






@bot.event
async def on_message(message):
    id = message.author.id


    with open('config.toml', 'r') as f:
        data = toml.load(f)
    # To connect MySQL database
    db = mysql.connector.connect(
        host=data["host"],
        user='admin',
        password=passw,
        db='discordBotDB',
    )
    cursor = db.cursor()
    now = datetime.now()

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

        reply = gptbot(ask)
        await message.channel.send(reply)

        data = {"timestamp": now.strftime('%Y-%m-%d %H:%M:%S'),
                "user_id": id,
                "message_content": '/summarize ' + channel_id,
                "reply_content": reply,
                "server_id": 1}  # placeholder

        insert_query = "INSERT INTO message_logs (timestamp, user_id, message_content, reply_content, server_id) VALUES (%s, %s, %s, %s, %s)"
        result = cursor.execute(insert_query, (
            data['timestamp'], data['user_id'], data['message_content'], data["reply_content"], data["server_id"]))
        db.commit()


    if message_content.lower().startswith("/chatbot "):
        #async with message.typing(): #todo make bot type in real time or show that bot is typing
            content = message_content.removeprefix("/chatbot ")
            reply = gptbot(content)
            if content:
                await message.channel.send(reply)
            else:
                message.channel.send("You have to ask me a question!")




            data = {"timestamp": now.strftime('%Y-%m-%d %H:%M:%S'),
                    "user_id": id,
                    "message_content": content,
                    "reply_content": reply,
                    "server_id": 1} #placeholder

            insert_query = "INSERT INTO message_logs (timestamp, user_id, message_content, reply_content, server_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (
            data['timestamp'], data['user_id'], data['message_content'], data["reply_content"], data["server_id"]))
            db.commit()

            # code for if the user already exists in the database
            insert_query = f"UPDATE user_data SET user_payment_info={data['user_payment_info']} user_tokens={data['user_tokens']} user_requests={data['user_requests']} WHERE user_id={data['user_id']}"
            data = {"user_id": id,
                    'user_payment_info': 0, # placeholder
                    "user_tokens": 300, #placeholder
                    "user_requests": 0 } #placeholder

            cursor.execute(insert_query, (
                data['user_id'], data['user_payment_info'], data['user_tokens'], data["user_requests"]))
            db.commit()

            #todo add code for new user


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