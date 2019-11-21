from modules.error_logging.error_catch_util import error_logger
from modules.utils.functions import async_find_commands
from telethon.tl.custom import Message
from telethon import events
from typing import Union
import functools


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$id([\s\S]*)"))
    @error_logger
    async def id_getter(event:Union[Message, events.NewMessage.Event]):
        commands, query = await async_find_commands(event)
        if "-f" in commands:
            replied = await event.get_reply_message()
            sender = replied.forward.sender
            text = f"```\nid: {sender.id}```"
            await event.edit(text)

        else:
            replied = await event.get_reply_message()
            sender = await replied.get_sender()
            text = f"```\nid: {sender.id}```"
            await event.edit(text)


    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$info([\s\S]*)"))
    @error_logger
    async def telegram_info(event:Union[Message, events.NewMessage.Event]):
        client = event.client
        commands, query = await async_find_commands(event)
        if "-f" in commands:
            replied = await event.get_reply_message()
            sender = replied.forward.sender
            user_name = f"{sender.first_name} {sender.last_name}" if sender.last_name else f"{sender.first_name}"
            user_tag = f"username: {sender.username}\n" if sender.username else "\n"

            odd_stat = f"\nbot:         {sender.bot}" \
                       f"\nverified:    {sender.verified}" \
                       f"\nrestricted:  {sender.restricted}" \
                       f"\nsupport:     {sender.support}" \
                       f"\nscam:        {sender.scam}"

            text = f"```\nStat\nuser: {user_name}\n{user_tag}user id: {sender.id}\n{odd_stat}```"
            await event.edit(text)

        else:
            replied = await event.get_reply_message()
            sender = await replied.get_sender()
            user_name = f"{sender.first_name} {sender.last_name}" if sender.last_name else f"{sender.first_name}"
            user_tag = f"username: {sender.username}\n" if sender.username else "\n"

            odd_stat = f"\nbot:         {sender.bot}" \
                       f"\nverified:    {sender.verified}" \
                       f"\nrestricted:  {sender.restricted}" \
                       f"\nsupport:     {sender.support}" \
                       f"\nscam:        {sender.scam}"

            text = f"```\nStat\nuser: {user_name}\n{user_tag}user id: {sender.id}\n{odd_stat}```"
            await event.edit(text)