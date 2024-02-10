""""
otto bot
Copyright © hi_skittles 2024
Contains code from © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja) Version: 6.1.0
"""

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from utils.wordle import Wordle
from utils.botlogger import Logs as BotLogger


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # TODO: somehow fix the duplicate yellow entries. no idea how..
    @commands.hybrid_command(
        name="wordle",
        description="Play a little wordle game.",
        aliases=["wl"],
    )
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def wordle(self, context: Context) -> None:
        try:
            game = Wordle("./utils/words.csv", 0, 5)
        except FileNotFoundError:
            await BotLogger.log_primary(self.bot, context, "wordle", True, "The file words.csv was not found.",
                                        discord.Colour.dark_red())
            embed = discord.Embed(description="I've encountered an error. Please check <#1200487447017046156> "
                                              "for more information.", colour=discord.Colour.dark_red())
            await context.send(embed=embed)
            return
        word_answer = game.retrieve_word
        await BotLogger.log_primary(self.bot, context, "wordle", False, f"{context.author.mention} "
                                                                        f"started a wordle game. Their answer is "
                                                                        f"**{word_answer}**.")
        game_embed = discord.Embed(description=f"Welcome to Wordle! You have {game.max_tries} tries to guess the word. "
                                               "The word is 5 letters long.", colour=discord.Colour.orange())
        bot_message = await context.send(embed=game_embed)
        feedback = ""
        while game.tries < game.max_tries:
            game.tries += 1
            guess = await self.bot.wait_for("message", check=lambda message: message.author == context.author,
                                            timeout=180)
            guess = guess.content.lower()
            if len(guess) != 5:
                game.tries -= 1
                await context.send(content="The word is 5 letters long.")
                continue
            else:
                if game.tries > 1:
                    feedback = "\n".join(feedback.splitlines()[:-1])
                feedback += "\n"
                for entry, word in zip(guess, word_answer):
                    if entry in word_answer and entry == word:
                        feedback += f"🟩"  # 🟩
                    elif entry in word_answer and entry != word:
                        # print(f"word: {word}, guess: {guess}, entry: {entry}")
                        feedback += f"🟨"  # 🟨
                    else:
                        feedback += f"⬛"  # ⬛
                feedback += "\n"
                for entry in guess:
                    feedback += f":regional_indicator_{entry}:"
                edited_embed = discord.Embed(description=f"\n{feedback}\n", colour=discord.Colour.orange())
                await bot_message.edit(embed=edited_embed)
            if guess == word_answer:
                embed = discord.Embed(description=f"You win! The answer was **{word_answer}**",
                                      colour=discord.Colour.brand_green())
                await context.send(embed=embed)
                # await bot_message.delete(delay=5)
                break
        else:
            await context.send(f"You lose! The word was {word_answer}.")
            # await bot_message.delete(delay=5)

    @commands.hybrid_command(
        name="meow",
        description="nothing :3",
    )
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def meow(self, context: Context) -> None:
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
