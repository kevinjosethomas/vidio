import arrow
import discord
import classyjson
from discord.ext import commands


class Events(commands.Cog):

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


def setup(bot: commands.Bot):
  bot.add_cog(Events(bot))