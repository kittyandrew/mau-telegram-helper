from modules.error_logging.error_catch_util import error_logger
from modules.utils.functions import async_find_commands
from telethon import events
import wikipedia


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$wiki([\s\S]*)"))
    @error_logger
    async def wikipedia_handler(event):
        client = event.client
        commands, query = await async_find_commands(event)
        is_url = True

        try:
            await event.edit("Searching..")
        except:
            pass

        try:
            if "-ru" in commands:
                wikipedia.set_lang("ru")
            if "-uk" in commands:
                wikipedia.set_lang("uk")
            else:
                wikipedia.set_lang("en")

            amount_sentences = 0
            for num in range(1, 11):
                if f"-{num}" in commands:
                    amount_sentences = num
                    break
            try:
                result = wikipedia.summary(query, sentences=amount_sentences)
            except wikipedia.exceptions.DisambiguationError:
                s = wikipedia.search(query, results=1)
                result = wikipedia.summary(s[0], sentences=amount_sentences)

        except Exception as e:
            print(f"{type(e)}({e})")

        await event.edit(f"`📘Wikipedia:`\n{result}")