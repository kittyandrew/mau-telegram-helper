from modules.error_logging.error_catch_util import error_logger
from telethon import events
import asyncio
import os, sys


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$(upd|update)([\s\S]*)"))
    @error_logger
    async def update_command(event):

        await event.edit("```Updating..```")

        await event.edit("```Pulling update..```")
        # Creating subproccess to pull latest update from repo
        proc = await asyncio.create_subprocess_shell("git pull")
        await proc.wait()

        await event.edit("```Reboot. Enjoy the latest version!```")
        os.execl(sys.executable, sys.executable, *sys.argv)
        # Any further code has no impact (Script is reloaded)
        # await event.edit("```Reboot is finished. Enjoy the latest version!```")