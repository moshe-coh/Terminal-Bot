from functions.functions import ip, get_server_speedtest, get_server_details
from config import allowed, help_text
from plugins.markups import start_and_help, refresh_space, base_markup
from pyrogram import Client, filters
from pyrogram.types import Message, ForceReply
import os


@Client.on_message(filters.command(['start', 'help']))
async def start(_, m: Message):
    await m.reply(help_text, reply_markup=start_and_help, disable_web_page_preview=True)


@Client.on_message(filters.command('ip') & filters.user(allowed))
async def ip_cmd(_, m: Message):
    await m.reply(ip(), parse_mode='markdown')


@Client.on_message(filters.command('stats') & filters.user(allowed))
async def stats(_, m: Message):
    await m.reply_text(get_server_details(), reply_markup=refresh_space)


@Client.on_message(filters.command(['st', 'speedtest']) & filters.user(allowed))
async def st_cmd(_, m: Message):
    server_speed_details, res_img = get_server_speedtest()
    try:
        await m.reply_photo(photo=res_img, caption=server_speed_details)
    except:
        await m.reply_text(text=server_speed_details)


@Client.on_message(filters.command("cd") & filters.user(allowed))
async def cd(client, m: Message):
    chdir = await client.ask(m.chat.id, "please enter the folder path that you want?",
                             timeout=120, filters=filters.reply, reply_markup=ForceReply())
    try:
        os.chdir(chdir.text)
    except FileNotFoundError:
        await m.reply_text("incorrect path!")
    except TimeoutError:
        pass
    except Exception as e:
        await m.reply_text(str(e))


@Client.on_message(filters.command('my_files') & filters.user(allowed))
async def my_files(_, m: Message):
    await m.reply_text('what you want to show?', reply_markup=base_markup)
