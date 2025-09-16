import os, sys, discord
from dotenv import load_dotenv
from discord.ext import commands

from gemini import predict_message
from message_counter import message_counter, format_results
from bookbot import bookbot


def main():

    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True # This makes sure that the bot can read previous messages

    load_dotenv()
    discord_key = os.environ.get("DISCORD_TOKEN")
    default_channel_ID = int(os.environ.get("DEFAULT_CHANNEL"))
    client = discord.Client(intents=intents)


    @client.event
    async def on_connect():
        channel = client.get_channel(default_channel_ID)
        if channel is not None:
            await channel.send("BlurtBot is up and ready for use!")
        else:
            print("Channel not found :(")

    @client.event
    async def on_disconnect():
        print("BlurtBot out 🫡")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if "hi" in message.content.lower() and "blurt" in message.content.lower():
            await message.channel.send(f"Hello there, {message.author}")
        
        elif message.content.lower() == "!predict":
            history = message.channel.history(limit=20)
            msg_lst = []
            async for msg in history:
                if not msg.content.startswith("!") and msg.author != client.user:
                    msg_lst.append(msg.content)

            print(msg_lst)
            if history:
                prediction = predict_message(msg_lst)
                await message.channel.send(prediction)
            else:
                print("Either message history is empty or the permission to view history is off")

        elif message.content.lower() == "!message-counter" or message.content.lower() == "!message_counter":
            history = message.channel.history(limit=10000)
            dic = await message_counter(history)
            results = format_results(dic, "# Message Count")
            await message.channel.send(results)

        elif message.content.lower() == "!bookbot" or message.content.lower() == "!book-bot":
            history = message.channel.history(limit=10000)
            dic = await bookbot(history)
            results = format_results(dic, "# Character Composition")
            await message.channel.send(results)


    client.run(discord_key)
    
if __name__ == "__main__":
    main()
