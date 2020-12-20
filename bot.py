import os
import asyncio
import asyncpg
import discord
import classyjson
from dotenv import load_dotenv
from discord.ext import commands


# Credentials
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")


# Initialization
bot = commands.AutoShardedBot(
    command_prefix="yt!",
    case_insentive=True,
    intents=discord.Intents.default()
)


# Database Setup
async def setup_database():
    """Created a database pool connection"""

    bot.database = await asyncpg.create_pool(
        host=DATABASE_HOST,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASS
    )

asyncio.get_event_loop().run_until_complete(setup_database())


# Configuration
with open("data/config.json", "r") as _config:
    bot.c = classyjson.load(_config)

with open("data/emojis.json", "r") as _emojis:
    bot.e = classyjson.load(_emojis)

@bot.check
def global_bot_check(ctx: commands.Context) -> bool:
    """Global bot check to block invalid commands"""

    return not ctx.author.bot and ctx.author.id != self.bot.user.id


# Execution
bot.cog_list = [
    "cogs.core.database",
    "cogs.core.events"
]

for cog in bot.cog_list:
    bot.load_extension(cog)

bot.run(TOKEN)
