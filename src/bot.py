import os
import discord
import asyncio
import config
import commands


print("Bot is starting...")

data = config.global_data()
client = discord.Client()
config = commands.config

async def timer():
    await client.wait_until_ready()
    while True:
        await asyncio.sleep(20)


@client.event
async def on_ready():
    os.system("echo \"We have logged in as {0.user}\"".format(client))

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith(config.prefix):
            text = message.content[config.prefix_len:]

            if text.startswith("ping"):
                message.channel.send("pong")

            elif text.startswith("music"):
                


client.loop.create_task(timer())
client.run(config.token)
