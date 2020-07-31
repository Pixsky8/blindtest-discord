import os
import asyncio
import discord
import config

config = config.Config()


async def summon(data, msg):
    if not msg.author.voice:
        msg.channel.send('You are neither connected to a voice channel nor specified a channel to join.')
    destination = msg.author.voice.channel
    if data.voice_client and data.voice_client.is_connected():
        await data.voice_client.move_to(destination)
    else:
        data.voice_client = await destination.connect()


async def disconnect(data):
    await data.voice_client.disconnect()


async def play(data, msg, arg):
    await summon(data, msg)

    if arg and arg != "":
        source = await discord.FFmpegOpusAudio.from_probe(arg)
        await data.voice_client.play(source)
    else:
        await msg.channel.send("No files specified.")


async def music(data, msg):
    args = msg.content.split()
    if len(args) > 1:
        if args[1] == "summon":
            await summon(data, msg)
        elif args[1] == "disconnect":
            await disconnect(data)
        elif args[1] == "play":
            if len(args) > 2:
                await play(data, msg, args[2])
