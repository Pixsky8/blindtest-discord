import json
import os

class Config:

    token = ""
    prefix = ""
    prefix_len = 0

    def __init__(self):
        fsett = open("config/settings.json")
        data = json.load(fsett)
        self.token = data["token"]
        self.prefix = data["prefix"]
        self.prefix_len = len(self.prefix)
        fsett.close()

    def save(self):
        data = {
            "token": self.token,
            "prefix": self.prefix,
        }

        json_data = json.dumps(data, indent=2)
        f = open("config/settings.json", "w+")
        f.write(json_data)
        f.close()


    def change_prefix(self, prefix):
        self.prefix = prefix
        self.prefix_len = len(self.prefix)
        self.save()

class global_data():
    def __init__(self):
        self.voice_client = None
