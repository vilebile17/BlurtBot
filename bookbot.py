import discord

async def bookbot(interaction, n):
    characters = {}
    messages = [word async for word in interaction.channel.history(limit=n)]
    for message in messages:
        content = message.content.lower()
        for i in range(len(content)):
            if content[i] in characters:
                characters[content[i]] += 1
            else:
                characters[content[i]] = 1

    new_dic = {}
    for char in characters:
        if char.is_alpha():
            new_dic[char] = characters[char]

    return new_dic
