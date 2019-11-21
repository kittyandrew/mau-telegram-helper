import re
import aiohttp


async def async_find_commands(event) -> (list, str):
    try:
        replied_to = await event.get_reply_message()
    except:
        replied_to = None

    if replied_to is None:
        query = event.pattern_match.group(1)
        query = query.strip("\n")
        commands, query = find_commands(query)
    else:
        commands, query = find_commands(event.pattern_match.group(1))
        if query != "":
            query = query.strip("\n")
        else:
            query = replied_to.text

    return commands, query



def find_commands(text: str("text to search in")) -> (list, str):
    '''
    :param: text (str)
    :return: Returns tuple of 2 objects, 1 (list) - commands, 2 (str) - text without commands
    '''
    pattern = r"(-[\S]*)"
    commands = re.findall(pattern, text)
    for i in commands:
        text = re.sub(i, "", text)
    text = text.strip()
    return commands, text


def extract_url(query:str) -> list:
    text = re.findall(r"\[[^\]]*\]\([^\)]*\)", query)
    if text:
        result = list()
        for i in text:
            result.append(i[i.index("](")+2:-1])
        return result
    else:
        result = list(x.strip().strip("\n") for x in query.split(","))
        return result


async def aiohttp_get_text(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
