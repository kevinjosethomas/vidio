import math
import string
import random
import asyncpg
from datetime import datetime
from discord.ext import commands, tasks


class Database(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db

        self.update_videos.start()

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
                'subscribers': 10,
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

        if isinstance(text, str):
            if len(text) == 0:
                return False
            if not text:
                return False
            if text.isspace():
                return False

            for letter in text:
                if letter not in string.printable:
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
                        if letter not in string.printable:
                            return False
                    return True
                else:
                    raise Exception(TypeError(f'Expected str or list, received {type(word)} in {type(text)}'))

            return True

        else:
            raise Exception(TypeError(f'Expected str or list, received {type(text)}'))

    async def check_banned(self, user_id):

        bans = await self.db.fetch("SELECT * FROM bans WHERE user_id = $1",
                                   user_id)

        if bans:
            return True
        else:
            return False

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

    async def add_ban(self, user_id):

        async with self.db.acquire() as conn:

            await conn.execute("INSERT INTO bans (user_id) VALUES ($1)",
                               user_id)

    async def add_subscriber(self, user_id, channel_id):

        async with self.db.acquire() as conn:

            subscribed = await self.get_subscribed(user_id)

            if (user_id, channel_id) in subscribed:
                return 'Already subscribed to this user'

            channels = await self.get_channel(user_id)
            channelids = []
            for channel in channels:
                channelids.append(channel[1])
            if channel_id in channels:
                return 'You cannot subscribe to your own channels.'

            await conn.execute("INSERT INTO subscribers (subscriber, channel) VALUES ($1, $2)",
                               user_id, channel_id)

    async def remove_subscriber(self, user_id, channel_id):

        async with self.db.acquire() as conn:

            await conn.execute("DELETE FROM subscribers WHERE subscriber = $1 AND channel = $2",
                               user_id, channel_id)

    async def remove_ban(self, user_id):

        async with self.db.acquire() as conn:

            await conn.execute("DELETE FROM bans WHERE user_id = $1",
                         user_id)

    async def remove_channel(self, user_id, cid):

        async with self.db.acquire() as conn:

            await conn.execute("DELETE FROM channels WHERE channel_id = $1 AND user_id = $2",
                               cid, user_id)

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

    async def get_subscribed(self, user_id):

        channels = await self.db.fetch("SELECT * FROM channels WHERE subscriber = $1",
                                       user_id)
        return channels

    async def get_subscribers(self, channel_id):

        await self.db.fetch("SELECT * FROM subscribers WHERE channel = $1",
                            channel_id)

    async def get_channels_count(self):

        length = await self.db.fetchrow("SELECT COUNT(*) FROM channels")

        return length[0]

    async def get_all_videos(self, cid, amount):

        videos = await self.db.fetch(
            "SELECT * FROM videos WHERE channel_id = $1 "
            "ORDER BY uploaded_at DESC LIMIT $2",
            cid, amount)

        if not videos:
            return 'No videos'

        return videos

    async def get_video(self, cid, name):

        videos = await self.db.fetch(
            "SELECT * FROM videos WHERE channel_id = $1 AND name LIKE $2",
            cid, name)

        if not videos:
            return 'No videos'

        return videos

    async def get_prefix(self, guild):

        prefix = await self.db.fetchrow(
            "SELECT prefix FROM guilds WHERE guild_id = $1",
            guild.id)

        if not prefix:
            return '-'
        return prefix

    async def set_prefix(self, guild, prefix):

        if not await self.text_check(prefix):
            return 'Bad Arguments'

        async with self.db.acquire() as conn:
            c_prefix = await self.db.fetchrow(
                "SELECT prefix FROM guilds WHERE guild_id = $1",
                guild.id, )
            if not c_prefix:
                await conn.execute(
                    "INSERT INTO guilds (guild_id, prefix) VALUES ($1, $2)",
                    guild.id, prefix)
                return prefix
            else:
                await conn.execute(
                    "UPDATE guilds SET prefix = $1 WHERE guild_id = $2",
                    prefix, guild.id)

        return prefix

    async def set_description(self, cid, description):

        if not await self.text_check(description):
            return 'Bad Arguments'

        async with self.db.acquire() as conn:

            await conn.execute("UPDATE channels SET description = $1 WHERE channel_id = $2",
                               description, cid)

    async def upload_video(self, user_id, channel, name, description):

        if not await self.text_check([name, description]):
            return 'Bad Arguments'

        choices = ['fail', 'poor', 'average', 'good', 'trending']
        status = random.choices(choices, weights=[20, 20, 50, 9.9999, 0.0001])[0]

        channel_data = await self.db.fetchrow(
            "SELECT channel_id, name, subscribers, total_views FROM channels WHERE user_id = $1 AND channel_id = $2",
            user_id, channel)

        channel_id = int(channel_data[0])
        channel_name = channel_data[1]
        subscribers = int(channel_data[2])
        total_views = int(channel_data[3])

        last_percentage = 1

        views = math.ceil(self.bot.algorithm[status]['views'][last_percentage] * subscribers / 100)

        new_subscribers = math.ceil(self.bot.algorithm[status]['subscribers'] * views / 100)

        likes = random.randint(
            self.bot.algorithm[status]['stats']['likes'][0],
            self.bot.algorithm[status]['stats']['likes'][1]) * views / 100
        dislikes = random.randint(
            self.bot.algorithm[status]['stats']['dislikes'][0],
            self.bot.algorithm[status]['stats']['dislikes'][1]
        ) * views / 100

        if subscribers < 20:
            status = 'average'
            new_subscribers = random.randint(5, 10)
            views = math.ceil(80 * subscribers / 100)
            likes = math.ceil(20 * views / 100)
            dislikes = math.ceil(10 * views / 100)

        total_views += views
        subscribers += new_subscribers

        async with self.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO videos (channel_id, name, description, status, new_subs, views, "
                "likes, dislikes, last_percentage, last_updated, uploaded_at) VALUES ($1, $2, $3, "
                "$4, $5, $6, $7, $8, $9, $10, $11)",
                channel_id, name, description, status, new_subscribers, views, likes, dislikes,
                last_percentage, datetime.now(), datetime.today())

            await conn.execute(
                "UPDATE channels SET subscribers = $1, total_views = $2 WHERE channel_id = $3",
                subscribers, total_views, channel_id)

        return {'status': status,
                'channel': channel_name,
                'new_subs': new_subscribers,
                'views': views,
                'likes': likes,
                'dislikes': dislikes}

    @tasks.loop(minutes=10)
    async def update_videos(self):
        try:

            videos = await self.db.fetch("SELECT * FROM videos WHERE now() - last_updated > make_interval(hours := 12);")

            for video in videos:

                video_id = video[0]
                channel_id = video[1]
                name = video[2]
                description = video[3]
                status = video[4]
                new_subscribers = video[5]
                views = video[6]
                likes = video[7]
                dislikes = video[8]
                last_percentage = video[9]
                last_updated = video[10]
                uploaded_at = video[11]

                if last_percentage == 10:
                    continue

                last_percentage += 1
                status = status.lower()

                channel_data = await self.db.fetchrow(
                    "SELECT subscribers, total_views FROM channels WHERE channel_id = $1",
                    channel_id)

                subscribers = int(channel_data[0])
                total_views = int(channel_data[1])

                if subscribers < 20:
                    continue

                views = views + math.ceil(self.bot.algorithm[status]['views'][last_percentage] * views / 100)

                new_subscribers = math.ceil(self.bot.algorithm[status]['subscribers'] * views / 100)

                likes = math.ceil(random.randint(
                    self.bot.algorithm[status]['stats']['likes'][0],
                    self.bot.algorithm[status]['stats']['likes'][1]) * views / 100)
                dislikes = math.ceil(random.randint(
                    self.bot.algorithm[status]['stats']['dislikes'][0],
                    self.bot.algorithm[status]['stats']['dislikes'][1]
                ) * views / 100)

                subscribers += new_subscribers
                total_views += views

                async with self.db.acquire() as conn:
                    await conn.execute(
                        "UPDATE videos SET new_subs = $1, views = $2, likes = $3, "
                        "dislikes = $4, last_percentage = $5, last_updated = $6 "
                        "WHERE video_id = $7",
                        new_subscribers, views, likes, dislikes, last_percentage, datetime.now(), video_id)

                    await conn.execute(
                        "UPDATE channels SET subscribers = $1, total_views = $2 WHERE channel_id = $3",
                        subscribers, total_views, channel_id)

        except Exception as e:
            print(e)

    @update_videos.before_loop
    async def before_updating(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Database(bot))
