import json
import os

class Config:

    token = ""      # string
    prefix = ""     # string
    prefix_len = 0  # integer
    admins = []     # array of integer

    def __init__(self):
        if not os.path.exists("config/settings.json"):
            os.system("echo \"Cannot find config/settings.json.\nFile is missing or not setup?\"")
            raise NameError("Cannot open config/settings.json")
        fsett = open("config/settings.json")
        data = json.load(fsett)
        self.token = data["token"]
        self.prefix = data["prefix"]
        self.prefix_len = len(self.prefix)
        if "admins" in data:
            self.admins = data["admins"]
        fsett.close()

    def save(self):
        data = {
            "token": self.token,
            "prefix": self.prefix,
            "admins": self.admins
        }

        json_data = json.dumps(data, indent=2)
        f = open("config/settings.json", "w+")
        f.write(json_data)
        f.close()

    def add_admin(self, user_id):
        if not user_id in self.admins:
            self.admins.append(user_id)
            self.save()

    def is_admin(self, user_id):
        return user_id in self.admins

    def change_prefix(self, prefix):
        self.prefix = prefix
        self.prefix_len = len(self.prefix)
        self.save()




class global_data():
    cmd = None          # commands class
    scores = {}         # dict: user_id: score
    notification = {}   # dict: user_id: response notification msg
    def __init__(self):
        self.voice_client = None
