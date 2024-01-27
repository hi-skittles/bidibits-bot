""""
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see:
        # https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="meow",
        description="nothing :3",
    )
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def meow(self, context: Context) -> None:
        """
        Meow :3c

        :param context: Command context.
        """
        meow_face = """
        ⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⡿⠈⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠿⡇⡀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢦⣧⡇⢰⡇⠀⠀⠀⠀⠀⠀⣾⠉⠙⠲⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣸⣿⣿⠀⣿⠀⠀⠀⠀⠀⠈⢾⣧⠀⠀⠙⢦⣂⡀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⡟⡇⠀⡏⠀⠀⠀⠀⠀⠀⠀⢻⢷⡀⠀⢀⣬⣶⡿⢠⣤⢠⣴⠶⠒⠒⠒⢦⣠⠀⠀⠀⠀⠀⠀⠀⣠⡴⠒⢶⠀⠀⠀⠀⠀⠀
⣿⡇⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣆⢾⣿⡿⣷⣿⣷⣿⣿⣱⣆⣽⡀⣼⣠⣤⣴⣶⠶⣶⣶⣾⠟⠁⠀⢸⡆⠀⠀⠀⠀⠀
⣿⡇⡇⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣷⣦⣿⣧⣼⣿⣿⣿⣼⣿⣿⡿⢳⣟⢡⣼⣿⣿⣾⣯⠞⠁⠀⠀⠀⣺⡇⠀⠀⠀⠀⠀
⣿⡿⡇⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⣻⣿⣿⣿⣯⣿⣿⡏⠘⣿⡗⣾⣿⢾⣿⣿⣿⠟⠁⠀⠀⠀⠀⠤⢶⠃⠀⠀⠀⠀⠀
⣿⡇⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢨⣿⣿⣿⣿⠋⠛⠉⠁⠀⢹⣿⣿⣇⣼⣿⡿⠏⠀⠲⢠⡴⠆⠀⠀⣸⠀⠀⠀⠀⠀⠀
⣿⡇⡗⠀⡇⠀⠀⠀⠀⠀⣀⣤⠤⠀⢀⣼⠛⠉⠛⠋⠀⠀⠀⠀⢠⣿⠙⡗⠻⡄⠁⠀⠀⠀⠚⠉⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀
⣿⣧⠃⠀⡇⠀⠀⣴⣾⣿⣿⣧⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⢷⣦⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠸⢧⡀⠀⠀⠀⠀⠀
⢿⣿⠀⠀⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣶⣮⣕⡠⠀⠀⠀⠀⠀⠀⣀⣀⣀⣠⣼⣧⣤⣤⣄⣀⣀⣀⡤⠿⠀⠀⠀⠙⣧⡀⠀⠀⠀
⣾⣿⠀⠀⡇⠀⠀⠚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀
⣿⢽⠇⠀⡇⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣤⠀⠀⠐⠀⠀⠀⠀⠀⠻⣆⠀⠀
⣿⢸⠀⠀⡇⠀⠀⠀⠀⠀⠈⠻⠿⣿⣿⣿⡿⡏⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠃⠀⠰⣄⠀⠀⠀⠀⠀⠀⢻⣆⠀
⣿⢸⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣶⣶⡦⠄⠀⠉⠙⠛⠛⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠁⠀⠠⡀⠀⠀⠀⠈⢿⡇
⣿⢸⠀⠘⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠠⢄⣀⣨⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧
⣿⢸⡀⠀⠀⠀⢀⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢦⣌⣁⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉
⠟⠸⠿⢾⣄⣤⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠰⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢰⡟⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠶⠶⠶⠟⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠆⠀⠈⠙⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
        await context.send(f"Hello {context.author.mention}! :3\n"
                           f"{meow_face}")  # <a:hyper:754213547000725504>


async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
