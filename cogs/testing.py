""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class Testing(commands.Cog, name="testing"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member) -> None:
        """
        This event is triggered when a member joins a guild.

        :param member: The member that joined the guild.
        """
        if member.guild.id == 737710058431053836:
            print(f"{member.display_name} joined the guild.")

    @commands.command(
        name="trigger_on_member_join",
        description="Triggers the on_member_join event.",
        aliases=["tomj"],
    )
    @commands.is_owner()
    async def trigger_on_member_join(self, context: Context, member_id: int) -> None:
        """
        Triggers the on_member_join event.

        :param context: The command context.
        :param member_id: The ID of the member to trigger the event with.
        """
        member = await context.guild.fetch_member(member_id)
        await self.on_member_join(member)

    @commands.command(
        name="templ",
        description="This is a testing command that does nothing.",
    )
    async def templ(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        await context.send(f"Hello {context.author.mention}! :3")  # <a:hyper:754213547000725504>


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Testing(bot))
