import os
import asyncio
import discord
import resource
import traceback
from datetime import datetime
from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.get_cog('Database')

    @commands.group(name="cog", aliases=['cogs'])
    @commands.is_owner()
    async def cog(self, ctx):

        if ctx.invoked_subcommand is None:

            message = f'``{ctx.prefix}cog load {{cog}}`` Loads the mentioned cog\n' \
                      f'``{ctx.prefix}cog unload {{cog}}`` Unloads the mentioned cog\n' \
                      f'``{ctx.prefix}cog reload {{cog}}`` Reloads the mentioned cog\n' \
                      f'``{ctx.prefix}cog list`` Lists all loaded cogs.'

            await ctx.send(message)

    @cog.command(name="load")
    async def load_cog(self, ctx, *, cog: str):

        cog = cog.lower()

        if cog == 'all':
            for cog in self.bot.cog_list:
                self.bot.load_extension(cog)

            message = "**Successfully loaded all cogs!**"
            await ctx.send(message)
            return

        if not cog.startswith('cogs.'):
            cog = f'cogs.{cog}'

        self.bot.load_extension(cog)

        message = f"*Successfully loaded** ``{cog}``"
        await ctx.send(message)

    @cog.command(name="unload")
    async def unload_cog(self, ctx, *, cog: str):

        cog = cog.lower()

        if cog == 'all':
            for cog in self.bot.cog_list:
                self.bot.unload_extension(cog)

            message = "**Successfully unloaded all cogs!**"
            await ctx.send(message)
            return

        if not cog.startswith('cogs.'):
            cog = f'cogs.{cog}'

        self.bot.unload_extension(cog)

        message = f"*Successfully unloaded** ``{cog}``"
        await ctx.send(message)

    @cog.command(name="reload")
    async def reload_cog(self, ctx, *, cog: str):

        cog = cog.lower()

        if cog == 'all':
            for cog in self.bot.cog_list:
                self.bot.reload_extension(cog)

            message = "**Successfully reloaded all cogs!**"
            await ctx.send(message)
            return

        if not cog.startswith('cogs.'):
            cog = f'cogs.{cog}'

        self.bot.reload_extension(cog)

        message = f"*Successfully reloaded** ``{cog}``"
        await ctx.send(message)

    @cog.command(name="list")
    async def list_cogs(self, ctx):
        cogs = ',\n'
        cog_list = list(self.bot.cogs)

        for cog in cog_list:
            cog_list[cog_list.index(cog)] = f'``{cog}``'

        cogs = cogs.join(cog_list)
        cogs_embed = discord.Embed(
            description=cogs,
            color=self.bot.embed
        )
        await ctx.send(embed=cogs_embed)

    @commands.command(
        aliases=['eval', 'ev'],
        usage='``-evaluate``',
        help='Executes the provided code.')
    @commands.is_owner()
    async def evaluate(self, ctx, *, code):

        eval_embed = discord.Embed(
            color=self.bot.embed)

        eval_embed.add_field(
            name='Input',
            value=f'```{code}```',
            inline=False)

        try:
            output = eval(code)
        except Exception as error:
            output = error

        eval_embed.add_field(
            name='Output',
            value=f'```{output}```',
            inline=False)

        await ctx.send(embed=eval_embed)

    @commands.command(
        aliases=['awaiteval', 'awaitev', 'awev'],
        usage='``-awaitevaluate``',
        help='Asynchronously executes the provided code.')
    @commands.is_owner()
    async def awaitevaluate(self, ctx, *, code):

        eval_embed = discord.Embed(
            color=self.bot.embed)

        eval_embed.add_field(
            name='Input',
            value=f'```{code}```',
            inline=False)

        try:
            output = await eval(code)
        except Exception as error:
            output = error

        eval_embed.add_field(
            name='Output',
            value=f'```{output}```',
            inline=False)

        await ctx.send(embed=eval_embed)

    @commands.command(
        aliases=['yeet', 'stop', 'murder', 'assassinate'],
        usage='``-ban {user}``',
        help='Bans the user from videonet.')
    @commands.is_owner()
    async def ban(self, ctx, *, user: discord.User):

        banned = await self.database.add_ban(user.id)

        if not banned:
            await ctx.send(f'{self.bot.EMOJIS["no"]} **<@{user.id}> is already banned.**')
            return
        await ctx.send(f"{self.bot.EMOJIS['yes']} **Successfully banned -** <@{user.id}>")

    @commands.command(
        aliases=['unyeet', 'revive', 'pardon'],
        usage='``-unban {user}``',
        help='Unbans the user from videonet.')
    @commands.is_owner()
    async def unban(self, ctx, *, user: discord.User):

        unbanned = await self.database.remove_ban(user.id)

        if not unbanned:
            await ctx.send(f'{self.bot.EMOJIS["no"]} **<@{user.id}> is not banned.**')
            return
        await ctx.send(f"{self.bot.EMOJIS['yes']} **Successfully unbanned -** <@{user.id}>")

    @commands.command(
        aliases=['update', 'gitpull'],
        usage='``-pull``',
        help='Pulls latest version from Github')
    @commands.is_owner()
    async def pull(self, ctx):
        os.system('git pull')
        await ctx.send(f'{self.bot.EMOJIS["yes"]} **Successfully pulled latest from Github!**')

    @commands.command(
        aliases=['ram', 'mem'],
        usage='``-memory``',
        help='Returns how much memory the bot is using.')
    @commands.is_owner()
    async def memory(self, ctx):

        memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        memory_embed = discord.Embed(
            description=f"Memory in use: ``{int(round(memory * .001 * 1.04858, 2))}mb``",
            color=self.bot.embed)
        await ctx.send(embed=memory_embed)

    # @commands.command(
    #     usage=f'``>restart``',
    #     help='Force restarts the bot.'
    # )
    # @commands.is_owner()
    # # async def restart(self, ctx):
    #     await ctx.send(f'{  self.bot.EMOJIS["yes"]} **Restarting the bot.**')
    #     await self.bot.logout()
    #     exit()


def setup(bot):
    bot.add_cog(Owner(bot))


