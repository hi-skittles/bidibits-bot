import discord
from discord.ext import commands
from discord.ext.commands import Context

guild_id = 737710058431053836


class Channels:
    @staticmethod
    def primary_channel(bot: commands.Bot, ctx: Context, command_ctx: str or list[str]):
        pass

    @staticmethod
    def debug_channel(bot: commands.Bot, ctx: Context, command_ctx: str or list[str]):
        channel_id = 1200487702240440391

        guild = bot.get_guild(guild_id)
        if not guild:
            return print(f"CRITICAL: Failed to get guild with ID {guild_id}. Could not send log message. Stopping.")

        channel = guild.get_channel(channel_id)
        if not channel:
            return print(f"CRITICAL: Failed to get channel with ID {channel_id}. Could not send log message. Stopping.")

        if len(command_ctx) > 1:
            command_ctx = "/" + " ".join(command_ctx)

        embed = discord.Embed(
            title="Debug Log",
            description=f"**Command:** {command_ctx}\n"
                        f"**User:** {ctx.author.mention}\n"
                        f"**Guild:** {ctx.guild} ({ctx.guild.id})\n"
                        f"**Channel:** {ctx.channel.mention}",
            color=discord.Color.dark_blue(),
        )
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.timestamp = ctx.message.created_at

        return channel.send(embed=embed)


class Dev:
    @staticmethod
    def primary_log(bot: commands.Bot, ctx: Context, command_ctx: str):
        log = Channels.primary_channel(bot, ctx, command_ctx)
        return log

    @staticmethod
    def debug_log(bot: commands.Bot, ctx: Context, command_ctx: str):
        log = Channels.debug_channel(bot, ctx, command_ctx)
        return log

    @staticmethod
    def critical_log(bot: commands.Bot, ctx: Context, command_ctx: str):
        pass
