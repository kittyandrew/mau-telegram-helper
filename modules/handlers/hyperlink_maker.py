from modules.error_logging.error_catch_util import error_logger
from telethon import events
import re


async def init(bot):
    def _pattern(event):
        text = re.findall(r"\[[^\]]*\]\([^\)]*\)", event.raw_text)
        return text

    @bot.on(events.MessageEdited(outgoing=True, func=_pattern))
    @bot.on(events.NewMessage(outgoing=True, func=_pattern))
    @error_logger
    async def hyperlinker(event):
        await event.edit(event.raw_text, parse_mode="Markdown", link_preview=False)
