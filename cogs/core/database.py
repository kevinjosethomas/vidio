import discord
from discord.ext import commands


class Database(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = self.bot.database


def setup(bot: commands.Bot):
    bot.add_cog(Database(bot))
