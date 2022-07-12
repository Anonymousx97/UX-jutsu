### Made by Ryuk ###
### Based on code from UX ###

import asyncio
import glob
import os
import shlex
import shutil
from os.path import basename
from time import time
from typing import Optional, Tuple

import yt_dlp
from pyrogram import filters
from userge import Config, Message, get_collection, userge
from userge.utils.exceptions import StopConversation

VID_LIST = get_collection("VID_LIST")
CHANNEL = userge.getCLogger(__name__)
_LOG = userge.getLogger(__name__)


@userge.on_cmd(
    "addv",
    about={
        "header": "add chat to Video LIST",
        "usage": "{tr}addv [chat username or id (optional)]",
    },
    allow_bots=False,
    allow_channels=False,
)
async def add_v(message: Message):
    """add chat to Video List."""
    chat_ = message.input_str
    if not chat_:
        chat_ = message.chat.id
    try:
        chat_ = await userge.get_chat(chat_)
    except BaseException:
        await message.edit(f"`Provided input ({chat_}) is not a chat...`", del_in=5)
        return
    chat_type = chat_.type
    if chat_type == "private":
        chat_name = full_name(chat_)
    else:
        chat_name = chat_.title
    chat_id = chat_.id
    found = await VID_LIST.find_one({"chat_id": chat_id})
    if found:
        await message.edit(f"Chat <b>{chat_name}</b> is already in list.", del_in=5)
        return
    await VID_LIST.insert_one(
        {"chat_name": chat_name, "chat_id": chat_id, "chat_type": chat_type}
    )
    msg_ = f"Successfully added <b>{chat_name}</b> (`{chat_id}`) in Video LIST."
    await message.edit(msg_, del_in=5)
    await CHANNEL.log(msg_)


@userge.on_cmd(
    "delv",
    about={
        "header": "delete chat from Video LIST",
        "flags": {
            "-all": "delete all chats from list",
        },
        "usage": "{tr}delv [chat username or id (optional)]",
    },
    allow_bots=False,
    allow_channels=False,
)
async def del_v(message: Message):
    """delete chat from list for Video list"""
    if "-all" in message.flags:
        msg_ = (
            "### <b>DELETING ALL CHATS FROM Video LIST</b> ###\n\n"
            "For confirmation of deleting all chats from Video LIST,\n"
            "please reply with '`Yes, delete all chats in list for video.`' <b>within 10 seconds</b>."
        )
        await message.edit(msg_)
        try:
            async with userge.conversation(message.chat.id, timeout=10) as conv:
                response = await conv.get_response(
                    mark_read=True,
                    filters=(
                        filters.user([one for one in Config.TRUSTED_SUDO_USERS])
                        | filters.me
                    ),
                )
        except (TimeoutError, StopConversation):
            msg_ += "\n\n### Process cancelled as no response given. ###"
            await message.edit(msg_)
            return
        resp = response.text
        if resp == "Yes, delete all chats in list for video.":
            await VID_LIST.drop()
            await message.delete(msg_)
            del_ = "Deleted whole <b>Video LIST</b> successfully."
            await message.edit(del_, del_in=5)
            await CHANNEL.log(del_)
            return

    chat_ = message.input_str
    if not chat_:
        chat_ = message.chat.id
    try:
        chat_ = await userge.get_chat(chat_)
    except BaseException:
        await message.edit(f"`Provided input ({chat_}) is not a chat...`", del_in=5)
        return
    chat_id = chat_.id
    found = await VID_LIST.find_one({"chat_id": chat_id})
    if found:
        msg_ = f"Successfully removed <b>{found['chat_name']}</b> from Video LIST."
        await VID_LIST.delete_one(found)
        await message.edit(msg_, del_in=5)
        await CHANNEL.log(msg_)
        return
    else:
        await message.edit(f"The chat <b>{chat_id}</b> doesn't exist in Video LIST.")


