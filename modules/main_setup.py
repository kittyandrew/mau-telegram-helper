from modules.bg_tasks.bio_updater import time_into_nickname
from modules.utils.time_profile import TimeKeeper
from telethon import TelegramClient
from modules import handlers
import config as c
import asyncio

class TelethonManager:

    def __init__(self, loop=None):
        self.loop = loop
        self.client = TelegramClient(session=f'telethon sessions/{c.Main_username}', api_hash=c.Main_api_hash, api_id=c.Main_api_id, loop=self.loop)


    def start(self):

        ## register handlers
        handlers.init(self.client)

        ## register background events
        asyncio.gather(time_into_nickname(self.client), loop=self.client.loop)

        # Start
        self.client.start(phone=c.Main_phone)
        self.client.run_until_disconnected()

    def get_client(self):
        return self.client