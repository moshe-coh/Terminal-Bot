from functions.functions import disk_space, ip, speed_test
from config import allowed, help_text
from plugins.markups import start_and_help, refresh, refresh_space

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command(['start', 'help']))
async def start(_, m: Message):
    await m.reply(help_text, reply_markup=start_and_help, disable_web_page_preview=True)


@Client.on_message(filters.command('ip') & filters.user(allowed))
async def ip_cmd(_, m: Message):
    await m.reply(ip(), parse_mode='markdown')


@Client.on_message(filters.command('stats') & filters.user(allowed))
async def stats(_, m: Message):
    space = disk_space()
    total = space[0]
    used = space[1]
    free = space[2]
    text = f"**💾 Total Storage:** {total}\n\n**💽 Storage Used:** {used}\n\n**💿 Free Storage:** {free}"
    await m.reply_text(text, reply_markup=refresh_space)


@Client.on_message(filters.command('st') & filters.user(allowed))
async def st_cmd(_, m: Message):
    send = await m.reply('Checking... ⏳')
    st = speed_test()
    down = st[0]
    up = st[1]
    ping = st[2]
    text = f"**📥 Download Speed:** {down}\n\n**📤 Upload Speed:** {up}\n\n**🩸 ping: ** {ping}"
    await send.delete()
    await m.reply_text(text, reply_markup=refresh)
