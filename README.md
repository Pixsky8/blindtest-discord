# blindtest-discord

This is a bot was created to assist the process of making blind test events
on discord servers.
It plays music, counts points and can display a scoreboard in a designated channel



# Installation

The bot should have admin privilleges on your discord server
for better compatibility.

#### settings.json configuration
Copy the config/settings_base.json to config/settings.json,
add the discord bot's token in the token field and your discord user id
in the admins section.
You can also change the prefix of the bot to your liking by replacing the `=` sign
that can be found in the prefix field.
The `false_malus` field represent the amount of point the players will lose if
their answer is wrong.

#### installing the files
If you are on linux and want to use docker, run the install.sh script.

Otherwise you need to install python3 and ffmpeg from your packet manager and 
discord.py and PyNaCl from pip.

#### adding music
It is recommanded to place the musics in data/ since it will be available inside
of the docker.



# Usage

#### Starting the bot
If you are using docker on linux, start the bot using the start.sh script.

Otherwise start the bot by running src/bot.py with python3.

#### Setting up the discord environement
You first need to select a discord channel that can only be seen by admins,
every answer will be displayed there.
To select a channel type the command `=set_adm_chan` inside.

To select the channel where the scoreboard will be displayed type the command
`=set_sb_chan`.

You can add other admins to help manage the bot by using the command `=add_admin`
followed by pinging the user using @.

#### Answering the questions
The players should answer the questions by DMing the bot if the speedmode is
disabled (default). Their answer will show up in the admin channel.
To give points to the players, admins have to react using the 1, 2, 3, 4 or 5
emotes and use the 🚫 emote to notify that the answer is wrong.

If speed mode is enabled. the players will have to dm the bot with any message
to be able to answer vocally. Admins will go through the same process to give
points to the player.



# TODO

    - quick music player with music.json
    - speed mode (1st to answer get the point) to play in teams
    - using nicknames from the server