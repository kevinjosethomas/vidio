import os
import dotenv
import asyncio
import asyncpg
import discord
import classyjson
from discord.ext import commands


# Load environment variables
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
STATCORD_KEY = os.getenv("STATCORD_KEY")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")


# Load JSON files
with open("data/config.json", "r") as _config:
    CONFIG = classyjson.load(_config)

with open("data/emojis.json", "r") as _emojis:
    EMOJIS = classyjson.load(_emojis)


async def get_prefix(bot: commands.Bot, ctx: commands.Context) -> str:
    """Fetches the prefix for a specific guild"""

    if not ctx.guild:
        return bot.c.default_prefix

    prefix = bot.cache.prefixes.get(ctx.guild.id, bot.c.default_prefix)

    return prefix


# Create bot instance
bot = commands.AutoShardedBot(
    command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.default()
)


# Create database instance
async def setup_database():
    """Create a database pool connection"""

    print(DATABASE_HOST, DATABASE_NAME, DATABASE_USER)

    bot.database = await asyncpg.create_pool(
        host=DATABASE_HOST, database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASS
    )


asyncio.get_event_loop().run_until_complete(setup_database())


# Register data globally
bot.c = CONFIG
bot.e = EMOJIS
bot.STATCORD_KEY = STATCORD_KEY


# Basic configuration
@bot.check
async def global_bot_check(ctx: commands.Context) -> bool:
    """Global bot check to block invalid commands"""

    if not ctx.bot.is_ready():
        await ctx.send(f"{bot.e.loading} gimme a minute, I'm still starting up")
        return False

    return not ctx.author.bot and ctx.author.id != ctx.bot.user.id


bot.cog_list = [
    "cogs.core.database",
    "cogs.core.events",
    "cogs.commands.owner",
    "cogs.commands.utility",
    "cogs.commands.simulation",
    "cogs.other.statcord"
]

for cog in bot.cog_list:
    bot.load_extension(cog)


# Execute
bot.run(TOKEN)
