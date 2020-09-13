import os
import asyncio
import discord
import config

voice_client = None
config = config.Config()
queue = []

async def summon(msg):
    global voice_client
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
    global voice_client
    if voice_client:
        await voice_client.disconnect()
        await channel.send("Disconnected.")
    else:
        await channel.send("Not connected.")


async def play_music():
    global voice_client
    global queue
    if voice_client:
        music_playing = queue.pop(0)
        source = await discord.FFmpegOpusAudio.from_probe(music_playing)
        await voice_client.play(source, after=play_music)


async def stop(channel):
    global voice_client
    global queue
    if voice_client:
        queue = []
        await channel.send("Stopped music.")
        await voice_client.stop()
    else:
        await channel.send("No music is playing.")


async def pause(channel):
    global voice_client
    if voice_client and voice_client.is_playing():
        await channel.send("Paused.")
        await voice_client.pause()
    else:
        await channel.send("Nothing is being played.")


async def resume(channel):
    global voice_client
    if voice_client and voice_client.is_paused():
        await channel.send("Music resumed.")
        await voice_client.resume()
    else:
        await channel.send("Music is not paused.")


async def enqueue(msg, arg):
    global voice_client
    global queue
    if not voice_client or not voice_client.is_connected():
        await summon(msg)

    if voice_client.is_paused():
        await resume(msg)

    if arg and arg != "":
        queue.append(arg)
        if not voice_client.is_playing():
            await play_music()
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
            else:
                await msg.channel.send("No files specified.")
        elif args[1] == "stop":
            await stop(msg.channel)
        elif args[1] == "pause":
            await pause(msg.channel)
        elif args[1] == "resume":
            await resume(msg.channel)
