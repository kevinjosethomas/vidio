import typing
import discord
from discord.ext import commands


class Database(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = self.bot.database

	async def populate_cache(self):
		"""Populates all bot cache"""

		self.bot.cache = {}
		self.bot.cache.prefixes = await self.get_all_prefixes()
		self.bot.cache.emoji_genre, self.bot.cache.genre_emoji = await self.get_all_genres()

	async def get_all_prefixes(self) -> dict:
		"""Fetches all guilds' prefixes from the database"""

		guilds = await self.db.fetch("SELECT id, prefix FROM guilds")

		return dict((guild["id"], guild["prefix"]) for guild in guilds if (guild["prefix"] != self.bot.c.default_prefix and guild["prefix"]))

	async def get_all_genres(self) -> typing.Tuple[list, list]:
		"""Fetches all genres from the database"""

		genres = await self.db.fetch("SELECT emoji, genre FROM genres")
		emoji_genre = genre_emoji = {}

		for genre in genres:
			emoji_genre[genre["emoji"]] = genre["genre"]
			genre_emoji[genre["genre"]] = genre["emoji"]
		
		return emoji_genre, genre_emoji


def setup(bot: commands.Bot):
	bot.add_cog(Database(bot))
