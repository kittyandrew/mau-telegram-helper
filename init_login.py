from telethon import TelegramClient
import config as c
import asyncio
import os

async def _init_session():
    client = TelegramClient(
                    session=f'telethon sessions/{c.Main_username}',
                    api_hash=c.Main_api_hash,
                    api_id=c.Main_api_id
                )
    await client.start(phone=c.Main_phone)
    await client.disconnect()

def init_session():
    future = asyncio.ensure_future(_init_session())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(future)
    print("Session was created.")

if __name__ == "__main__":
    if not os.path.exists("telethon sessions"):
        os.mkdir("telethon sessions")
    if not os.path.exists("buffer"):
        os.mkdir("buffer")

    init_session()