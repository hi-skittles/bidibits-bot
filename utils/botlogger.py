import discord
from discord.ext import commands
from discord.ext.commands import Context

guild_id = 737710058431053836


class Channels:
    # TODO
    @staticmethod
    def primary_channel(bot: commands.Bot, ctx: Context, command_or_action: str or list[str], is_action: bool):
        pass

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
            description=f"{f'**Command:** /{command_or_action}' if is_action is False else f'**Action:** '
                                                                                          f'{command_or_action}'}\n"
                        f"**User:** {ctx.author.mention}\n"
                        f"**Guild:** {ctx.guild} ({ctx.guild.id})\n"
                        f"**Channel:** {ctx.channel.mention}",
            color=discord.Color.dark_blue(),
        )
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.timestamp = ctx.message.created_at

        return channel.send(embed=embed)

    # TODO
    @staticmethod
    def critical_channel(bot: commands.Bot, ctx: Context, command_or_action: str or list[str], is_action: bool):
        pass


class Dev:
    # TODO
    @staticmethod
    def primary_log(bot: commands.Bot, ctx: Context, command_or_action: str, is_action: bool):
        log = Channels.primary_channel(bot, ctx, command_or_action, is_action)
        return log

    @staticmethod
    def debug_log(bot: commands.Bot, ctx: Context, command_or_action: str, is_action: bool):
        log = Channels.debug_channel(bot, ctx, command_or_action, is_action)
        return log

    # TODO
    @staticmethod
    def critical_log(bot: commands.Bot, ctx: Context, command_or_action: str, is_action: bool):
        log = Channels.critical_channel(bot, ctx, command_or_action, is_action)
        return log
