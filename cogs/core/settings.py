import random
import discord
import traceback
from discord.ext import commands, tasks


class MyHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):

        help_embed = discord.Embed(
            color=self.context.bot.embed)

        for category in mapping:
            command = ', '

            command_list = list(map(lambda c: c.name, set(mapping[category])))

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
            text='For more help use >help {command} | '
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
        return f'{self.context.bot.no} Invalid command: ``{string}``'

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
                'aliases': ['h'],
                'usage': '``>help {command}``'}
        )
        self.db = self.bot.get_cog('Database')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Videonet is back online!")
        self.bot.support_server = self.bot.get_guild(self.bot.support_server_id)
        # self.change_presence.start() # Turns out this is API abuse so BYEE

    # @tasks.loop(minutes=random.randint(20, 26))
    # async def change_presence(self):
    #     presences = [
    #         discord.Activity(
    #             name='youtube videos',
    #             type=discord.ActivityType.watching),
    #         discord.Activity(
    #             name='pewdiepie fail',
    #             type=discord.ActivityType.watching),
    #         discord.Activity(
    #             name='satisfying slime videos',
    #             type=discord.ActivityType.watching),
    #         discord.Activity(
    #             name='some viral videos',
    #             type=discord.ActivityType.watching),
    #         discord.Activity(
    #             name='youtube videos',
    #             type=discord.ActivityType.watching),
    #         discord.Activity(
    #             name=f'{len(self.bot.guilds)} servers',
    #             type=discord.ActivityType.watching),
    #         discord.Activity(
    #             name=f'{len(self.bot.users)} users play.',
    #             type=discord.ActivityType.watching),
    #         discord.Game(name='with VillagerBot')
    #     ]
    #     await self.bot.change_presence(activity=random.choice(presences))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.db.add_guild(guild)

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
                'minutes before trying again!',
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
                description=f'{self.bot.no} **You do not have the necessary permissions to run this command.**'
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
                    description=f'{self.bot.no} **The provided cog does not exist.**',
                    color=self.bot.embed)
                await ctx.send(embed=unknown_error_embed)
                return

            elif isinstance(error.original, commands.ExtensionError) \
                    or isinstance(error.original, commands.ExtensionFailed):
                unknown_error_embed = discord.Embed(
                    description=f'{self.bot.no} **Unknown cog error. Please try again later**',
                    color=self.bot.embed)
                unknown_error_embed.set_footer(
                    text='If this issue persists, '
                         'please contact support at https://discord.gg/rB2EGa4')
                await ctx.send(embed=unknown_error_embed)
                return

            elif isinstance(error.original, commands.ExtensionAlreadyLoaded):
                unknown_error_embed = discord.Embed(
                    description=f'{self.bot.no} **The provided cog does is already loaded..**',
                    color=self.bot.embed)
                await ctx.send(embed=unknown_error_embed)
                return

            elif isinstance(error.original, commands.ExtensionNotLoaded):
                unknown_error_embed = discord.Embed(
                    description=f"{self.bot.no} **The provided cog is not loaded (or doesn't exist).**",
                    color=self.bot.embed)
                await ctx.send(embed=unknown_error_embed)
                return

        except AttributeError:
            pass

        else:
            unknown_error_embed = discord.Embed(
                description=f'{self.bot.no} **Unknown error. Please try again later**',
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

            error_channel = self.bot.support_server.get_channel(self.bot.error_channel_id)

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
                inline=False
            )
            print(traceback_text)
            await error_channel.send(embed=error_embed)
            return


def setup(bot):
    bot.add_cog(Default(bot))
