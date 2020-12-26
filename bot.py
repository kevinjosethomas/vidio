import os
import asyncio
import asyncpg
import discord
import classyjson
from dotenv import load_dotenv
from discord.ext import commands


# Configuration
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
STATCORD_KEY = os.getenv("STATCORD_KEY")

with open("data/config.json", "r") as _config:
    _CONFIG = classyjson.load(_config)

with open("data/emojis.json", "r") as _emojis:
    _EMOJIS = classyjson.load(_emojis)

async def get_prefix(bot: commands.Bot, ctx: commands.Context) -> str:
    """Fetches guild specific prefix"""

    if not ctx.guild:
        return bot.c.default_prefix

    prefix = bot.cache.prefixes.get(ctx.guild.id)

    return prefix if prefix else bot.c.default_prefix


# Initialization
bot = commands.AutoShardedBot(
    command_prefix=get_prefix,
    case_insensitive=True,
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
bot.c = _CONFIG
bot.e = _EMOJIS
bot.STATCORD_KEY = STATCORD_KEY

@bot.check
def global_bot_check(ctx: commands.Context) -> bool:
    """Global bot check to block invalid commands"""

    return not ctx.author.bot and ctx.author.id != ctx.bot.user.id and ctx.bot.is_ready()


# Execution
bot.cog_list = [
    "cogs.core.database",
    "cogs.core.events",
    "cogs.commands.owner",
    "cogs.commands.simulation",
    "cogs.commands.utility",
    "cogs.other.statcord"
]

for cog in bot.cog_list:
    bot.load_extension(cog)

bot.run(TOKEN)
