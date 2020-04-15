import locale
import asyncio
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from discord.ext.commands.cooldowns import BucketType


class VideoCord(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    @commands.command(
        aliases=['cc'],
        usage='``-create_channel``',
        help='A simple command that creates a channel for you.')
    @commands.cooldown(1, 10, BucketType.user)
    async def create_channel(self, ctx):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild

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
                   'how you want it to be. Only ``alphabets``, ``digits``, ' \
                   '``punctuation`` and ``whitespaces`` are allowed. ' \
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
                          'about your channel! Only ``alphabets``, ``digits``, ' \
                          '``punctuation`` and ``whitespaces`` are allowed. ' \
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

        if query == 'Bad arguments.':
            await ctx.send(f"{self.bot.no} **Error.** Please make "
                           "sure your entries only have alphabets, numbers, punctuation "
                           "and spaces.")
            await message.delete()
            return

        elif query == 'Channel with same name exists':
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

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild

        if user is None:
            user = ctx.author.id

        if isinstance(user, discord.User):
            user = user.id

        channels = await self.database.get_channel(user)

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **This user doesn't have a channel.**")
            return

        elif len(channels) == 1:
            name = channels[0][2]
            description = channels[0][3]
            subs = channels[0][4]
            total_views = channels[0][5]
            category = channels[0][6]
            created_at = channels[0][7]
            date = f'{created_at.strftime("%B")} {created_at.strftime("%d")}, {created_at.strftime("%Y")}'

        elif len(channels) > 1:

            message = f"{self.bot.youtube} **This user has multiple channels.** Use the index (number) given" \
                      f" to the channels in the list below to choose which channel you want to see.\n"

            for channel in channels:
                message += f"• ``{channels.index(channel)+1}.`` {channel[2]}\n"

            message += "\n To cancel channel search, simply type ``cancel``."

            while True:
                await ctx.send(message)
                channel_index = await self.bot.wait_for('message', check=author_check, timeout=120)

                if channel_index.content.lower() == 'cancel':
                    await ctx.send(f'{self.bot.yes} **Successfully canceled channel search process...**')
                    return

                try:
                    if int(channel_index.content) > 3:
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

            name = channels[channel_index][2]
            description = channels[channel_index][3]
            subs = channels[channel_index][4]
            total_views = channels[channel_index][5]
            category = channels[channel_index][6]
            created_at = channels[channel_index][7]
            date = f'{created_at.strftime("%B")} {created_at.strftime("%d")}, {created_at.strftime("%Y")}'

        user = self.bot.get_user(user)

        subs = locale.format_string("%d", subs, grouping=True)
        total_views = locale.format_string("%d", total_views, grouping=True)

        yt_embed = discord.Embed(
            title=f'**{name}**',
            description=f'{self.bot.subscribers} **Subscribers:** {subs}\n'
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
        aliases=['u'],
        usage='``-upload``',
        help='A command that uploads a video on the author\'s channel.')
    @commands.cooldown(1, 10, BucketType.user)
    async def upload(self, ctx):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild

        channels = await self.database.get_channel(ctx.author.id)

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **You don't have a channel.** You must create a channel to upload videos.")
            return

        if len(channels) > 1:

            message = f"{self.bot.youtube} **You have multiple channels.** Use the index (number) given" \
                      f" to the channels in the list below to choose which channel you want to upload to.\n"

            for channel in channels:
                message += f"• ``{channels.index(channel)+1}.`` {channel[2]}\n"

            message += "\n To cancel video upload, simply type ``cancel``."

            while True:
                await ctx.send(message)
                channel_index = await self.bot.wait_for('message', check=author_check, timeout=120)

                if channel_index.content.lower() == 'cancel':
                    await ctx.send(f'{self.bot.yes} **Successfully canceled channel search process...**')
                    return

                try:
                    if int(channel_index.content) > 3 or int(channel_index.content) < 1:
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

        else:
            channel_index = 0

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
                    '**Your video name must not exceed 50 characters. **' \
                    'Only ``alphabets``, ``digits``, ``punctuation`` ' \
                    'and ``whitespaces`` are allowed.\n\n' \
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
                          'for your video! Only ``alphabets``, ``digits``, ' \
                          '``punctuation`` and ``whitespaces`` are allowed. ' \
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

        if video == 'Bad Arguments':
            await ctx.send(f"{self.bot.no} **Error.** Please make sure your "
                           "entries only have alphabets, numbers, punctuation and spaces.")
            await message.delete()
            return

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        status = video['status']
        channel_name = video['channel']
        new_subs = locale.format_string('%d', video['new_subs'], grouping=True)
        views = locale.format_string('%d', video['views'], grouping=True)
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
                        f'{self.bot.views} **Views:** {views}\n\n'
                        f'{self.bot.likes} **Likes:** {likes}\n'
                        f'{self.bot.dislikes} **Dislikes:** {dislikes}\n\n'
                        f'{self.bot.description} **Description:** {description}',
            color=self.bot.embed)

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

    @commands.command(
        aliases=['lb'],
        usage='``-leaderboard``',
        help='Returns the 10 people with the most subscribers.')
    async def leaderboard(self, ctx):

        lb = await self.database.get_leaderboard()

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        desc = ''
        pos = 1

        for entry in lb:
            desc += f'{pos}. ``{locale.format_string("%d", entry[2], grouping=True)} ' \
                    f'subs`` {self.bot.subscribers} {entry[1]} - <@{entry[0]}>\n'
            pos += 1

        lb_embed = discord.Embed(
            title='vloger subscriber leaderboard',
            description=desc,
            color=self.bot.embed)

        await ctx.send(embed=lb_embed)

    @commands.command(
        aliases=['v'],
        usage='``-video``',
        help='A command that (inaccurately) searches for videos uploaded on your channel.')
    async def video(self, ctx, video_name):

        def author_check(msg):
            return msg.author == ctx.message.author and ctx.guild == msg.guild

        channels = await self.database.get_channel(ctx.author.id)

        if channels == "Channel doesn't exist":
            await ctx.send(f"{self.bot.no} **You don't have a channel.** You must create a channel to upload videos.")
            return

        if len(channels) > 1:

            message = f"{self.bot.youtube} **You have multiple channels.** Use the index (number) given" \
                      f" to the channels in the list below to choose which channel you want to upload to.\n"

            for channel in channels:
                message += f"• ``{channels.index(channel)+1}.`` {channel[2]}\n"

            message += "\n To cancel video upload, simply type ``cancel``."

            while True:
                await ctx.send(message)
                channel_index = await self.bot.wait_for('message', check=author_check, timeout=120)

                if channel_index.content.lower() == 'cancel':
                    await ctx.send(f'{self.bot.yes} **Successfully canceled channel search process...**')
                    return

                try:
                    if int(channel_index.content) > 3 or int(channel_index.content) < 1:
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

        else:
            channel_index = 0

        channel_id = channels[channel_index][1]

        videos = await self.database.get_video(channel_id, video_name)

        if videos == 'No videos':
            await ctx.send(f'{self.bot.no} **Unknown video.** Could not find a video with that name on videonet.')
            return

        description = ''


        for video in videos:
            description += f'• {video[2]}'

        if len(description) > 2043:
            description = description[:2043]

        videos_embed = discord.Embed(
            title=f'We found ``{len(videos)}`` video(s) related to ``{video_name}``',
            description=description)

        await ctx.send(embed=videos_embed)


def setup(bot):
    bot.add_cog(VideoCord(bot))
