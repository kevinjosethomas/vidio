import math
import time
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from discord.ext.commands.cooldowns import BucketType


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    @commands.command(
        usage='``-info``',
        help='Provides you with some information about the bot.')
    async def info(self, ctx):

        info_embed = discord.Embed(
            title='vidio - Information',
            description='**vidio** is a new youtube simulator discord bot with new features coming out regularly!'
                        ' vidio allows you and the members of your server to create a simulation of a '
                        f'youtube channel on Discord!\n\n vidio is in {len(self.bot.guilds)} servers and has made a '
                        f'total of {await self.database.get_channels_count()} channel simulations!',
            color=self.bot.embed)

        info_embed.set_footer(text=f'Check out {ctx.prefix}help, {ctx.prefix}credits and {ctx.prefix}stats for '
                                   f'more information!')

        info_embed.set_author(name='vidio', icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=info_embed)

    @commands.command(
        aliases=['stats'],
        usage='``-statistics``',
        help='Provides you with some in-depth statistics about the bot.')
    async def statistics(self, ctx):
        emb = discord.Embed(
            description=f'**Total Channel Simulations:** ``{str(await self.database.get_channels_count())}``\n'
            f'**Total Users:** ``{len(self.bot.users)} users``\n'
            f'**Total Guilds:** ``{len(self.bot.guilds)} servers``\n'
            f'**Total DMs:** ``{len(self.bot.private_channels)} DMs``\n'
            f'**Total Commands:** ``{self.bot.command_count} commands since startup.``\n'
            f'**Average commands/s:** ``{str(math.ceil(self.bot.command_count / (int(time.time()) - self.bot.start_time)))}``\n'
            f'**Latency:** ``{round(self.bot.latency * 1000, 2)} ms``\n',
            color=self.bot.embed)

        emb.set_author(name='vidio', icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=emb)

    @commands.command(
        aliases=["pong"],
        usage='``-ping``',
        help="Returns the bot's latency in milliseconds.")
    async def ping(self, ctx):
        if 'ping' in ctx.message.content.lower():
            reply = "Pong"
        else:
            reply = "Ping"

        ping_embed = discord.Embed(
            description=f'{self.bot.EMOJIS["heartbeat"]} **{reply}!** ``{round(self.bot.latency * 1000, 2)} ms``',
            color=self.bot.embed
        )
        await ctx.send(embed=ping_embed)

    @commands.command(
        aliases=['creds'],
        usage='``-credits``',
        help='Lists some people and services that helped build vidio.')
    async def credits(self, ctx):
        credits_embed = discord.Embed(
            description='Some people and services that helped build vidio.',
            color=self.bot.embed)

        credits_embed.add_field(
            name='Developers',
            value='TrustedMercury#1953\nIapetus11#6821',
            inline=False)

        credits_embed.add_field(
            name='Design and Ideas',
            value='Credit to [ravy](https://ravy.xyz) for the Help Command design.',
            inline=False)

        credits_embed.add_field(
            name='Other',
            value='A special thanks to thebrownbatman for helping out with the vidio algorithm and it\'s formulas.')

        credits_embed.set_author(name='vidio', icon_url='https://i.imgur.com/7mf0D6z.png')

        await ctx.send(embed=credits_embed)

    @commands.command(
        aliases=['sp', 'setprefix', 'set_prefix'],
        usage='``-prefix``',
        help='Sets a different prefix for your server.')
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def prefix(self, ctx, *, prefix):

        if len(prefix) > 10:
            await ctx.send(f"{self.bot.EMOJIS['no']} **Your prefix is too long!** (Maximum length - 10)")
            return

        prefix = await self.database.set_prefix(ctx.guild, prefix)

        if prefix == 'Bad Arguments':
            await ctx.send(f"{self.bot.EMOJIS['no']} **Error.** Please make "
                           "sure your prefix only have alphabets, numbers, punctuation "
                           "and spaces.")
            return

        await ctx.send(f"{self.bot.EMOJIS['yes']} **Successfully set this bot's prefix to -** ``{prefix}``!")

    @commands.command(
        aliases=['s'],
        usage='``-suggest``',
        help='Broadcasts your suggestion to the vidio support server.')
    @commands.cooldown(1, 10, BucketType.user)
    async def suggest(self, ctx, *, suggestion):

        support_server = self.bot.get_guild(self.bot.CONFIG["support_server_id"])
        suggestions_channel = support_server.get_channel(self.bot.CONFIG["suggestions_channel_id"])

        suggestion_embed = discord.Embed(
            title=f'{self.bot.EMOJIS["pencil"]} New Suggestion!',
            description=suggestion,
            color=self.bot.embed)

        suggestion_embed.set_footer(text="Make your own suggestions with -suggest!")
        suggestion_embed.set_author(name=ctx.author.name+'#'+ctx.author.discriminator+' | '+str(ctx.author.id),
                                    icon_url=ctx.author.avatar_url)

        message = await suggestions_channel.send(embed=suggestion_embed)
        await ctx.send(f'{self.bot.EMOJIS["yes"]} **Sent your suggestion to the vidio support server!**')

        await message.add_reaction(self.bot.EMOJIS["yes"])
        await message.add_reaction(self.bot.EMOJIS["no"])

    @commands.command(
        aliases=['report'],
        usage='``-bug``',
        help='Send your bug to the vidio support server!')
    @commands.cooldown(1, 10, BucketType.user)
    async def bug(self, ctx, *, bug):

        support_server = self.bot.get_guild(self.bot.CONFIG["support_server_id"])
        bugs_channel = support_server.get_channel(self.bot.CONFIG["bugs_channel_id"])

        bug_embed = discord.Embed(
            title=f'{self.bot.bug} New Bug!',
            description=bug,
            color=self.bot.embed)

        bug_embed.set_footer(text="Report your bug with -bug")
        bug_embed.set_author(
            name=ctx.author.name + '#' + ctx.author.discriminator+' | '+str(ctx.author.id),
            icon_url=ctx.author.avatar_url)

        await bugs_channel.send(embed=bug_embed)
        await ctx.send(f'{self.bot.EMOJIS["yes"]} **Sent your suggestion to the vidio support server!**')

    @commands.command(
        aliases=['changes'],
        usage='``-changelog``',
        help='Shows you a list of recent changes made to the bot.')
    async def changelog(self, ctx):

        changelog_embed = discord.Embed(
            title='Changelog - vidio',
            color=self.bot.embed)

        # changelog_embed.add_field(
        #     name='**• Monday, 11th May 2020**',
        #     value='- \n',
        #     inline=False
        # )

        changelog_embed.add_field(
            name='**• Monday, 11th May 2020**',
            value='- Added video search command with statistics\n'
                  '- Moved old help command to -uglyhelp or -uh\n'
                  '- Made a new help command.\n',
            inline=False
        )

        changelog_embed.add_field(
            name='**• Thursday, 7th May 2020**',
            value='- Removed wait after uploading.\n'
                  '- Added play buttons.\n',
            inline=False
        )

        changelog_embed.add_field(
            name='**• Monday, 27th April 2020**',
            value='- Increased chance of good videos and reduced chance of fail videos.\n'
                  '- Reduced decent advertisement price.\n'
                  '- Removed cooldowns from most commands.\n',
            inline=False
        )

        await ctx.send(embed=changelog_embed)

    @commands.command(
        usage='``-uptime``',
        help='Shows you how long the bot has been online for.')
    async def uptime(self, ctx):

        uptime = datetime.now() - self.bot.start_time

        days = uptime.days
        hours = uptime.seconds // 60 // 60
        minutes = uptime.seconds // 60 % 60

        message = '**vidio** has been online for '

        if days:
            if days > 1:
                ds = 'days'
            else:
                ds = 'day'
            message += f'{str(days)} {ds}, '

        if hours:
            if hours > 1:
                hs = 'hours'
            else:
                hs = 'hour'
            message += f'{str(hours)} {hs} and '

        if minutes > 1:
            ms = 'minutes'
        else:
            ms = 'minute'
        message += f'{str(minutes)} {ms}.'

        await ctx.send(message)

    @commands.command(
        aliases=['inv', 'invite', 'vote'],
        usage='``-links``',
        help='Sends an invite to the support server.')
    async def links(self, ctx):

        link_embed = discord.Embed(
            title='vidio invites',
            description='[Join the Support Server](https://discord.gg/pGzQUvE)\n'
                        '[Invite the Bot](https://discordapp.com/api/oauth2/authorize?client_id=689210550680682560&'
                        'permissions=379968&scope=bot)\n'
                        '[Upvote the Bot](https://top.gg/bot/689210550680682560/vote)\n'
                        '[Source Code](https://github.com/codebytedev/vidio)',
            color=self.bot.embed)

        link_embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=link_embed)

    @commands.command(
        aliases=['vr'],
        usage='``-voteReminder {enable | on | disable | off}``',
        help='Configure voting reminders!')
    async def voteReminder(self, ctx, status):

        if status.lower() == 'enable' or status.lower() == 'on':
            status = True
        elif status.lower() == 'disable' or status.lower() == 'off':
            status = False
        else:
            await ctx.send(f'{self.bot.EMOJIS["no"]} **Invalid Input.** Valid inputs are - ``enable | on | disable | off``')
            return

        success = await self.database.set_vote_reminder(ctx.author.id, status)

        if success == 'Already active':
            if status is False:
                status = 'disabled'
            elif status is True:
                status = 'enabled'
            await ctx.send(f'{self.bot.EMOJIS["no"]} **Vote reminders are already {status}.**')

        elif success:
            if status is False:
                status = 'disabled'
            elif status is True:
                status = 'enabled'
            await ctx.send(f'{self.bot.EMOJIS["yes"]} **Successfully {status} vote reminders!** '
                           f'You will now be reminded to vote around every 12 hours!')


def setup(bot):
    bot.add_cog(Utility(bot))