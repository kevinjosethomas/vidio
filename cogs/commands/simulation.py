import discord
from ..exceptions import *
from discord.ext import commands


class Simulation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")

    @commands.command(
        usage="``yt!start``",
        help="Starts the channel creation process"
    )
    async def start(self, ctx: commands.Context):
        """Command - Starts the channel creation process"""

        def check(message: discord.Message) -> bool:
            return message.author.id == ctx.author.id and message.channel.type == discord.ChannelType.private

        def reaction_check(reaction, user):
            return user.id == ctx.author.id and reaction.emoji in self.bot.cache.emoji_genre.keys()

        channel = await self.database.get_channel(ctx.author.id)
        if channel:
            return await ctx.send(f"{self.bot.e.cross} You already have a channel")

        message = await ctx.send(f"{self.bot.e.loading} Started the channel creation process in your DMs. Cancel anytime by replying with ``cancel``.")


        name_message = f"{self.bot.e.youtube} **Step 1/3 | Channel Name**\n" \
                    "Provide us with your channel's name below! Make sure it's under 32 characters long " \
                    "and please refrain from using profanity in your channel names! Also remember, you can change this later!"

        await ctx.author.send(name_message)

        name = await self.bot.wait_for("message", check=check, timeout=60)

        if name.content.lower().strip() == "cancel":
            await name.add_reaction(self.bot.e.check)
            await message.edit(content=f"{self.bot.e.cross} Cancelled the channel creation process")
            return

        name = name.content

        if len(name) < 3:
            await ctx.author.send(f"{self.bot.e.cross} The provided name was under 3 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        if len(name) > 32:
            await ctx.author.send(f"{self.bot.e.cross} The provided name was over 32 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        description_message = f"{self.bot.e.youtube} **Step 2/3 | Channel Description**\n" \
                            "Send a brief channel description below. Keep it short and concise, under 200 characters long. " \
                            "Please refrain from using profanity in your channel description and keep in mind that you can change this later!"
        await ctx.author.send(description_message)

        description = await self.bot.wait_for("message", check=check, timeout=120)

        if description.content.lower().strip() == "cancel":
            await description.add_reaction(self.bot.e.check)
            await message.edit(content=f"{self.bot.e.cross} Cancelled the channel creation process")
            return

        description = description.content

        if len(description) < 25:
            await ctx.author.send(f"{self.bot.e.cross} The provided description was under 25 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        if len(description) > 200:
            await ctx.send(f"{self.bot.e.cross} The provided description was over 200 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return


        genre_message = f"{self.bot.e.youtube} **Step 3/3 | Channel Genre**\n" \
                    "Choose *one* genre from the list of genres below by reacting to this message with the respective emojis. You're almost done!\n\n"

        for genre in self.bot.cache.emoji_genre:
            genre_message += f"{genre} {self.bot.cache.emoji_genre[genre]}\n"

        genre_message_object = await ctx.author.send(genre_message)

        for genre in self.bot.cache.emoji_genre:
            await genre_message_object.add_reaction(genre)

        reaction, user = await self.bot.wait_for("reaction_add", check=reaction_check, timeout=60)

        genre = self.bot.cache.emoji_genre[reaction.emoji]
        if not genre:
            await ctx.send(f"{self.bot.e.cross} Invalid genre reaction provided. Canceled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        try:
            await self.database.add_channel(ctx.author.id, name, description, genre)
        except ChannelError:
            await ctx.author.send(f"{self.bot.e.cross} Channel creation process cancelled. Make sure the details you provided follow our guidelines.")
            await message.edit(content=f"{self.bot.e.cross} Failed to create channel")
            return

        await ctx.author.send(f"{self.bot.e.check} Successfully created your channel, you're now one step closer to world domination. Poggers!")

        await message.edit(content=f"{self.bot.e.check} Successfully created your channel")

    @commands.group(invoke_without_command=True)
    async def edit(self, ctx: commands.Context):
        """Command Group for editing channel details"""

        description = "Want to edit your channel details? Here's what you can change -\n" \
                    "• ``name``\n" \
                    "• ``description``\n"\
                    "• ``genre``\n"\

        embed = discord.Embed(
            description=description,
            color=self.bot.c.red
        )

        embed.set_footer(text=f"Usage - {ctx.prefix}edit {{ name | description | genre }}")

        await ctx.send(embed=embed)

    @edit.command()
    async def name(self, ctx: commands.Context):
        """Edits the user's channel name"""

        def check(message: discord.Message) -> bool:
            return message.author.id == ctx.author.id and message.channel.type == discord.ChannelType.private

        channel = await self.database.get_channel(ctx.author.id)
        if not channel:
            return await ctx.send(f"{self.bot.e.cross} You don't have a channel, create one with ``{ctx.prefix}start``")

        message = await ctx.send(f"{self.bot.e.loading} Started the channel name edit process in your DMs. Cancel anytime by replying with ``cancel``.")

        name_message = f"{self.bot.e.youtube} **Edit Channel Name**\n" \
                    "Provide us with your channel's new name below! Make sure it's under 32 characters long " \
                    "and please refrain from using profanity in your channel name! Also remember, you can change this again later!"

        await ctx.author.send(name_message)

        name = await self.bot.wait_for("message", check=check, timeout=60)

        if name.content.lower().strip() == "cancel":
            await name.add_reaction(self.bot.e.check)
            await message.edit(content=f"{self.bot.e.cross} Cancelled the channel name edit process")
            return

        name = name.content

        if len(name) < 3:
            await ctx.author.send(f"{self.bot.e.cross} The provided name was under 3 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        if len(name) > 32:
            await ctx.author.send(f"{self.bot.e.cross} The provided name was over 32 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        try:
            await self.database.edit_name(ctx.author.id, name)
        except ChannelError:
            await ctx.author.send(f"{self.bot.e.cross} Channel name edit process cancelled. Make sure the name you provided follows our guidelines.")
            await message.edit(content=f"{self.bot.e.cross} Failed to edit channel name")
            return

        await ctx.author.send(f"{self.bot.e.check} Successfully updated your channel's name")
        await message.edit(content=f"{self.bot.e.check} Successfully updated your channel's name")

    @edit.command()
    async def description(self, ctx: commands.Context):
        """Edits the user's channel description"""

        def check(message: discord.Message) -> bool:
            return message.author.id == ctx.author.id and message.channel.type == discord.ChannelType.private

        channel = await self.database.get_channel(ctx.author.id)
        if not channel:
            return await ctx.send(f"{self.bot.e.cross} You don't have a channel, create one with ``{ctx.prefix}start``")

        message = await ctx.send(f"{self.bot.e.loading} Started the channel description edit process in your DMs. Cancel anytime by replying with ``cancel``.")

        description_message = f"{self.bot.e.youtube} **Edit Channel Description**\n" \
                            "Send a new brief channel description below. Keep it short and concise, under 200 characters long. " \
                            "Please refrain from using profanity in your channel description and keep in mind that you can change this again later!"
        await ctx.author.send(description_message)

        description = await self.bot.wait_for("message", check=check, timeout=120)

        if description.content.lower().strip() == "cancel":
            await description.add_reaction(self.bot.e.check)
            await message.edit(content=f"{self.bot.e.cross} Cancelled the channel description edit process")
            return

        description = description.content

        if len(description) < 25:
            await ctx.author.send(f"{self.bot.e.cross} The provided description was under 25 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        if len(description) > 200:
            await ctx.author.send(f"{self.bot.e.cross} The provided description was over 200 characters. Cancelled the channel creation process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel creation process.")
            return

        try:
            await self.database.edit_description(ctx.author.id, description)
        except ChannelError:
            await ctx.author.send(f"{self.bot.e.cross} Channel description edit process cancelled. Make sure the description you provided follows our guidelines.")
            await message.edit(content=f"{self.bot.e.cross} Failed to edit channel description")
            return

        await ctx.author.send(f"{self.bot.e.check} Successfully updated your channel's description")
        await message.edit(content=f"{self.bot.e.check} Successfully updated your channel's description")

    @edit.command()
    async def genre(self, ctx: commands.Context):
        """Edits the user's channel genre"""

        def reaction_check(reaction, user):
            return user.id == ctx.author.id and reaction.emoji in self.bot.cache.emoji_genre.keys()

        channel = await self.database.get_channel(ctx.author.id)
        if not channel:
            return await ctx.send(f"{self.bot.e.cross} You don't have a channel, create one with ``{ctx.prefix}start``")

        message = await ctx.send(f"{self.bot.e.loading} Started the channel genre edit process in your DMs. Cancel anytime by replying with ``cancel``.")

        genre_message = f"{self.bot.e.youtube} **Step 3/3 | Channel Genre**\n" \
                    "Choose *one* new genre from the list of genres below by reacting to this message with the respective emojis.\n\n"

        for genre in self.bot.cache.emoji_genre:
            genre_message += f"{genre} {self.bot.cache.emoji_genre[genre]}\n"

        genre_message_object = await ctx.author.send(genre_message)

        for genre in self.bot.cache.emoji_genre:
            await genre_message_object.add_reaction(genre)

        reaction, user = await self.bot.wait_for("reaction_add", check=reaction_check, timeout=60)

        genre = self.bot.cache.emoji_genre[reaction.emoji]
        if not genre:
            await ctx.send(f"{self.bot.e.cross} Invalid genre reaction provided. Canceled the channel genre edit process.")
            await message.edit(content=f"{self.bot.e.cross} Invalid input was provided, cancelled channel genre edit process.")
            return

        try:
            await self.database.edit_genre(ctx.author.id, genre)
        except ChannelError:
            await ctx.author.send(f"{self.bot.e.cross} Channel genre edit process cancelled")
            await message.edit(content=f"{self.bot.e.cross} Failed to edit channel genre")
            return

        await ctx.author.send(f"{self.bot.e.check} Successfully updated your channel's genre")
        await message.edit(content=f"{self.bot.e.check} Successfully updated your channel's genre")


def setup(bot: commands.Bot):
    bot.add_cog(Simulation(bot))
