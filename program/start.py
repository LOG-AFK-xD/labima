import asyncio

from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.core import user, bot
from driver.filters import command, other_filters
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dbpunish import is_gbanned_user
from driver.database.dbusers import add_served_user
from driver.database.dblockchat import blacklisted_chats
from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, MessageNotModified
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ **𝐁𝐡𝐞𝐥𝐜𝐨𝐦𝐞 {message.from_user.first_name}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) 𝗮𝗹𝗹𝗼𝘄 𝘆𝗼𝘂 𝘁𝗼 𝗽𝗹𝗮𝘆 𝗺𝘂𝘀𝗶𝗰 𝗼𝗻 𝗴𝗿𝗼𝘂𝗽𝘀 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 𝘁𝗵𝗲 𝗻𝗲𝘄 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺'𝘀 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀 𝐩𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 𝐃𝐞𝐂𝐨𝐝𝐞!**

💡 **𝗙𝗶𝗻𝗱 𝗼𝘂𝘁 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗕𝗼𝘁'𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗮𝗻𝗱 𝗵𝗼𝘄 𝘁𝗵𝗲𝘆 𝘄𝗼𝗿𝗸 𝗯𝘆 𝗰𝗹𝗶𝗰𝗸𝗶𝗻𝗴 𝗼𝗻 𝘁𝗵𝗲 » 📚 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻 !**

❓ **𝗙𝗼𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗮𝗯𝗼𝘂𝘁 𝗮𝗹𝗹 𝗳𝗲𝗮𝘁𝘂𝗿𝗲 𝗼𝗳 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁, 𝗷𝘂𝘀𝘁 𝘁𝘆𝗽𝗲 /help**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴜʀ ᴄʜᴀᴛꜱ 😄", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "😢 ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴍᴇ", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         "😄 ᴄᴏᴍᴍᴀɴᴅꜱ", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "💝 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/DeeCodeDevs")
                ],[
                    InlineKeyboardButton(
                        "👥 ᴏꜰꜰɪᴄɪᴀʟ ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/DeCodeSupport"
                    ),
                    InlineKeyboardButton(
                        "🔥 ᴏꜰꜰɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/DeeCodeBots")
                ],[
                    InlineKeyboardButton(
                        "😁 ᴏꜰꜰɪᴄɪᴀʟ ᴄʜᴀᴛ", url="https://t.me/hindi_shayri_story")
                ],[
                    InlineKeyboardButton(
                        "😉 ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ😍", url="https://github.com/TeamDeeCode/DeCoDeMusic"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )
        

@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(c: Client, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text("❗️ **You've blocked from using this bot!**")
        return
    chat_id = message.chat.id
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    BOT_NAME = (await c.get_me()).first_name
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ Group", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "📣 Channel", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    alive = f"**Hello {message.from_user.mention()}, i'm {BOT_NAME}**\n\n🧑🏼‍💻 My Master: [{ALIVE_NAME}](https://t.me/{OWNER_USERNAME})\n👾 Bot Version: `v{__version__}`\n🔥 Pyrogram Version: `{pyrover}`\n🐍 Python Version: `{__python_version__}`\n✨ PyTgCalls Version: `{pytover.__version__}`\n🆙 Uptime Status: `{uptime}`\n\n❤ **Thanks for Adding me here, for playing video & music on your Group's video chat**"

    await c.send_photo(
        chat_id,
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(c: Client, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text("❗️ **You've blocked from using this bot!**")
        return
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(c: Client, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text("❗️ **You've blocked from using this bot!**")
        return
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )


@Client.on_chat_join_request()
async def approve_join_chat(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    chat_id = m.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if chat_id in await blacklisted_chats():
            await m.reply(
                "❗️ This chat has blacklisted by sudo user and You're not allowed to use me in this chat."
            )
            return await bot.leave_chat(chat_id)
        if member.id == bot_id:
            return await m.reply(
                "❤️ Thanks for adding me to the **Group** !\n\n"
                "Appoint me as administrator in the **Group**, otherwise I will not be able to work properly, and don't forget to type `/userbotjoin` for invite the assistant.\n\n"
                "Once done, then type `/reload`",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 Channel", url=f"https://t.me/{UPDATES_CHANNEL}"),
                            InlineKeyboardButton("💭 Support", url=f"https://t.me/{GROUP_SUPPORT}")
                        ],
                        [
                            InlineKeyboardButton("👤 Assistant", url=f"https://t.me/{ass_uname}")
                        ]
                    ]
                )
            )


chat_watcher_group = 10

@Client.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message: Message):
    if message.from_user:
        user_id = message.from_user.id
        await add_served_user(user_id)
        return
    try:
        userid = message.from_user.id
    except Exception:
        return
    suspect = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"👮🏼 (> {suspect} <)\n\n**Gbanned** user detected, that user has been gbanned by sudo user and was blocked from this Chat !\n\n🚫 **Reason:** potential spammer and abuser."
        )
