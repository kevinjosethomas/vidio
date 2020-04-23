import discord
from discord.ext import commands


class Data(commands.Cog):

    def __int__(self, bot):
        self.bot = bot

        # some bot variables the bot uses for various purposes
        self.bot.embed = 0x2f3136

        # some emojis used by the bot
        self.bot.bug = '🐛'
        self.bot.money = '💵'
        self.bot.views = '👀'
        self.bot.pencil = '📝'
        self.bot.category = '📂'
        self.bot.real_subscribers = '🤝'
        self.bot.likes = '<:likes:694721324517556255>'
        self.bot.subscribers = '<:live:693869294051655721>'
        self.bot.dislikes = '<:dislikes:694721324483870760>'

        self.bot.fail = '🔴'
        self.bot.average = '⚪'
        self.bot.success = '🟢'

        self.bot.no = '<:no:692399981910556733>'
        self.bot.yes = '<:yes:692399981834928138>'

        self.bot.youtube = '<:youtube:693484343074619423>'
        self.bot.heartbeat = '<a:ping:692399981935722607>'
        self.bot.loading = '<a:loading:693852613812158494>'

        # some channels the bot uses
        self.bot.bugs_channel_id = 696014942083612742
        self.bot.error_channel_id = 692405881115246603
        self.bot.support_server_id = 689210707232686158
        self.bot.suggestions_channel_id = 696014954532438116

        self.bot.support_server = self.bot.get_guild(self.bot.support_server_id)


def setup(bot):
    bot.add_cog(Data(bot))
