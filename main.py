import os, sys, random, discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

from gemini import predict_message, mention, magic_8_ball, user_join, user_leave
from message_counter import message_counter, format_results
from bookbot import bookbot


intents = discord.Intents.default()
intents.message_content = True 
intents.messages = True 
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
discord_key = os.environ.get("DISCORD_TOKEN")

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

@bot.event 
async def on_member_join(member):
    default_channel = bot.get_channel(int(os.environ.get("DEFAULT_CHANNEL")))
    await default_channel.send(user_join(member.display_name))

@bot.event 
async def on_member_remove(member):
    default_channel = bot.get_channel(int(os.environ.get("DEFAULT_CHANNEL")))
    await default_channel.send(user_leave(member.display_name))

# PREDICT
@bot.tree.command(name="predict", description="Predicts a message using Google Gemini based on the last 20 messages")
async def predict(interaction: discord.Interaction):
    msg_lst = []

    async for msg in interaction.channel.history(limit=20):
        msg_lst.append(msg.content)

    print("just scanned through history")
    print(msg_lst, "\n")

    if msg_lst:
        prediction = predict_message(msg_lst)
        await interaction.response.send_message(prediction)
    else:
        print("Either message history is empty or the permission to view history is off")
print("defined predict")

# MESSAGE COUNTER
@bot.tree.command(name="message-counter", description="Counts the number of messages sent by each user in the last n messages")
async def _message_counter(interaction: discord.Interaction, num_messages: int = 10000):
    dic = await message_counter(interaction, num_messages)
    results = format_results(dic, "# Message Count")
    await interaction.response.send_message(results)
print("defined message-counter")

# BOOK BOT
@bot.tree.command(name="bookbot", description="Counts the number of times each character shows up in the channel")
async def _bookbot(interaction: discord.Interaction, num_messages: int = 10000):
    dic = await bookbot(interaction, num_messages)
    results = format_results(dic, "# Character Composition")
    await interaction.response.send_message(results)
print("defined bookbot")

# 8-BALL
@bot.tree.command(name="8ball", description="Gives a magic-8-ball like response")
async def _8ball(interaction: discord.Interaction, inquiry: str):
    await interaction.response.send_message(
        f"_{inquiry}_... \n\n{magic_8_ball(inquiry)}"
    )
print("defined 8-ball")

# RANDOM PERSON
@bot.tree.command(name="random-person", description="Picks a random person who has access to this channel")
async def _random_dude(interaction: discord.Interaction):
    member_list = [member.display_name for member in interaction.channel.members]
    member_list.remove("BlurtBot")
    print(member_list, "\n")
    chosen_one = random.choice(member_list)
    await interaction.response.send_message(chosen_one)
print("defined random-person")

# Bot set up and syncing
@bot.event
async def on_ready():
    load_dotenv()
    guild = discord.Object(id=int(os.environ.get("SERVER_ID")))
    if guild is None:
        print("Err guys, the guild ain't guilding")
        sys.exit(1089)

    for cmd in bot.tree.get_commands():
        print(f"old commmand: {cmd.name}")
    print()

    # sync up the commands
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("Sync failed: ", e)

    for cmd in bot.tree.get_commands():
        print(f"new command: {cmd.name}")
    print()

    default_channel = bot.get_channel(int(os.environ.get("DEFAULT_CHANNEL")))
    if default_channel is not None:
        await default_channel.send("BlurtBot is up and ready for use!")
    else:
        print("Channel not found :(")


bot.run(discord_key)
