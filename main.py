import os, sys, random, discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

from gemini import predict_message, mention, magic_8_ball
from message_counter import message_counter, format_results
from bookbot import bookbot



intents = discord.Intents.default()
intents.message_content = True 
intents.messages = True 
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
discord_key = os.environ.get("DISCORD_TOKEN")
default_channel_ID = int(os.environ.get("DEFAULT_CHANNEL"))

@bot.event
async def on_disconnect():
    print("BlurtBot out 🫡")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message) # Just incase I add invisible prefix commands

    if bot.user.mention in message.content:
        await message.channel.send(mention(message.content))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Oops that command doesn't appear to exist. Please use !help for a list of commands")
    else:
        print(error)


# PREDICT
@bot.tree.command(name="predict", description="Predicts a message using Google Gemini based on the last 20 messages")
async def predict(interaction: discord.Interaction):
    msg_lst = []

    async for msg in interaction.channel.history(limit=20):
        msg_lst.append(msg.content)

    print("just scanned through history")
    print(msg_lst)

    if msg_lst:
        prediction = predict_message(msg_lst)
        await interaction.response.send_message(prediction)
    else:
        print("Either message history is empty or the permission to view history is off")

# MESSAGE COUNTER
@bot.tree.command(name="message-counter", description="Counts the number of messages sent by each user in the last n messages")
async def _message_counter(interaction: discord.Interaction, n: int = 10000):
    dic = await message_counter(interaction, n)
    results = format_results(dic, "# Message Count")
    await interaction.response.send_message(results)

# BOOK BOT
@bot.tree.command(name="bookbot", description="Counts the number of times each character shows up in the channel")
async def _bookbot(interaction: discord.Interaction, n: int = 10000):
    dic = await bookbot(interaction, n)
    results = format_results(dic, "# Character Composition")
    await interaction.response.send_message(results)

# 8-BALL
@bot.tree.command(name="8ball", description="Gives a magic-8-ball like response")
async def _8ball(interaction: discord.Interaction, inquiry: str):
    await interaction.response.send_message(
        f"_{inquiry}_... \n\n{magic_8_ball(inquiry)}"
    )

# Bot set up and syncing basically
@bot.event
async def on_ready():
    # sync up the commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("Sync failed: ", e)

    channel = bot.get_channel(default_channel_ID)
    if channel is not None:
        await channel.send("BlurtBot is up and ready for use!")
    else:
        print("Channel not found :(")


bot.run(discord_key)
