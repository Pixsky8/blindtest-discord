import asyncio
import discord
import config

class Commands:
    client = None
    channel = None
    scoreboard_chan = None
    scoreboard_msg = None
    answers = {}    # dict: {answer_text(message), author(discord user)}
    points = {}     # dict: {author, points(int)}

    def __init__(self, client, channel):
        self.channel = channel
        self.client = client

    def set_sb_chan(self, channel):
        self.scoreboard_chan = channel

    def answer(message):
        answers.append((message.author, async channel.send(message.author.name + ": \"" + message.content + '\"')))

    def give_pts(): # takes tuple
        for answer in answers:
            if len(answer.reactions) > 0:
                answers.pop(answer)
                for react in answer.reactions:
                    if react.emoji == "1": # TODO
                        points[answers[answer]] += 1
                    elif react.emoji == "2":
                        points[answers[answer]] += 2
                    elif react.emoji == "3":
                        points[answers[answer]] += 3
                    elif react.emoji == "4":
                        points[answers[answer]] += 4
                    elif react.emoji == "5":
                        points[answers[answer]] += 5

    async def update_scoreboard():
        l = []  # list of users ordered per pts
        for user in self.points:
            added = False
            for i in range(len(l)):
                if points[l[i]] < points[user]:
                    l.insert(i, user)
                    added = True
            if not added:
                l.append(user)
        new_sb = "```"
        for user in l:
            new_sb = self.client.get_user(user) + ": " + self.points[user] + '\n'
        new_sb = new_sb + "```"
        await self.scoreboard_msg.edit(content=new_sb)
