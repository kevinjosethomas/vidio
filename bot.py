import os
import dotenv
import discord
from discord.ext import commands

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.AutoShardedBot(
    command_prefix="v.",
    case_insensitive=True,
    intents=discord.Intents.default()
)

bot.run(TOKEN)
