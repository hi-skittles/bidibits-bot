""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
import typing
from sqlite3 import OperationalError
from typing import Tuple, Any

import discord
from discord.ext import commands
from discord.ext.commands import Context
from utils.botlogger import Dev as BotLogger

import csv
from secrets import choice
from typing import List


# Here we name the cog and create a new class for the cog.
class Testing(commands.Cog, name="testing"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
    # ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
    # █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
    # ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
    # ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
    # ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

    @commands.Cog.listener(name="on_guild_update")
    async def on_guild_update(self, before, after) -> None:
        """
        This event is triggered when a guild is updated.

        :param before: The guild before the update.
        :param after: The guild after the update.
        """
        print(f"Guild {before.name} updated.")

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member) -> None:
        """
        This event is triggered when a member joins a guild.

        :param member: The member that joined the guild.
        """
        print(f"{member.display_name} joined the (a) guild.")

    @commands.Cog.listener(name="on_guild_join")
    async def on_guild_join(self, guild) -> None:
        """
        This event is triggered when the bot joins a guild.

        :param guild: The guild the bot joined.
        """
        print(f"GUILD_JOIN_TRIGGER: {guild.name}.")

        db_simple_callback = await self.bot.servers_database.create_server_table(guild.id, guild.name)
        if db_simple_callback is False:
            print(f"Failed to create table for {guild.name}.")
        else:
            print(f"Created table for {guild.name} successfully.")

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝
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

    @commands.command(
        name="trigger_on_guild_join",
        description="Triggers the on_guild_join event.",
        aliases=["togj"],
    )
    @commands.is_owner()
    @commands.guild_only()
    async def trigger_on_guild_join(self, context: Context, server_id: int) -> None:
        """
        Triggers the on_member_join event.

        :param context: The command context.
        :param server_id: The ID of the server to trigger the event with.
        """
        try:
            server = context.bot.get_guild(server_id)
            await self.on_guild_join(server)
            await context.send(f"Joined {server.name}.")
        except AttributeError as att:
            print(f"An error occurred while fetching the server.\n{att}\n\nThis is likely because the bot isn't "
                  f"actually in the server.")
            await context.send(f"An error occurred while fetching the server. The action failed."
                               f"\n{att}\nThis is likely because the bot isn't actually in the server.")

    @commands.command(
        name="grab_data",
        aliases=["gd"],
    )
    @commands.is_owner()
    @commands.guild_only()
    async def grab_data(self, context: Context, server_id: typing.Optional[int] = None) -> None:
        """
        This command will grab data from the database.

        :param context: The command context.
        :param server_id: The ID of the server to grab the data from. If none, current server.
        """
        try:
            target_server_id = int(server_id) if server_id is not None else context.guild.id
        except ValueError as value_error:
            print(f"Error while converting server ID to integer.\n{value_error}")
            await context.send("The server ID must be an integer.")
            return
        try:
            data = await self.bot.servers_database.get_server_data(target_server_id)
        except OperationalError:
            await context.send(embed=discord.Embed(description="Server not found.", colour=discord.Colour.brand_red()))
            return
        embed = discord.Embed(title=data[0], description=f"```{data}```", colour=discord.Colour.blue())
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Testing(bot))
