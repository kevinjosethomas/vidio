import dbl
import discord
from discord.ext import commands


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = self.bot.DBL_TOKEN
        self.database = self.bot.get_cog('Database')
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    # @commands.Cog.listener()
    # async def on_dbl_vote(self):


def setup(bot):
    bot.add_cog(TopGG(bot))
