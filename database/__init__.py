""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""
import sqlite3

import aiosqlite


# TODO: unsafe to use same class for any DB connection
class GeneralDbManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_warn(
            self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a warn from the database.

        :param warn_id: The ID of the warn.
        :param user_id: The ID of the user that was warned.
        :param server_id: The ID of the server where the user has been warned
        """
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    # TODO: rename this function
    async def create_server_table(self, server_id: int, server_name: str) -> bool:
        """
        This method will create a new table for each server the bot joins.

        :param server_id: The ID of the server.
        :param server_name: The name of the server.
        """
        await self.connection.execute(
            f"""CREATE TABLE IF NOT EXISTS "{server_id}" ("server_name" TEXT NOT NULL, "server_id" INTEGER NOT NULL,
            "custom_joins_channel" INTEGER, PRIMARY KEY("server_id"))"""
        )

        await self.connection.execute(
            f"INSERT INTO '{server_id}' VALUES (?, ?, ?)",
            (server_id, server_name, None)
        )

        try:
            await self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error while creating server table.\n{e}")
            return False

    async def get_server_data(self, server_id: int) -> list:
        """
        This method will fetch the server data from the database.

        :param server_id: The ID of the server.
        :return: A tuple containing the server data.
        """
        rows = await self.connection.execute(
            f"SELECT * FROM '{server_id}'"
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result

    async def update_server_data(self, server_id: int, column: str, value: str) -> None:
        """
        Update server data. This method is usually called

        :param server_id: The ID of the server.
        :param column: The column to update.
        :param value: The value to update.
        """
        await self.connection.execute(
            f"UPDATE '{server_id}' SET {column}=?",
            (value,)
        )

        await self.connection.commit()


class InternalBotSettingsDbManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def get_blacklisted_users(self, count: bool) -> list or int:
        """
        Retrieve all blacklisted users.
        Blacklisted users can access no functionality of the bot, but are not ignored from its monitoring or events.
        Blacklisted users will be visibly flagged when a command is ran on them, or an action involving them is made.

        :param count: A boolean indicating if the count of blacklisted users should be returned instead.
        :return: A list of all the blacklisted users.
        """
        if count:
            rows = await self.connection.execute(
                "SELECT COUNT(*) FROM 'blacklisted_users'"
            )
            async with rows as cursor:
                result = await cursor.fetchone()
                return result[0] if result is not None else 0
        try:
            rows = await self.connection.execute("SELECT * FROM 'blacklisted_users' LIMIT 15")
            async with rows as cursor:
                result = await cursor.fetchall()
                result_list = [row for row in result]
                return result_list
        except sqlite3.Error as e:
            print(f"Error while getting blacklisted users.\n{e}")
            return ["error", e]

    async def is_blacklisted(self, user_id: int) -> bool:
        """
        Check if a user is blacklisted.
        Blacklisted users can access no functionality of the bot, but are not ignored from its monitoring or events.
        Blacklisted users will be visibly flagged when a command is ran on them, or an action involving them is made.

        :param user_id: The ID of the user to check.
        :return: A boolean indicating if the user is blacklisted or not.
        """
        rows = await self.connection.execute(
            "SELECT * FROM 'blacklisted_users' WHERE user_id=?", (user_id,)
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result is not None

    async def add_user_to_blacklist(self, user_id: int, user_name: str, t: int, reason: None = None) -> int:
        """
        Add a user to blacklist.

        :param user_id: The ID of the user to add to the blacklist.
        :param user_name: The name of the user to add to the blacklist.
        :param reason: The reason why the user should be blacklisted.
        :param t: The time the user should was blacklisted.
        """
        reason = "NYI" if reason is None else reason
        await self.connection.execute(
            "INSERT INTO 'blacklisted_users' VALUES (?, ?, ?, ?)", (user_id, user_name, reason, t)  # dont ask...
        )
        await self.connection.commit()
        total = await self.get_blacklisted_users(True)
        return total

    async def remove_user_from_blacklist(self, user_id: int) -> int:
        """
        Remove a user from blacklist.

        :param user_id: The ID of the user to remove from the blacklist.
        """
        await self.connection.execute(
            "DELETE FROM 'blacklisted_users' WHERE user_id=?", (user_id,)
        )
        await self.connection.commit()
        total = await self.get_blacklisted_users(True)
        return total


class ProfilesManagement:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection


