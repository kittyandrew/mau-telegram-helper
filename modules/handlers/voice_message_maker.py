# Title
''' Project is currently dead due to the lack of technology to create realistic voice of the person '''

# Codes
'''
from modules.error_logging.error_catch_util import error_logger
from modules.utils.functions import async_find_commands
from telethon.tl.types import DocumentAttributeAudio
from telethon.tl.custom import Message
from config import VOICE_API_URL
from telethon import events
from typing import Union
from urllib import parse
import asyncio
import aiohttp
import io


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$voice([\s\S]*)"))
    @error_logger
    async def voice_maker(event:Union[Message, events.NewMessage.Event]):
        client = event.client
        commands, query = await async_find_commands(event)
        msg_reply = await event.get_reply_message()
        chat_id = event.chat_id

        # Clearing command event
        await event.delete()

        query = parse.quote(query)
        url = VOICE_API_URL + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status = response.status
                voice = await response.read()

        if str(status) == '200':
            voice = io.BytesIO(voice)
            voice.name = 'a.ogg'

            # Adding some missing info about audio
            # TODO: Make telegram show audio length
            # TODO: and add a proper waveform
            attributes = None

            file = await client.upload_file(voice)
            await client.send_file(chat_id, file, voice_note=True, reply_to=msg_reply, attributes=attributes)

        else:
            raise ServerError(f"{status}, {voice}")


    class ServerError(Exception):
        """ Error specifically for server errors """
'''