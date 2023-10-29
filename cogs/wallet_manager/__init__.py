import json
from configparser import ConfigParser


with open("config.json", "r") as f:
    configs = json.load(f)

bot_settings = ConfigParser()
bot_settings.read("settings.ini")

