import os, sys, discord
from dotenv import load_dotenv
from discord.ext import commands

from gemini import get_message


def main():
    message = get_message([
"""Yakha — 23/07/2025, 03:03
I shall ask my birthers if I may participate, if you would allow my presence that is""",
'''XSET-IGL
[GOAT]
 — 23/07/2025, 03:03
🤓''',
"""peasandbeans34
[FC]
 — 23/07/2025, 10:00
I shall also ask my birther if I may participate, if you would allow my presence that is 
""",
"""Ibrahim — 23/07/2025, 11:29
of course you can all come but i need to 
remind you i've got 6 seats in my car""",
"""peasandbeans34
[FC]
 — 23/07/2025, 13:10
we can probably get *escorted* by our birther"""
    ])

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
        channel = client.get_channel(default_channel_ID)
        if channel is not None:
            await channel.send("BlurtBot out 🫡")
        else:
            print("Channel not found :(")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if "hi" in message.content.lower() and "blurt" in message.content.lower():
            await message.channel.send(f"Hello there, {message.author}")
        
        elif message.content.lower() == "predict":
            history = message.channel.history(limit=50)
            msg_lst = []
            async for msg in history:
                if msg.content != "predict" and msg.author != client.user:
                    msg_lst.append(msg.content)

            print(msg_lst)
            if history:
                prediction = get_message(msg_lst)
                await message.channel.send(prediction)
            else:
                print("Either message history is empty or the permission to view history is off")

    client.run(discord_key)

    #print(message.text)
    #print(f"Prompt tokens: {message.usage_metadata.prompt_token_count}")
    
if __name__ == "__main__":
    main()
