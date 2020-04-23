"""
This file has the basic setup and configuration for the vidio discord bot.
It loads the token, creates and runs bot instances, loads it's cogs and prefixes
and defines a bunch of bot variables including emojis.
"""


import os
import dotenv
import asyncpg
import asyncio
import logging
from discord.ext import commands


# loads .env and gets important data
dotenv.load_dotenv()
PASSWORD = os.getenv('password')
TOKEN = os.getenv('token')
YT_KEY = os.getenv('yt_key')
HOSTNAME = os.getenv('hostname')
DBL_TOKEN = os.getenv('dbl_token')


async def get_prefix(bot, message):

    """
       This function gets the custom prefixes for servers from the database,
       and allows servers to use them.

       Args:
           :param bot: The bot instance.
           :param message: The message object.

       Returns:
           :return (str): Returns the prefix
       """

    if message.guild is None:
        return '-'

    guild_id = message.guild.id

    prefix = await bot.db.fetchrow(
        "SELECT prefix FROM guilds WHERE guild_id = $1",
        guild_id,)

    if not prefix:
        async with bot.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO guilds (guild_id, prefix) VALUES ($1, $2)",
                guild_id, '-')
        return '-'

    return prefix[0]


# defines the bot variable
bot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True)


async def database_setup():

    """
        This function creates a database pool connection that will be used
        throughout all cogs.
    """

    bot.db = await asyncpg.create_pool(
        user='postgres',
        password=PASSWORD,
        database='vidio',
        host=HOSTNAME)

# Calls the database_setup function.
asyncio.get_event_loop().run_until_complete(database_setup())


bot.YT_KEY = YT_KEY
bot.PASSWORD = PASSWORD
bot.DBL_TOKEN = DBL_TOKEN


bot.logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
bot.logger.addHandler(handler)

# defines the list of cogs in the bot
bot.cog_list = [
    'cogs.core.data',
    'cogs.core.database',
    'cogs.core.settings',
    'cogs.core.owner',
    'cogs.core.topgg',
    'cogs.commands.youtube',
    'cogs.commands.utility',
    'cogs.commands.vidio']

# loads all the cogs from the cog list
for cog in bot.cog_list:
    bot.load_extension(cog)


# runs the bot instance with the token
bot.run(TOKEN)
