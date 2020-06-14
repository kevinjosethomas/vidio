import time
from discord.ext import commands


class Settings(commands.Cog):
    """
    cog with initialization and useful utility and settings for the bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """event called when a command is executed"""

        self.bot.logger.info(f'COMMAND {ctx.command} EXECUTED BY {ctx.author} AT {int(time.time())}')
