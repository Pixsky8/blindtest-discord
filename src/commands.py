import asyncio
import discord
import config
import music

class Commands:
    client = None           # discord.client
    channel = None          # discord.channel: adm channel
    scoreboard_msg = None   # discord.message
    is_speed_mode = False   # bool: speed or answer mode
    answers = {}            # dict {answer_text(message): author(discord user)}
    points = {}             # dict {author: points(int)}

    def __init__(self, client, channel, is_speed_mode):
        self.channel = channel
        self.client = client
        self.is_speed_mode = is_speed_mode

    async def set_sb_chan(self, channel):
        self.scoreboard_msg = await channel.send("```Scoreboard\n```")

    async def answer(self, message):
        if is_speed_mode:
            music.pause(channel)
        else:
            msg_id = await self.channel.send(message.author.name + ": \"" + message.content + '\"')
            self.answers[message.author] = msg_id
        await message.add_reaction('👍')

    async def give_pts(self): # takes tuple
        for answer in self.answers:
            if len(answer.reactions) > 0:
                for react in answer.reactions:
                    if react.emoji == "1️⃣": # TODO
                        self.points[self.answers[answer]] += 1
                    elif react.emoji == "2️⃣":
                        self.points[self.answers[answer]] += 2
                    elif react.emoji == "3️⃣":
                        self.points[self.answers[answer]] += 3
                    elif react.emoji == "4️⃣":
                        self.points[self.answers[answer]] += 4
                    elif react.emoji == "5️⃣":
                        self.points[self.answers[answer]] += 5
                self.answers.pop(answer)
        if scoreboard_msg:
            await update_scoreboard()

    async def update_scoreboard(self):
        l = []  # list of users ordered per pts
        for user in self.points:
            added = False
            for i in range(len(l)):
                if self.points[l[i]] < self.points[user]:
                    l.insert(i, user)
                    added = True
            if not added:
                l.append(user)
        for user in l:
            new_sb = self.client.get_user(user) + ": " + self.points[user] + '\n'
        save_scores(new_sb)
        if scoreboard_chan:
            new_sb = "```Scoreboard\n" + new_sb + "```"
            await self.scoreboard_msg.edit(content=new_sb)

    def save_scores(self, scoreboard):
        f = open("data/score.txt", "w")
        f.write(scoreboard)
        f.close()
