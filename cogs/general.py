""""
otto bot
Copyright © hi_skittles 2024
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

import platform

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from utils.botlogger import Logs as BOTLOGGER
from utils.definitions import Customs

from utils.definitions import Statics as definitions


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
            await BOTLOGGER.log_debug(self.bot, ctx, command_or_action, True)

        # TODO: implement this better!! add custom options for each guild. good foundation =)
        # if message.guild.id == 737710058431053836:
        #     if message.channel.id == 737713464755224586:
        #         if re.search(r"discord.gg", message.content):
        #             await message.delete()
        #             await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in "
        #                                        f"this channel.")

    #  ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
    # ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
    # ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
    # ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
    # ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
    #  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝

    @commands.hybrid_command(
        name="online_members",
        description="Display the first 20 online members with access to the channel.",
        aliases=["om"],
    )
    async def online_members(self, ctx):
        """
        Display the first 20 online members with access to the channel.

        :param ctx: The command context.
        """
        members_with_access = [member for member in ctx.guild.members if
                               ctx.channel.permissions_for(member).read_messages]

        online_members = [member for member in members_with_access if member.status == discord.Status.online]

        online_members = online_members[:20]

        if online_members:
            online_members_str = "\n".join([member.display_name for member in online_members])
            embed = discord.Embed(title="Online Members", description=online_members_str,
                                  colour=discord.Colour.dark_blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send("No online members with access to this channel.")

    @commands.hybrid_command(
        name="pinit",
        description="Pin the last message in the current channel or the last message from a specified user.",
        aliases=["pin", "p"],
    )
    @commands.guild_only()
    @app_commands.describe(
        user="The user to pin the last message from. Can only go back 100 messages.",
        delete_my_response="Whether or not to delete the bots response; kinda gimmicky.",
    )
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def pinit(self, context: Context, *, user: discord.User = None, delete_my_response: bool = False) -> None:
        """
        Pin the last message in the current channel or the last message from a specified user.
        https://discordpy.readthedocs.io/en/stable/api.html?highlight=history#discord.TextChannel.history

        :param context: The command context.
        :param user: Optional argument, a user mention or ID.
        :param delete_my_response: Whether or not to delete the bots response; gimmicky.
        """
        if user is None:
            try:
                #  hacky?
                last_message = [message async for message in context.channel.history(limit=2, before=context.message)]
            except discord.Forbidden:
                embed = discord.Embed(description="I don't have permission to do that. I require the"
                                                  "`Read Message History` permission.",
                                      colour=discord.Colour.brand_red())
                await context.send(embed=embed)
                return
            except discord.HTTPException as _:
                embed = discord.Embed(description=f"An error occurred while fetching the message.\n{_}",
                                      colour=discord.Colour.brand_red())
                await context.send(embed=embed)
                return
        else:
            try:
                last_message = [message async for message in context.channel.history(limit=100, before=context.message)
                                if message.author == user]
            except discord.Forbidden:
                embed = discord.Embed(description="I don't have permission to do that. I require the"
                                                  "`Read Message History` permission.",
                                      colour=discord.Colour.brand_red())
                await context.send(embed=embed)
                return
            except discord.HTTPException as _:
                embed = discord.Embed(description=f"An error occurred while fetching the message.\n{_}",
                                      colour=discord.Colour.brand_red())
                await context.send(embed=embed)
                return

        if last_message[0]:
            await last_message[0].pin()
            embed = discord.Embed(description=f"I've pinned the last message by "
                                              f"{last_message[0].author.mention}.",
                                  colour=discord.Colour.dark_blue())
            response = await context.send(embed=embed)
            if delete_my_response:
                await response.delete(delay=15)

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            description="List of available commands:", color=discord.Color.dark_blue()
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
        Bot information.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Otto is a multifunctional profile-bot aimed at creating an inclusive server environment for "
                        "role-playing servers. ",
            color=discord.Colour.og_blurple(),
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="hi_skittles", inline=True)
        embed.add_field(name="Python Version:", value=f"{platform.python_version()}", inline=True)
        embed.add_field(name="Bot version:", value=lambda version_file: open("./version", "r").read().strip(),
                        inline=True)
        embed.add_field(
            name="Prefix:",
            value=f"I can support slash commands or legacy text commands via the `{self.bot.config['prefix']}` prefix.",
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

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=discord.Color.dark_blue()
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="embed",
        description="Say something in a description only embed.",
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
        description="Send a full embed with title, description, colour and footer.",
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
        Sends a full embed.

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
