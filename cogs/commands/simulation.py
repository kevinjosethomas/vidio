import discord
from discord.ext import commands


class Simulation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")


def setup(bot: commands.Bot):
    bot.add_cog(Simulation(bot))
