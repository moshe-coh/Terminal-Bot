import os
import shutil
from typing import List
import sys
from disk import Path
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
from pyrogram.errors import MessageNotModified, ReplyMarkupInvalid
from functions.functions import get_server_details
from functions.terminal import Terminal
from functions.filebrowserapi import run as fb_api
import time

#your filebrowser server address. PS. It could set in config.py and import it.
filebrowser_server = '127.0.0.1:18080'
current_items = [0,0]
path = Path(os.curdir)
files_num = path.get_num_files()

start_and_help = InlineKeyboardMarkup([[InlineKeyboardButton(text='Creator 🦾', url='https://t.me/MosheNew')],
                                       [
                                           InlineKeyboardButton(text='Source Code 🗃',
                                                                url='https://github.com/moshe-coh/Terminal-Bot')
                                       ]])

refresh_space = InlineKeyboardMarkup([[InlineKeyboardButton(text='Refresh 💫', callback_data='space')]])

base_folder_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('📁 Show Folders', callback_data='ShowFolders')

    ]
])

base_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('🗃 Show Files', callback_data='ShowFiles'),
        InlineKeyboardButton('📁 Show Folders', callback_data='ShowFolders')

    ],
    [
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]
])


def folder_markup():
    directories = path.directories
    keyboard: List[List[InlineKeyboardButton]] = []
    keyboard.append(
            [InlineKeyboardButton(f"⬆️ {os.getcwd().split('/')[-2]}", callback_data=f"folder={'up'}")]
        )
    for folder in directories[current_items[1]:current_items[1]+10]:
        print('dir',directories.index(folder),folder.name)
        keyboard.append(
            #以文件名在列表的index参数callback
            #passing folder index parameter to callback function
            [InlineKeyboardButton(f"📁 {folder.name}", callback_data=f"folder={str(directories.index(folder))}")]
        )

        
    
    keyboard.append([
        InlineKeyboardButton('⬅️Up Page', callback_data='ShowFolders0'),
        InlineKeyboardButton("➡️Down Page", callback_data="ShowFolders1")
    ])

    keyboard.append([
        InlineKeyboardButton('🗃 Show Files', callback_data='ShowFiles')
    ])
    keyboard.append([
        InlineKeyboardButton("↩️Back To Menu", callback_data="BackToMenu")
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def TurnPage(id,gid):
    current_items[id] = current_items[id]+gid

def files_markup():
    files = path.files
    keyboard: List[List[InlineKeyboardButton]] = []
    #间距10，即一页显示10个。
    #10 as initial steps for showing files in one page.
    for file in files[current_items[0]:current_items[0]+10]:
        keyboard.append(
            [InlineKeyboardButton(f"{'🗃'} {file.full_name}", callback_data=f"file={files.index(file)}")]
        )
    keyboard.append([
        InlineKeyboardButton('⬅️Up Page', callback_data='ShowFiles0'),
        InlineKeyboardButton("➡️Down Page", callback_data="ShowFiles1")
    ])
    keyboard.append([
        InlineKeyboardButton('📁 Show Folders', callback_data='ShowFolders'),
        InlineKeyboardButton("↩️Back To Menu", callback_data="BackToMenu")
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def file_markup(file):
    keyboard = [#[InlineKeyboardButton("❌ Delete", callback_data=f"delete={file}")],
                #[InlineKeyboardButton("✏️Rename", callback_data=f"rename={file}")],
                [InlineKeyboardButton("📓 Download File", callback_data=f"download={file}")],
                [InlineKeyboardButton("🔗 Get link", callback_data=f"get_link={file}")],
                [InlineKeyboardButton("📺 Paly on TV", callback_data=f"play={file}")],
                [InlineKeyboardButton("↩️Back To Menu", callback_data="BackToMenu")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

#I Deprecated it for my personal using,I don't need to operate folder by tg.
'''
def folders_markup(folder):
    keyboard = [
                [InlineKeyboardButton("❌ Delete", callback_data=f"fdelete={folder}")],
                [InlineKeyboardButton("✏️ Rename", callback_data=f"rename={folder}")],
                [InlineKeyboardButton("↩️Back To Menu", callback_data="BackToMenu")]
               ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
'''

@Client.on_callback_query()
async def callback(_, cb: CallbackQuery):
    ##确定回调函数中,文件及文件夹的信息，以列表形式存在(list)
    ##make sure all the files and folders are lists in the callback function.
    directories = path.directories
    files = path.files
    data = cb.data
    if data.startswith("ShowFolders"):
        current_items[0] = 0
        curse = [-10,10]
        folders_num = len(directories)
        try:
            direction = curse[int(data[11])]
            if folders_num%abs(current_items[1]+direction+0.01) == folders_num:
                current_items[1] = 0
            else:
                TurnPage(1,direction)
        except:
            pass

        try:
            files_num2 = path.get_num_files()
            await cb.message.edit_text(
                                        f"**The Current Path:**\n `{path.absolute_path}`\n**Total Files and Folders are:** {files_num2}"
                                        f"\n📁 Here is your folders:", reply_markup=folder_markup()
                                      )
        except ReplyMarkupInvalid:
            await cb.answer("something wrong in the folder", show_alert=True)

    elif data.startswith("ShowFiles"):
        ##同样初始化为10个
        ##10 as initial steps
        curse = [-10,10]
        _files_num = path.get_num_files()
        try:
            direction = curse[int(data[9])]
            if _files_num%abs(current_items[0]+direction+0.01) == _files_num :
                current_items[0] = 0
            else:
                TurnPage(0,direction)
        except:
            pass
        
        try:
            await cb.message.edit_text(
                f"**The Current Path:**\n `{path.absolute_path}`\n**Total Files and Folders are:** {_files_num}"
                f"\n🗃 Here is your Files:", reply_markup=files_markup())
        except ReplyMarkupInvalid:
            await cb.answer("you have no files here, yet.", show_alert=True)
    elif data == "BackToMenu":
        await cb.message.edit_text('what you want to show?', reply_markup=base_markup)
    elif data == "close":
        await cb.message.delete()
    elif data.startswith('file'):
        none, file_name = data.split("=")
        await cb.message.edit_text(f"**File:** `{file_name}`\n**Path:** `{path.absolute_path}`",
                                   reply_markup=file_markup(file_name))
    
    elif data.startswith("folder"):
        FolderCmd = {'up':'..','up2':'../..','up3':''}
        none, FolderIndex = data.split("=")
        try:
            folder = directories[int(FolderIndex)].full_name
            current_items[1] = 0
        except:
            if os.getcwd() == '/root':
                folder = FolderCmd['up3']
            else:
                folder = FolderCmd[FolderIndex]
        os.chdir(os.path.abspath(os.path.join(os.getcwd(),folder)))
        path2 = Path(os.getcwd())
        files_num2 = path2.get_num_files()
        await cb.message.edit_text(f"**The Current Path**\n `{path2.absolute_path}`\n"
                                   f"**Total Files and Folders are:** {files_num2}",
                                   reply_markup=folder_markup())
    
    elif data.startswith('delete'):
        none, name = data.split("=")
        try:
            os.remove(name)
            await cb.message.edit_text(f"File {name} Deleted!", reply_markup=files_markup())
        except Exception as e:
            await cb.message.edit_text(f"Can't To delete this file...\n\n{str(e)}")
    elif data.startswith('rename'):
        none, name = cb.data.split("=")
        try:
            new_name = await _.ask(cb.message.chat.id, 'Send me the new name:', filters=filters.reply,
                                   reply_markup=ForceReply(), timeout=300)
            os.rename(name, new_name.text)
            await cb.message.edit_text(f"Renamed successfully", reply_markup=files_markup())
        except TimeoutError:
            pass
        except Exception as e:
            await cb.message.edit_text(f"Can't rename this file...\n\n{str(e)}")

    elif data.startswith("download"):
        none, f_id = cb.data.split("=")
        name = files[int(f_id)].full_name
        print(name,type(name))
        try:
            await cb.answer("File will download soon. please wait...")
            await cb.message.reply_document(name)
        except Exception as e:
            await cb.message.edit_text(f"Can't download this file...\n\n{str(e)}")

    elif data.startswith("get_link"):
        none, f_id = cb.data.split("=")
        name = files[int(f_id)].full_name
        f_path = f'{path.absolute}/{name}'
        hash = fb_api(f_path)
        dlink = f'https://{filebrowser_server}/fb/api/public/dl/{hash}'
        try:
            await cb.answer("Generate download link, please wait...")
            await cb.message.reply_text(f'{path},\n**[{name}]({dlink})**')
        except Exception as e:
            await cb.message.edit_text(f"Can't generate file link for your file...\n\n{str(e)}")
    
    elif data.startswith("play"):
        none, f_id = cb.data.split("=")
        name = files[int(f_id)].full_name
        f_path = f'{path.absolute}/{name}'
        hash = fb_api(f_path)
        
        #Some TV like Honor's Harmony OS need a filename in it, so give a file name 'test.mp4'.
        dlink = f'https://{filebrowser_server}/fb/api/public/dl/{hash}?filename=test.mp4'
        dlink = dlink.replace(' ','\ ')
        cmd = f'/root/.virtualenvs/Terminal-Bot-kmpt/bin/dlna play \'{dlink}\' -d "http://127.0.0.1:25826"'
        CallBackTerminal = await Terminal.execute(cmd)
        await cb.answer("Paly on your Tv...")

    elif data.startswith('fdelete'):
        none, folder_name = data.split("=")
        shutil.rmtree(folder_name)
        await cb.message.edit_text(f"folder {folder_name} successfully deleted", reply_markup=base_markup)
    elif data == "space":
        await cb.message.edit_text('Checking Again... ⏳')

        try:
            await cb.message.edit_text(get_server_details(), reply_markup=refresh_space)
        except MessageNotModified:
            pass
