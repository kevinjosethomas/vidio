import os
import asyncpg
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv("BOT_TOKEN")

bot = commands.AutoShardedBot(
    command_prefix="@",
    case_insentive=True,
    intents=discord.Intents.default()
)

bot.cog_list = [
    "cogs.core.events"
]

for cog in bot.cog_list:
    bot.load_extension(cog)

bot.run(token)
