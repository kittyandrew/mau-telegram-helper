from modules.utils.functions import async_find_commands, extract_url
from modules.error_logging.error_catch_util import error_logger
from modules.utils.executing_youtube_dl import download_by_url
from telethon.utils import get_attributes
from telethon.tl.custom import Message
from telethon import events
from typing import Union
import datetime
import secrets
import asyncio
import time
import os

""" Command for using youtube-dl module from telegram """
async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$dl([\s\S]*)"))
    @error_logger
    async def dl_manager(event:Union[Message, events.NewMessage.Event]):
        client = event.client
        commands, query = await async_find_commands(event)

        # Extracting urls from text
        urls = extract_url(query)
        # Making sure any amount of links are being
        # found and downloaded from
        for url in urls:
            # Make sure deletion of your message is not raising
            try:
                await event.edit(f"Downloading file(s)..")
            except:
                pass

            #   Creating new random folder for each link
            # ( Many videos in one link possible aka playlists )
            real_path = os.path.join("buffer", f"folder_{secrets.token_urlsafe(16)}")
            # Creating new folder directory
            os.mkdir(real_path)

            # Boolean to decide is this video or audio
            is_audio = "-audio" in commands or "-mp3" in commands
            is_document = "-f" in commands or "-d" in commands

            # TODO: Implement callback in chat
            # Async wrapper for smooth download-converting change
            async def smooth_switch(d, event):
                if d['status'] == 'finished':
                    await event.edit("Downloading..\n(Progress: `finished`)")
                    if is_audio:
                        await asyncio.sleep(0.7)
                        await event.edit("Converting to audio..")

            # Async wrapper for download progress
            async def downloading(d, event):
                if d['status']:
                    if time.time()%2==0:
                        await event.client.send_message("me", (f"{d['status']}, type:{type(d['status'])}"))

            # Gathering async functions in synchronous context
            # ( On finish downloading, before converting; )
            # ( During downloading, progress bar. )
            def sync_progress(d):
                asyncio.run_coroutine_threadsafe(smooth_switch(d, event), loop=client.loop)
                #asyncio.run_coroutine_threadsafe(downloading(d, event), loop=client.loop)

                # Download video, passing callback function here
            await download_by_url(
                                url,
                                real_path,
                                is_audio = is_audio,
                                callback = [sync_progress]
                            )

            try:
                # Finding all downloaded videos in the current directory
                for path in [f for f in os.listdir(real_path) if os.path.isfile(os.path.join(real_path, f))]:
                    path = os.path.join(real_path, path)
                    try:
                        last_dt = datetime.datetime.now()
                        diff = datetime.timedelta(seconds=2)
                        first_time_update = True

                        # On-progress upload asynchronous callback func
                        async def on_progress_upload(sent_bytes, total_bytes):
                            nonlocal last_dt, first_time_update
                            perc = round((sent_bytes / total_bytes) * 100)
                            curr = datetime.datetime.now()
                            if first_time_update:
                                first_time_update = False
                                # Make sure deletion of your message is not raising
                                try:
                                    await event.edit(f"Uploading..\n(Progress: `{perc}%`)")
                                except:
                                    pass
                            elif curr - last_dt >= diff:
                                last_dt = curr
                                # Make sure deletion of your message is not raising
                                try:
                                    await event.edit(f"Uploading..\n(Progress: `{perc}%`)")
                                except:
                                    pass

                        # Uploading file to telegram servers with telethon
                        file = await client.upload_file(
                                        path,
                                        progress_callback= on_progress_upload
                                    )

                        # Make sure deletion of your message is not raising
                        try:
                            await event.edit(f"Uploading..\n(Progress: `Done`)")
                            await asyncio.sleep(0.5)
                            await event.edit(f"`Task has been completed.`")
                            await asyncio.sleep(0.5)
                            await event.delete()
                        except:
                            pass

                        # Getting attributes of the uploaded file
                        try:
                            attributes = get_attributes(path)
                        except Exception as e:
                            attributes = None

                        # Make sure deletion of your message is not raising
                        try:
                            await client.send_file(
                                            event.chat_id,
                                            file,
                                            attributes=attributes[0],
                                            reply_to=event,
                                            force_document=is_document
                                        )
                        except:
                            await client.send_file(
                                            event.chat_id,
                                            file,
                                            attributes=attributes[0],
                                            force_document=is_document
                                        )

                    finally:
                        # Finally remove downloaded file
                        os.remove(path)
            finally:
                # Finally delete empty folder
                os.rmdir(real_path)
