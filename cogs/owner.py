""""
otto bot
Copyright © hi_skittles 2024
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

import time

import discord
from discord import app_commands, Message
from discord.ext import commands
from discord.ext.commands import Context

from utils.botlogger import Logs as BotLogger


# TODO: log and owner 'stuffs' in primary channel please
class Owner(commands.Cog, name="developer"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="guilds",
        description="List all guilds the bot is in.",
    )
    @commands.is_owner()
    async def list_guilds(self, context: Context) -> None:
        """
        List all guilds the bot is in.

        :param context: The command context.
        """
        guilds = self.bot.guilds
        guilds_list = "\n".join([f"{guild.name} - {guild.id}" for guild in guilds])
        await context.send(f"```{guilds_list}```")

    @commands.hybrid_command(
        name="ping",
        description="Gives self.bot.latency.",
    )
    @commands.has_guild_permissions(administrator=True)
    async def ping(self, context: Context) -> None:
        """
        Hello?

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Hello. Latency is, **{round(self.bot.latency * 1000)}**ms.",
            color=discord.Color.dark_blue()
        )
        await context.send(embed=embed)

    @commands.command(
        name="sync",
        description="Synchronizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchronizes  slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized.",
                color=discord.Color.dark_blue(),
            )
            await context.send(embed=embed)
            await BotLogger.log_primary_simple(bot=self.bot, title="Global Sync",
                                               description="Slash commands have been globally synchronized.")
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synchronized in this guild.",
                color=discord.Color.dark_blue(),
            )
            await context.send(embed=embed)
            await BotLogger.log_primary_simple(bot=self.bot, title="Guild Sync",
                                               description="Slash commands have been locally synchronized in "
                                                           f"{context.guild.name}.")
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=discord.Color.dark_red()
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Desynchronizes the slash commands.",
    )
    @app_commands.describe(
        scope="The scope of the sync. Can be `global`, `current_guild` or `guild`"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Desynchonizes slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally desynchronized.",
                color=discord.Color.dark_blue(),
            )
            await context.send(embed=embed)
            await BotLogger.log_primary_simple(bot=self.bot, title="Global Desync",
                                               description="Slash commands have been globally desynchronized.")
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been desynchronized in this guild.",
                color=discord.Color.dark_blue(),
            )
            await context.send(embed=embed)
            await BotLogger.log_primary_simple(bot=self.bot, title="Global Desync",
                                               description="Slash commands have been locally desynchronized in "
                                                           f"{context.guild.name}.")
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=discord.Color.dark_red()
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                description=f"{cog}: {e}", color=discord.Color.dark_red()
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully loaded the `{cog}` cog.", color=discord.Color.dark_blue()
        )
        await BotLogger.log_primary_simple(bot=self.bot, title="Cog",
                                           description=f"Loaded the `{cog}` cog.")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not unload the `{cog}` cog.", color=discord.Color.dark_red()
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully unloaded the `{cog}` cog.", color=discord.Color.dark_blue()
        )
        await BotLogger.log_primary_simple(bot=self.bot, title="Cog",
                                           description=f"Unloaded the `{cog}` cog.")
        await context.send(embed=embed)

    # TODO: log any reloading in primary channel
    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except commands.ExtensionNotFound:
            embed = discord.Embed(description=f"Could not find the `{cog}` cog.", color=discord.Colour.dark_red())
            await context.send(embed=embed)
            return
        except commands.ExtensionNotLoaded:
            embed = discord.Embed(description=f"Could not load the `{cog}` cog. It may not exist.",
                                  color=discord.Colour.dark_red())
            await context.send(embed=embed)
            return
        except Exception as e:
            embed = discord.Embed(
                description=f"Could not reload the `{cog}` cog.\nSee exception: {e}",
                color=discord.Color.dark_red(),
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully reloaded the `{cog}` cog.", color=discord.Color.teal()
        )
        await BotLogger.log_primary_simple(bot=self.bot, title="Cog",
                                           description=f"Reloaded the `{cog}` cog.")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

    @commands.hybrid_command(
        name="status",
        description="Manually change the bot's status.",
    )
    @app_commands.describe(message="The message that should be the bot's status")
    @commands.is_owner()
    async def status(self, context: Context, *, message: str) -> Message:
        """
        Change the bot's status.

        :param context: The hybrid command context.
        :param message: The message that should be the bot's status.
        """
        try:
            await self.bot.change_presence(activity=discord.Game(name=message))
        except Exception as e:
            embed = discord.Embed(
                description=f"Could not change the bot's status."
                            f"\nException: {e}",
                color=discord.Color.brand_red(),
            )
            return await context.send(embed=embed)
        embed = discord.Embed(
            description=f"The bot's status has been changed to `{message}`.",
            color=discord.Color.dark_gray(),
        )
        await BotLogger.log_primary_simple(bot=self.bot, title="Status Change",
                                           description=f"Status has been manually changed to `{message}` "
                                                       f"by {context.author}.")
        await context.send(embed=embed)

    @commands.hybrid_group(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    @commands.is_owner()
    async def blacklist(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(description="You need to specify a subcommand.\n\n**Subcommands:**\n`add` - Add a"
                                              "user to the blacklist.\n`remove` - Remove a user from the blacklist.",
                                  color=discord.Colour.dark_red(),)
            await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="show",
        description="Shows the list of all blacklisted users.",
    )
    @commands.is_owner()
    async def blacklist_show(self, context: Context) -> None:
        """
        Shows the list of all blacklisted users.

        :param context: The hybrid command context.
        """
        blacklisted_users = await self.bot.internal_bot_settings.get_blacklisted_users(False)
        if len(blacklisted_users) == 0:
            embed = discord.Embed(description="There are currently no blacklisted users.",
                                  color=discord.Colour.blurple())
            await context.send(embed=embed)
            return

        if blacklisted_users[0] == ["error"]:
            embed = discord.Embed(description=f"An error occurred while getting the blacklisted users.\n"
                                              f"{blacklisted_users[1]}",
                                  color=discord.Colour.dark_red())
            await context.send(embed=embed)
            return

        embed = discord.Embed(title="Blacklisted Users", color=discord.Colour.blue())
        users = []
        for bluser in blacklisted_users:
            user = self.bot.get_user(int(bluser[0])) or await self.bot.fetch_user(int(bluser[0]))
            users.append(f"• {user.mention} ({user}) - Blacklisted <t:{bluser[3]}>")
        embed.description = "\n".join(users)
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="add",
        description="Lets you add a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be added to the blacklist")
    @commands.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        Lets you add a user from not being able to use the bot.

        :param context: The hybrid command context.
        :param user: The user that should be added to the blacklist.
        """
        user_id = user.id
        if await self.bot.internal_bot_settings.is_blacklisted(user_id):
            embed = discord.Embed(description=f"**{user.name}** is already in the blacklist.",
                                  color=discord.Colour.dark_red(),)
            await context.send(embed=embed)
            return
        total = await self.bot.internal_bot_settings.add_user_to_blacklist(user_id, user.name, int(time.time()), None)
        embed = discord.Embed(description=f"**{user.name}** has been successfully added to the blacklist",
                              color=discord.Colour.green())
        embed.set_footer(text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} "
                              f"in the blacklist")
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be removed from the blacklist.")
    @commands.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User) -> None:
        """
        Lets you remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        :param user: The user that should be removed from the blacklist.
        """
        user_id = user.id
        if not await self.bot.internal_bot_settings.is_blacklisted(user_id):
            embed = discord.Embed(description=f"**{user}** is not in the blacklist.", color=discord.Colour.dark_red())
            await context.send(embed=embed)
            return
        total = await self.bot.internal_bot_settings.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** has been successfully removed from the blacklist",
            color=discord.Colour.green(),
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} "
                 f"in the blacklist"
        )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
