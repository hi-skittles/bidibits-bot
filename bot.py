""""
otto bot
Copyright © hi_skittles 2024
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0

Notes:
    https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
    self.bot.http.ban()
"""

import json
import logging
import os
import platform
import random
import sys
import time

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

from database import GeneralDbManager, InternalBotSettingsDbManager, ProfilesManagement

from utils.botlogger import Logs as BotLogger

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("Help! I couldn't find the 'config.json' file! Please make sure it is in the same directory as bot.py.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""

intents = discord.Intents.all()

"""
Uncomment this if you want to use prefix (normal) commands.
It is recommended to use slash commands and therefore not use prefix commands.

If you want to use prefix commands, make sure to also enable the intent below in the Discord developer portal.
"""
intents.message_content = True

# Setup both of the loggers


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The config is available using the following code:
        - self.config # In this class
        - bot.config # In this file
        - self.bot.config # In cogs
        """
        self.logger = logger
        self.config = config
        self.internal_bot_settings = None
        self.servers_database = None
        self.profiles_database = None

    # TODO profile schema
    async def init_db(self) -> None:
        async with aiosqlite.connect(
            f"{os.path.realpath(os.path.dirname(__file__))}/database/internal_bot_settings.db"
        ) as db:
            with open(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/internal_bot_settings_schema.sql"
            ) as file:
                await db.executescript(file.read())
            await db.commit()

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    @tasks.loop(minutes=15.0)
    async def status_task(self) -> None:
        """
        Set up the game status task of the bot.
        """
        statuses = ["with Maximus", "with your feelings", "with your heart", "pycharm", "not with java", "LWJGL", "Minecraft!", "90% bug free", "Euclidian", "OpenGL 1.2", "not Spock", "sqrt(-1)", "[] == []", "20 GOTO 10", "[[]] lines of code!", "OICU812", "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch", "Llanfairpwllgwyngyll", "Jason!", "idspispopd", "Stop This Flame (MK edit)"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
        await self.init_db()
        await self.load_cogs()
        self.status_task.start()
        self.internal_bot_settings = InternalBotSettingsDbManager(
            connection=await aiosqlite.connect(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/internal_bot_settings.db"
            )
        )
        self.servers_database = GeneralDbManager(
            connection=await aiosqlite.connect(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/servers.db"
            )
        )
        self.profiles_database = ProfilesManagement(
            connection=await aiosqlite.connect(
                f"{os.path.realpath(os.path.dirname(__file__))}/database/profiles.db"
            )
        )

    async def on_message(self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if (await bot.internal_bot_settings.is_blacklisted(message.author.id)
                or message.author == self.user or message.author.bot):
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by "
                f"{context.author} (ID: {context.author.id})"
            )
            await BotLogger.log_debug(self, context, split, False)
        else:
            self.logger.info(f"Executed {executed_command} command by {context.author} "
                             f"(ID: {context.author.id}) in DMs")

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in "
                            f"{f'{round(hours)} hours' if round(hours) > 0 else ''} "
                            f"{f'{round(minutes)} minutes' if round(minutes) > 0 else ''} "
                            f"{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=discord.Color.dark_red(),
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="huh", color=discord.Color.dark_red()
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild "
                    f"{context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the "
                    f"bot's DMs, but the user is not an owner of the bot."
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="Looks like *you* aren't setup to perform that command. You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command",
                color=discord.Color.dark_red(),
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRole):
            pass
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="Looks like I'm not setup to perform that task. I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command.",
                color=discord.Color.dark_red(),
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="MissingRequiredArgument",
                description=str(error),  # .capitalize(),
                color=discord.Color.brand_red(),
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                description="Not sure about that one. Try /help.", color=discord.Color.dark_red()
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            timestamp = time.time()
            embed = discord.Embed(
                description="An internal error occurred while executing the command.\n"
                            f"Error ID: `{timestamp}`",
                color=discord.Color.dark_red(),
            )
            await context.send(embed=embed, ephemeral=True)
            await BotLogger.log_critical_simple(self, str(int(timestamp)), f"An error occurred while executing a command: {error}\n", discord.Colour.brand_red())
        else:
            raise error


load_dotenv()

bot = DiscordBot()
bot.run(os.getenv("TOKEN"))
