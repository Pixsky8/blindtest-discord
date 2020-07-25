import os
import discord
import asyncio
import config
import music
import commands


print("Bot is starting...")

data = config.global_data()
client = discord.Client()
config = music.config
cmd = None


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

        if message.channel.type is discord.DMChannel:
            if cmd:
                command.main(message)
            else:
                await message.channel.send("The game is not open yet.")

        # admin commands
        elif message.content.startswith(config.prefix):
            text = message.content[config.prefix_len:]

            if text.startswith("ping"):
                await message.channel.send("pong")

            elif text.startswith("music") and message.author.id in config.admins:
                if message.author.id in config.admins:
                    music.music(data, message)

            elif text.startswith("add_admin") and message.author.id in config.admins:
                for user in message.mentions:
                    config.add_admin(user.id)
                config.save()

            elif text.startswith("set_adm_chan") and message.author.id in config.admins:
                cmd = commands.Commands(client, message.channel)



client.loop.create_task(timer())
client.run(config.token)
