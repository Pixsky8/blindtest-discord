import os
import discord
import asyncio
import config
import music
import commands

from debug import *

IS_SPEED_MODE = False

print("Bot is starting...")

data = config.global_data()
client = discord.Client()
conf = music.config


async def timer():
    await client.wait_until_ready()
    while True:
        if data.cmd:
            dbg_print_answer_dict(data.cmd.answers)
            await data.cmd.give_pts()
        await asyncio.sleep(20)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global conf, data, client
    if message.author != client.user:

        if message.content.startswith(conf.prefix):
            text = message.content[conf.prefix_len:]

            if text.startswith("ping"):
                await message.channel.send("pong")

            # admin commands
            elif text.startswith("music") and message.author.id in conf.admins:
                if message.author.id in conf.admins:
                    await music.music(data, message)

            elif text.startswith("is_adm"):
                if message.author.id in conf.admins:
                    await message.channel.send("True")
                else:
                    await message.channel.send("False")

            elif text.startswith("add_admin") and message.author.id in conf.admins:
                for user in message.mentions:
                    conf.add_admin(user.id)
                    print(user.name + " is now admin: " + message.author)
                conf.save()

            elif text.startswith("set_adm_chan") and message.author.id in conf.admins:
                print("adm channel set")
                data.cmd = commands.Commands(client, message.channel, IS_SPEED_MODE)
                msg_tmp = await data.cmd.channel.send("adm channel set")
                await message.delete()
                await msg_tmp.delete(delay=20)

            elif text.startswith("set_sb_chan") and message.author.id in conf.admins:
                if data.cmd:
                    print("sb channel set")
                    await data.cmd.set_sb_chan(message.channel)
                else:
                    await message.channel.send("Set admin channel first.")
                    await message.delete(delay=30)
                await message.delete()
            # end admin commands

        elif message.channel.type is discord.ChannelType.private:
            if data.cmd:
                await data.cmd.answer(message)
            else:
                await message.channel.send("The game is not open yet.")


client.loop.create_task(timer())
client.run(conf.token)
