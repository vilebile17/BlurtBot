import os
import random
import sys

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from bookbot import bookbot
from message_counter import format_results, message_counter

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv(".env")
discord_key = os.environ.get("DISCORD_TOKEN")


def get_random_emoji(lst: list[int]) -> str:
    num = random.choice(lst)
    if num == 0:
        return ":sponge:"
    elif num == 1:
        return "<a:bigbrain:1420492173111201822>"
    elif num == 2:
        return "<a:amongus:1420490397137768561>"
    elif num == 3:
        return "<:trollface:1420489873562927205>"
    elif num == 4:
        return "<:gigachad:1417832993883557980>"
    elif num == 5:
        return "<:Blurt:1417547920722366686>"
    return ""


@bot.event
async def on_disconnect():
    print("BlurtBot out 🫡")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)  # Just incase I add invisible prefix commands

    if bot.user.mention in message.content and (
        "hello" in message.content.lower() or "hi" in message.content.lower()
    ):
        await message.channel.send(
            f"Hello there {message.author}! {get_random_emoji([0, 2, 4, 5])}"
        )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Oops that command doesn't appear to exist. Please use !help for a list of commands"
        )
    else:
        print(error)


@bot.event
async def on_member_join(member):
    default_channel = bot.get_channel(int(os.environ.get("DEFAULT_CHANNEL")))
    await default_channel.send(
        f"Welcome, {member.display_name}, I hope you enjoy your stay!"
    )


@bot.event
async def on_member_remove(member):
    default_channel = bot.get_channel(int(os.environ.get("DEFAULT_CHANNEL")))
    await default_channel.send(
        f"Goodbye, we hope to see you soon {member.display_name}."
    )


# PREDICT
# @bot.tree.command(
# name="predict",
# description="Predicts a message using Google Gemini based on the last 20 messages",
# )
# async def predict(interaction: discord.Interaction):
# msg_lst = []

# async for msg in interaction.channel.history(limit=20):
#   msg_lst.append(msg.content)

# print("just scanned through history")
# print(msg_lst, "\n")

# if msg_lst:
#   prediction = predict_message(msg_lst)
#   await interaction.response.send_message(prediction)
# else:
# print(
# "Either message history is empty or the permission to view history is off"
# )


# MESSAGE COUNTER
@bot.tree.command(
    name="message-counter",
    description="Counts the number of messages sent by each user in the last n messages",
)
async def _message_counter(interaction: discord.Interaction, limit: int):
    print("interaction received")
    await interaction.response.defer()
    print("deferred")
    print(f"Message counter called with a limit of {limit}")
    messages = [word async for word in interaction.channel.history(limit=limit)]
    dic = message_counter(messages)
    results = format_results(dic, "# Message Count")
    await interaction.followup.send(results)


# BOOK BOT
@bot.tree.command(
    name="bookbot",
    description="Counts the number of times each character shows up in the channel",
)
async def _bookbot(interaction: discord.Interaction, limit: int):
    await interaction.response.defer()
    print(f"Book Bot called with a limit of {limit}")
    messages = [word async for word in interaction.channel.history(limit=limit)]
    dic = bookbot(messages)
    results = format_results(dic, "# Character Composition")
    await interaction.followup.send(results)


# 8-BALL
@bot.tree.command(name="8ball", description="Gives a magic-8-ball like response")
async def _8ball(interaction: discord.Interaction):
    options = [
        "The stars have aligned in your favour...",
        "It may be wise to avoid...",
        "You lack conviction; speak from the heart.",
        "Indeed, my brother, it is necessary.",
        "I find the suggestion amusing...",
        "Thou shall findeth in thy afair great difficulty...",
        "Go forth; I find no reason to back away.",
        "Cool your embers, empty your mind from the shackles and turn again to the ball for assistance.",
        "I think you've gone a bit crazy...",
        "https://klipy.com/gifs/just-do-it-shia-la-beouf-1",
        ":man_shrugging:",
    ]
    await interaction.response.send_message(random.choice(options))


# RANDOM PERSON
@bot.tree.command(
    name="random-person",
    description="Picks a random person who has access to this channel",
)
async def _random_dude(interaction: discord.Interaction):
    member_list = [member for member in interaction.channel.members]
    member_list.remove(bot.user)
    print([member.display_name for member in member_list], "\n")
    chosen_one = random.choice(member_list)
    num = random.randint(1, 6)
    await interaction.response.send_message(
        chosen_one.mention + (" :sponge:" if num == 6 else "")
    )
    print(f"Ran randomDude with a num of {num}")


# Bot set up and syncing
@bot.event
async def on_ready():
    print("[1/3] connected to discord")
    load_dotenv()
    await bot.tree.sync()
    print("[2/3 syncing tree")

    default_channel = bot.get_channel(int(os.environ.get("DEFAULT_CHANNEL")))
    print("[3/3] finding default channel")
    if default_channel is not None:
        await default_channel.send("BlurtBot is up and ready for use!")
    else:
        print("Channel not found :(")


try:
    bot.run(discord_key)
except Exception as e:
    print(e, flush=True)
    print()

    if isinstance(e, TypeError):
        print("Likely missing .env file", flush=True)
        print("Docker: docker run --env-file .env vilebile17/blurt_bot", flush=True)
        print("If you haven't made the .env file yet, check out the docs", flush=True)
        print(
            "Docs: https://hub.docker.com/repository/docker/vilebile17/blurt_bot/general",
            flush=True,
        )

    sys.exit(1)
