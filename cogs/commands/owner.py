import discord
from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
