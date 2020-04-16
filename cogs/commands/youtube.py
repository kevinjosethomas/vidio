import discord
from discord.ext import commands
from youtube_api import YouTubeDataAPI
from discord.ext.commands.cooldowns import BucketType


class YouTube(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['vs'],
                      help='Fetches the first youtube video with the provided argument.',
                      usage='``-search {query}``')
    @commands.cooldown(1, 10, BucketType.user)
    async def search(self, ctx, *, query):

        yt = YouTubeDataAPI(self.bot.YT_KEY)

        video = yt.search(q=query, max_results=1, safe_search='strict')

        if not video:
            await ctx.send(f'{self.bot.no} **Not Found.** No video found for the provided search term.')
            return

        await ctx.send(f'{self.bot.yes} https://youtube.com/watch?v={video[0]["video_id"]}')


def setup(bot):
    bot.add_cog(YouTube(bot))