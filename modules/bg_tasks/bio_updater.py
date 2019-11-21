from telethon.tl.functions.account import UpdateProfileRequest
from modules.utils.time_profile import TimeKeeper
import asyncio


async def time_into_nickname(client):

    await asyncio.sleep(5)
    # Time in profile keeper
    time = TimeKeeper()

    await client(UpdateProfileRequest(about=time._time_stringified()))

    while True:
        await asyncio.sleep(5)

        change = time.update_time()
        if change[0]:
            await client(UpdateProfileRequest(about=change[1]))