from discord.ext import commands


class Vidio(commands.Cog):
    """
    basic cog that holds all the simulation commands
    """

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Vidio(bot))
