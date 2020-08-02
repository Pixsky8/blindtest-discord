import os
import asyncio
import discord
import config

voice_client = None
config = config.Config()
queue = {}

async def summon(msg):
    if not msg.author.voice:
        await msg.channel.send('You are neither connected to a voice channel nor specified a channel to join.')
    destination = msg.author.voice.channel
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(destination)
        await msg.channel.send("Moved to channel.")
    else:
        voice_client = await destination.connect()
        await msg.channel.send("Connected to channel.")


async def disconnect(channel):
    await voice_client.disconnect()
    await channel.send("Disconnected.")


async def play():
    source = await discord.FFmpegOpusAudio.from_probe(queue.pop(0))
    await voice_client.play(source, after=play)


async def stop(channel):
    await voice_client.stop()
    await channel.send("Stopped music.")


async def pause(channel):
    if voice_client.is_playing():
        await voice_client.pause()
        await channel.send("Paused.")
    else:
        await channel.send("Nothing is being played.")


async def resume(channel):
    if voice_client.is_paused():
        await voice_client.resume()
        await channel.resume("Music resumed.")
    else:
        await channel.resume("Music is not paused.")


async def enqueue(msg, arg):
    if not voice_client.is_connected():
        await summon(msg)

    if voice_client.is_paused():
        await resume(msg)

    if arg and arg != "":
        queue.append(arg)
        if not voice_client.is_playing():
            await play()
            msg.channel.send("Now playing.")
        else:
            msg.channel.send("Music queued.")
    else:
        await msg.channel.send("No files specified.")


async def music(msg):
    args = msg.content.split()
    if len(args) > 1:
        if args[1] == "summon":
            await summon(msg)
        elif args[1] == "disconnect":
            await disconnect(msg.channel)
        elif args[1] == "play":
            if len(args) > 2:
                await enqueue(msg, args[2])
        elif args[1] == "stop":
            await stop(msg.channel)
        elif args[1] == "pause":
            await pause(msg.channel)
        elif args[1] == "resume":
            await resume(msg.channel)
