import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def predict_message(previous_messages):
    # Uses gemini to predict the next message based on a list of previous messages

    load_dotenv()
    gemini_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)
    
    instructions = """
    You are a discord bot which tries to predict the next message based on the last few,
    You will recieve a list of past messages (the first item is the most recent and the last item is the oldest message in the sample) and with that you must align to the tone, abreviations (or lack of them), message length and context to try and be as human as possible.
    I hope you are up for the challenge.
    All that I need you to return is the message you will send; ** NO NAME OF SENDER **, no date, just simply the message.
    You may use markdown formating, however based on the conversation tone that may not be appropriate
    """

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=f"{previous_messages}",
        config=types.GenerateContentConfig(
            system_instruction=instructions
        )
    )

    return response.text
