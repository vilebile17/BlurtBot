import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_message(previous_messages):
    # Uses gemini to predict the next message based on a list of previous messages
    # it returns a response object (very important note)

    load_dotenv()
    gemini_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)
    
    instructions = """
    You are a discord bot which tries to predict the next message based on the last few,
    You will recieve a list of past messages (last item is most recent and first is the oldest) and with that you must align to the tone, abreviations (or lack of them), message length and context to try and be as human as possible.
    I hope you are up for the challenge.
    All that I need you to return is the message you will send; no name of sender, no date, just simply the message.
    """

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=f"{previous_messages}",
        config=types.GenerateContentConfig(
            system_instruction=instructions
        )
    )

    return response

