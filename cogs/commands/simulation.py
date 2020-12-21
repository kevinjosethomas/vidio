import discord
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

        name = (await self.bot.wait_for("message", check=check, timeout=60)).content

        if name.lower().strip() == "cancel":
            await ctx.author.send(f"{self.bot.e.check} Successfully cancelled the channel creation process")
            await message.edit(f"{self.bot.e.check} Cancelled the channel creation process")
            return

        if len(name) < 3:
            return await ctx.author.send(f"{self.bot.e.cross} The provided name was under 3 characters. Cancelled the channel creation process.")


        description_message = f"{self.bot.e.youtube} **Step 2/3 | Channel Description**\n" \
                            "Send a brief channel description below. Keep it short and concise, under 200 characters long. " \
                            "Please refrain from using profanity in your channel description and keep in mind that you can change this later!"
        await ctx.author.send(description_message)

        description = (await self.bot.wait_for("message", check=check, timeout=120)).content

        if description.lower().strip() == "cancel":
            await ctx.author.send(f"{self.bot.e.check} Successfully cancelled the channel creation process")
            await message.edit(f"{self.bot.e.check} Cancelled the channel creation process")
            return

        if len(description) < 25:
            return await ctx.author.send(f"{self.bot.e.cross} The provided description was under 25 characters. Cancelled the channel creation process.")


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
            return await ctx.send(f"{self.bot.e.cross} Invalid genre reaction provided. Canceled the channel creation process.")

        await self.database.add_channel(ctx.author.id, name, description, genre)

        await ctx.author.send(f"{self.bot.e.check} Successfully created your channel, you're now one step closer to world domination. Poggers!")

        await message.edit(f"{self.bot.e.check} Successfully created your channel")


def setup(bot: commands.Bot):
    bot.add_cog(Simulation(bot))
