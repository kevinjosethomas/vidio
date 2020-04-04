import locale
import asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class VideoCord(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog('Database')

    @commands.command(
        aliases=['cc'],
        usage='``-create_channel``',
        help='A simple command that creates a channel for you.')
    async def create_channel(self, ctx):

        channels = await self.database.get_channel(ctx.author.id)

        if channels == "Channel doesn't exist":
            channels = None
        elif len(channels) >= 3:
            await ctx.send(
                f"{self.bot.no} **You cannot create more than 3 channels.**")
            return

        def author_check(msg):
            return msg.author == ctx.message.author

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

            if len(name.content) > 20:
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
                           f"Check it out with ``>channel``!")
            await message.delete()


def setup(bot):
    bot.add_cog(VideoCord(bot))
