from modules.error_logging.error_catch_util import error_logger
from modules.trash_guy_module.trashguy import TrashGuy, Symbols
from modules.utils.functions import async_find_commands
from telethon.tl.custom import Message
from telethon import events
from typing import Union
import asyncio


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$trash([\s\S]*)"))
    @error_logger
    async def the_trash_guy(event:Union[Message, events.NewMessage.Event]):
        client = event.client
        commands, query = await async_find_commands(event)

        z = lambda c: any([(each in commands) for each in c])

        if z(["-d", "-desktop", "-ed", "-de"]):
            if z(["-e", "-emoji", "-emojis", "-ed", "-de"]):
                trashguy = TrashGuy(user_input=query,
                                    symbol_spacing=Symbols.SPACER_EMOJI,
                                    # wrap_monospace=True
                                    )
            else:
                trashguy = TrashGuy(user_input=query,
                                    symbol_spacing=Symbols.SPACER_WIDE,
                                    # wrap_monospace=True
                                    )
        else:
            if z(["-e", "-emoji", "-emojis"]):
                trashguy = TrashGuy(user_input=query,
                                    symbol_spacing=Symbols.SPACER_EMOJI,
                                    # wrap_monospace=True
                                    )
            else:
                trashguy = TrashGuy(user_input=query,
                                    # symbol_spacing=Symbols.SPACER_WIDE,
                                    wrap_monospace=True
                                    )

        while True:
            try:
                await event.edit(next(trashguy))
                await asyncio.sleep(0.2)
            except StopIteration:
                break