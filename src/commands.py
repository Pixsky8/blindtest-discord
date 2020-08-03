import asyncio
import discord
import config
import music
from threading import Thread, Lock
from debug import *

class Commands:
    client = None           # discord.client
    channel = None          # discord.channel: adm channel
    scoreboard_msg = None   # discord.message
    is_speed_mode = False   # bool: speed or answer mode
    answers_mutex = Lock()
    answers = {}            # dict {answer_text(message): author(discord user)}
    points = {}             # dict {author: points(int)}

    def __init__(self, client, channel, is_speed_mode):
        self.channel = channel
        self.client = client
        self.is_speed_mode = is_speed_mode

    async def set_sb_chan(self, channel):
        self.scoreboard_msg = await channel.send("```Scoreboard\n```")

    async def answer(self, message):
        if self.is_speed_mode:
            music.pause(channel)
        else:
            msg_id = await self.channel.send(message.author.name + ": \"" + message.content + '\"')
            self.answers_mutex.acquire()
            try:
                self.answers[msg_id] = message.author
            finally:
                self.answers_mutex.release()
        await message.add_reaction('👍')

    async def update_scoreboard(self):
        #print("updating scoreboard")
        dbg_print_points_dict("points b4", self.points)
        l = []  # list of users ordered per pts
        for user in self.points:
            added = False
            for i in range(len(l)):
                if self.points[l[i]] < self.points[user]:
                    l.insert(i, user)
                    added = True
            if not added:
                l.append(user)
        dbg_print_points_dict("points after", self.points)
        new_sb = ""
        for user in l:
            new_sb = new_sb + user.name + ": " + self.points[user] + '\n'
        self.save_scores(new_sb)
        if self.scoreboard_msg:
            new_sb = "```Scoreboard\n" + new_sb + "```"
            await self.scoreboard_msg.edit(content=new_sb)
        print("scoreboard updated")


    def save_scores(self, scoreboard):
        f = open("data/score.txt", "w")
        f.write(scoreboard)
        f.close()

    async def give_pts(self): # takes tuple
        self.answers_mutex.acquire()
        try:
            to_pop = []
            for ans in self.answers:
                ans_upd = await self.channel.fetch_message(ans.id)
                if len(ans_upd.reactions) > 0:
                    if not self.answers[ans] in self.points:
                        self.points[self.answers[ans]] = 0
                    for react in ans_upd.reactions:
                        if str(react) == "1️⃣":
                            self.points[self.answers[ans]] += 1
                            print("1pt given to " + self.answers[ans].name)
                        elif str(react) == "2️⃣":
                            self.points[self.answers[ans]] += 2
                            print("2pts given to " + self.answers[ans].name)
                        elif str(react) == "3️⃣":
                            self.points[self.answers[ans]] += 3
                            print("3pts given to " + self.answers[ans].name)
                        elif str(react) == "4️⃣":
                            self.points[self.answers[ans]] += 4
                            print("4pts given to " + self.answers[ans].name)
                        elif str(react) == "5️⃣":
                            self.points[self.answers[ans]] += 5
                            print("5pts given to " + self.answers[ans].name)
                    to_pop.append(ans)
            for ans in to_pop:
                self.answers.pop(ans)
            if self.scoreboard_msg:
                await self.update_scoreboard()
        finally:
            self.answers_mutex.release()
