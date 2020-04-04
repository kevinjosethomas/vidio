import math
import string
import random
import asyncpg
from datetime import datetime
from discord.ext import commands


class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db

        bot.algorithm = {
            'fail': {
                'views': {
                    1: 8,
                    2: 20,
                    3: 10,
                    4: 10,
                    5: 10,
                    6: 5,
                    7: 5,
                    8: 5,
                    9: 5,
                    10: 5,
                    11: 5
                },
                'subscribers': -30,
                'stats': {
                    'likes': [1, 3],
                    'dislikes': [5, 7]
                }
            },

            'poor': {
                'views': {
                    1: 2,
                    2: 30,
                    3: 20,
                    4: 20,
                    5: 20,
                    6: 10,
                    7: 5,
                    8: 5,
                    9: 5,
                    10: 5,
                    11: 5
                },
                'subscribers': [-10, 10],
                'stats': {
                    'likes': [2, 4],
                    'dislikes': [2, 4]
                }
            },

            'average': {
                'views': {
                    1: 15,
                    2: 30,
                    3: 20,
                    4: 20,
                    5: 20,
                    6: 10,
                    7: 5,
                    8: 5,
                    9: 5,
                    10: 5,
                    11: 5
                },
                'subscribers': 15,
                'stats': {
                    'likes': [3, 5],
                    'dislikes': [1, 3]
                }
            },

            'good': {
                'views': {
                    1: 20,
                    2: 40,
                    3: 30,
                    4: 20,
                    5: 10,
                    6: 10,
                    7: 5,
                    8: 5,
                    9: 5,
                    10: 5,
                    11: 5
                },
                'subscribers': 20,
                'stats': {
                    'likes': [8, 10],
                    'dislikes': [1, 3]
                }
            },

            'trending': {
                'views': {
                    1: 10000,
                    2: 10,
                    3: 10,
                    4: 8,
                    5: 8,
                    6: 5,
                    7: 3,
                    8: 3,
                    9: 3,
                    10: 3,
                    11: 3
                },
                'subscribers': 10,
                'stats': {
                    'likes': [8, 10],
                    'dislikes': [1, 3]
                }
            }
        }

    @staticmethod
    async def text_check(text):

        printable = string.printable

        if isinstance(text, str):
            if len(text) == 0:
                return False
            if not text:
                return False
            if text.isspace():
                return False

            for letter in text:
                if letter not in printable:
                    return False
            return True

        elif isinstance(text, list):
            for word in text:
                if isinstance(word, str):
                    if len(word) == 0:
                        return False
                    if word.isspace():
                        return False

                    for letter in word:
                        if letter not in printable:
                            return False
                    return True
                else:
                    raise Exception(TypeError(f'Expected str or list, received {type(word)} in {type(text)}'))

            return True

        else:
            raise Exception(TypeError(f'Expected str or list, received {type(text)}'))

    async def add_channel(self, user_id, name, description, category):

        if not await self.text_check([name, description, category]):
            return 'Bad Arguments'

        async with self.db.acquire() as conn:
            user = await self.bot.db.fetch(
                "SELECT * FROM users WHERE user_id = $1",
                user_id,)
            if not user:
                await conn.execute(
                    "INSERT INTO users (user_id, money) VALUES ($1, $2)",
                    user_id, 0)

            channels = await self.get_channel(user_id)

            if not channels == "Channel doesn't exist":
                for channel in channels:
                    if channel[2].lower() == name.lower():
                        return 'Channel with same name exists'

            await conn.execute(
                "INSERT INTO channels (user_id, name, description, subscribers, "
                "total_views, category, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                user_id, name, description, 0, 0, category, datetime.today())

        return 'Successful'

    async def add_guild(self, guild):

        async with self.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO guilds (guild_id, prefix) VALUES ($1, $2)",
                guild.id, '-')

    async def get_channel(self, query_id):

        if isinstance(query_id, int):
            if len(str(query_id)) >= 15:  # Provided id is a a discord snowflake.
                channel = await self.db.fetch(
                    "SELECT * FROM channels WHERE user_id = $1",
                    query_id)
                if channel:
                    return channel
                else:
                    return "Channel doesn't exist"

            else:  # Provided id is a channel id.
                channel = await self.db.fetch(
                    "SELECT * FROM channels WHERE channel_id = $1",
                    query_id)
                if channel:
                    return channel
                else:
                    return "Channel doesn't exist"
        else:
            raise TypeError(f'Expected int, received {type(query_id)}')

    async def get_leaderboard(self):

        leaderboard = await self.db.fetch(
            "SELECT user_id, name, subscribers FROM channels "
            "ORDER BY subscribers DESC LIMIT 10")

        return leaderboard

    async def set_prefix(self, guild, prefix):

        async with self.db.acquire() as conn:
            conn.execute(
                "UPDATE guilds SET prefix = $1 WHERE guild_id = $2",
                prefix, guild.id)

    async def upload_video(self, user_id, channel, name, description):

        if not await self.text_check([name, description]):
            return 'Bad Arguments'

        choices = ['fail', 'poor', 'average', 'good', 'trending']
        status = random.choices(choices, weights=[20, 20, 50, 9.9999, 0.0001])

        channel_data = self.db.fetch(
            "SELECT channel_id, subscribers, total_views FROM channels WHERE user_id = $1 AND name = $2",
            user_id, channel)
        channel_id = channel_data[0]
        subscribers = channel_data[1]
        total_views = channel_data[2]

        if status == 'fail':
            last_percentage = 1
            views = self.bot.algorithm['fail']['views'][last_percentage] * subscribers / 100
            new_subscribers = self.bot.algorithm['fail']['subscribers'] * views / 100
            likes = random.randint(
                self.bot.algorithm['fail']['stats']['likes'][0],
                self.bot.algorithm['fail']['stats']['likes'][1]) * views / 100
            dislikes = random.randint(
                self.bot.algorithm['fail']['stats']['dislikes'][0],
                self.bot.algorithm['fail']['stats']['dislikes'][1]
            ) * views / 100
            subscribers += new_subscribers
            total_views += views

            async with self.db.acquire() as conn:
                conn.execute(
                    "INSERT INTO videos (channel_id, name, description, status, new_subs, views, "
                    "likes, dislikes, last_percentage, last_updated, created_at) VALUES $1, $2, $3"
                    "$4, $5, $6, $7, $8, $9, $10, $11)",
                    channel_id, name, description, status, new_subscribers, views, likes, dislikes,
                    last_percentage, datetime.now(), datetime.today())

                conn.execute(
                    "UPDATE channels SET subscribers = $1, total_views = $2 WHERE channel_id = $3",
                    subscribers, total_views, channel_id)

        elif status == 'poor':
            last_percentage = 1
            views = self.bot.algorithm['poor']['views'][last_percentage] * subscribers / 100
            new_subscribers = self.bot.algorithm['poor']['subscribers'] * views / 100
            likes = random.randint(
                self.bot.algorithm['poor']['stats']['likes'][0],
                self.bot.algorithm['poor']['stats']['likes'][1]) * views / 100
            dislikes = random.randint(
                self.bot.algorithm['poor']['stats']['dislikes'][0],
                self.bot.algorithm['poor']['stats']['dislikes'][1]
            ) * views / 100
            subscribers += new_subscribers
            total_views += views

            async with self.db.acquire() as conn:
                conn.execute(
                    "INSERT INTO videos (channel_id, name, description, status, new_subs, views, "
                    "likes, dislikes, last_percentage, last_updated, created_at) VALUES ($1, $2, $3"
                    "$4, $5, $6, $7, $8, $9, $10, $11)",
                    channel_id, name, description, status, new_subscribers, views, likes, dislikes,
                    last_percentage, datetime.now(), datetime.today())

                conn.execute(
                    "UPDATE channels SET subscribers = $1, total_views = $2 WHERE channel_id = $3",
                    subscribers, total_views, channel_id)

        elif status == 'average':
            last_percentage = 1
            views = self.bot.algorithm['average']['views'][last_percentage] * subscribers / 100
            new_subscribers = self.bot.algorithm['average']['subscribers'] * views / 100
            likes = random.randint(
                self.bot.algorithm['average']['stats']['likes'][0],
                self.bot.algorithm['average']['stats']['likes'][1]) * views / 100
            dislikes = random.randint(
                self.bot.algorithm['average']['stats']['dislikes'][0],
                self.bot.algorithm['average']['stats']['dislikes'][1]
            ) * views / 100
            subscribers += new_subscribers
            total_views += views

            async with self.db.acquire() as conn:
                conn.execute(
                    "INSERT INTO videos (channel_id, name, description, status, new_subs, views, "
                    "likes, dislikes, last_percentage, last_updated, created_at) VALUES ($1, $2, $3"
                    "$4, $5, $6, $7, $8, $9, $10, $11)",
                    channel_id, name, description, status, new_subscribers, views, likes, dislikes,
                    last_percentage, datetime.now(), datetime.today())

                conn.execute(
                    "UPDATE channels SET subscribers = $1, total_views = $2 WHERE channel_id = $3",
                    subscribers, total_views, channel_id)

        elif status == 'good':
            last_percentage = 1
            views = self.bot.algorithm['good']['views'][last_percentage] * subscribers / 100
            new_subscribers = self.bot.algorithm['good']['subscribers'] * views / 100
            likes = random.randint(
                self.bot.algorithm['good']['stats']['likes'][0],
                self.bot.algorithm['good']['stats']['likes'][1]) * views / 100
            dislikes = random.randint(
                self.bot.algorithm['good']['stats']['dislikes'][0],
                self.bot.algorithm['good']['stats']['dislikes'][1]
            ) * views / 100
            subscribers += new_subscribers
            total_views += views

            async with self.db.acquire() as conn:
                conn.execute(
                    "INSERT INTO videos (channel_id, name, description, status, new_subs, views, "
                    "likes, dislikes, last_percentage, last_updated, created_at) VALUES ($1, $2, $3"
                    "$4, $5, $6, $7, $8, $9, $10, $11)",
                    channel_id, name, description, status, new_subscribers, views, likes, dislikes,
                    last_percentage, datetime.now(), datetime.today())

                conn.execute(
                    "UPDATE channels SET subscribers = $1, total_views = $2 WHERE channel_id = $3",
                    subscribers, total_views, channel_id)

        elif status == 'trending':
            last_percentage = 1
            views = self.bot.algorithm['trending']['views'][last_percentage] * subscribers / 100
            new_subscribers = self.bot.algorithm['trending']['subscribers'] * views / 100
            likes = random.randint(
                self.bot.algorithm['trending']['stats']['likes'][0],
                self.bot.algorithm['trending']['stats']['likes'][1]) * views / 100
            dislikes = random.randint(
                self.bot.algorithm['trending']['stats']['dislikes'][0],
                self.bot.algorithm['trending']['stats']['dislikes'][1]
            ) * views / 100
            subscribers += new_subscribers
            total_views += views

            async with self.db.acquire() as conn:
                conn.execute(
                    "INSERT INTO videos (channel_id, name, description, status, new_subs, views, "
                    "likes, dislikes, last_percentage, last_updated, created_at) VALUES ($1, $2, $3"
                    "$4, $5, $6, $7, $8, $9, $10, $11)",
                    channel_id, name, description, status, new_subscribers, views, likes, dislikes,
                    last_percentage, datetime.now(), datetime.today())

                conn.execute(
                    "UPDATE channels SET subscribers = $1, total_views = $2 WHERE channel_id = $3",
                    subscribers, total_views, channel_id)

        return {'status': status,
                'new_subs': new_subscribers,
                'views': views,
                'likes': likes,
                'dislikes': dislikes}


def setup(bot):
    bot.add_cog(Database(bot))
