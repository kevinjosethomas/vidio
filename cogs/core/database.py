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
from discord.ext import commands, tasks


class Database(commands.Cog):

    def __init__(self, bot: commands.Bot):
        """
        basic initialization of the database cog
        """

        self.bot = bot
        self.db = self.bot.db

    async def add_ban(self, user: int):
        """
        botbans the provided user
        """

        banned = await self.db.fetchrow("select * from bans where user_id = $1",
                                        user)

        if banned:
            raise AlreadyBotBanned()

        async with self.db.acquire() as conn:

            await conn.execute("insert into botbans (user_id) values ($1)",
                               user)

    async def add_channel(self, user: int, name: str, description: str, category: str):
        """
        creates a new channel under the provided user's name
        """

        async with self.db.acquire() as conn:

            database_user = await self.db.fetchrow("select * from users where user_id = $1",
                                                   user)

            if not database_user:
                await conn.execute("insert into users (user_id, money, commands) values ($1, $2, $3)",
                                   user, 0, 1)

            channels = await self.get_channels(user)

            if len(channels) >= 3:
                raise ChannelLimitError

            for channel in channels:
                if channel.name == name:
                    raise DuplicateChannelNameError

            if len(name) > 50:
                raise NameTooLongError

            if len(description) > 1000:
                raise DescriptionTooLongError

            await conn.execute('insert into channels (user_id, name, description, '
                               'subscribers, total_views, category, created_at) '
                               'values ($1, $2, $3, $4, $5, $6, $7)',
                               user, name, description, 0, 0, category, int(time.time()))

    async def add_guild(self, guild: int):
        """
        adds the provided guild to the database
        """

        async with self.db.acquire() as conn:

            await conn.execute("insert into guilds (guild_id, prefix, commands) values ($1, $2, $3)",
                               guild, '-', 0)

    async def add_subscriber(self, user: int, channel: channel):
        """
        adds a subscription to the provided channel from the provided user
        """

        user = await self.get_user(user)
        channel = await self.get_user(channel)

        subscribers = await self.db.fetch('select * from subscriptions where user_id = $1 and channel_id = $2',
                                          user.user_id, channel.user_id)

        if subscribers:
            raise AlreadySubscribedError

        if channel.user_id == user.user_id:
            raise SelfSubscribeError

        async with self.db.acquire() as conn:

            await conn.execute("insert into subscriptions (user_id, channel_id) values ($1, $2)",
                               user.user_id, channel.user_id)

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
            raise NotEnoughMoneyError

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
            raise NotEnoughMoneyError

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

    async def get_awards(self, channel: int) -> Union[list, None]:
        """
        fetches all the awards that belong to the provided channel
        """

        awards = await self.db.fetch("select award from awards where channel_id = $1",
                                     channel)

        if awards:
            return list(awards)

        return awards

    async def get_channel(self, channel_id: int) -> Union[Channel, bool]:
        """
        gets a channel with the provided channel id
        """

        channel = await self.db.fetchrow("select * from channels where channel_id = $1",
                                         channel_id)

        if not channel:
            raise InvalidChannel
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
            raise InvalidChannel
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

    async def get_channels_count(self) -> int:
        """
        returns the total number of channels in the vidio database
        """

        channels = await self.db.fetchrow("select count(*) from channels")

        return channels

    async def get_leaderboard(self, category: str) -> list:
        """
        gets top 10 people of various categories - subscribers, views, money, commands and guild commands for guilds
        """

        assert category == "subscribers" or \
               category == "total_views" or \
               category == "money" or \
               category == "commands" or \
               category == "gcommands"

        if category == "subscribers" or category == "views":

            channels = await self.db.fetch(f"select * from channels order by {category} desc limit 10")
            for channel in channels:
                channels[channels.index(channel)] = Channel(
                    channel_id=channel[0],
                    user_id=channel[1],
                    name=channel[2],
                    description=channel[3],
                    subscribers=channel[4],
                    total_views=channel[5],
                    category=channel[6],
                    created_at=channel[7]
                )
            return list(channels)

        elif category == "money" or category == "commands":

            users = await self.db.fetch(f"select * from users order by {category} desc limit 10")
            for user in users:
                users[users.index(user)] = User(
                    user_id=user[0],
                    money=user[1],
                    commands=user[2]
                )
            return list(users)

        else:
            guilds = await self.db.fetch("select * from guilds order by commands desc limit 10")
            return list(guilds)

    async def get_prefix(self, guild: int):
        """fetches the custom prefix for the provided server"""

        prefix = await self.db.fetchrow(
            "select prefix from guilds where guild_id = $1",
            guild
        )

        if not prefix:
            async with self.db.acquire() as conn:
                await conn.execute(""
                                   "insert into guilds (guild_id, prefix) values ($1, $2)",
                                   guild, '-')

                return '-'
        return prefix

    async def get_subscribers(self, channel: int) -> Union[list, None]:
        """
        returns all the users who are subscribed to the provided channel
        """

        subscribers = await self.db.fetch("select * from subscriptions where channel_id = $1",
                                          channel)
        if subscribers:
            return list(subscribers)

        return subscribers

    async def get_subscriptions(self, user: int) -> Union[list, None]:
        """
        returns all the channels the provided user is subscribed to
        """

        subscriptions = await self.db.fetch("select * from subscriptions where user_id = $1",
                                            user)

        if subscriptions:
            return list(subscriptions)

        return subscriptions

    async def get_user(self, user_id: int) -> Union[User, bool]:
        """
        gets a user with the provided user id
        """

        user = await self.db.fetchrow("select * from users where user_id = $1",
                                      user_id)

        if not user:
            raise InvalidUser
        else:
            return User(
                user_id=user[0],
                money=user[1],
                commands=user[2]
            )

    async def get_users_count(self) -> int:
        """
        returns the total number of unique users in the vidio database
        """

        users = await self.db.fetchrow("select count(*) from users")

        return users

    async def get_video_by_search(self, channel: int, search: str) -> Union[list, None]:
        """
        fetches a video with a similar search term that was uploaded by the provided channel
        """

        videos = await self.db.fetch("select * from videos where channel_id = $1 and name like $2",
                                     channel, search)

        if videos:
            for video in videos:
                videos[videos.index(video)] = Video(
                    video_id=video[0],
                    channel_id=video[1],
                    name=video[2],
                    description=video[3],
                    status=video[4],
                    new_subscribers=video[5],
                    new_money=video[6],
                    views=video[7],
                    likes=video[8],
                    dislikes=video[9],
                    subscriber_cap=video[10],
                    iteration=video[11],
                    last_updated=video[12],
                    uploaded_at=video[13]
                )
            return list(videos)
        return videos

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

    async def remove_ban(self, user: int):
        """
        unbotbans the provided user
        """

        banned = await self.db.fetchrow("select * from bans where user_id = $1",
                                        user)

        if not banned:
            raise AlreadyBotBanned()

        async with self.db.acquire() as conn:
            await conn.execute("delete from botbans where user_id = $1",
                               user)

    async def remove_channel(self, channel: int):
        """
        deletes the provided channel
        """

        channel = await self.get_channel(channel)

        async with self.db.acquire() as conn:

            await conn.execute("delete from channels where channel_id = $1",
                               channel.channel_id)

    async def remove_subscription(self, user: int, channel: int):
        """
        deletes a subscription from a channel with the provided user
        """

        subscription = await self.db.fetchrow("select * from subscribers where user_id = $1 and channel_id = $2",
                                              user, channel)

        if not subscription:
            raise SubscriptionDoesntExist

        async with self.db.acquire() as conn:

            await conn.execute("delete from subscriptions where user_id = $1 and channel_id = $2",
                               user, channel)

    async def set_channel_name(self, channel: int, name: str):

        channel = await self.get_channel(channel)

        if len(name) > 50:
            raise NameTooLongError

        async with self.db.acquire() as conn:

            await conn.execute("update channels set name = $1 where channel_id = $2",
                               name, channel)

    async def set_description(self, channel: int, description: str):
        """
        updates the channel description for the provided channel
        """

        channel = await self.get_channel(channel)

        if len(description) > 1000:
            raise DescriptionTooLongError

        async with self.db.acquire() as conn:

            await conn.execute("update channels set description = $1 where channel_id = $2",
                               description, channel.description)

    async def set_money(self, user: int, money: int):
        """
        sets the given user's balance to the money provided
        """

        async with self.db.acquire() as conn:

            await conn.execute("update users set money = $1 where user_id = $2",
                               money, user)

    async def set_prefix(self, guild: int, prefix: str):
        """
        updated the custom prefix for the provided guild
        """

        if len(prefix) > 10:
            raise PrefixTooLongError

        async with self.db.acquire() as conn:

            current_prefix = await self.db.fetchrow("select * from guilds where guild_id = $1",
                                                    guild)
            if not current_prefix:
                await conn.execute("insert into guilds (guild_id, prefix) values ($1, $2)",
                                   guild, prefix)
                return

            await conn.execute("update guilds set prefix = $1 where guild_id = $2",
                               prefix, guild)
            return

    async def toggle_vote_reminder(self, user: int):
        """
        toggles a vote reminder for the provided user
        """

        user = await self.get_user(user)

        reminder = await self.db.fetch("select * from vote_reminders where user_id = $1",
                                       user.user_id)

        vote = await self.db.fetchrow("select * from votes where user_id = $1 order by timestamp desc limit 1")
        if vote is None:
            vote = 0
        else:
            vote = [1]

        async with self.db.acquire() as conn:

            if reminder is None:
                await conn.execute("insert into vote_reminders (user_id, toggle, last_reminded, last_voted) values ($1, $2, $3, $4)",
                                   user.user_id, True, 0, vote)
                reminder = False
            elif not reminder:
                await conn.execute("update vote_reminders set toggle = $1 where user_id = $2",
                                   True, user.user_id)
            elif reminder:
                await conn.execute("update vote_reminders set toggle = $1 where user_id = $2",
                                   False, user.user_id)

        return not reminder

    # loops

    @tasks.loop(minutes=30)
    async def vote_reminder(self):
        """
        reminds every user who has enabled vote_reminders to vote if it's been 12 hours since they last votes
        """

        votes = await self.db.fetchrow("select * from votes where (extract(epoch from now()) - timestamp) > 43200")

        for vote in votes:

            user = await self.db.fetchrow("select * from vote_reminders where user_id = $1",
                                          vote[0])

            if not user[1]:
                continue

            if not user[3]:
                user[3] = await self.db.fetchrow("select timestamp from votes where user_id = $1 order by timestamp desc limit 1",
                                                 user[0])

            if user[2] and user[3]:

                if user[2] > user[3]:
                    continue

            await self.bot.get_user(user[0]).send(
                f"{self.bot.EMOJIS['heart']} **hey!** It's been 12 hours since you last voted for **vidio**! "
                f"Since you set vote reminders on, I'm assuming you would be interested to get some sweet "
                f"money by voting here - https://top.gg/bot/689210550680682560"
            )

            async with self.db.acquire() as conn:

                await conn.execute("update vote_reminders set last_reminded = $1 where user_id = $2",
                                   int(time.time()), user[0])

    @vote_reminder.before_loop
    async def before_vote_reminding(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Database(bot))
