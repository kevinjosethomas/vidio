import discord
from discord.ext import commands


class Owner(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")

    @commands.group(name="cog", aliases=["cogs"])
    @commands.is_owner()
    async def cog(self, ctx: commands.Context):
        """Command Group for all cog management commands"""

        if not ctx.invoked_subcommand:
            description = f"• ``{ctx.prefix}cog list`` Lists all loaded cogs\n" \
                        f"• ``{ctx.prefix}cog load {{cog}}`` Loads the mentioned cog\n" \
                        f"• ``{ctx.prefix}cog reload {{cog}}`` Reloads the mentioned cog\n" \
                        f"• ``{ctx.prefix}cog unload {{cog}}`` Unloads the mentioned cog\n"

            embed = discord.Embed(
                title=":gear: Cog Commands",
                description=description,
                color=self.bot.c.red
            )

            await ctx.send(embed=embed)

    @cog.command()
    async def list(self, ctx: commands.Context):
        """Lists all available cogs that belong to the bot"""

        description = ""
        for cog in self.bot.cog_list:
            description += f"• ``{cog}``\n"

        embed = discord.Embed(
            title=":gear: All Cogs",
            description=description,
            color=self.bot.c.red
        )

        await ctx.send(embed=embed)

    @cog.command()
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


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
