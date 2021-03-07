import os
import dotenv
import asyncio
import asyncpg
import discord
from discord.ext import commands

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")

bot = commands.AutoShardedBot(
    command_prefix="v.",
    case_insensitive=True,
    intents=discord.Intents.default()
)


async def setup_database():
    """Create a database pool connection"""

    bot.database = await asyncpg.create_pool(
        host=DATABASE_HOST,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASS
    )

asyncio.get_event_loop().run_until_complete(setup_database())


bot.run(TOKEN)
