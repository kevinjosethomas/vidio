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

    async def get_channel(self, query_id):

        if isinstance(query_id, int):
            if len(str(query_id)) >= 15:  # Provided id is a a discord snowflake.
                channel = await self.db.fetchrow(
                    "SELECT * FROM channels WHERE user_id = %s",
                    (query_id,))
                if channel:
                    return channel
                else:
                    return 'Channel doesn\'t exist'
            else:  # Provided id is a channel id.
                channel = await self.db.fetchrow(
                    "SELECT * FROM channels WHERE channel_id = %s",
                    (query_id,))
                if channel:
                    return channel
                else:
                    return 'Channel doesn\'t exist'
        else:
            raise TypeError(f'Expected int, received {type(query_id)}')

    async def add_channel(self, user_id, name, description, category):

        if not self.text_check([name, description, category]):
            return 'Bad Arguments'

        async with self.db.acquire() as conn:
            user = self.bot.db(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,))
            if not user:
                await conn.execute(
                    "INSERT INTO users (user_id, money) VALUES (%s, %s)",
                    (user_id, 0))
            await conn.execute(
                "INSERT INTO channels (user_id,  name, description, subscribers, "
                "total_views, category, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s",
                (user_id, name, description, 0, 0, category, datetime.today()))
            
        return 'Successful'
