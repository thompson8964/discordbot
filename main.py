from gpt import gptbot
import discord
import toml

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

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')

    if message.content.lower().startswith("/chatbot "):
        #async with message.typing():
        content = message.content.removeprefix("/chatbot ")
        await message.channel.send(gptbot(content))


client.run(serverkey)