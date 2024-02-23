""""
otto bot
Copyright © hi_skittles 2024
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

import discord
from discord.ext import commands
import sqlite3

from discord.ext.commands import Context

from database import GeneralDbManager


class Profiles(commands.Cog, name="profiles"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn = sqlite3.connect("database/profiles.db")
        self.cursor = self.conn.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{guild.id}" (
                                user_id INTEGER PRIMARY KEY,
                                name TEXT,
                                age TEXT,
                                gender TEXT,
                                species TEXT,
                                orientation TEXT,
                                height TEXT,
                                weight TEXT,
                                bio TEXT,
                                custom_image_url TEXT,
                                color TEXT,
                                moderation_flag INTEGER,
                                status INTEGER,
                                moderator_comment TEXT
                                )""")
        self.conn.commit()

    @commands.hybrid_group(name="profile", help="Displays a user profile.", invoke_without_command=True)
    async def profile(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Run `/profile help` for help", ephemeral=True)  # ephemeral doesn't work here u stinky

    @profile.command(name="help", description="Display valid subcommands.")
    async def profile_help(self, ctx: Context) -> None:
        embed = discord.Embed(title="Profile Commands Help", description="List of available profile commands:",
                              color=discord.Colour.dark_blue())

        profile_group = self.bot.get_command('profile')
        if profile_group:
            for subcommand in profile_group.commands:
                name = subcommand.name
                description = subcommand.description or "No description available"
                embed.add_field(name=name, value=description, inline=True)

        await ctx.send(embed=embed)

    @profile.command(name="view", description="Displays a user profile.", )
    async def view_profile(self, ctx: Context, member: discord.Member) -> None:
        self.cursor.execute(f"SELECT * FROM '{ctx.guild.id}' WHERE user_id = ?", (member.id,))
        profile_data = self.cursor.fetchone()

        if profile_data is None:
            await ctx.send("Profile not found.", ephemeral=True)
            return

        if profile_data[10]:
            color = profile_data[10]
            try:
                getattr(discord.Color, color)()
            except:
                color = "dark_blue"
            color = getattr(discord.Color, color)()

        if profile_data[9]:
            image_url = profile_data[9]

        embed = discord.Embed(title=f"Viewing {profile_data[1]}", description=f"Profile of {member.mention}",
                              color=color)
        embed.set_image(url=image_url if profile_data[9] else member.avatar.url)

        # Skipping user_id (index 0) and including up to moderator_comment (index -1), adjust based on your actual data
        fields = ['Age', 'Gender', 'Orientation', 'Species', 'Height', 'Weight', 'Bio']
        for i, field_name in enumerate(fields, start=2):
            if profile_data[i]:  # If the field is not None or empty
                embed.add_field(name=field_name, value=profile_data[i], inline=True)

        await ctx.send(embed=embed)

    @profile.command(name="new",
                     description="Create a new user profile. Once it's created, you can edit each field individually.", )
    async def create_profile(self, ctx):
        default_fields = ["None"] * 7
        default_image_url = ctx.author.avatar_url
        default_color = "orange"
        name = ctx.author.name
        moderation_flag = 0
        status = 0
        moderator_comment = None

        self.cursor.execute(f"SELECT 1 FROM '{ctx.guild.id}' WHERE user_id = ?", (ctx.author.id,))
        if self.cursor.fetchone():
            await ctx.send("You already have a profile!", ephemeral=True)
            return

        sql_insert_query = f"""
            INSERT INTO '{ctx.guild.id}' (
                user_id, name, age, gender, species, orientation, height, weight, bio, 
                custom_image_url, color, moderation_flag, status, moderator_comment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.cursor.execute(sql_insert_query, (
            ctx.author.id, name, *default_fields, default_image_url, default_color, moderation_flag, status,
            moderator_comment))

        self.conn.commit()
        await ctx.send("Your profile has been created! You can now edit it by using `/profile edit` :)", ephemeral=True)

    @profile.command(name="edit",
                     description="Edit your profile. You can use standard Discord markdown in the field values.")
    async def edit_profile(self, ctx: Context, field: str, new_value: str) -> None:
        # List of editable fields, adjust based on your actual profile schema
        editable_fields = ["name", "age", "gender", "species", "orientation", "height", "weight", "bio",
                           "custom_image_url", "color"]
        new_status = False

        # Check if the specified field is editable
        if field not in editable_fields:
            await ctx.send(
                f"This field cannot be edited or does not exist. Fields you can edit:\n{', '.join(editable_fields)}",
                ephemeral=True)
            return

        self.cursor.execute(f"SELECT status FROM '{ctx.guild.id}' WHERE user_id = ?", (ctx.author.id,))
        if self.cursor.fetchone()[0] == 0:
            new_status = True
            status = 1

        # Update the specified field in the database
        try:
            update_query = f"UPDATE '{ctx.guild.id}' SET {field} = ? WHERE user_id = ?"
            self.cursor.execute(update_query, (new_value, ctx.author.id))
            self.conn.commit()
            if new_status:
                update_query = f"UPDATE '{ctx.guild.id}' SET status = ? WHERE user_id = ?"
                self.cursor.execute(update_query, (status, ctx.author.id))
                self.conn.commit()
            await ctx.send(f"Your {field} has been updated to: `{new_value}`", ephemeral=True)
        except sqlite3.Error as e:
            await ctx.send("An internal error occurred while updating your profile.", ephemeral=True)
            print(f"SQLite error: {e}")  # Logging the error to console or consider logging to a file

    @profile.command(name="delete", description="Delete your profile.")
    async def delete_profile(self, ctx: Context) -> None:
        pass

    @profile.command(name="publish", description="Publish your profile for others to view.")
    async def publish_profile(self, ctx: Context) -> None:
        pass

    @profile.group(name="moderate", description="Manage moderation settings.")
    async def moderation(self, ctx: Context) -> None:
        pass

    @moderation.command(name="remove", description="Remove a users profile.")
    @commands.has_role("Moderator")
    async def remove_profile(self, ctx: Context, member: discord.Member, reason) -> None:
        pass

    @moderation.command(name="edit", description="Moderate a users profile.")
    @commands.has_role("Moderator")
    async def moderator_edit_profile(self, ctx: Context, member: discord.Member, field: str, content_editable: str) -> None:
        pass

    @moderation.command(name="view", description="View flags and reports on a users profile.")
    @commands.has_role("Moderator")
    async def moderator_view_profile(self, ctx: Context, member: discord.Member) -> None:
        pass

    @remove_profile.error
    @edit_profile.error
    async def remove_profile_error(self, ctx: Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have permission to do that.", ephemeral=True)

    @create_profile.error
    async def create_profile_error(self, ctx: Context, error: commands.CommandError) -> None:
        # if isinstance(error, sqlite3.Error):
        await ctx.send(f"An error occurred while creating your profile.\nType: {error.__class__}", ephemeral=True)

    @view_profile.error
    async def view_profile_error(self, ctx: Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member provided.", ephemeral=True)
        await ctx.send("An internal error occurred.", ephemeral=True)

    @edit_profile.error
    async def edit_profile_error(self, ctx: Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide a field and a new value to edit.", ephemeral=True)
        await ctx.send("An internal error occurred.", ephemeral=True)

    @publish_profile.error
    async def publish_profile_error(self, ctx: Context, error: commands.CommandError) -> None:
        await ctx.send("An internal error occurred.", ephemeral=True)


async def setup(bot) -> None:
    await bot.add_cog(Profiles(bot))
