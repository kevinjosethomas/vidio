import os
import asyncpg
import discord
import classyjson
from dotenv import load_dotenv
from discord.ext import commands


# Credentials
load_dotenv()
token = os.getenv("BOT_TOKEN")


# Initialization
bot = commands.AutoShardedBot(
    command_prefix="@",
    case_insentive=True,
    intents=discord.Intents.default()
)


# Configuration
with open("data/config.json", "r") as _config:
    bot.c = classyjson.load(_config)

with open("data/emojis.json", "r") as _emojis:
    bot.e = classyjson.load(_emojis)


# Execution
bot.cog_list = [
    "cogs.core.events"
]

for cog in bot.cog_list:
    bot.load_extension(cog)

bot.run(token)
