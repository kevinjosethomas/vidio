import typing
import asyncpg
from discord.ext import commands

from ..exceptions import *
from ..models import Channel


class Database(commands.Cog):

    """
    Database; includes functions for all database queries
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = self.bot.database

    async def populate_cache(self):
        """Populates all bot cache"""

        self.bot.cache.prefixes = await self.get_all_prefixes()
        self.bot.cache.botbans = await self.get_all_botbans()

    async def get_all_prefixes(self) -> dict:
        """Fetches all guilds' prefixes from the database"""

        guilds = await self.db.fetch("SELECT * FROM guilds")

        return dict(
            (guild["guild_id"], guild["prefix"])
            for guild in guilds
            if (guild["prefix"] != self.bot.c.default_prefix and guild["prefix"])
        )

    async def get_all_botbans(self) -> list:
        """Fetches all botbans from the database"""

        botbans = await self.db.fetch("SELECT * FROM botbans")

        return [botban["botban_id"] for botban in botbans]

    async def add_guild(
        self,
        conn: asyncpg.Connection,
        guild_id: int,
        prefix: typing.Union[str, None] = None,
    ):
        """Adds a guild to the database"""

        prefix = prefix if prefix else self.bot.c.default_prefix

        guild = await self.get_guild(guild_id)
        if guild:
            raise GuildError("Provided guild already exists")

        await conn.execute("INSERT INTO guilds (id, prefix) VALUES ($1, $2)", guild_id, prefix)
        self.bot.cache.prefixes[guild_id] = prefix

    async def get_guild(self, guild_id: int) -> typing.Union[asyncpg.Record, None]:
        """Fetches a guild from the database"""

        guild = await self.db.fetchrow("SELECT * FROM guilds WHERE guild_id = $1", guild_id)

        return guild

    async def update_guild_prefix(self, conn: asyncpg.Connection, guild_id: int, prefix: str):
        """Updates a guild's prefix in the database"""

        if len(prefix) > 10:
            raise GuildError("Invalid prefix provided")

        guild = await self.get_guild(guild_id)
        if not guild:
            await self.add_guild(guild_id, prefix)
            self.bot.cache.prefixes[guild_id] = prefix
            return

        await conn.execute(
            "UPDATE guilds SET prefix = $1 WHERE guild_id = $2",
            prefix,
            guild_id,
        )
        self.bot.cache.prefixes[guild_id] = prefix

    async def remove_guild(self, conn: asyncpg.Connection, guild_id: int):
        """Removes a guild from the database"""

        guild = await self.get_guild(guild_id)
        if not guild:
            raise GuildError("Provided guild does not exist")

        await conn.execute("DELETE FROM guilds WHERE guild_id = $1", guild_id)

    async def get_channel(self, channel_id: int) -> Channel:
        """Gets a channel from the database"""

        channel = await self.db.fetchrow("SELECT * FROM channels WHERE channel_id = $1", channel_id)

        if not channel:
            return None

        return Channel(
            channel_id=channel.get("channel_id"),
            banner=channel.get("banner"),
            name=channel.get("name"),
            vanity=channel.get("vanity"),
            description=channel.get("description"),
            awards=channel.get("awards"),
            subscribers=channel.get("subscribers"),
            balance=channel.get("balance"),
            views=channel.get("views"),
            genre=channel.get("genre"),
            created_at=channel.get("created_at"),
        )

    async def add_channel(
        self, conn: asyncpg.Connection, channel_id: int, name: str, description: str, genre: str
    ):
        """Adds a channel to the database"""

        await conn.execute(
            "INSERT INTO channels (channel_id, name, description, genre, created_at) VALUES ($1, $2, $3, $4, NOW())",
            channel_id,
            name,
            description,
            genre,
        )

    async def add_botban(self, conn: asyncpg.Connection, user_id: int, reason: str = None):
        """Adds a botban to the database"""

        await conn.execute(
            "INSERT INTO botbans (botban_id, reason, banned_at) VALUES ($1, $2, NOW())",
            user_id,
            reason,
        )
        self.bot.cache.botbans.append(user_id)

    async def get_botban(self, user_id: int):
        """Gets a botban from the database"""

        botban = await self.db.fetchrow("SELECT * FROM botbans WHERE botban_id = $1", user_id)

        return botban

    async def remove_botban(self, conn: asyncpg.Connection, user_id: int):
        """Removes a botban from the database"""

        await conn.execute("DELETE FROM botbans WHERE botban_id = $1", user_id)
        self.bot.cache.botbans.remove(user_id)


def setup(bot: commands.Bot):
    bot.add_cog(Database(bot))
