""""
otto bot
Copyright © hi_skittles 2024
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

from discord.ext import commands


class Template(commands.Cog, name="template"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="foo",
        description="bar",
    )
    async def foo(self, context) -> None:
        await context.send("bar")


async def setup(bot) -> None:
    await bot.add_cog(Template(bot))
