import discord

async def bookbot(history):
    # returns a dic
    string = ""
    async for message in history:
        string += message.content.strip()

    dic = {}
    for char in string:
        if char and char != " ":
            if char in dic:
                dic[char] += 1
            else:
                dic[char] = 1

    return dic
