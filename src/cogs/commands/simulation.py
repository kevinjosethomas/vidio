from typing import Callable
import discord
from discord.ext import commands


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

        print(name)

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

        print(description)


def setup(bot: commands.Cog):
    bot.add_cog(Simulation(bot))
