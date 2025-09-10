import os, sys, discord
from dotenv import load_dotenv
from discord.ext import commands
from google import genai

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
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    @bot.command()
    async def hello(ctx):
        await ctx.send("Hello! Blurt Bot is here and ready to cause some carnage!")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return  
        print(f"{message.author}: {message.content}")
        if message.content.lower() == "ping":
            await message.channel.send("pong!")
        await bot.process_commands(message)
 
    load_dotenv()
    discord_key = os.environ.get("DISCORD_TOKEN")
    bot.run(discord_key)
    #print(message.text)
    #print(f"Prompt tokens: {message.usage_metadata.prompt_token_count}")
    
if __name__ == "__main__":
    main()