@userge.on_cmd(
    "listv",
    about={
        "header": "list chats in Video List",
        "flags": {
            "-id": "list chat IDs as well",
        },
        "usage": "{tr}listv",
    },
    allow_bots=False,
    allow_channels=False,
)
async def list_video(message: Message):
    """list chats in Video list"""
    s_groups = ""
    s_total = 0
    groups = ""
    g_total = 0
    priv = ""
    p_total = 0
    out_ = "List of chats in <b>Video List</b>: [{}]\n\n"
    async for chat_ in VID_LIST.find():
        chat_id = chat_["chat_id"]
        chat_name = chat_["chat_name"]
        type_ = chat_["chat_type"]
        id_ = f"'`{chat_id}`' - " if "-id" in message.flags else ""
        if type_ == "supergroup":
            s_total += 1
            s_groups += f"• [{s_total}] {id_}<b>{chat_name}</b>\n"
        elif type_ == "group":
            g_total += 1
            groups += f"• [{g_total}] {id_}<b>{chat_name}</b>\n"
        else:
            p_total += 1
            priv += f"• [{p_total}] {id_}<b>{chat_name}</b>\n"
    total_ = s_total + g_total + p_total
    out_ += (
        f"<b>Supergroup/s:</b> [{s_total}]\n"
        f"{s_groups}\n"
        f"<b>Normal group/s:</b> [{g_total}]\n"
        f"{groups}\n"
        f"<b>Private chat/s:</b> [{p_total}]\n"
        f"{priv}"
    )
    out_ = out_.format(total_)
    if len(out_) <= 4096:
        await message.edit(out_)
    else:
        link_ = pt("List of chats in Video List.", out_)
        await message.edit(
            f"List of chats in Video List is <a href='{link_}'><b>HERE</b></a>."
        )


@userge.on_message(
    ~filters.edited
    & (
        filters.regex(r"^https://www.instagram.com/reel/*")
        | filters.regex(r"^https://vm.tiktok.com/*")
        | filters.regex(r"^https://www.instagram.com/tv/*")
        | filters.regex(r"https://twitter.com/*")
        | filters.regex(r"^https://youtube.com/shorts/*")
    )
)
async def my_handler(userge, message: Message):
    chat_id = message.chat.id
    chat = await VID_LIST.find_one({"chat_id": chat_id})
    if chat:
        x = message.text.split()
        for L in x:
            if "http" in L:
                link = L
        starttime = time()
        dl_path = os.path.join(Config.DOWN_PATH, str(starttime))
        try:
            await _tubeDl([link], starttime)
        except Exception as f_e:
            _LOG.exception(f_e)
            CHANNEL.log(f_e)
            return await message.reply("**Link not supported or private.** 🥲")
        _fpath = ""
        for _path in glob.glob(os.path.join(dl_path, "*")):
            if not _path.lower().endswith((".jpg", ".png", ".webp")):
                _fpath = _path
        await take_screen_shot(_fpath, 0.1, starttime)
        _tpath = ""
        for _path in glob.glob(os.path.join(dl_path, "*")):
            if _path.lower().endswith((".jpg", ".png", ".webp")):
                _tpath = _path
        await message.reply_video(video=_fpath, thumb=_tpath)
        if os.path.exists(str(dl_path)):
            shutil.rmtree(dl_path)


async def _tubeDl(url: list, starttime):
    _opts = {
        "outtmpl": os.path.join(
            Config.DOWN_PATH, str(starttime), "vid-%(format)s.%(ext)s"
        ),
        "format": "bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "prefer_ffmpeg": True,
        "postprocessors": [{"key": "FFmpegMetadata"}],
    }
    x = yt_dlp.YoutubeDL(_opts)
    x.download(url)


async def take_screen_shot(video_file: str, duration: int, starttime) -> Optional[str]:
    """take a screenshot"""
    ttl = duration // 2
    thumb_image_path = os.path.join(
        Config.DOWN_PATH, str(starttime), f"{basename(video_file)}.jpg"
    )
    command = f'''ffmpeg -ss {ttl} -i "{video_file}" -vframes 1 "{thumb_image_path}"'''
    (await runcmd(command))[1]
    return thumb_image_path if os.path.exists(thumb_image_path) else None


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


def full_name(user: dict):
    try:
        f_name = " ".join([user.first_name, user.last_name or ""])
    except BaseException:
        raise
    return f_name
