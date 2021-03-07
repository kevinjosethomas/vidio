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
        """Rreturns the bot's latency"""

        embed = discord.Embed(
            description=f"{self.bot.e.ping} Pong! ``{round(self.bot.latency * 1000)}ms``",
            color=self.bot.c.red
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """Returns the bot's uptime"""

        duration = self.bot.started_at.humanize()
        time = self.bot.started_at.format("HH:mm").lower()
        date = self.bot.started_at.format("MMMM DD")

        embed = discord.Embed(
            description=f":calendar_spiral: The bot started **{duration}**, at **{time} EST** on **{date}**",
            color=self.bot.c.red
        )

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
