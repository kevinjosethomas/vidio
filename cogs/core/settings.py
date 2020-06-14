import random
import time
from discord.ext import commands


class Settings(commands.Cog):
    """
    cog with initialization and useful utility and settings for the bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    async def bot_check(self, ctx):

        banned = await self.database.check_banned(ctx.author.id)

        if banned:
            return False

        if not self.bot.is_ready():
            await ctx.send(f'**{random.choice(["Hold up", "Wait a moment"])}!** vidio is still starting up!')
            return

        return True

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """
        event called when a command is executed
        """

        self.bot.logger.info(f'COMMAND {ctx.command} EXECUTED BY {ctx.author.id} AT {int(time.time())}')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        """
        event called when a command execution is complete
        """

        replies = [
            'Upvote the bot to get some money! https://top.gg/bot/689210550680682560/vote',
            f'Regularly check ``{ctx.prefix}changelog`` to learn about new cool features!',
            'Join the vidio support server to stay updated about '
            'new features! https://discord.gg/pGzQUvE',
            f'Use ``{ctx.prefix}toggle_vote_reminder`` to enable bot vote reminders!']

        if random.choice([True, False, False, False, False]):
            await ctx.send(f'**Tip:** {random.choice(replies)}')

        await self.database.add_user_command(ctx.author.id, 1)
        await self.database.add_guild_command(ctx.guild.id, 1)

        self.bot.commands += 1

    @commands.Cog.listener()
    async def on_ready(self):
        """
        event initiated when the bot is ready
        """

        print(f"vidio is back online!")
        self.bot.start_time = int(time.time())
        self.bot.commands = 0
        self.bot.support_server = self.bot.get_guild(self.bot.CONFIG["support_server_id"])


def setup(bot):
    bot.add_cog(Settings(bot))
