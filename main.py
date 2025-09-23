import os, sys, random, discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

from gemini import predict_message, mention, magic_8_ball
from message_counter import message_counter, format_results
from bookbot import bookbot


def main():

    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True # This makes sure that the bot can read previous messages

    load_dotenv()
    discord_key = os.environ.get("DISCORD_TOKEN")
    default_channel_ID = int(os.environ.get("DEFAULT_CHANNEL"))
    bot = commands.Bot(command_prefix='!', intents=intents)


    @bot.event
    async def on_ready():
        bot.tree.clear_commands(guild=discord.Object(id=1415382708758122608))
        await bot.tree.sync(guild=discord.Object(id=1415382708758122608))
        channel = bot.get_channel(default_channel_ID)
        if channel is not None:
            await channel.send("BlurtBot is up and ready for use!")
        else:
            print("Channel not found :(")

    @bot.event
    async def on_disconnect():
        print("BlurtBot out 🫡")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        await bot.process_commands(message)

        if bot.user.mention in message.content:
            await message.channel.send(mention(message.content))

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Oops that command doesn't appear to exist. Please use !help for a list of commands")
        else:
            print(error)


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

    @bot.tree.command(name="message-counter", description="Counts the number of messages sent by each user in the last n messages")
    async def _message_counter(interaction: discord.Interaction, n: int = 10000):
        dic = await message_counter(interaction, n)
        results = format_results(dic, "# Message Count")
        await interaction.response.send_message(results)

    @bot.command(name="bookbot", aliases=["bb", "character-composition"], help="Counts the number of times each character shows up in the channel")
    async def _bookbot(ctx):
        dic = await bookbot(ctx)
        results = format_results(dic, "# Character Composition")
        await ctx.send(results)

    @bot.command(name="8ball", aliases=["decision", "eightball", "eight-ball"], help="Gives a magic-8-ball like response")
    async def _8ball(ctx):
        options = ["yes", "no", "perhaps"]
        enum = random.choice(options)
        await ctx.send(magic_8_ball(enum))

    bot.run(discord_key)
    
if __name__ == "__main__":
    main()
