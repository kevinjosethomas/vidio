import discord
import statcord
from discord.ext import commands


class Statcord(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = statcord.Client(self.bot, self.bot.STATCORD_KEY)
        self.client.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        """Event triggered when a command is executed"""

        self.bot.command_count += 1
        self.Client.command_run(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(Statcord(bot))
