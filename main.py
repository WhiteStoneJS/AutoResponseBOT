import discord, time, pymongo, json
from pymongo import MongoClient
f = open('info.json')
data = json.load(f)
cluster = MongoClient(data["mongodb"])
db = cluster["AutoResponse"]
responses = db["Responses"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    checkifresponse = responses.find_one({"srvid":message.guild.id,"response":message.content})
    if checkifresponse is not None:
        await message.reply(checkifresponse["answer"])
    if message.content.startswith("$response"):
        msg = message.content.split()
        if msg[1] == "add":
            await message.reply('Adding response ' + msg[2] + '!')
            response_message = message.content
            responses.insert_one({"srvid":message.guild.id,"response":msg[2],"answer":response_message.replace(f"$response add {msg[2]}"," ")}) 
        if msg[1] == "del":
            test = responses.find_one({"srvid":message.guild.id,"response":msg[2]})
            if test is not None:
                responses.find_one_and_delete({"srvid":message.guild.id,"response":msg[2]})
                await message.reply('Deleted response ' + msg[2] + '!')
client.run(data["token"])