import math
import locale
import asyncio
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from discord.ext.commands.cooldowns import BucketType


class Vidio(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    async def multi_channels(self, ctx, channels):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild and ctx.channel == msg.channel

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **This user doesn't have any channels.**")
            return False

        message = f"{self.bot.youtube} **This user has multiple channels.** Use the index (number) given" \
                  f" to the channels in the list below to choose which channel you want to see.\n"

        for channel in channels:
            message += f"• ``{channels.index(channel) + 1}.`` {channel[2]}\n"

        message += "\n To cancel channel search, simply type ``cancel``."

        while True:
            await ctx.send(message)
            channel_index = await self.bot.wait_for('message', check=author_check, timeout=120)

            if channel_index.content.lower() == 'cancel':
                await ctx.send(f'{self.bot.yes} **Successfully canceled channel search process...**')
                return False

            try:
                if int(channel_index.content) > len(channels) or int(channel_index.content) <= 0:
                    await ctx.send(f"{self.bot.no} **Invalid index provided.** Please try again.")
                    continue
            except ValueError:
                await ctx.send(f"{self.bot.no} **Invalid index provided.** Please try again.")
                continue

            try:
                channel_index = int(channel_index.content) - 1
            except IndexError:
                await ctx.send(f"{self.bot.no} **Invalid index provided.** Please try again.")
                continue
            break
        return channel_index

    @commands.command(
        aliases=['cc'],
        usage='``-create_channel``',
        help='A simple command that creates a channel for you.')
    @commands.cooldown(1, 10, BucketType.user)
    async def create_channel(self, ctx):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild and ctx.channel == msg.channel

        channels = await self.database.get_channel(ctx.author.id)

        if channels == "Channel doesn't exist":
            channels = None
        elif len(channels) >= 3:
            await ctx.send(
                f"{self.bot.no} **You cannot create more than 3 channels.**")
            return

        name_msg = f'{self.bot.youtube} **Step 1/3: Choose a name ' \
                   'for your channel**\nLet\'s create your channel! First, ' \
                   'enter the name of your channel exactly ' \
                   'how you want it to be. ' \
                   '**Your channel name must not exceed 50 characters.**\n\n' \
                   'To cancel channel setup, simply type ``cancel``.'

        while True:
            await ctx.send(name_msg)
            name = await self.bot.wait_for('message', check=author_check, timeout=120)

            if name.content.lower() == 'cancel':
                await ctx.send(f'{self.bot.yes} **Successfully canceled channel creation process...**')
                return

            if len(name.content) > 50:
                continue

            name = name.content
            break

        description_msg = f'{self.bot.youtube} **Step 2/3: Write a description' \
                          ' for your channel**\n Perfect! Now, write a cool description ' \
                          'about your channel! ' \
                          '**Your channel description must not exceed 250 characters.**\n\n' \
                          'To skip this, simply type ``skip``\n' \
                          'To cancel channel setup, simply type ``cancel``.'

        while True:

            await ctx.send(description_msg)

            description = await self.bot.wait_for('message', check=author_check, timeout=180)

            if description.content.lower() == 'cancel':
                await ctx.send(f'{self.bot.yes} **Successfully canceled channel creation process...**')
                return

            if description.content.lower() == 'skip':
                description = ''
                break

            if len(description.content) > 250:
                continue

            description = description.content
            break

        categories = [
            '``art``', '``animation``',
            '``beauty``', '``comedy``',
            '``cooking``', '``dance``',
            '``diy``', '``family``',
            '``fashion``', '``gaming``',
            '``health``', '``learning``',
            '``music``', '``pranks``',
            '``sports``', '``tech``',
            '``travel``', '``vlogs``']

        category_str = ',\n'.join(categories)

        category_msg = f'{self.bot.youtube} **Step 3/3: Choose your channel ' \
                       ' category**\n Nice! Now choose a category from this list!\n' \
                       f'{category_str}\n\n To skip this, simply type ``skip``\n' \
                       'To cancel channel setup, simply type ``cancel``.'

        while True:

            await ctx.send(category_msg)

            category = await self.bot.wait_for('message', check=author_check, timeout=120)

            if category.content.lower() == 'cancel':
                await ctx.send(f'{self.bot.yes} **Successfully canceled channel creation process...**')
                return

            if category.content.lower() == 'skip':
                category = ''
                break

            if category.content.replace('``', '').lower() in category_msg.replace('``', ''):
                category = category.content
            else:
                continue

            break

        message = await ctx.send(f"{self.bot.loading} Validating "
                                 f"your entries and creating your channel.")

        await asyncio.sleep(1)

        query = await self.database.add_channel(ctx.author.id, name, description, category)

        if query == 'Channel with same name exists':
            await ctx.send(f"{self.bot.no} **You have a channel with the same name.** "
                           f"This makes it really hard for us to handle."
                           f" Please retry with a different name.")
            await message.delete()
            return

        elif query == 'Successful':
            await ctx.send(f"{self.bot.yes} **Successfully created your channel!** "
                           f"Check it out with ``{ctx.prefix}channel``!")
            await message.delete()

    @create_channel.error
    async def create_channel_error(self, ctx, error):

        try:
            if isinstance(error.original, asyncio.TimeoutError):
                await ctx.send(f'{self.bot.yes} **Canceled channel creation process...** (Timed Out)')
                ctx.handled = True
                return
            ctx.handled = False
        except AttributeError:
            ctx.handled = False

    @commands.command(
        aliases=['c'],
        usage='``-channel``',
        help='A simple command that returns the user\'s channel information!')
    @commands.cooldown(1, 10, BucketType.user)
    async def channel(self, ctx, *, user: discord.User = None):

        if user is None:
            user = ctx.author.id

        if isinstance(user, discord.User):
            user = user.id

        channels = await self.database.get_channel(user)

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        if len(channels) == 1:
            channel_index = 0

        elif len(channels) > 1:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        name = channels[channel_index][2]
        description = channels[channel_index][3]
        subs = channels[channel_index][4]
        total_views = channels[channel_index][5]
        category = channels[channel_index][6]
        created_at = channels[channel_index][7]
        date = f'{created_at.strftime("%B")} {created_at.strftime("%d")}, {created_at.strftime("%Y")}'

        real_subscribers = await self.database.get_subscribers(channels[channel_index][1])
        real_subscribers = len(real_subscribers)

        user = self.bot.get_user(user)

        subs = locale.format_string("%d", subs, grouping=True)
        total_views = locale.format_string("%d", total_views, grouping=True)

        yt_embed = discord.Embed(
            title=f'**{name}**',
            description=f'{self.bot.subscribers} **Subscribers:** {subs}\n'
                        f'{self.bot.real_subscribers} **Real Subscribers:** {real_subscribers}\n\n'
                        f'{self.bot.views} **Total Views:** {total_views}\n'
                        f'{self.bot.category} **Category:** {category}\n'
                        f':calendar_spiral: **Created on:** {date}\n\n'
                        f':notepad_spiral: **Description:** {description}',
            color=self.bot.embed)

        yt_embed.set_author(name=user.name, icon_url=user.avatar_url)
        yt_embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=yt_embed)

    @channel.error
    async def channel_error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{self.bot.no} **Unknown user -** ``{ctx.message.content.split()[1]}``")
            ctx.handled = True
            return
        ctx.handled = False

        try:
            if isinstance(error.original, asyncio.TimeoutError):
                await ctx.send(f'{self.bot.yes} **Canceled channel viewing process...** (Timed Out)')
                ctx.handled = True
                return
            ctx.handled = False
        except AttributeError:
            ctx.handled = False

        ctx.handled = False

    @commands.command(
        aliases=['edit_dsc', 'set_dsc', 'set_description'],
        usage='``-edit_description``',
        help='A command that changes your channel description')
    @commands.cooldown(1, 10, BucketType.user)
    async def edit_description(self, ctx):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild and ctx.channel == msg.channel

        user = ctx.author.id
        channels = await self.database.get_channel(user)

        if len(channels) == 1:
            channel_index = 0
        else:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        description_msg = f'{self.bot.youtube} **Step 1/1: Write a new description' \
                          ' for your channel**\n Write a cooler description ' \
                          'about your channel! ' \
                          '**Your channel description must not exceed 250 characters.**\n\n' \
                          'To cancel edit, simply type ``cancel``.'

        while True:

            await ctx.send(description_msg)

            description = await self.bot.wait_for('message', check=author_check, timeout=180)

            if description.content.lower() == 'cancel':
                await ctx.send(f'{self.bot.yes} **Successfully canceled channel editing process...**')
                return

            if len(description.content) > 250:
                continue

            description = description.content
            break

        query = await self.database.set_description(channels[channel_index][1], description)

        await ctx.send(f"{self.bot.yes} **Successfully changed your channel description!**")

    @commands.command(
        aliases=['set_name'],
        usage='``-edit_name``',
        help='A command that changes your channel name.')
    async def edit_name(self, ctx):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild and ctx.channel == msg.channel

        user = ctx.author.id
        channels = await self.database.get_channel(user)

        if len(channels) == 1:
            channel_index = 0
        else:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        description_msg = f'{self.bot.youtube} **Step 1/1: Enter a new channel name' \
                          ' for your channel**\n Enter a cooler name ' \
                          'for your channel! ' \
                          '**Your channel name must not exceed 50 characters.**\n\n' \
                          'To cancel edit, simply type ``cancel``.'

        while True:

            await ctx.send(description_msg)

            name = await self.bot.wait_for('message', check=author_check, timeout=180)

            if name.content.lower() == 'cancel':
                await ctx.send(f'{self.bot.yes} **Successfully canceled channel editing process...**')
                return

            if len(name.content) > 50:
                continue

            name = name.content
            break

        query = await self.database.set_channel_name(channels[channel_index][1], name)

        await ctx.send(f"{self.bot.yes} **Successfully changed your channel name!**")

    @commands.command(
        aliases=['dc'],
        usage='``-delete_channel``',
        help='A command that deleted a particular channel for you.')
    @commands.cooldown(1, 10, BucketType.user)
    async def delete_channel(self, ctx):

        user = ctx.author.id

        channels = await self.database.get_channel(user)

        if len(channels) == 1:
            channel_index = 0
        elif len(channels) > 1:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        channel = channels[channel_index]

        await self.database.remove_channel(channel[0], channel[1])

        await ctx.send(f"{self.bot.yes} **Successfully deleted your channel -** ``{channel[2]}``")

    @commands.command(
        aliases=['up'],
        usage='``-upload``',
        help='A command that uploads a video on the author\'s channel.')
    @commands.max_concurrency(1, BucketType.user, wait=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def upload(self, ctx):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild and ctx.channel == msg.channel

        channels = await self.database.get_channel(ctx.author.id)

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **You don't have a channel.** You must create a channel to upload videos.")
            return

        if len(channels) == 1:
            channel_index = 0
        elif len(channels) > 1:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        latest_video = await self.database.get_all_videos(channels[channel_index][1], 1)

        if not latest_video == 'No videos':
            difference = datetime.now() - latest_video[0][11]

            if difference < timedelta(hours=1):
                remaining = ((timedelta(hours=1) - difference).seconds // 60) % 60

                cooldown_embed = discord.Embed(
                    description=f'You need to wait {str(remaining)} '
                                'minutes before trying again!',
                    color=self.bot.embed)
                await ctx.send(embed=cooldown_embed)
                return

        video_msg = f'{self.bot.youtube} ** Step 1/2 Enter a name for your video**\n' \
                    '**Your video name must not exceed 50 characters. **\n\n' \
                    'To cancel video upload, simply type ``cancel``.'

        while True:

            await ctx.send(video_msg)

            video_name = await self.bot.wait_for('message', check=author_check, timeout=60)

            if video_name.content == 'cancel':
                await ctx.send(f'{self.bot.yes} Successfully '
                               'canceled video upload process...')
                return

            if len(video_name.content) > 50:
                await ctx.send(f"{self.bot.no} **Your title is too long.** Please try again.")
                continue

            video_name = video_name.content
            break

        description_msg = f'{self.bot.youtube} **Step 2/2: Write a description for your video**\n' \
                          'Perfect! Now, write a cool description ' \
                          'for your video! ' \
                          '**Your channel description must not exceed 250 characters.**\n\n' \
                          'To skip this, simply type ``skip``\n' \
                          'To cancel channel setup, simply type ``cancel``.'

        while True:

            await ctx.send(description_msg)

            description = await self.bot.wait_for('message', check=author_check, timeout=180)

            if description.content.lower() == 'cancel':
                await ctx.send(f'{self.bot.yes} **Successfully canceled channel creation process...**')
                return

            if description.content.lower() == 'skip':
                description = ''
                break

            if len(description.content) > 250:
                continue

            description = description.content
            break

        message = await ctx.send(f"{self.bot.loading} Validating your entries and uploading your video.")

        await asyncio.sleep(1)

        video = await self.database.upload_video(ctx.author.id, channels[channel_index][1], video_name, description)

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        status = video['status']
        channel_name = video['channel']
        new_subs = locale.format_string('%d', video['new_subs'], grouping=True)
        views = locale.format_string('%d', video['views'], grouping=True)
        money = locale.format_string('%d', video['money'], grouping=True)
        likes = locale.format_string('%d', video['likes'], grouping=True)
        dislikes = locale.format_string('%d', video['dislikes'], grouping=True)

        if status == 'successful' or status == 'good':
            status_quote = f'{self.bot.success} Status'
        elif status == 'average':
            status_quote = f'{self.bot.average} Status'
        elif status == 'poor' or status == 'fail':
            status_quote = f'{self.bot.fail} Status'
        else:
            status_quote = 'Status'

        if not str(new_subs).startswith('-'):
            new_subs = f"+{new_subs}"

        video_embed = discord.Embed(
            title=video_name,
            description=f'{self.bot.youtube} **Channel:** {channel_name}\n'
                        f'**{status_quote}:** {status.capitalize()}\n\n'
                        f'{self.bot.subscribers} **Subscribers:** {new_subs}\n'
                        f'{self.bot.views} **Views:** {views}\n'
                        f'{self.bot.money} **Money:** ${money}\n\n'
                        f'{self.bot.likes} **Likes:** {likes}\n'
                        f'{self.bot.dislikes} **Dislikes:** {dislikes}\n\n'
                        f'{self.bot.description} **Description:** {description}',
            color=self.bot.embed)

        video_embed.set_footer(
            text='⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n'
                 'Note: The statistics of your video will continue changing for the next 5 days.'
        )

        await message.delete()
        await ctx.send(embed=video_embed)

    @upload.error
    async def upload_error(self, ctx, error):

        try:
            if isinstance(error.original, asyncio.TimeoutError):
                await ctx.send(f'{self.bot.yes} **Canceled video upload process...** (Timed Out)')
                ctx.handled = True
                return
            ctx.handled = False
        except AttributeError:
            ctx.handled = False

    @commands.group(
        aliases=['lb'])
    async def leaderboard(self, ctx):

        if ctx.invoked_subcommand is None:
            lb_embed = discord.Embed(
                description=f'• Subscriber Leaderboard | ``{ctx.prefix}leaderboard subscribers``\n'
                            f'• Views Leaderboard | ``{ctx.prefix}leaderboard views``\n'
                            f'• Money Leaderboard | ``{ctx.prefix}leaderboard money``',
                color=self.bot.embed)
            await ctx.send(embed=lb_embed)

    @leaderboard.command(
        aliases=['subs', 's'],
        usage='``-leaderboard subscribers``',
        help='List the 10 most subscribed users on vidio.')
    async def subscribers(self, ctx):

        lb = await self.database.get_leaderboard('subscribers')

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        desc = ''
        pos = 1

        for entry in lb:
            desc += f'{pos}. ``{locale.format_string("%d", entry[2], grouping=True)} ' \
                    f'subs`` {self.bot.subscribers} {entry[1]} - <@{entry[0]}>\n'
            pos += 1

        lb_embed = discord.Embed(
            title='vidio subscriber leaderboard',
            description=desc,
            color=self.bot.embed)

        await ctx.send(embed=lb_embed)

    @leaderboard.command(
        aliases=['v'],
        usage='``-leaderboard views``',
        help='List the 10 most viewed users on vidio.')
    async def views(self, ctx):

        lb = await self.database.get_leaderboard('total_views')

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        desc = ''
        pos = 1

        for entry in lb:
            desc += f'{pos}. ``{locale.format_string("%d", entry[3], grouping=True)} ' \
                    f'views`` {self.bot.views} {entry[1]} - <@{entry[0]}>\n'
            pos += 1

        lb_embed = discord.Embed(
            title='vidio views leaderboard',
            description=desc,
            color=self.bot.embed)

        await ctx.send(embed=lb_embed)

    @leaderboard.command(
        aliases=['m'],
        usage='``-leaderboard money``',
        help='List the 10 richest users on vidio.')
    async def money(self, ctx):

        lb = await self.database.get_user_leaderboard()

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        desc = ''
        pos = 1

        for entry in lb:
            desc += f'{pos}. ``${locale.format_string("%d", entry[1], grouping=True)}`` ' \
                    f'- <@{entry[0]}>\n'
            pos += 1

        lb_embed = discord.Embed(
            title='vidio money leaderboard',
            description=desc,
            color=self.bot.embed)

        await ctx.send(embed=lb_embed)

    @commands.command(
        aliases=['v'],
        usage='``-video``',
        help='A command that (inaccurately) searches for videos uploaded on your channel.')
    async def video(self, ctx, *, video_name):

        channels = await self.database.get_channel(ctx.author.id)

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **You don't have a channel.** You must create a channel to upload videos.")
            return

        if len(channels) == 1:
            channel_index = 0

        elif len(channels) > 1:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        channel_id = channels[channel_index][1]

        videos = await self.database.get_video(channel_id, video_name)

        if videos == 'No videos':
            await ctx.send(f'{self.bot.no} **Unknown video.** Could not find a video with that name on vidio.')
            return

        description = ''

        for video in videos:
            description += f'• {video[2]}\n'

        if len(description) > 2043:
            description = description[:2043]

        videos_embed = discord.Embed(
            title=f'We found ``{len(videos)}`` video(s) related to ``{video_name}``',
            description=description)

        await ctx.send(embed=videos_embed)

    @commands.command(
        aliases=['sub'],
        usage='``-subscribe {user}``',
        help='A command that subscribes to another user\'s channel.')
    async def subscribe(self, ctx, user: discord.User):

        user = user.id
        author = ctx.author.id

        if user == ctx.author.id:
            await ctx.send(f'{self.bot.no} **You cannot subscribe to your own channels.**')
            return

        channels = await self.database.get_channel(user)

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **This user doesn't have a channel.**")
            return

        if len(channels) == 1:
            channel_index = 0
        elif len(channels) > 1:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        status = await self.database.add_subscriber(author, channels[channel_index][1])

        if status == 'Already subscribed to this user':
            await ctx.send(f'{self.bot.no} **You are already subscribed to this user.** '
                           f'You can\'t subscribe to the same person twice.')
            return
        elif status == 'You cannot subscribe to your own channels.':
            await ctx.send(f'{self.bot.no} **You cannot subscribe to your own channels.**')
            return

        subscribed_embed = discord.Embed(
            description=f'{self.bot.yes} Successfully subscribed to **{channels[channel_index][2]}** '
                        f'<@{channels[channel_index][0]}>',
            color=self.bot.embed)

        await ctx.send(embed=subscribed_embed)

    @commands.command(
        aliases=['unsub'],
        usage='``-unsubscribe {user}``',
        help='A command that unsubscribes from another user\'s channel.')
    async def unsubscribe(self, ctx, user: discord.User):

        user = user.id
        author = ctx.author.id

        if user == ctx.author.id:
            await ctx.send(f'{self.bot.no} **You cannot unsubscribe from your own channels.**')
            return

        channels = await self.database.get_channel(user)

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **This user doesn't have a channel.**")
            return

        if len(channels) == 1:
            channel_index = 0
        elif len(channels) > 1:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        status = await self.database.remove_subscriber(author, channels[channel_index][1])

        if status == 'Subscription doesn\'t exist':
            await ctx.send(f'{self.bot.no} **You are not subscribed to this channel.** You can\'t '
                           f'unsubscribe from a channel you were never subscribed to.')
            return

        subscribed_embed = discord.Embed(
            description=f'{self.bot.yes} Successfully subscribed to **{channels[channel_index][2]}** '
                        f'<@{channels[channel_index][0]}>',
            color=self.bot.embed)

        await ctx.send(embed=subscribed_embed)

    @commands.command(
        aliases=['u', 'p'],
        usage='``-profile {user}``',
        help='Shows the profile of the user.')
    async def profile(self, ctx, user: discord.User = None):

        if not user:
            user = ctx.author
            user_id = ctx.author.id
        else:
            user_id = user.id

        user_details = await self.database.get_user(user_id)

        if user_details == 'User doesn\'t exist':
            await ctx.send(f'{self.bot.no} **This user is not vidio.**')
            return

        description = f'<@{user_details[0]}>\n' \
                      f'**Money:** ``${user_details[1]}``'

        channels = await self.database.get_channel(user_id)

        if channels == "Channel doesn't exist":
            channels = None
        else:
            description += '\n\n **Channels**\n'
            for channel in channels:
                description += f'• {channel[2]} | ``{channel[4]} subscribers``\n'

        user_embed = discord.Embed(
            title=user.name+user.discriminator,
            description=description,
            color=self.bot.embed)

        user_embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=user_embed)

    @commands.group(
        aliases=['shop', 'buy'],
        usage='``-store``',
        help='Lists the things you can buy.')
    async def store(self, ctx):

        if ctx.invoked_subcommand is None:

            channels = await self.database.get_channel(ctx.author.id)

            if len(channels) == 1:
                channel_index = 0
            elif len(channels) > 1:
                channel_index = await self.multi_channels(ctx, channels)

            if channel_index is False:
                return

            store_embed = discord.Embed(
                title='vidio store',
                description=f'Buy some cheats! Use ``{ctx.prefix}buy {{index}}`` to buy what you want.',
                color=self.bot.embed
            )

            store_embed.add_field(
                name='1. Decent Advertisement',
                value=f'Costs ``${3 * math.ceil(channels[channel_index][4])}`` | ``{ctx.prefix}buy 1``',
                inline=False
            )

            store_embed.add_field(
                name='2. Average Advertisement',
                value=f'Costs ``${1 * math.ceil(channels[channel_index][4])}`` | ``{ctx.prefix}buy 2``',
                inline=False
            )

            store_embed.add_field(
                name='3. Sub Bot',
                value=f'Costs ``$5 / sub`` | ``{ctx.prefix}buy 3 {{subscribers}}``'
            )

            store_embed.set_footer(text='Note: The prices keep changing as your channel grows.')

            await ctx.send(embed=store_embed)

    @store.command(
        aliases=['1'],
        usage='``-buy 1``',
        help='Purchases a decent advertisement.')
    async def decent_ad(self, ctx):

        user_id = ctx.author.id
        channels = await self.database.get_channel(user_id)

        if len(channels) == 1:
            channel_index = 0
        else:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        channel_id = channels[channel_index][1]

        status = await self.database.buy_average_ad(user_id, channel_id)
        if status == 'Not enough money':
            await ctx.send(f'{self.bot.no} **You do not have enough money to buy a decent advertisement. **'
                           f'An average advertisement costs ``${channels[channel_index][4]}``.')
            return

        await ctx.send(f'**{self.bot.yes} Successfully bought a decent advertisement.** '
                       f'You got ``{status["new_subs"]}`` new subscribers and it costed $``{status["cost"]}``')

    @store.command(
        aliases=['2'],
        usage='``-buy 2``',
        help='Purchases a average advertisement.')
    async def average_ad(self, ctx):

        user_id = ctx.author.id
        channels = await self.database.get_channel(user_id)

        if len(channels) == 1:
            channel_index = 0
        else:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        channel_id = channels[channel_index][1]

        status = await self.database.buy_average_ad(user_id, channel_id)
        if status == 'Not enough money':
            await ctx.send(f'{self.bot.no} **You do not have enough money to buy an average advertisement.**'
                           f'An average advertisement costs {channels[channel_index][4]}.')
            return

        await ctx.send(f'**{self.bot.yes} Successfully bought an average advertisement.** '
                       f'You got ``{status["new_subs"]}`` new subscribers and it costed $``{status["cost"]}``')

    @store.command(
        aliases=['3'],
        usage='``-buy 3``',
        help='Buys subbot - input subscribers')
    async def subbot(self, ctx, subscriber_amount: int):

        user_id = ctx.author.id
        channels = await self.database.get_channel(user_id)

        if len(channels) == 1:
            channel_index = 0
        else:
            channel_index = await self.multi_channels(ctx, channels)

        if channel_index is False:
            return

        channel_id = channels[channel_index][1]

        status = await self.database.buy_subbot(user_id, channel_id, subscriber_amount)

        if status == 'Not enough money':
            await ctx.send(f'{self.bot.no} **You do not have enough money to buy a subbot.**'
                           f'``{subscriber_amount}`` subscribers would cost ``${subscriber_amount * 5}``')
            return

        await ctx.send(f'**{self.bot.yes} Successfully bought subbot.** '
                       f'You got ``{status["new_subs"]}`` new subscribers and it costed $``{status["cost"]}``')

    @commands.command(
        aliases=['how'],
        usage='``-command``',
        help='Sends a basic tutorial to use the bot.')
    async def tutorial(self, ctx):

        tutorial_embed = discord.Embed(
            title='vidio tutorial',
            color=self.bot.embed)

        tutorial_embed.add_field(
            name='**what is vidio?**',
            value=f'**vidio** is a *new* discord bot that allows you to create a simulation of a *YouTube Channel* '
                  'on Discord! It\'s a simulation game that allows you to manage your very own **virtual '
                  'youtube channel**! *Upload videos, earn money and find your way through the leaderboard!*',
            inline=False
        )

        tutorial_embed.add_field(
            name='**how do I get started?**',
            value=f'to start your youtube simulation journey, you need to first create a channel. '
                  f'You can do that with ``{ctx.prefix}create_channel``. Read the prompts and enter '
                  f'your channel name, description and category. Once you\'ve created your channel, '
                  f'you\'re ready to go! *Note: You can create a maximum of 3 channels.*',
            inline=False
        )

        tutorial_embed.add_field(
            name='**uploading videos**',
            value=f'you can upload videos on a channel once an hour. Use ``{ctx.prefix}upload`` to upload '
                  f'a video. Follow the prompts and then the bot is going to send an embed showing you how '
                  f'your video did! *Note: the statistics(subscribers, views, likes, dislikes, money) of '
                  f'your video will continue changing for the next 5 days.*',
            inline=False
        )

        tutorial_embed.add_field(
            name='**other commands**',
            value=f'now, as you\'ve got a hang on the basics of operating **vidio**! '
                  f'Before you go around streaming, here are a few fun commands you should know about -\n'
                  f'• ``{ctx.prefix}help`` - Shows you a list of all the commands that you can use.\n'
                  f'• ``{ctx.prefix}channel``  - Shows you information about your channel.\n'
                  f'• ``{ctx.prefix}profile`` - Shows you information about your **vidio** account.\n',
            inline=False
        )

        await ctx.send(embed=tutorial_embed)


def setup(bot):
    bot.add_cog(Vidio(bot))
