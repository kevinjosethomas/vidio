import arrow
import discord
from typing import Callable
from discord.ext import commands
from discord_components import Button


class Simulation(commands.Cog):

    """
    Simulation; contains all commands related to YouTube simulation
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")

    async def validate_wait(self, ctx: commands.Context, message: str, _type: int, check: Callable):
        """Function that repeatedly asks and validates a wait_for"""

        # _type
        # 0 - Guild channel
        # 1 - DM channel

        def check_channel(message: discord.Message):
            """Validates guild channel wait_for event"""

            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

        def check_dm(message: discord.Message):
            """Validates DM channel wait_for event"""

            return message.author.id == ctx.author.id and isinstance(
                message.channel, discord.DMChannel
            )

        while True:

            if _type == 0:
                await ctx.send(message)
            else:
                await ctx.author.send(message)

            input_message = await self.bot.wait_for(
                "message", check=check_channel if _type == 0 else check_dm
            )

            if await check(input_message):
                return input_message
            else:
                continue

    @commands.command(usage="start")
    async def start(self, ctx: commands.Context):
        """Creates a channel for the author"""

        channel = await self.database.get_channel(ctx.author.id)
        if channel:
            await ctx.send(f"{self.bot.e.cross} you cannot create more than one channel")
            return

        await ctx.send(f"{self.bot.e.check} starting channel creation process in your DMs")

        name_message = (
            f"{self.bot.e.youtube} **Channel Name** 1/3\n"
            "Provide a creative name for your channel!\n"
            "Minimum 3 characters and maximum 32 characters in length.\n"
            "You can change this later."
        )

        async def check_name(message):
            """Validates name input"""

            if len(message.content) < 3:
                await message.channel.send(
                    f"{self.bot.e.cross} your name must not be less than 3 characters in length, please try again"
                )
                return False

            if len(message.content) > 32:
                await message.channel.send(
                    f"{self.bot.e.cross} your name must not be more than 32 characters in length, please try again"
                )
                return False

            return True

        name = (await self.validate_wait(ctx, name_message, 1, check_name)).content

        description_message = (
            f"{self.bot.e.youtube} **Channel Description** 2/3\n"
            "Provide a cool description for your channel!\n"
            "Minimum 15 characters and maximum 300 characters in length.\n"
            "You can change this later."
        )

        async def check_description(message):
            """Validates description input"""

            if len(message.content) < 15:
                await message.channel.send(
                    f"{self.bot.e.cross} your name must not be less than 15 characters in length, please try again"
                )
                return False

            if len(message.content) > 300:
                await message.channel.send(
                    f"{self.bot.e.cross} your name must not be more than 300 characters in length, please try again"
                )
                return False

            return True

        description = (
            await self.validate_wait(ctx, description_message, 1, check_description)
        ).content

        genre_message = (
            f"{self.bot.e.youtube} **Channel Genre** 3/3\n"
            "Choose a topic that most accurately describes your channel!\n"
            "You can change this later too."
        )

        genre_buttons = []
        genre_row = []
        for index, genre in enumerate(self.bot.genres, 1):
            genre_row.append(Button(label=genre.name, emoji=genre.emoji))
            if index % 5 == 0:
                genre_buttons.append(genre_row)
                genre_row = []

        if genre_row:
            genre_buttons.append(genre_row)

        sent_genre_message = await ctx.author.send(genre_message, components=genre_buttons)

        def check_button(interaction):
            """Validates DM channel wait_for event"""

            return (
                interaction.user.id == ctx.author.id
                and interaction.message.id == sent_genre_message.id
            )

        interaction = await self.bot.wait_for("button_click", check=check_button)

        genre = interaction.component.label
        await interaction.respond(type=6)

        new_genre_buttons = []
        for genre_row in genre_buttons:
            new_genre_row = []
            for genre_button in genre_row:
                if genre_button.label == genre:
                    genre_button.style = 3
                new_genre_row.append(genre_button)

            new_genre_buttons.append(new_genre_row)

        await sent_genre_message.edit(genre_message, components=new_genre_buttons)

        async with self.bot.database.acquire() as conn:
            await self.database.add_channel(conn, ctx.author.id, name, description, genre)

        await ctx.author.send(
            f"{self.bot.e.check} successfully created your channel, use ``{ctx.prefix}channel`` to check it out!"
        )

    @commands.command(usage="channel [user]", aliases=["c", "profile", "p"])
    async def channel(self, ctx: commands.Context, user: discord.User = None):
        """Returns data about the provided user's channel"""

        user = user if user else ctx.author
        channel = await self.database.get_channel(user.id)

        if not channel:
            await ctx.send(f"{self.bot.e.cross} you do not have a channel")
            return

        description = (
            f"{channel.description}\n\n"
            f"**Subscribers:** {channel.subscribers}\n"
            f"**Total views:** {channel.views}\n"
            f"**Genre:** {channel.genre}\n"
            f"Joined {arrow.get(channel.created_at).format('MMMM DD, YYYY')}\n\n"
            f"👤 **Inventory**\n"
            f"⌬ {channel.balance} dollars\n"
        )

        embed = discord.Embed(description=description, color=self.bot.c.red)
        embed.set_author(name=channel.name, icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot: commands.Cog):
    bot.add_cog(Simulation(bot))
