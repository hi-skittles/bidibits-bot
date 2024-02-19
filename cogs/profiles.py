""""
otto bot
Copyright © hi_skittles 2024
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

import discord
from discord.ext import commands
import sqlite3

from discord.ext.commands import Context


class Profiles(commands.Cog, name="profiles"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = sqlite3.connect("database/profiles.db")
        self.c = self.conn.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.c.execute(f"""CREATE TABLE IF NOT EXISTS "{guild.id}" (
                                user_id INTEGER PRIMARY KEY,
                                field1 TEXT,
                                field2 TEXT,
                                field3 TEXT,
                                field4 TEXT,
                                custom_image_url TEXT,
                                color TEXT,
                                moderation_flag INTEGER
                                )""")
        self.conn.commit()

    @commands.hybrid_group(
        name="profile",
        help="Displays a user profile.",
    )
    async def profile(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(description="You need to specify a subcommand."
                                              "\n\n**Subcommands:**\n"
                                              "`view` - View a profile.\n",
                                  color=discord.Colour.dark_red(), )
            await ctx.send(embed=embed)

    @profile.command(
        base="profile",
        name="view",
        description="Displays a user profile.",
    )
    async def view_profile(self, ctx: Context, member: discord.Member) -> None:
        member = member or ctx.author
        self.c.execute(f"SELECT * FROM '{ctx.guild.id}' WHERE user_id = ?", (member.id,))
        profile_data = self.c.fetchone()
        if profile_data:
            # Here you would format the data into a Discord Embed and send it
            embed = discord.Embed(title=f"{member.name}'s Profile", color=0x00ff00)
            # Add fields to the embed using the data from the database
            await ctx.send(embed=embed)
        else:
            await ctx.send("No profile found.")


async def setup(bot) -> None:
    await bot.add_cog(Profiles(bot))
