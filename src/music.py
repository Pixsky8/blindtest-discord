import os
import asyncio
import discord
import config

config = config.Config()


def summon(data, msg):
    if not message.author.voice:
        msg.channel.send('You are neither connected to a voice channel nor specified a channel to join.')
    destination = msg.author.voice.channel
    if data.voice_client and data.voice_client.is_connected():
        await voice_client.move_to(destination)
    else:
        data.voice_client = await destination.connect()


def disconnect():
    await data.voice_client.disconnect()


def play(data, msg, arg):
    summon(data, msg)

    if arg and arg != "":
        source = await discord.FFmpegOpusAudio.from_probe(arg)
        data.voice_client.play(source)
    else:
        msg.channel.send("No files specified.")


def music(data, msg):
    args = msg.split()
    if len(args) > 1:
        if args[1] == "summon":
            summon(data, msg)
        elif args[1] == "disconnect":
            disconnect()
        elif args[1] == "play":
            if len(args) > 2:
                play(data, msg, args[2])
