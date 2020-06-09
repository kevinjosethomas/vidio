import dbl
import discord
from discord.ext import commands, tasks


class TopGG(commands.Cog):

    """class for topgg integration for votes and prizes."""

    def __init__(self, bot):
        """basic initialization of topgg class"""

        self.bot = bot
        self.token = self.bot.DBL_TOKEN
        self.database = self.bot.get_cog('Database')
        self.dblpy = dbl.DBLClient(
            self.bot,
            self.token,
            autopost=True,
            webhook_path='/upvote',
            webhook_port=5000,
            webhook_auth=self.bot.PASSWORD)

    @commands.Cog.listener()
    async def on_guild_post(self):
        """event called when the server count is updated on top.gg"""

        print("Server count posted successfully")

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """event called when someone votes for the bot on top.gg"""

        bot_id = int(data["bot"])
        user_id = int(data["user"])
        is_weekend = data["isWeekend"]

        if bot_id != self.bot.user.id:
            return

        upvote = await self.database.on_vote(user_id, is_weekend)

        if upvote == 'User doesn\'t exist':
            return

        money = upvote[0]
        added_money = upvote[1]

        user = self.bot.get_user(user_id)

        await user.send(f':heart: **Thanks for upvoting!** {self.bot.money} You got ${added_money} for helping '
                        f'vidio grow!')

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print("Successful Test")
        print(data)

        bot_id = int(data["bot"])
        user_id = int(data["user"])
        is_weekend = data["isWeekend"]

        if bot_id != self.bot.user.id:
            return

        upvote = await self.database.on_vote(user_id, is_weekend)

        if not upvote:
            return

        money = upvote[0]
        added_money = upvote[1]

        user = self.bot.get_user(user_id)

        await user.send(f':heart: **Thanks for upvoting!** {self.bot.money} You got ``${added_money}`` for helping '
                        f'videonet grow!')


def setup(bot):
    bot.add_cog(TopGG(bot))
