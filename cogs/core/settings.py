import time
import random
import asyncio
import discord
import traceback
from ..exceptions.exceptions import *
from discord.ext import commands, tasks


class Settings(commands.Cog):
    """
    cog with initialization and useful utility and settings for the bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    async def bot_check(self, ctx):
        """
        global bot_check initiated before every command that checks if the
        command author is banned, and also if the bot is ready
        """

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
    async def on_command_error(self, ctx, error):
        """
        event triggered when an error/exception is raised
        """

        try:
            if ctx.handled is True:
                return
        except AttributeError:
            pass

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            message = f"**Try again later!** " \
                      f"You need to wait {str(error.retry_after // 60)} " \
                      f"minutes and {str(error.retry_after % 60)} seconds " \
                      f"to execute this command again!"
            await ctx.send(message)
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            message = "**Missing command parameters!** Please make sure you " \
                      "are providing the right arguments for this command. " \
                      f"You are missing the ``{error.param}`` argument."
            await ctx.send(message)
            return

        elif isinstance(error, commands.MissingPermissions):
            message = "**Missing Permissions!** You are missing the required " \
                      "permissions to execute that command. You need " \
                      f"``{', '.join(error.missing_perms)}``"
            await ctx.send(message)
            return

        elif isinstance(error, commands.NoPrivateMessage):
            return

        elif isinstance(error, InvalidUser):
            message = '**Invalid User!** This user is not in the database.'
            await ctx.send(message)
            return

        elif isinstance(error, InvalidChannel):
            message = '**Invalid Channel!** This user does not have a channel.'
            await ctx.send(message)
            return

        elif isinstance(error, NotEnoughMoneyError):
            message = "**Not Enough Money!** You do not have enough money to complete this purchase!"
            await ctx.send(message)
            return

        elif isinstance(error, ChannelLimitError):
            message = '**Channel Limit Reacher!** You cannoto have more than 3 channels as a user.'
            await ctx.send(message)
            return

        elif isinstance(error, NameTooLongError):
            message = '**Invalid Input!** The provided channel name is too long! ' \
                      'Please make sure it is under 50 characters.'
            await ctx.send(message)
            return

        elif isinstance(error, DescriptionTooLongError):
            message = '**Invalid Input!** The provided channel description is too long! ' \
                      'Please make sure it is under 500 characters.'
            await ctx.send(message)
            return

        elif isinstance(error, DuplicateChannelNameError):
            message = '**Duplicate Channel Name!** You cannot have more than one channel with the same name.'
            await ctx.send(message)
            return

        elif isinstance(error, AlreadyBotBanned):
            message = '**Already Banned!** This user is already botbanned.'
            await ctx.send(message)
            return

        elif isinstance(error, NotBotBanned):
            message = '**Not Banned!** This user is not botbanned.'
            await ctx.send(message)
            return

        elif isinstance(error, AlreadySubscribedError):
            message = '**Invalid Action!* You are already subscribed to this channel.'
            await ctx.send(message)
            return

        elif isinstance(error, SelfSubscribeError):
            message = '**Invalid Action!** You cannot subscribe to yourself.'
            await ctx.send(message)
            return

        elif isinstance(error, SubscriptionDoesntExist):
            message = '**Invalid Action!** You are not subscribed to this user.'
            await ctx.send(message)
            return

        elif isinstance(error, InvalidChannel):
            message = '**Invalid Input!** The provided custom prefix is too long! ' \
                      'Please make sure it is under 10 characters.'
            await ctx.send(message)
            return

        try:
            if isinstance(error.original, commands.ExtensionNotFound):
                message = "**Invalid Cog!** The mentioned cog does not exist."
                await ctx.send(message)
                return

            elif isinstance(error.original, commands.ExtensionError):
                message = f"**Unknown Cog Error!** Error in extension - ``{error.original.name}``."
                await ctx.send(message)
                return

            elif isinstance(error.original, commands.ExtensionNotLoaded):
                message = f"**Invalid Cog!** The mentioned cog is not loaded."
                await ctx.send(message)
                return

            elif isinstance(error.original, commands.ExtensionAlreadyLoaded):
                message = "**Invalid Cog!** The mentioned cog is already loaded."
                await ctx.send(message)
                return

            elif isinstance(error.original, commands.ExtensionFailed):
                message = f"**Cog Error!** Failed to load the mentioned cog - ``{error.original.name}``."
                await ctx.send(message)
                return

            elif isinstance(error.original, discord.Forbidden):
                message = "**Missing Bot Permissions!** I do not have permission to send " \
                          "messages in the channel you initiated the command in."
                await ctx.author.send(message)
                return

            elif isinstance(error.original, asyncio.TimeoutError):
                message = "**Timed Out!** Canceled the input process as you took too long to reply!"
                await ctx.send(message)
                return

        except AttributeError:
            pass

        else:

            message = "**Unknown Error!** Please try again later. " \
                      f"If this issue persists, please report it in the support server. (``{ctx.prefix}links``)"
            await ctx.send(message)

            etype = type(error)
            trace = error.__traceback__
            verbosity = 2
            lines = traceback.format_exception(etype, error, trace, verbosity)
            traceback_error = ''.join(lines)

            error_channel = self.bot.support_server.get_channel(self.bot.CONFIG["error_channel_id"])

            user_input = ctx.message.content
            guild = ctx.guild
            timestamp = int(time.time())
            channel = ctx.channel
            user = ctx.author.id
            try:
                invites = await guild.invites()
            except discord.Forbidden:
                invites = None

            embed = discord.Embed()

            embed.add_field(
                name="Input",
                value=f"```{user_input}```"
            )
            embed.add_field(
                name="Guild",
                value=guild
            )
            embed.add_field(
                name="Channel",
                value=channel
            )
            embed.add_field(
                name="User",
                value=f"{user} at {timestamp}"
            )
            if invites:
                embed.add_field(
                    name="Invites",
                    value=invites[:4]
                )
            embed.add_field(
                name="Traceback",
                value=f"```traceback_error```"
            )

            await error_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        event initiated when the bot joins a server
        """

        await self.database.add_guild(guild)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        event triggered when a message is sent that the bot has read access to
        """

        if self.bot.user in message.mentions:
            await message.channel.send(
                f'The prefix for this server is -'
                f'** ``{(await self.database.get_prefix(message.guild.id))}``')

    @commands.Cog.listener()
    async def on_ready(self):
        """
        event initiated when the bot is ready
        """

        print(f"vidio is back online!")
        self.bot.start_time = int(time.time())
        self.bot.command_count = 0
        self.bot.support_server = self.bot.get_guild(self.bot.CONFIG["support_server_id"])

        self.change_presence.start()

    # loops

    @tasks.loop(minutes=random.randint(20, 25))
    async def change_presence(self):
        """
        loop that is ran every 20-25 minutes that changes the bot's presence status
        """

        presences = [
            discord.Activity(
                name='youtube videos',
                type=discord.ActivityType.watching),
            discord.Activity(
                name='satisfying slime videos',
                type=discord.ActivityType.watching),
            discord.Activity(
                name='some viral videos',
                type=discord.ActivityType.watching),
            discord.Activity(
                name='youtube videos',
                type=discord.ActivityType.watching),
            discord.Activity(
                name=f'{len(self.bot.guilds)} servers',
                type=discord.ActivityType.watching),
        ]
        await self.bot.change_presence(activity=random.choice(presences))


def setup(bot):
    bot.add_cog(Settings(bot))
