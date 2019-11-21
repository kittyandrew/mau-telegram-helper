from modules.error_logging.error_catch_util import error_logger
from telethon import events
from os import remove
import datetime
import asyncio

async def init(bot):
    @bot.on(events.MessageEdited(outgoing=True, pattern=r"^\$bash ([\s\S]*)"))
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$bash ([\s\S]*)"))
    @error_logger
    async def bash_executor(event):
        command = event.pattern_match.group(1).strip("\n")

        process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        stdout, stderr = await process.communicate()
        stderr = str(stderr.decode().strip())
        stdout = str(stdout.decode().strip())

        result = f"**Command:**\n`{command}`\n\n"
        if stdout:
            result += f"**Result:**\n`{stdout}`\n\n"
        if stderr:
            result += f"**Errors:**\n`{stderr}`"

        # Handle too long output (writing it to *.txt file and sending)
        if len(result) > 4096:
            name = "buffer/bash_output.txt"
            file = open(name, "w+")
            file.write(result)
            file.close()

            try:
                await event.edit(f'`{command}`')
            except:
                pass

            await event.client.send_file(
                event.chat_id,
                name,
                reply_to=event.id,
                caption="`Output`", )
            remove(name)
            return
        else:
            await event.edit(result)

