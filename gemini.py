import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_response(instructions, contents):
    # This is the main function, all of the others in this file use this to actually generate a response
    load_dotenv()
    gemini_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=instructions
        )
    )
    return response.text


def predict_message(previous_messages):
    instructions = """
    You are a discord bot named 'BlurtBot' which tries to predict the next message based on the last few,
    You will recieve a list of past messages (the first item is the most recent and the last item is the oldest message in the sample) and with that you must align to the tone, abreviations (or lack of them), message length and context to try and be as human as possible.
    I hope you are up for the challenge.
    All that I need you to return is the message you will send; ** NO NAME OF SENDER **, no date, just simply the message.
    You may use markdown formating, however based on the conversation tone that may not be appropriate
    """
    return get_response(instructions, previous_messages)

def mention(message):
    instructions ="""You are a discord bot named 'BlurtBot' who just got mentioned, you need to give a response, ideally relatively short, which responds to the message

    if you wish, you may use the following custom emojis (you can of course use standard ones) As a quick note, you must type the emojis as they appear in the format <:name:id>
    <:Blurt:1417547920722366686> (This is your profile picture)
    <:gigachad:1417832993883557980>
    <:bigbrain:1417833269440938035>

    If you are asked about yourself, you have the following commands: !predict, !message-counter and !bookbot,
    !predict predicts the next message
    !message-counter counts the number of messages each user sent in the channel
    !bookbot returns the character composition of all of the messages sent on the channel (eg. how many 'a's, 'b's etc.)
    !8ball generates a magic 8-ball like response

    extra information is on the github: https://github.com/vilebile17/BlurtBot

    if you are unsure what to say, just rip off a random, unrelated quote. Remember you can use markdown formating. And in this case, don't end a message with an emoji.
    """
    return get_response(instructions, message)

def magic_8_ball(result):
    instructions = f"You are a magic eight ball. Given the result: {result}, you must give a short response just like a magic eight ball would"
    return get_response(instructions, "")
