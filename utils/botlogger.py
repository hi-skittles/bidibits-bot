import discord
from discord.ext import commands
from discord.ext.commands import Context

#  f"{value_if_true if condition else value_if_false}"
guild_id = 737710058431053836


class Channels:
    # TODO
    @staticmethod
    def primary_channel(bot: commands.Bot, ctx: Context, command_or_action: list[str] or str, is_action: bool,
                        log_content: str, colour_override: discord.Colour = None):
        channel_id = 1200487447017046156

        try:
            guild = bot.get_guild(guild_id)
        except Exception:
            return print(f"CRITICAL: Failed to get guild with ID {guild_id}. Could not send log message. Stopping.")

        try:
            channel = guild.get_channel(channel_id)
        except Exception:
            return print(f"CRITICAL: Failed to get channel with ID {channel_id}. Could not send log message. Stopping.")

        if isinstance(command_or_action, list):  # and all(isinstance(item, str) for item in command_or_action):
            command_or_action = " ".join(command_or_action)

        embed = discord.Embed(
            title=f"{f'/{command_or_action}' if is_action is False else f'Action {command_or_action}'}: "
                  f"{ctx.author.global_name}",
            description=log_content,
            color=discord.Color.dark_blue() if colour_override is None else colour_override,
        )
        embed.add_field(name="User", value=ctx.author.mention, inline=True)
        embed.add_field(name="Guild", value=f"{ctx.guild} ({ctx.guild.id})", inline=True)
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.timestamp = ctx.message.created_at

        return channel.send(embed=embed)

    @staticmethod
    def debug_channel(bot: commands.Bot, ctx: Context, command_or_action: list[str] or str, is_action: bool):
        channel_id = 1200487702240440391

        guild = bot.get_guild(guild_id)
        if not guild:
            return print(f"CRITICAL: Failed to get guild with ID {guild_id}. Could not send log message. Stopping.")

        channel = guild.get_channel(channel_id)
        if not channel:
            return print(f"CRITICAL: Failed to get channel with ID {channel_id}. Could not send log message. Stopping.")

        if isinstance(command_or_action, list):  # and all(isinstance(item, str) for item in command_or_action):
            command_or_action = " ".join(command_or_action)

        embed = discord.Embed(
            title="Debug Log",
            #  f"{value_if_true if condition else value_if_false}"
            #  this seems to be an issue with python 3.11 or something.
            #  trying to format this line just breaks everything. whatever.
            description=f"{f'**Command:** /{command_or_action}' if is_action is False else f'**Action:** {command_or_action}'}\n**User:** {ctx.author.mention}\n**Guild:** {ctx.guild} ({ctx.guild.id})\n**Channel:** {ctx.channel.mention}",
            color=discord.Color.dark_blue(),
        )
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.timestamp = ctx.message.created_at

        return channel.send(embed=embed)

    # TODO
    @staticmethod
    def critical_channel(bot: commands.Bot, ctx: Context, command_or_action: list[str] or str, is_action: bool):
        pass


class Dev:
    # TODO
    @staticmethod
    def log_primary(bot: commands.Bot, ctx: Context, command_or_action: list[str] or str, is_action: bool, log_content: str,
                    colour_override: discord.Color = None):
        if log_content is None:
            log_content = "*👀 No info was entered for this log...*"
        log = Channels.primary_channel(bot, ctx, command_or_action, is_action, log_content, colour_override)
        return log

    @staticmethod
    def log_debug(bot: commands.Bot, ctx: Context, command_or_action: list[str] or str, is_action: bool):
        log = Channels.debug_channel(bot, ctx, command_or_action, is_action)
        return log

    # TODO
    @staticmethod
    def log_critical(bot: commands.Bot, ctx: Context, command_or_action: list[str] or str, is_action: bool):
        log = Channels.critical_channel(bot, ctx, command_or_action, is_action)
        return log
