import typing
import asyncpg
from discord.ext import commands

from ..exceptions import *


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

    async def add_guild(self, conn: asyncpg.Connection, guild_id: int, prefix: typing.Union[str, None] = None):
        """Adds a guild to the database"""

        prefix = prefix if prefix else self.bot.c.default_prefix

        guild = await self.get_guild(guild_id)
        if guild:
            raise GuildError("Provided guild already exists")

        await conn.execute(
            "INSERT INTO guilds (id, prefix) VALUES ($1, $2)",
            guild_id, prefix
        )

    async def get_guild(self, guild_id: int) -> typing.Union[asyncpg.Record, None]:
        """Fetches a guild from the database"""

        guild = await self.db.fetchrow(
            "SELECT * FROM guilds WHERE guild_id = $1",
            guild_id
        )

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
            prefix, guild_id
        )
        self.bot.cache.prefixes[guild_id] = prefix

    async def remove_guild(self, conn: asyncpg.Connection, guild_id: int):
        """Removes a guild from the database"""

        guild = await self.get_guild(guild_id)
        if not guild:
            raise GuildError("Provided guild does not exist")

        await conn.execute(
            "DELETE FROM guilds WHERE guild_id = $1",
            guild_id
        )

    async def add_botban(self, conn: asyncpg.Connection, user_id: int, reason: str = None):
        """Adds a botban to the database"""

        botban = await self.get_botban(user_id)
        if not botban:
            raise BotBanError("Provided botban already exists")

        await conn.execute(
            "INSERT INTO botbans (botban_id, reason, banned_at) VALUES ($1, $2, NOW())",
            user_id, reason
        )

    async def get_botban(self, user_id: int):
        """Gets a botban from the database"""

        botban = await self.db.fetchrow(
            "SELECT * FROM botbans WHERE botban_id = $1",
            user_id
        )

        return botban

    async def remove_botban(self, conn: asyncpg.Connection, user_id: int):
        """Removes a botban from the database"""

        botban = await self.get_botban(user_id)
        if not botban:
            raise BotBanError("Provided botban does not exist")

        await conn.execute(
            "DELETE FROM botbans WHERE botban_id = $1",
            user_id
        )


def setup(bot: commands.Bot):
    bot.add_cog(Database(bot))
