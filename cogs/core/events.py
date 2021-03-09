import arrow
import random
import discord
import classyjson
from discord.ext import commands, tasks


class Events(commands.Cog):

    """
    Events; includes all event handlers and basic utility
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")

    @commands.Cog.listener()
    async def on_ready(self):
        """Event triggered when the bot is ready"""

        self.bot.votes = 0
        self.bot.command_count = 0
        self.bot.started_at = arrow.now("America/Toronto")

        self.bot.guild = self.bot.get_guild(self.bot.c.guild_id)
        self.bot.errors_channel = self.bot.guild.get_channel(self.bot.c.errors_channel_id)

        self.bot.cache = classyjson.classify({})
        await self.database.populate_cache()

        print("vidio going brrrr")

        await self.change_presence.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Event triggered when a message is sent"""

        await self.bot.wait_until_ready()

        if message.content.lower() == f"<@!{self.bot.user.id}>":

            prefix = self.bot.cache.prefixes.get(message.guild.id, self.bot.c.default_prefix)

            description = (
                f":yo_yo: **Hello, I'm vidio!**\n"
                f"My prefix in this server is ``{prefix}`` \n"
                f"Type ``{prefix}help`` for a list of all my commands!"
            )

            embed = discord.Embed(description=description, color=self.bot.c.red)

            await message.channel.send(embed=embed)

    @tasks.loop(minutes=random.randint(5, 10))
    async def change_presence(self):
        """Automatically changes the bot's presence every 10-20 minutes"""

        presences = [
            discord.Activity(name="spicy youtube videos", type=discord.ActivityType.watching),
            discord.Activity(name="satisfying slime videos", type=discord.ActivityType.watching),
            discord.Activity(name="my daily dose of internet", type=discord.ActivityType.watching),
            discord.Activity(name="mrbeast spend more money", type=discord.ActivityType.watching),
            discord.Activity(name="mark rober troll some porch pirates", type=discord.ActivityType.watching),
            discord.Activity(name="cocomelon get dissed", type=discord.ActivityType.watching),
        ]

        await self.bot.change_presence(activity=random.choice(presences))


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
