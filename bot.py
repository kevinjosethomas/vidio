"""
bot.py
basic initialization and configuration of vidio
- loads external files - .env, .json
- loads cogs and prefixes
- creates bot instance
"""

import os
import json
import dotenv
import asyncio
import asyncpg
import discord
import logging
from discord.ext import commands


# loads environment variables
dotenv.load_dotenv()
TOKEN = os.getenv('discord_token')
DBL_TOKEN = os.getenv('dbl_token')
AUTH = os.getenv('dbl_auth')
HOSTNAME = os.getenv('database_hostname')
NAME = os.getenv('database_name')
USER = os.getenv('database_user')
PASSWORD = os.getenv('database_password')


async def get_prefix(_bot: commands.Bot, message: discord.Message) -> str:
    """Fetches the custom prefix for the provided server"""

    if not message.guild:  # if the command is initiated in direct messages
        return '-'

    guild_id = message.guild.id

    prefix = await _bot.db.fetchrow(
        "select prefix from guilds where guild_id = $1",
        guild_id
    )

    if not prefix:
        async with _bot.db.acquire() as conn:
            await conn.execute(""
                               "insert into guilds (guild_id, prefix) values ($1, $2)",
                               guild_id, '-')

        return '-'
    return prefix


bot = commands.AutoShardedBot(
    command_prefix=get_prefix,
    case_insensitive=True
)


async def database_setup() -> None:
    """Sets up the database pool connection"""

    bot.db = await asyncpg.create_pool(
        user=USER,
        password=PASSWORD,
        database=NAME,
        host=HOSTNAME
    )

asyncio.get_event_loop().run_until_complete(database_setup())


bot.logger = logging.getLogger('events')
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler(filename='events.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
bot.logger.addHandler(handler)


with open('data/config.json', encoding="utf8") as CONFIG:
    bot.CONFIG = json.load(CONFIG)

with open('data/emojis.json', encoding="utf8") as EMOJIS:
    bot.EMOJIS = json.load(EMOJIS)

with open('data/comments.json', encoding="utf8") as COMMENTS:
    bot.COMMENTS = json.load(COMMENTS)


bot.cog_list = [
    'cogs.core.database'
]

for cog in bot.cog_list:
    bot.load_extension(cog)

bot.run(TOKEN)
