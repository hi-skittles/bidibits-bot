""""
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

import platform
import random
import re

import aiohttp
import discord
from discord import app_commands
from discord.app_commands import TransformerError
from discord.ext import commands
from discord.ext.commands import Context

from utils.definitions import Customs
from utils.botlogger import Dev as BOTLOGGER


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        # self.context_menu_user = app_commands.ContextMenu(
        #     name="User ID", callback=self.grab_id
        # )
        # self.bot.tree.add_command(self.context_menu_user)
        # self.context_menu_message = app_commands.ContextMenu(
        #     name="Remove spoilers", callback=self.remove_spoilers
        # )
        # self.bot.tree.add_command(self.context_menu_message)

    # ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
    # ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
    # █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
    # ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
    # ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
    # ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message) -> None:
        """
        Universal general message triggers. Stuff that doesn't have any particular category, or is bundled with QoL
        stuff, will appear here.

        :param message: Message object.
        """
        ctx = await self.bot.get_context(message)
        if message.author.bot or message.content.startswith(self.bot.config["prefix"]):
            return
        is_twitter, twitter_username, twitter_status_id = Customs.has_twitter_link(message.content)  # !!
        if is_twitter:
            build = f"https://fxtwitter.com/{twitter_username}/status/{twitter_status_id}"
            await message.channel.send(build)
            command_or_action = f"Twitter Embed\n**Contents:** {build}"
            await BOTLOGGER.debug_log(self.bot, ctx, command_or_action, True)

        # TODO: implement this better!! add custom options for each guild. good foundation =)
        # if message.guild.id == 737710058431053836:
        #     if message.channel.id == 737713464755224586:
        #         if re.search(r"discord.gg", message.content):
        #             await message.delete()
        #             await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in "
        #                                        f"this channel.")

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            description="List of available commands:", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Descriptive system information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Otto is a multifunctional bot designed to be helpful in a range of situations.",
            color=discord.Colour.og_blurple(),
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="hi_skittles", inline=True)
        embed.add_field(name="Python Version:", value=f"{platform.python_version()}", inline=True)
        embed.add_field(
            name="Prefix:",
            value=f"I support slash commands or the legacy prefix, `{self.bot.config['prefix']}`",
            inline=False,
        )
        embed.set_footer(text="Part of this bot uses code from Krypton's (https://krypton.ninja) template.",
                         icon_url="https://krypton.ninja/_next/image?url=%2Fstatic%2FKrypton-Avatar.png&w=96&q=75")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying [50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0xBEBEFE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Gives self.bot.latency.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Hello. Latency is, **{round(self.bot.latency * 1000)}**ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.has_guild_permissions(manage_messages=True)
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="send_embed",
        description="Sends a full embed.",
    )
    @app_commands.describe(
        title="The title of the embed",
        description="The description of the embed",
        color="The color of the embed",
        footer="The footer of the embed",
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def send_embed(
            self,
            context: Context,
            title: str,
            description: str,
            color: str = None,
            footer: str = None,
    ) -> None:
        """
        Sends a "full" embed.

        :param context: The hybrid command context.
        :param title: The title of the embed.
        :param description: The description of the embed.
        :param color: The color of the embed.
        :param footer: The footer of the embed.
        """
        try:
            if color is None:
                color = discord.Color.random()
            else:
                color = getattr(discord.Color, color)()
        except AttributeError:
            embed = discord.Embed(description=f"Seems like you provided an invalid colour..",
                                  color=discord.Color.dark_red())
            await context.send(embed=embed)
            return

        if footer is None:
            footer = f"Requested by {context.author}"

        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=footer)

        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
