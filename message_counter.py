import discord

async def message_counter(history):
    # Takes a list of discord messages and returns a dictionary containing each sender mapped to the number of messages that they sent
    message_counts =  {}
    async for message in history:
        if message.author in message_counts:
            message_counts[message.author] += 1
        else:
            message_counts[message.author] = 1
    return dict(sorted(message_counts.items(), key=lambda item: item[1], reverse=True))
