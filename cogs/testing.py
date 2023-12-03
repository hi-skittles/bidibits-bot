""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
from typing import Tuple, Any

import discord
from discord.ext import commands
from discord.ext.commands import Context
import re


# Here we name the cog and create a new class for the cog.
def has_twitter_link(url: str) -> tuple[bool, str | Any, str | Any] | bool:
    """
    Checks if the given URL is a Twitter link.

    :param url: The URL to check.
    :return: True if the URL is a Twitter link, False otherwise.
    """
    twitter_regex = re.compile(r'https?://twitter\.com/(\w+)/status/(\d+)')
    # r"(https?:\/\/)?(www\.)?twitter\.com\/([a-zA-Z0-9_]+)\/status\/([0-9]+)"

    match = twitter_regex.search(url)

    if match:
        return True, match.group(1), match.group(2)
    else:
        return False, None, None


class Testing(commands.Cog, name="testing"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # ---------------
    # EVENT LISTENERS
    # ---------------

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member) -> None:
        """
        This event is triggered when a member joins a guild.

        :param member: The member that joined the guild.
        """
        if member.guild.id == 737710058431053836:
            print(f"{member.display_name} joined the guild.")

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message) -> None:
        """
        This event is triggered when a message is sent.

        :param message: The message that was sent.
        """
        if message.author.bot:
            return
        is_twitter, twitter_username, twitter_status_id = has_twitter_link(message.content)
        if is_twitter:
            await message.channel.send(f"https://fxtwitter.com/{twitter_username}/status/{twitter_status_id}")
        if message.guild.id == 737710058431053836:
            if message.channel.id == 737713464755224586:
                if re.search(r"discord.gg", message.content):
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in "
                                               f"this channel.")

    # -------------
    # -- COMMANDS -
    # -------------

    @commands.command(
        name="trigger_on_member_join",
        description="Triggers the on_member_join event.",
        aliases=["tomj"],
    )
    @commands.is_owner()
    @commands.guild_only()
    async def trigger_on_member_join(self, context: Context, member_id: int) -> None:
        """
        Triggers the on_member_join event.

        :param context: The command context.
        :param member_id: The ID of the member to trigger the event with.
        """
        member = await context.guild.fetch_member(member_id)
        await self.on_member_join(member)


async def setup(bot) -> None:
    await bot.add_cog(Testing(bot))
