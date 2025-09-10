import os, sys, discord
from dotenv import load_dotenv
from discord.ext import commands
from google import genai

from gemini import get_message


def main():
    message = get_message([
        "Ibrahim: guys can you bring",
        "Ibrahim: Some spare clothes and",
        "Ibrahim: Some walking shoes",
        "Ibrahim: Thank you",
        "Yahya: Do walking sandles count as walking shoes?",
        "Ibrahim: yh ig",
        "Ali: Ibrahim, what time are u going to pick us up?"
    ])
    print(message.text)

if __name__ == "__main__":
    main()
