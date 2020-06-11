"""
database.py
holds all database methods and functions
"""

import math
import time
import random
from ..models import *
from typing import Union, List
from ..exceptions.exceptions import *
from discord.ext import commands


class Database(commands.Cog):

    def __init__(self, bot: commands.Bot):
        """
        basic initialization of the database cog
        """

        self.bot = bot
        self.db = self.bot.db

    async def adjust_money(self, user: int, added_money: int):
        """
        add's the given balance to the provided user
        """

        user = await self.get_user(user)

        money = user.money
        money += added_money

        async with self.db.acquire() as conn:

            await conn.execute("update users set money = $1 where user_id = $2",
                               money, user)

    async def buy_advertisement(self, channel: int, type: str) -> dict:
        """
        buys an advertisement for the given channel
        """

        assert type == "average" or type == "decent"

        channel = await self.get_channel(channel)
        user = await self.get_user(channel.user_id)

        if type == "average":
            cost = math.ceil(0.03 * channel.subscribers)
            new_subscribers = math.ceil(0.01 * channel.subscribers)
        elif type == "decent":
            cost = math.ceil(0.06 * channel.subscribers)
            new_subscribers = math.ceil(0.02 * channel.subscribers)
        else:
            raise UnknownError("Invalid advertisement type input")

        if cost > user.money:
            raise NotEnoughMoney

        cost = -1 * cost

        async with self.db.acquire() as conn:

            await self.adjust_money(user.user_id, cost)

            await conn.execute("update channels set subscribers = $1 where channel_id = $2",
                               channel.subscribers + new_subscribers, channel.channel_id)

        return {
            "cost": -1 * cost,
            "new_subscribers": new_subscribers}

    async def buy_subbot(self, channel: int, amount: int) -> dict:
        """
        buys x amount of subscribers for the channel
        """

        channel = await self.get_channel(channel)
        user = await self.get_user(channel.user_id)

        cost = -1 * (amount * 5)

        if cost > user.money:
            raise NotEnoughMoney

        new_subscribers = amount

        async with self.db.acquire() as conn:

            await self.adjust_money(user.user_id, cost)

            await conn.execute("update channels set subscribers = $1 where channel_id = $2",
                               channel.subscribers + new_subscribers, channel.channel_id)

        return {
            "cost": -1 * cost,
            "new_subscribers": new_subscribers
        }

    async def check_award(self, ctx: commands.Context, channel: Channel):
        """
        checks if the provided channel hit a subscriber milestone
        """

        award = []

        if 100000 <= channel.subscribers < 1000000:
            award.append('silver')
        elif 1000000 <= channel.subscribers < 10000000:
            award.append('gold')
        elif 10000000 <= channel.subscribers < 100000000:
            award.append('diamond')
        elif 100000000 < channel.subscribers:
            award.append('ruby')
        else:
            return

        awards = await self.db.fetch("SELECT award FROM awards WHERE channel_id = $1",
                                     channel.channel_id)

        for awarded in awards:
            for new_award in award:
                if awarded == new_award:
                    award.pop(award.index(new_award))

        for new_award in award:
            award[award.index(new_award)] = (channel.channel_id, new_award)

        async with self.db.acquire() as conn:

            await conn.executemany("insert into awards (channel_id, award) values ($1, $2)",
                                   award)

        for new_award in award:
            await ctx.author.send(f":heart: **Congratulations!** You just got a {new_award[1]} play "
                                  f"button award for being an amazing vidio creator! Keep "
                                  f"growing and shining!")

    async def check_banned(self, user_id: int) -> bool:
        """
        checks if a user is bot banned
        """

        bans = await self.db.fetchrow("select * from botbans where user_id = $1",
                                      user_id)
        if bans:
            return True
        else:
            return False

    async def get_user(self, user_id: int) -> Union[User, bool]:
        """
        gets a user with the provided user id
        """

        user = await self.db.fetchrow("select * from users where user_id = $1",
                                      user_id)

        if not user:
            return False
        else:
            return User(
                user_id=user[0],
                money=user[1],
                commands=user[2]
            )

    async def get_channel(self, channel_id: int) -> Union[Channel, bool]:
        """
        gets a channel with the provided channel id
        """

        channel = await self.db.fetchrow("select * from channels where channel_id = $1",
                                         channel_id)

        if not channel:
            return False
        else:
            return Channel(
                channel_id=channel[0],
                user_id=channel[1],
                name=channel[2],
                description=channel[3],
                subscribers=channel[4],
                total_views=channel[5],
                category=channel[6],
                created_at=channel[7]
            )

    async def get_channels(self, user_id: int) -> Union[List[Channel], bool]:
        """
        gets a list of channels that belong to the provided user
        """

        channels = await self.db.fetch("select * from channels where user_id = $1",
                                       user_id)

        if not channels:
            return False
        else:
            channel_list = []
            for channel in channels:
                channel_list.append(
                    Channel(
                        channel_id=channel[0],
                        user_id=channel[1],
                        name=channel[2],
                        description=channel[3],
                        subscribers=channel[4],
                        total_views=channel[5],
                        category=channel[6],
                        created_at=channel[7]
                    )
                )

            return channel_list

    async def on_vote(self, user: int, is_weekend: bool) -> Union[int, bool]:
        """
        method triggered when someone votes for the bot on dbl
        """

        user = await self.get_user(user)

        if not user:
            return False

        money = user.money

        if is_weekend:
            new_money = math.ceil(money * 0.02)
        else:
            new_money = math.ceil(money * 0.01)

        if not new_money:
            new_money = random.randint(1, 5)

        await self.adjust_money(user.user_id, new_money)

        async with self.db.acquire() as conn:

            await conn.execute("insert into votes (user_id, timestamp) values ($1, $2)",
                               user.user_id, int(time.time()))

        return new_money

    async def set_money(self, user: int, money: int):
        """
        sets the given user's balance to the money provided
        """

        async with self.db.acquire() as conn:

            await conn.execute("update users set money = $1 where user_id = $2",
                               money, user)


def setup(bot):
    bot.add_cog(Database(bot))
