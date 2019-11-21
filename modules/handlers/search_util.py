from modules.error_logging.error_catch_util import error_logger
from modules.utils.functions import async_find_commands
from telethon import events
from urllib import parse
import config as c
import requests
import asyncio


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$search([\s\S]*)"))
    @error_logger
    async def search(event):
        client = event.client
        commands, query = await async_find_commands(event)
        is_url = True

        try:
            await event.edit("Searching..")
        except:
            pass

        if "-wf" in commands or "-wfa" in commands:
            is_url = False
            url = f"https://api.wolframalpha.com/v1/result?i={parse.quote_plus(query)}&appid={c.wolframalpha_id}"

            request = requests.get(url)
            result = request.text

        elif "-google" in commands or "-g" in commands:
            google_url = "https://www.google.com/search?q="
            google_map_url = "https://www.google.com/maps/search/"
            url_query = parse.quote_plus(query)
            if "-img" in commands:
                url = f'<a href="{google_url}{url_query}&tbm=isch">{query}</a>'
            elif "-vid" in commands:
                url = f'<a href="{google_url}{url_query}&tbm=vid">{query}</a>'
            elif "-map" in commands:
                url = f'<a href="{google_map_url}{url_query}">{query}</a>'
            elif "-news" in commands:
                url = f'<a href="{google_url}{url_query}&tbm=nws">{query}</a>'
            else:
                url = f'<a href="{google_url}{url_query}">{query}</a>'
        else:
            duck_url = "https://duckduckgo.com/?q="
            url_query = parse.quote_plus(query)
            if "-img" in commands:
                url = f'<a href="{duck_url}{url_query}&ia=images&iax=images">{query}</a>'
            elif "-vid" in commands:
                url = f'<a href="{duck_url}{url_query}&ia=videos&iax=videos">{query}</a>'
            elif "-map" in commands:
                url = f'<a href="{duck_url}{url_query}&iaxm=maps">{query}</a>'
            elif "-news" in commands:
                url = f'<a href="{duck_url}{url_query}&iar=news&ia=news">{query}</a>'
            else:
                url = f'<a href="{duck_url}{url_query}">{query}</a>'

        if is_url:
            result = f"🔍 Let me search that for you:\n{url}"
            await event.edit(result, parse_mode="html")
        else:
            if result == "Wolfram|Alpha did not understand your input":
                result = "🔍 I didn't understand the question, sorry.."
                await event.edit(result, parse_mode="html")
                await asyncio.sleep(3)
                await event.delete()
            else:
                result = f"🔍 Here is your result:\n{result}"
                await event.edit(result, parse_mode="html")
