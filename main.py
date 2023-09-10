from gpt import gptbot
import discord
from discord.ext import commands
import toml
import re
import sys
import copy
import time
from gtts import gTTS
import os
import pymongo

from audioFunction import text_to_speech

from datetime import datetime

#pinned post on patreon that tells people they have to verify through email
#!help command -> "I don't have paid tokens even though i have subscribed" -> check your email to verify, check spam folder
#/verify 2983748927349872
#

ids ={"#general": "1081639868423221278"}
intents = discord.Intents.all()
# client = discord.BotIntegration(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)

with open('config.toml', 'r') as f:
    data = toml.load(f)
exitKey = data["exitKey"]


myclient = pymongo.MongoClient(data["mongoAddress"])
mydb = myclient["chatbotDB"]
messageLogs = mydb["messageLogs"]
userData = mydb["userData"]









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


    # To connect MySQL database


    now = datetime.now()


    id = str(message.author.id) # convert the discord user id to string for easier querying

    idExists = False

    #print("rows:", rows)

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


    if message_content.lower().startswith("/chatbot "):


        #async with message.typing(): #todo make bot type in real time or show that bot is typing
        content = message_content.removeprefix("/chatbot ")



        if content:
            reply = gptbot(content)
            await message.channel.send(reply)
        else:
            message.channel.send("You have to ask me a question!")


        mydict = {"time": datetime.utcnow(), "content": content, "reply": reply}
        x = messageLogs.insert_one(mydict)
        print(reply)




        data = {"timestamp": now.strftime('%Y-%m-%d %H:%M:%S'),
                "user_id": id,
                "message_content": content,
                "reply_content": reply,
                "server_id": 1} #placeholder


        # code for if the user already exists in the database
        print(id)

        print("id:", id)

        result: dict = userData.find_one({"discordId": id})
        if result:
            print("discord id found. updating the tokens")

            result = userData.update_one({"discordId": id}, {"$set": {'tokensLeft': result["tokensLeft"]-1}})
            print(f"Successfully updated message records: {result.modified_count}")

        else:
            print("discord id not found")
            data = {"patreonId": "",
                    "discordId": id,
                    "email": "",
                    "tier": 0,
                    "verifcode": "",
                    "tokensLeft": 299,
                    "requestsLeft": 10,
                    }
            result = userData.insert_one(data)
            print(f"Successfully inserted one record: {result.inserted_id}")
            print(data)








    if message.author == bot.user:
        return
    if not message.guild:
        if message_content.lower().startswith("/exit " + exitKey):
            try:
                await message.channel.send("Shutting down!")
                sys.exit("Recieved shutdown command.")
            except discord.errors.Forbidden:
                pass

        elif message_content.lower().startswith("/verify"):
            content = message_content.removeprefix("/verify ")




        if message_content.lower().startswith("/verify "):
            id = str(message.author.id)  # convert the discord user id to string for easier querying
            content = message_content.removeprefix("/verify ")
            for x in userData.find({"verifcode": content}):  # { "_id": 0,"patreonId":0,"discordId": 0,"email": 0,"tier": 0, "verifcode": 1, "tokensLeft": 0,  "requestsLeft": 0}):
                if x["verifcode"] == content:
                    userData.update_one({"verifcode": content}, {"$set": {'discordId': id, "tier": 1, "tokensLeft": 300, "requestsLeft": 0}})
                    await message.channel.send("You have been successfully verified.")
                    print("User verified successfully!")
                    break
                else:
                    await message.channel.send("Looks like you entered the wrong code! Make sure you copied the right code and try again.")
        if message_content.lower().startswith("/checkTokens "):
            id = str(message.author.id)  # convert the discord user id to string for easier querying
            content = message_content.removeprefix("/checkTokens ")
            for x in userData.find({}, {"_id": 0, "patreonId": 0, "discordId": 1, "email": 0, "tier": 0, "verifcode": 0,
                                        "tokensLeft": 1, "requestsLeft": 1}):
                if x["discordId"] == id:
                    await message.channel.send(f"You have {x['tokensLeft']} tokens and {x['requestsLeft']} requests left.")
                    break











bot.run(data["serverkey"])