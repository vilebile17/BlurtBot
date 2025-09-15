import discord

async def message_counter(history):
    # Takes a list of discord messages and returns a dictionary containing each sender mapped to the number of messages that they sent
    message_counts =  {}
    async for message in history:
        if message.author in message_counts:
            message_counts[message.author] += 1
        else:
            message_counts[message.author] = 1
    return message_counts


def dic_sum(dic):
    # Used for the next function
    total = 0
    for item in dic:
        total += dic[item]
    return total


def format_results(dic):
    # formats the results from message_counter() nicely
    sorted_dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
    string = "# Message count"
    counter, total_message_count = 0, dic_sum(sorted_dic)

    for sender in sorted_dic:
        counter += 1
        percentage = round((dic[sender] / total_message_count) * 100, 2) 
        string += f"\n{counter}. {sender}: **{dic[sender]}** ({percentage}%)"  
        # example format: 1. User123: **87** (24.30%)
    return string 
