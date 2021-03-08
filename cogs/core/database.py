import typing
import discord
from discord.ext import commands

from ..exceptions import *


class Database(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = self.bot.database

    async def populate_cache(self):
        """Populates all bot cache"""

        self.bot.cache.prefixes = await self.get_all_prefixes()
        self.bot.cache.emoji_genre, self.bot.cache.genre_emoji = await self.get_all_genres()

    async def get_all_prefixes(self) -> dict:
        """Fetches all guilds' prefixes from the database"""

        guilds = await self.db.fetch("SELECT id, prefix FROM guilds")

        return dict(
            (guild["id"], guild["prefix"])
            for guild in guilds
            if (guild["prefix"] != self.bot.c.default_prefix and guild["prefix"])
        )

    async def get_all_genres(self) -> typing.Tuple[list, list]:
        """Fetches all genres from the database"""

        genres = await self.db.fetch("SELECT emoji, genre FROM genres")
        emoji_genre = genre_emoji = {}

        for genre in genres:
            emoji_genre[genre["emoji"]] = genre["genre"]
            genre_emoji[genre["genre"]] = genre["emoji"]

        return emoji_genre, genre_emoji

    async def add_guild(self, guild_id: int, prefix: typing.Union[str, None] = None):
        """Adds a guild to the database"""

        prefix = prefix if prefix else self.bot.c.default_prefix

        guild = await self.get_guild(guild_id)
        if guild:
            raise GuildError("Provided guild already exists")
            return

        async with self.db.acquire() as conn:
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

    async def update_guild_prefix(self, guild_id: int, prefix: str):
        """Updates a guild's prefix in the database"""

        if len(prefix) > 10:
            raise GuildError("Invalid prefix provided")

        guild = await self.get_guild(guild_id)
        if not guild:
            await self.add_guild(guild_id, prefix)
            self.bot.cache.prefixes[guild_id] = prefix
            return

        async with self.db.acquire() as conn:
            await conn.execute(
                "UPDATE guilds SET prefix = $1 WHERE guild_id = $2",
                prefix, guild_id
            )
            self.bot.cache.prefixes[guild_id] = prefix


def setup(bot: commands.Bot):
    bot.add_cog(Database(bot))
