from modules.error_logging.error_catch_util import error_logger
from collections import defaultdict, deque
from telethon import events
import asyncio
import re

SED_PATTERN = re.compile(r'^\$sed/((?:\\/|[^/])+)/((?:\\/|[^/])*)/?(.*)')
PREFIX = '「edit」\n'

last_msgs = defaultdict(lambda: deque(maxlen=10))
last_replies = defaultdict(lambda: deque(maxlen=10))

class UnknownFlag(ValueError):
    def __init__(self, flag):
        super().__init__(f'unknown flag: {flag}')
        self.flag = flag

def build_substitute(pattern, repl, flag_str):
    repl = repl.replace('\\/', '/').replace('\\0', '\\g<0>')

    count = 1
    flags = 0
    for f in (flag_str or ''):
        if f in 'Gg':
            count = 0
            continue

        try:
            flags |= getattr(re.RegexFlag, f.upper())
        except AttributeError:
            raise UnknownFlag(f) from None

    def substitute(string):
        if string.startswith(PREFIX):
            string = string[len(PREFIX):]

        s, i = re.subn(pattern, repl, string, count=count, flags=flags)
        if i > 0:
            return PREFIX + s

    return substitute


async def init(bot):
    @bot.on(events.NewMessage)
    @error_logger
    async def new_message_collector(event):
        last_msgs[event.chat_id].append(event.message)

    @bot.on(events.MessageEdited(outgoing=True, pattern=SED_PATTERN))
    @bot.on(events.NewMessage(outgoing=True, pattern=SED_PATTERN))
    @error_logger
    async def sed_commands(event):
        if event.is_reply:
            messages = [await event.get_reply_message()]
        else:
            messages = reversed(last_msgs[event.chat_id])

        try:
            substitute = build_substitute(*event.pattern_match.groups())
        except UnknownFlag as e:
            await event.reply(str(e))
            await event.delete()
            return

        for message in messages:
            new = substitute(message.raw_text)
            if new is None:
                continue

            try:
                sent = await message.reply(new, parse_mode=None)
            except Exception as e:
                await message.reply('owh :(\n' + str(e))
            else:
                last_msgs[event.chat_id].append(sent)

            break

        await event.edit(f"```\ns{event.text.strip('$sed')}```")
