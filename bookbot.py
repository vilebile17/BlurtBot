def bookbot(messages) -> dict:
    characters = {}
    for message in messages:
        content = message.content.lower()
        add_message_to_dic(characters, content)
    return characters


def add_message_to_dic(dic, message):
    not_wanted_chars = " .:'\";?!-*\n()[]{}%&@><|^+-=`/“”#"
    for char in message:
        if char in dic:
            dic[char] += 1
        elif char not in not_wanted_chars:
            dic[char] = 1
