import dbl
import discord
from discord.ext import commands, tasks


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = self.bot.DBL_TOKEN
        self.database = self.bot.get_cog('Database')
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True, webhook_path='/upvote', webhook_port=5000)

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):

        bot_id = int(data["bot"])
        user_id = int(data["user"])
        upvote_type = data["type"]
        is_weekend = data["isWeekend"]

        if bot_id != self.bot.id:
            return

        upvote = self.database.on_vote(user_id, is_weekend)

        if upvote == 'User doesn\'t exist':
            return

        money = upvote[0]
        added_money = upvote[1]

        user = self.bot.get_user(user_id)

        await user.send(f':heart: **Thanks for upvoting!** {self.bot.money} You got ${added_money} for helping '
                        f'videonet grow!')

    @commands.Cog.listener()
    async def on_dbl_test(self, data):

        print("test vote")


def setup(bot):
    bot.add_cog(TopGG(bot))
