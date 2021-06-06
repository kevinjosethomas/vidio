import arrow
import psutil
import discord
from discord.ext import commands


class CustomHelpCommand(commands.MinimalHelpCommand):

    """
    Help; lists all commands, cogs and groups
    """

    async def send_bot_help(self, _):
        """
        Auto-generated global help command
        """

        message = ""

        cogs = self.context.bot.cogs
        for cog_name in cogs:
            cog = cogs[cog_name]
            command_objects = cog.get_commands()
            commands = []

            for command in command_objects:
                try:
           s         if await command.can_run(self.context):

                        commands.append(f"``{command.name}``")
                except:
                    continue

            commands = sorted(commands)

            if commands:
                message += f"**{cog_name}**\n{' '.join(commands)}\n\n"

        embed = discord.Embed(
            title=":tools: Command Help",
            description=message,
            color=self.context.bot.c.red,
        )

        embed.set_footer(
            text=f"To get help for a specific command, use - {self.context.prefix}help {{command}}"
        )

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """
        Auto-generated command help
        """

        message = (
            f"**{self.context.prefix}{command.name} [{', '.join(command.aliases)}]**\n"
            f"{command.help}\n\n**• Usage**\n``{self.context.prefix}{command.usage}``"
        )
        embed = discord.Embed(
            description=message,
            color=self.context.bot.c.red,
        )

        await self.context.send(embed=embed)


class Utility(commands.Cog):

    """
    Utility; contains all utility commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(usage="ping")
    async def ping(self, ctx: commands.Context):
        """Returns the bot's latency"""

        embed = discord.Embed(
            description=f"{self.bot.e.ping} Pong! ``{round(self.bot.latency * 1000)}ms``",
            color=self.bot.c.red,
        )

        await ctx.send(embed=embed)

    @commands.command(usage="uptime")
    async def uptime(self, ctx: commands.Context):
        """Returns the bot's uptime"""

        duration = self.bot.started_at.humanize()
        time = self.bot.started_at.format("HH:mm").lower()
        date = self.bot.started_at.format("MMMM DD")

        embed = discord.Embed(
            description=f":calendar_spiral: The bot started **{duration}**, at **{time} EST** on **{date}**",
            color=self.bot.c.red,
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["stats"], usage="statistics")
    async def statistics(self, ctx: commands.Context):
        """Returns various statistics related to the bot"""

        # Bot Information
        guild_count = len(self.bot.guilds)
        dm_count = len(self.bot.private_channels)
        user_count = len(self.bot.users)
        command_count = self.bot.command_count
        commands_minute = round(
            self.bot.command_count
            / (
                (
                    arrow.now("America/Toronto") - self.bot.started_at
                ).total_seconds()
                / 60
            ),
            2,
        )
        vote_count = self.bot.votes
        votes_hour = round(
            self.bot.votes
            / (
                (
                    arrow.now("America/Toronto") - self.bot.started_at
                ).total_seconds()
                / 3600
            ),
            2,
        )

        # System Information
        process = psutil.Process()
        with process.oneshot():
            memory = (
                str(round(process.memory_full_info().uss / 1000000)) + "mb"
            )
            threads = process.num_threads()
            process.cpu_percent(interval=0.1)

        shards = self.bot.shard_count
        duration = self.bot.started_at.humanize(only_distance=True)
        ping = str(round(self.bot.latency * 1000, 2)) + "ms"
        cpu = str(round(process.cpu_percent() / psutil.cpu_count())) + "%"
        time = self.bot.started_at.format("HH:mm").lower()
        date = self.bot.started_at.format("MMMM DD")

        description = (
            f"vidio is in -\n"
            f"• **{guild_count}** servers\n"
            f"• **{dm_count}** DMs\n"
            f"• contact with **{user_count}** users\n\n"
        )

        description += (
            f"vidio has -\n"
            f"• executed **{command_count}** commands\n"
            f"• received **{vote_count}** votes\n\n"
            f"with an average of -\n"
            f"• **{commands_minute}** commands a minute\n"
            f"• **{votes_hour}** votes an hour\n\n"
            f"over the last -\n"
            f"• **{duration}**\n"
            f"• since **{time} EST** on **{date}**\n\n"
        )

        description += (
            f"vidio is using -\n"
            f"• **{memory}** RAM\n"
            f"• **{cpu}** of the CPU\n"
            f"• **{threads}** threads\n"
            f"• **{shards}** shards\n"
            f"with a response time of **{ping}**\n\n"
        )

        description += (
            f"[More Stats](https://statcord.com/bot/{self.bot.user.id})"
        )

        embed = discord.Embed(description=description, color=self.bot.c.red)

        await ctx.send(embed=embed)

    @commands.command(usage="links")
    async def links(self, ctx: commands.Context):
        """Returns a list of relevant links"""

        description = (
            "Here are some useful links relevant to vidio -\n\n"
            f"• [Invite]({self.bot.c.guild_invite})\n"
            f"• [Support Server]({self.bot.c.guild_invite})\n"
            "• [GitHub Repository](https://github.com/TrustedMercury/vidio)\n\n"
            f"• [Statistics](https://statcord.com/bot/{self.bot.user.id})\n"
            "• [DBL Page](https://top.gg/bot/689210550680682560)\n"
            "• [DBL Vote](https://top.gg/bot/689210550680682560/vote)\n"
        )

        embed = discord.Embed(description=description, color=self.bot.c.red)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
