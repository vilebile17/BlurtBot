import os, sys, random, discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

from message_counter import message_counter, format_results
from bookbot import bookbot


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
discord_key = os.environ.get("DISCORD_TOKEN")


@bot.event
async def on_disconnect():
    print("BlurtBot out 🫡")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)  # Just incase I add invisible prefix commands

    # if bot.user.mention in message.content:
    # await message.channel.send(mention(message.content))


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
    print(f"Message counter called with a limit of {limit}")
    await interaction.response.defer()
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
    print(f"Book Bot called with a limit of {limit}")
    await interaction.response.defer()
    messages = [word async for word in interaction.channel.history(limit=limit)]
    dic = bookbot(messages)
    results = format_results(dic, "# Character Composition")
    await interaction.followup.send(results)


# 8-BALL
@bot.tree.command(name="8ball", description="Gives a magic-8-ball like response")
async def _8ball(interaction: discord.Interaction):
    options = [
        "The starts have aligned in your favour...",
        "It may be wise to avoid...",
        "You lack conviction; speak from the heart.",
        "Indeed, my brother, it is necessary.",
        "I find the suggestion amusing...",
        "Thou shall findeth in thy afair great difficulty...",
        "Go forth; I find no reason to back away.",
        "Cool your embers, empty your mind from the shackles and turn again to the ball for assistance.",
    ]
    await interaction.response.send_message(random.choice(options))


# RANDOM PERSON
@bot.tree.command(
    name="random-person",
    description="Picks a random person who has access to this channel",
)
async def _random_dude(interaction: discord.Interaction):
    member_list = [member.display_name for member in interaction.channel.members]
    member_list.remove("BlurtBot")
    print(member_list, "\n")
    chosen_one = random.choice(member_list)
    await interaction.response.send_message(chosen_one)


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


bot.run(discord_key)
