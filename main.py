from modules.main_setup import TelethonManager
import logging
import os

if __name__ == "__main__":

    if not os.path.exists("telethon sessions"):
        os.mkdir("telethon sessions")
    if not os.path.exists("buffer"):
        os.mkdir("buffer")

    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

    manager = TelethonManager()
    manager.start()