from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from functions.functions import speed_test, stats_server

start_and_help = InlineKeyboardMarkup([[InlineKeyboardButton(text='Creator 🦾', url='https://t.me/MosheWin')],
                                       [
                                           InlineKeyboardButton(text='Source Code 🗃',
                                                                url='https://github.com/moshe-coh/Terminal-Bot')
                                       ]])

refresh = InlineKeyboardMarkup([[InlineKeyboardButton(text='Refresh 💫', callback_data='refresh')]])

refresh_space = InlineKeyboardMarkup([[InlineKeyboardButton(text='Refresh 💫', callback_data='space')]])


@Client.on_callback_query()
async def bt(_, cb: CallbackQuery):
    if cb.data == "refresh":
        await cb.message.edit_text('Checking Again... ⏳ ')
        st = speed_test()
        down = st[0]
        up = st[1]
        ping = st[2]
        text = f"**📥 Download Speed:** {down}\n\n**📤 Upload Speed:** {up}\n\n**🩸 ping: ** {ping}"
        try:
            await cb.message.edit_text(text, reply_markup=refresh)
        except MessageNotModified:
            pass
    elif cb.data == "space":
        await cb.message.edit_text('Checking Again... ⏳')

        try:
            await cb.message.edit_text(stats_server(), reply_markup=refresh_space)
        except MessageNotModified:
            pass
