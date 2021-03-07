import discord
from discord.ext import commands


class Utility(commands.Cog):

    """
    Utility; contains all utility commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
