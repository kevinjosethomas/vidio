import discord
from discord.ext import commands


class Utility(commands.Cog):

    """
    Utility; contains all utility commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Ping command that returns the bot's latency"""

        embed = discord.Embed(
            description=f"{self.bot.e.ping} Pong! ``{round(self.bot.latency * 1000)}ms``",
            color=self.bot.c.red
        )

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
