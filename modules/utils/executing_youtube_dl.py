from typing import Union, List, Callable
import youtube_dl
import asyncio
import re
import os

async def download_by_url(
                url: str("str(url) OR str(youtube video id)"),
                path: str,
                is_audio: bool = False,
                callback: Union[callable, List[callable]] = None
                                        ) -> None:

    # Callback hack
    if callback == None:
        callback = [lambda x: None]
    elif callable(callback):
        callback = [callback]

    # Defining postprocessing for converting to mp3
    if is_audio:
        postproc = {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        },
    else:
        postproc = {}

    # Options for youtube-dl
    ydl_opts = {
        'format': "bestaudio/best",
        'postprocessors': postproc,
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s') if ("playlist?list=" not in url \
                   or "list=" not in url) else os.path.join(path, '%(playlist_index)s-%(title)s.%(ext)s'),
        'progress_hooks': callback,
    }

    # Download video with youtube-dl, passing options
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# TESTs
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(download_by_url("ZX3B953Rc0I", "tmp_12345", is_audio=True))
    loop.run_until_complete(future)