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


# some bot variables the bot uses for various purposes
bot.embed = 0x2f3136

# some emojis used by the bot
bot.bug = '🐛'
bot.money = '💵'
bot.views = '👀'
bot.pencil = '📝'
bot.category = '📂'
bot.real_subscribers = '🤝'
bot.silver = '<:silver_play_button:706842448650829887>'
bot.gold = '<:gold_play_button:706842730776625172>'
bot.diamond = '<:diamond_play_button:706842448751755355>'
bot.ruby = '<:ruby_play_button:706955526272974859>'
bot.likes = '<:likes:694721324517556255>'
bot.subscribers = '<:live:693869294051655721>'
bot.dislikes = '<:dislikes:694721324483870760>'

bot.fail = '🔴'
bot.average = '⚪'
bot.success = '🟢'

bot.no = '<:no:708060636919365696>'
bot.yes = '<:yes:708060632171413525>'

bot.youtube = '<:youtube:708330611756105768>'
bot.heartbeat = '<a:ping:692399981935722607>'
bot.loading = '<a:loading:693852613812158494>'

# some channels the bot uses
bot.bugs_channel_id = 696014942083612742
bot.error_channel_id = 692405881115246603
bot.support_server_id = 689210707232686158
bot.suggestions_channel_id = 696014954532438116

# defines the list of cogs in the bot
bot.cog_list = [
    'cogs.core.database',
    'cogs.core.settings',
    'cogs.core.owner',
    'cogs.core.topgg',
    'cogs.commands.utility',
    'cogs.commands.vidio']

# loads all the cogs from the cog list
for cog in bot.cog_list:
    bot.load_extension(cog)


# runs the bot instance with the token
bot.run(TOKEN)
