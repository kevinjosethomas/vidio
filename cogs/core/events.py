import time
import discord
import classyjson
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")

    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot is ready"""

        self.bot.started_at = int(time.time())
        self.bot.guild = self.bot.get_guild(self.bot.c.guild_id)
        self.bot.errors_channel = self.bot.guild.get_channel(self.bot.c.errors_channel_id)
        self.bot.bug_reports_channel = self.bot.guild.get_channel(self.bot.c.bug_reports_channel_id)
        self.bot.suggestions_channel = self.bot.guild.get_channel(self.bot.c.suggestions_channel_id)

        self.bot.cache = classyjson.classify({})
        await self.database.populate_cache()

        print("vidio going brrrr")


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
