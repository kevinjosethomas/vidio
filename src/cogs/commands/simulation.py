import discord
from discord.ext import commands


class Simulation(commands.Cog):

    """
    Simulation; contains all commands related to YouTube simulation
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")


def setup(bot: commands.Cog):
    bot.add_cog(Simulation(bot))
