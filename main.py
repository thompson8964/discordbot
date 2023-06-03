from gpt import gptbot
import discord
from discord.ext import commands
import toml
import re
import sys
import copy
import mysql.connector
import time
from gtts import gTTS
import os

from audioFunction import text_to_speech

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
    message_content = copy.copy(message.content)
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself
    if message_content.lower().startswith("/texttospeech "):
        content = message_content.removeprefix("/texttospeech ")
        if content:
            file,path = text_to_speech(content)
            await message.channel.send(file=file)
            os.remove(path)


    with open('config.toml', 'r') as f:
        data = toml.load(f)
    # To connect MySQL database
    db = mysql.connector.connect(
        host=data["host"],
        user='admin',
        password=passw,
        db='discordBotDB',
    )
    cursor = db.cursor(buffered=True)
    now = datetime.now()


    id = message.author.id

    idExists = False
    query = f"SELECT * FROM user_data WHERE user_id = {id};"
    cursor.execute(query)
    rows = cursor.fetchall()
    print("rows:", rows)
    user_data = {}
    if rows:
        idExists = True
        user_data = {
            "user_id": rows[0][0],
            "pay_info":  rows[0][1],
            "tokens":  rows[0][2],
            "requests":  rows[0][3]
        }





    if message.author == bot.user:
        return
    if message_content.lower().startswith("/summarize "):
        if user_data["requests"] <= 0:
            await message.channel.send("You need more requests!")  #todo test if this works
            return
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
        if user_data["tokens"] <= 0:  #todo test if this works
            await message.channel.send("You need more tokens!")
            return

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
            print(id)
            if idExists:
                data = {"user_id": id,
                        'user_payment_info': 0, # placeholder
                        "user_tokens": 300, #placeholder
                        "user_requests": 0 } #placeholder
                insert_query = f"UPDATE user_data SET user_payment_info={data['user_payment_info']}, user_tokens={data['user_tokens']}, user_requests={data['user_requests']} WHERE user_id={data['user_id']}"

                cursor.execute(insert_query)
                db.commit()
            else: #code for new user
                print("id:", id)

                insert_query = f"INSERT INTO user_data (user_id, user_payment_info, user_tokens, user_requests) VALUES (%s, %s, %s, %s)"
                data = {"user_id": id,
                        'user_payment_info': 0,  # placeholder
                        "user_tokens": 299,
                        "user_requests": 0}  # placeholder
                print(data)
                cursor.execute(insert_query, (
                    data['user_id'], data['user_payment_info'], data['user_tokens'], data["user_requests"]))
                db.commit()




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