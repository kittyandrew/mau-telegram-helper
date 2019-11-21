from telethon.tl.custom import Message
from telethon import events
from typing import Union
import config as c
import functools

ERROR = 10
FATAL_ERROR = 20

def error_logger(func, importance=10):

    if importance <= 10:
        @functools.wraps(func)
        async def wrapped(event:Union[Message, events.NewMessage.Event]):
            try:
                await func(event)
            except events.StopPropagation as sp:
                raise sp
            except Exception as e:
                log_msg = f"```\nHandler: {func.__name__}\n\n{(e.__class__.__name__)}: {e}```"
                await event.client.send_message(c.ERROR_LOG_CHANNEL_ID, log_msg)
    else:
        raise NotImplementedError("There is no such logging method yet")
    return wrapped
