import discord

async def bookbot(ctx):
    # returns a dic
    string = ""
    async for message in ctx.history(limit=10000):
        string += message.content.strip()

    dic = {}
    for char in string:
        if char and char != " " and "\n" not in char:
            if char in dic:
                dic[char] += 1
            else:
                dic[char] = 1

    return dic
