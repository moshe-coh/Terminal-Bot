import asyncio
import logging
import config
from pyromod import listen
from pyrogram import Client, idle, __version__
from pyrogram.raw.all import layer


logging.basicConfig(level=logging.INFO)
plugins = dict(root="plugins")
bot = Client('ssh', api_id=config.app_id, api_hash=config.app_hash, bot_token=config.token, plugins=plugins)


async def main():
    await bot.start()
    me = await bot.get_me()
    print(f"\n{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
