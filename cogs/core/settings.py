import asyncio
import random
import logging
import discord
import traceback
from datetime import datetime
from discord.ext import commands, tasks, menus


class HelpMenu(menus.Menu):

    async def send_initial_message(self, ctx, channel):

        help_embed = discord.Embed(
            description='**React to this message with -**\n\n'
                        f'{self.bot.EMOJIS["youtube"]} for **simulation** commands\n\n'
                        f':tools: for **utility** commands\n\n'
                        f':octagonal_sign: to return here',
            color=self.bot.embed)

        return await ctx.send(embed=help_embed)

    @menus.button(f'<:youtube:708330611756105768>')
    async def on_simulation(self, payload):

        description = '**tutorial** ``(how)``\nA basic tutorial on how to use the bot.\n\n' \
                      '**create_channel** ``(cc)``\nCreates a channel simulation with your user account. (prompts)\n\n' \
                      '**upload** ``(up)``\nUploads a video on the selected channel. (prompts)\n\n' \
                      '**profile** ``(p, bal, user)``\nDisplays current balance and list of channels that belong to the user.\n\n' \
                      '**channel** ``(c)``\nShows metrics about the selected channel. (prompts)\n\n' \
                      '**leaderboard** ``(lb)``\nShows the top 10 users of various metrics.\n\n' \
                      '**store** ``(shop, buy)``\nLists the things you can buy, also used to buy stuff from the store\n\n' \
                      '**video** ``(v, vid)``\nA command that shows statistics about a selected video.\n\n' \
                      '**subscribe** ``(sub)``\n A command that subscribes to the selected channel. (prompts)\n\n' \
                      '**unsubscribe** ``(unsub)``\nA command that unsubscribes from the selected channel. (prompts)\n\n' \
                      '**edit_description** ``(edit_dsc)``\nChanges your selected channel\'s description. (prompts)\n\n' \
                      '**edit_name** ``(edit_name)``\nChanges your selected channel\'s name. (prompts)\n\n' \
                      '**delete_channel** ``(dc)``\nDeletes the selected channel. (prompts)'

        help_embed = discord.Embed(
            title=f'{self.bot.EMOJIS["youtube"]} Simulation Commands',
            description=description,
            color=self.bot.embed
        )
        await self.message.edit(embed=help_embed)

    @menus.button('🛠️')
    async def on_utility(self, payload):

        description = "**prefix** ``(sp, setprefix, set_prefix)``\nChanges the bot prefix for your guild.\n\n" \
                      "**changelog** ``(changes)``\nShows a list of major changes made to the bot.\n\n" \
                      "**credits** ``(creds)``\nLists some amazing people who helped build vidio.\n\n" \
                      "**info**\nProvides you with some cool information about vidio.\n\n" \
                      "**links** ``(inv, vote, invite)``\nLists some important links for vidio.\n\n" \
                      "**bug** ``(report)``\nReport a bug that is broadcasted to the support server.\n\n" \
                      "**suggest** ``(s)``\nSuggest a vidio feature that is broadcasted to the support server.\n\n" \
                      "**statistics** ``(stats)``\nReturns some statistics about the vidio bot.\n\n" \
                      "**uptime**\nReturns how much time the bot has been online for.\n\n" \
                      "**ping** ``(pong)``\nReturns the bot's latency in milliseconds.\n\n" \
                      "**voteReminder** ``(vr)``\nToggles the voting reminder for vidio."

        help_embed = discord.Embed(
            title=f':tools: Utility Commands',
            description=description,
            color=self.bot.embed
        )
        await self.message.edit(embed=help_embed)

    @menus.button('🛑')
    async def on_stop(self, payload):

        help_embed = discord.Embed(
            description='**React to this message with -**\n\n'
                        f'{self.bot.EMOJIS["youtube"]} for **simulation** commands\n\n'
                        f':tools: for **utility** commands\n\n'
                        f':octagonal_sign: to return here',
            color=self.bot.embed)

        await self.message.edit(embed=help_embed)


class MyHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):

        help_embed = discord.Embed(
            color=self.context.bot.embed)

        for category in mapping:
            command = ', '

            command_list = list(map(lambda c: c.name, set(mapping[category])))

            for command_name in command_list:
                index = command_list.index(command_name)
                command_list[index] = f'``{command_name}``'

            command = command.join(command_list)

            if not command_list:
                continue

            if category is None:
                help_embed.add_field(
                    name='Uncategorized',
                    value=command,
                    inline=False)
                continue

            help_embed.add_field(
                name=category.qualified_name,
                value=command,
                inline=False)

        help_embed.set_footer(
            text='For more help use -help {command} | '
                 'Join our support server - https://discord.gg/rB2EGa4')

        await self.context.send(embed=help_embed)

    async def send_command_help(self, command):

        help_embed = discord.Embed(
            color=self.context.bot.embed)

        aliases = ', '
        aliases = aliases.join(command.aliases)

        help_embed.add_field(
            name=f'{command.name} ({aliases})',
            value=command.help,
            inline=False
        )

        help_embed.add_field(
            name='• Usage',
            value=command.usage,
            inline=False
        )

        await self.context.send(embed=help_embed)

    async def command_not_found(self, string):
        return f'{self.context.bot.no} **Invalid command:** ``{string}``'

    async def send_error_message(self, error):
        await self.context.send(
            embed=discord.Embed(
                color=self.context.bot.embed,
                description=error
            ))


