import asyncpg
import discord
from typing import Union
from discord.ext import commands
from ..exceptions import *


class Database(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = self.bot.database

    async def add_guild(self, guild_id: int, prefix: Union[str, None]):
        """Adds a guild to the database"""

        prefix = prefix if prefix else self.bot.c.default_prefix

        guild = await self.get_guild(guild_id)
        if guild:
            raise GuildError("Provided guild already exists!")
            return

        async with self.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO guilds VALUES ($1, $2, $3)",
                [guild_id, prefix, 0]
            )

    async def get_guild(self, guild_id: int) -> Union[asyncpg.Record, None]:
        """Fetches a guild from the database"""

        guild = await self.db.fetchrow(
            "SELECT * FROM guilds WHERE guild_id = $1",
            [guild_id]
        )

        return guild

    async def remove_guild(self, guild_id: int):
        """Removes a guild from the database"""

        guild = await self.get_guild(guild_id)
        if not guild:
            raise GuildError("Provided guild does not exist!")
            return

        async with self.db.acquire() as conn:
            await conn.execute(
                "DELETE FROM guilds WHERE guild_id = $1",
                [guild_id]
            )


def setup(bot: commands.Bot):
    bot.add_cog(Database(bot))
