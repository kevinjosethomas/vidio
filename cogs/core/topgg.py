import dbl
import discord
from discord.ext import commands, tasks


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = self.bot.DBL_TOKEN
        self.auth = self.bot.AUTH
        self.dblpy = dbl.DBLClient(
            self.bot,
            self.token,
            autopost=True,
            webhook_path='/upvote',
            webhook_port='5000',
            webhook_auth=self.auth
        )
        self.database = self.bot.get_cog('Database')

    @commands.Cog.listener()
    async def on_guild_post(self):

        print("Server Count successfully posted on top.gg")

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):

        bot = int(data["bot"])
        user = int(data["user"])
        isWeekend = data["isWeekend"]

        if bot != self.bot.user.id:
            return

        vote = self.database.on_vote(user, isWeekend)

        if vote is None:
            return

        money = vote
        user = self.bot.get_user(user)

        await user.send(
            f'{self.bot.heart} **Thanks for upvoting!** Voting on top.gg is an essential part of vidio\'s growth '
            f'after donations. As a reward, you get ``${str(money)}``! '
            f'{"The value is doubled as it is a weekend :)" if isWeekend else ""}')

    @commands.Cog.listener()
    async def on_dbl_test(self, data):

        print("successful test")
        print(data)
        print(type(data))


def setup(bot):
    bot.add_cog(TopGG(bot))



