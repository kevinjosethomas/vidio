import os
import ast
import time
import asyncio
import discord
from discord.ext import commands

from ..exceptions import *


class Owner(commands.Cog):

    """
    Owner; contains all owner only commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")

    @commands.command(usage="list_servers")
    @commands.is_owner()
    async def list_servers(self, ctx: commands.Context):
        """Lists all the servers the bot is in"""

        channel = self.bot.guild.get_channel(842052429649936414)

        for guild in self.bot.guilds:
            await channel.send(guild.name + " " + str(guild.member_count))

    @commands.group(name="cog", aliases=["cogs"])
    @commands.is_owner()
    async def cog(self, ctx: commands.Context):
        """Command Group for all cog management commands"""

        if not ctx.invoked_subcommand:
            description = (
                f"• ``{ctx.prefix}cog list`` Lists all loaded cogs\n"
                f"• ``{ctx.prefix}cog load {{cog}}`` Loads the mentioned cog\n"
                f"• ``{ctx.prefix}cog reload {{cog}}`` Reloads the mentioned cog\n"
                f"• ``{ctx.prefix}cog unload {{cog}}`` Unloads the mentioned cog\n"
            )

            embed = discord.Embed(
                title=":gear: Cog Commands",
                description=description,
                color=self.bot.c.red,
            )

            await ctx.send(embed=embed)

    @cog.command(usage="cog list < cog | all >")
    async def list(self, ctx: commands.Context):
        """Lists all available cogs that belong to the bot"""

        description = ""
        for cog in self.bot.cog_list:
            description += f"• ``{cog}``\n"

        embed = discord.Embed(
            title=":gear: All Cogs",
            description=description,
            color=self.bot.c.red,
        )

        await ctx.send(embed=embed)

    @cog.command(usage="cog load < cog | all >")
    async def load(self, ctx: commands.Context, *, cog: str):
        """Loads to specified cogs"""

        cog = cog.lower()

        if cog == "all":
            for cog in self.bot.cog_list:
                self.bot.load_extension(cog)

            return await ctx.message.add_reaction(self.bot.e.check)

        cogs = cog.split()

        for cog in cogs:
            if not cog.startswith("cogs."):
                cog = f"cogs.{cog}"

            self.bot.load_extension(cog)

        await ctx.message.add_reaction(self.bot.e.check)

    @cog.command(usage="cog reload")
    async def reload(self, ctx: commands.Context, *, cog: str):
        """Reloads the specified cogs"""

        cog = cog.lower()

        if cog == "all":
            for cog in self.bot.cog_list:
                self.bot.reload_extension(cog)

            return await ctx.message.add_reaction(self.bot.e.check)

        cogs = cog.split()

        for cog in cogs:
            if not cog.startswith("cogs."):
                cog = f"cogs.{cog}"

            self.bot.reload_extension(cog)

        await ctx.message.add_reaction(self.bot.e.check)

    @cog.command(usage="cog unload < cog | all >")
    async def unload(self, ctx: commands.Context, *, cog: str):
        """Unloads the specified cogs"""

        cog = cog.lower()

        if cog == "all":
            for cog in self.bot.cog_list:
                self.bot.unload_extension(cog)

            return await ctx.message.add_reaction(self.bot.e.check)

        cogs = cog.split()

        for cog in cogs:
            if not cog.startswith("cogs."):
                cog = f"cogs.{cog}"

            self.bot.unload_extension(cog)

        await ctx.message.add_reaction(self.bot.e.check)

    def insert_returns(self, body: str):
        """Inserts required return statements to the eval code"""

        # Insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # For if statements, we insert returns into the body and the or else
        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)

        # For with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)

    @commands.command(usage="eval <code>")
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, command: str):
        """Evaluates the provided code"""

        fn_name = "_eval_expr"

        command = command.strip("` ")

        # Add a layer of indentation
        command = "\n".join(f"    {i}" for i in command.splitlines())

        # Wrap in async def body
        body = f"async def {fn_name}():\n{command}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        self.insert_returns(body)

        env = {
            "discord": discord,
            "commands": commands,
            "asyncio": asyncio,
            "time": time,
            "os": os,
            "ctx": ctx,
            "bot": self.bot,
            "__import__": __import__,  # Your variables go here
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = await eval(f"{fn_name}()", env)

        await ctx.message.add_reaction(self.bot.e.check)
        await ctx.send(result)

    @commands.command(usage="lookup <user>")
    @commands.is_owner()
    async def lookup(self, ctx: commands.Context, user: discord.User):
        """Returns all the bot's mutual guild with the provided user"""

        message = ""
        index = 1

        for guild in self.bot.guilds:
            if guild.get_member(user.id):
                message += f"{index}. {guild.name} ``{guild.id}``\n"
                index += 1

        embed = discord.Embed(
            title=":mag_right: User Lookup",
            description=message if message else "No mutual guilds found",
            color=self.bot.c.red,
        )

        await ctx.send(embed=embed)

    @commands.command(usage="top_guilds")
    @commands.is_owner()
    async def top_guilds(self, ctx: commands.Context):
        """Returns the 10 most popular guilds"""

        message = ""
        guilds = sorted(
            self.bot.guilds,
            key=(lambda guild: guild.member_count),
            reverse=True,
        )[:10]

        for index, guild in enumerate(guilds, 1):
            message += f"{index}. {guild.name} ({guild.member_count}) ``{guild.id}``\n"

        embed = discord.Embed(
            title=":trophy: Top Guilds",
            description=message,
            color=self.bot.c.red,
        )

        await ctx.send(embed=embed)

    @commands.command(usage="botban <user> [reason]")
    @commands.is_owner()
    async def botban(
        self, ctx: commands.Context, user: discord.User, reason: str = None
    ):
        """Bans the provided user from using the bot"""

        async with self.bot.database.acquire() as conn:
            await self.database.add_botban(conn, user.id, reason)

        await ctx.message.add_reaction(self.bot.e.check)

    @botban.error
    async def botban_error(self, ctx: commands.Context, error: Exception):
        """Error handler for botban command"""

        if getattr(error, "original"):
            if isinstance(error.original, BotBanError):
                await ctx.send(
                    f"{self.bot.e.cross} this user is already banned"
                )
                ctx.handled = True

    @commands.command(usage="unbotban <user>")
    @commands.is_owner()
    async def unbotban(self, ctx: commands.Context, user: discord.User):
        """Unbans the provided user and allows them to use the bot"""

        async with self.bot.database.acquire() as conn:
            await self.database.remove_botban(conn, user.id)

        await ctx.message.add_reaction(self.bot.e.check)

    @unbotban.error
    async def botban_error(self, ctx: commands.Context, error: Exception):
        """Error handler for unbotban command"""

        if getattr(error, "original"):
            if isinstance(error.original, BotBanError):
                await ctx.send(f"{self.bot.e.cross} this user is not banned")
                ctx.handled = True


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