class Default(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = MyHelpCommand(
            command_attrs={
                'name': 'uglyhelp',
                'aliases': ['uh'],
                'usage': '``-uhelp {command}``'})
        self.database = self.bot.get_cog('Database')

    @commands.command(
        aliases=['h'])
    async def help(self, ctx):
        help_menu = HelpMenu()
        await help_menu.start(ctx)

    @commands.Cog.listener()
    async def on_command(self, ctx):

        self.bot.logger.info(f'COMMAND {ctx.command} EXECUTED BY {ctx.author} AT {datetime.now()}')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):

        replies = [
            'Upvote the bot to get some money! https://top.gg/bot/689210550680682560/vote',
            f'Regularly ``{ctx.prefix}changelog`` to learn about new cool features!',
            'Join the vidio support server to stay updated about '
            'new features! https://discord.gg/pGzQUvE',
            f'Use ``{ctx.prefix}voteReminder on`` to enable bot vote reminders!']

        if random.choice([True, False, False, False, False]):
            await ctx.send(f'**Tip:** {random.choice(replies)}')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"vidio is back online!")
        self.bot.start_time = datetime.now()
        self.bot.support_server = self.bot.get_guild(self.bot.GLOBAL["support_server_id"])
        self.change_presence.start()

    async def bot_check(self, ctx):

        banned = await self.database.check_banned(ctx.author.id)

        if banned:
            return False

        if not self.bot.is_ready():
            await ctx.send(f'**{random.choice(["Hold up", "Wait a moment"])}!** vidio is still starting up!')
            return

        return True

    @tasks.loop(minutes=random.randint(20, 26))
    async def change_presence(self):
        presences = [
            discord.Activity(
                name='youtube videos',
                type=discord.ActivityType.watching),
            discord.Activity(
                name='pewdiepie fail',
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
            discord.Activity(
                name=f'{len(self.bot.users)} users play.',
                type=discord.ActivityType.watching)
        ]
        await self.bot.change_presence(activity=random.choice(presences))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.database.add_guild(guild)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        try:
            if ctx.handled:
                return
        except AttributeError:
            pass

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                description=f'You need to wait {str(int(error.retry_after // 60))} '
                f'minutes {str(int(error.retry_after % 60))} seconds before trying again!',
                color=self.bot.embed)
            await ctx.send(embed=cooldown_embed)
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            missing_arg_embed = discord.Embed(
                description=f'``{error.param}`` is a required argument for {ctx.command}. '
                'Please retry with the necessary parameters.',
                color=self.bot.embed)
            await ctx.send(embed=missing_arg_embed)
            return

        elif isinstance(error, commands.MissingPermissions):
            missing_permissions_embed = discord.Embed(
                description=f'{self.bot.EMOJIS["no"]} **You do not have the necessary permissions to run this command.**'
            )
            missing_permissions_embed.set_footer(
                text=f'Required Permissions: {", ".join(error.missing_perms)}')

            await ctx.send(embed=missing_permissions_embed)
            return

        elif isinstance(error, commands.NoPrivateMessage):
            return

        try:
            if isinstance(error.original, commands.ExtensionNotFound):
                unknown_error_embed = discord.Embed(
                    description=f'{self.bot.EMOJIS["no"]} **The provided cog does not exist.**',
                    color=self.bot.embed)
                await ctx.send(embed=unknown_error_embed)
                return

            elif isinstance(error.original, commands.ExtensionError) \
                    or isinstance(error.original, commands.ExtensionFailed):
                unknown_error_embed = discord.Embed(
                    description=f'{self.bot.EMOJIS["no"]} **Unknown cog error. Please try again later**',
                    color=self.bot.embed)
                unknown_error_embed.set_footer(
                    text='If this issue persists, '
                         'please contact support at https://discord.gg/rB2EGa4')
                await ctx.send(embed=unknown_error_embed)
                return

            elif isinstance(error.original, commands.ExtensionAlreadyLoaded):
                unknown_error_embed = discord.Embed(
                    description=f'{self.bot.EMOJIS["no"]} **The provided cog does is already loaded..**',
                    color=self.bot.embed)
                await ctx.send(embed=unknown_error_embed)
                return

            elif isinstance(error.original, commands.ExtensionNotLoaded):
                unknown_error_embed = discord.Embed(
                    description=f"{self.bot.EMOJIS['no']} **The provided cog is not loaded (or doesn't exist).**",
                    color=self.bot.embed)
                await ctx.send(embed=unknown_error_embed)
                return

            elif isinstance(error.original, discord.Forbidden):
                await ctx.author.send(
                    f"{self.bot.EMOJIS['no']} **vidio doesn't have permissions to send messages** in the channel "
                    f"where you initiated ``{ctx.command}``")
                return

            elif isinstance(error.original, asyncio.TimeoutError):
                await ctx.send(f'{self.bot.EMOJIS["yes"]} **Canceled process...** (Timed Out)')
                ctx.handled = True
                return

        except AttributeError:
            pass

        else:
            unknown_error_embed = discord.Embed(
                description=f'{self.bot.EMOJIS["no"]} **Unknown error. Please try again later**',
                color=self.bot.embed
            )
            unknown_error_embed.set_footer(
                text='If this issue persists, '
                     'please contact support at https://discord.gg/rB2EGa4')
            await ctx.send(embed=unknown_error_embed)

            etype = type(error)
            trace = error.__traceback__
            verbosity = 2
            lines = traceback.format_exception(etype, error, trace, verbosity)
            traceback_text = ''.join(lines)

            error_channel = self.bot.support_server.get_channel(self.bot.GLOBAL["error_channel_id"])

            input = ctx.message.content

            if len(traceback_text) > 1024:
                traceback_text = traceback_text[:1023]

            error_embed = discord.Embed(color=self.bot.embed)
            error_embed.add_field(
                name='Input',
                value=f'```{input}```',
                inline=False)

            error_embed.add_field(
                name='Output',
                value=f'```{traceback_text}```',
                inline=False)
            print(traceback_text)
            self.bot.logger.error(traceback_text)
            await error_channel.send(embed=error_embed)
            return

    @commands.Cog.listener()
    async def on_message(self, message):

        if self.bot.user in message.mentions:

            await message.channel.send(f'**The prefix for this server is -'
                                       f'** ``{(await self.database.get_prefix(message.guild))[0]}``')


def setup(bot):
    bot.add_cog(Default(bot))
