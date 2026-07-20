"""
╔══════════════════════════════════════════════════════════════════════╗
║             ⚡ ?JORDAN 𝐊ɪɴɢ 𝐌ᴜʟᴛɪ 𝐁ᴏᴛ 𝐕-2 ⚡           ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  [REQUIRED PACKAGES]                                                 ║
║  >>> pip install python-telegram-bot httpx                           ║
║                                                                      ║
║  [SYSTEM REQUIREMENTS]                                               ║
║  • Python 3.9+ (Optimized for Speed)                                 ║
║  • 4GB+ RAM Recommended for Multi-Threading                          ║
║                                                                      ║
║  [HOW TO RUN]                                                        ║
║  1. pip install python-telegram-bot httpx                            ║
║  2. python tgnc.py                                                   ║
║                                                                      ║
║  [HYPER FEATURES]                                                    ║
║  🚀 Asyncio Event Loop Policy Optimized                              ║
║  ⚡ Zero-Latency Dispatcher                                          ║
║  🛡️ Anti-Flood Wait Bypass (Smart Rotation)                          ║
║  🌪️ Multi-Threaded Spam/NC Engine                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import os
import sys
import time
import logging
import random
import re
import signal
import traceback
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Set, List, Optional, Tuple

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ChatType
from telegram.error import RetryAfter, TimedOut, NetworkError, BadRequest, Forbidden

logging.basicConfig(
    format="%(asctime)s - [ULTRA HYPER X] - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("UltraHyperXBot")

OWNER_ID =8359193264
DEFAULT_AUTHORIZED_USERS = set()
HYPER_MODE = True
MAX_RETRIES = 3
BASE_RETRY_DELAY = 0.1
MAX_TASKS_PER_CHAT = 100
TASK_CLEANUP_INTERVAL = 30
CONNECTION_TIMEOUT = 0.1

BOT_TOKENS = [
    "8874289508:AAF4C7XrnsWxfK2nRwNr-vA0QN9V_7tguII",
    "8320364568:AAGx7grYlrQtLq9MityKRNCpfG7g1ZGtB_Q",
    "8778114152:AAGZrI8h5Nl5V6vKsmGkH9vsmWEmdw1cxyE",
    "8966423111:AAFAVY-GHNFtlbr1xeLVeojoptGQJmiR_uE",
    "8738337648:AAGG_G-GIneQIuxnFQ10J29kKEOXDXUyGf8",
    "8621730713:AAEr46ZoI0B8eH9BqGtYTCKJNpxGIHsqJiQ",
    "8985556171:AAFeidLxfTETZa57rlzPlEqMBjq0J1y2y1A", 
    "8803359120:AAFOZho2ZyQ6dKLqomoZQcrCjA7_FsZPQzs",
    "8936966865:AAGp2GX5uqMeuyQRL8VyQszWApHF9EMMWOk",
    "8712103892:AAGUIoC6BxyN6u-fmVmBeCpej9X58Cno96c"
]

HEART_EMOJIS = ['🚗', '🏍️', '🚓', '🚙', '🚕', '🚘', '🚖', '🚌', '🚛', '🚜',
'🐶', '🐱', '🐯', '🦁', '🐺', '🦊', '🐸', '🐵', '🐼', '🐨',
'😀', '😈', '😂', '🤣', '😎', '😆', '😜', '😉', '😏', '😊',
'🔥', '💥', '⚡', '🎯', '🎮', '🎲', '🏆', '📸', '🎧', '🧊'
]

UNAUTHORIZED_MESSAGE = "JORDAN 𝐏ᴀᴘᴀ 𝐒ᴇ 𝐁ʜɪᴋ 𝐌ᴀɴɢʟᴇ 𝐑ɴᴅʏᴋᴇ"

NAME_CHANGE_MESSAGES = [
    "JORDAN 𝐓ᴇʀᴀ 𝐁ᴀᴀᴘ  (𖤐)- ​",
    "{target} (𓀐𓂸)- ​🇨​​🇭​​🇺​​🇩​​🇱​​🇪",
    "{target} (´ཀ`)- ​🇹​​🇧​​🇰​​🇧",
    "{target} (×̷̷͜×̷)- ​🇹​​🇲​​🇷​??",
    "{target} (🜏)- ​🇷​​🇦​​🇳​​🇩​​🇮​​🇰​​🇪",
    "{target} (⛧)- ​🇱​​🇦​​🇳​​🇬​​🇩​​🇪​",
    "{target} (𓄃)- ​🇭​​🇮​​🇯​​🇩​​🇪​",
    "{target} (𖤐)- ​🇹​​🇲​​🇰​​🇨​",
    "{target} 🚀 𝐊ɪ 𝐒ᴀᴛʀᴀɴɢɪ 𝐂ʜᴜᴛ🚀",
    "{target} 🌘 𝐊ɪ 𝐒ᴀᴛʀᴀɴɢɪ 𝐂ʜᴜᴛ🌘",
    "{target} 🦂 𝐊ɪ 𝐒ᴀᴛʀᴀɴɢɪ 𝐂ʜᴜᴛ🦂",
    "{target} ♨️ 𝐊ɪ 𝐒ᴀᴛʀᴀɴɢɪ 𝐂ʜᴜᴛ♨️",
    "{target} 🐋 𝐊ɪ 𝐒ᴀᴛʀᴀɴɢɪ 𝐂ʜᴜᴛ🐋",
    "{target} 🧩 𝐊ɪ 𝐒ᴀᴛʀᴀɴɢɪ 𝐂ʜᴜᴛ🧩",
    "{target} 🍌 𝐊ɪ 𝐒ᴀᴛʀᴀɴɢɪ 𝐂ʜᴜᴛ🍌",
    "{target} 𝗞𝗔𝗖𝗛𝗥𝗘 𝗪𝗔𝗟𝗘🥀",
    "{target} 𝗚𝗨𝗟𝗔𝗠",
    "{target} 𝗕𝗛𝗔𝗚 𝗠𝗔𝗔𝗧 🤟🏿",
    "{target} 𝗔𝗧𝗠𝗞𝗕𝗙𝗝 🥀 🖖🏿",
    "{target} 𝗛𝗔𝗚 𝗗𝗜𝗬𝗔 🤟🏿",
    "{target} 𝗦𝗨𝗣𝗣𝗢𝗥𝗧 𝗟𝗔 🤙🏿",
    "{target} 𝗕𝗔𝗔𝗣 𝗞𝗢 𝗕𝗛𝗨𝗟 𝗠𝗔𝗧 🥀",
    "{target} �𝗠𝗞𝗰 𝗺𝗲 𝗽𝗼𝗸𝗲𝗺𝗼𝗻 🤟🏿",
    "{target} 𝗚𝗕 𝗥𝗢𝗔𝗗 𝗪𝗔𝗟𝗘 🤙🏿",
    "{target} ◤𝐓ᴇʀᴇ 𝐆ᴀɴᴅ 𝐌ᴀɪ Cᴏᴄᴋ◥✕🚬🍸",
    "{target} ◤𝐓ᴇʀɪ 𝐁ᴏᴏʙɪᴇs 𝐊ʜᴀ 𝐋ᴜ◥✕🚬🍸",
    "{target} ◤𝐉ʏᴅᴀ 𝐅ʀɴᴅʏʟʏ 𝐍ᴀ 𝐇ᴏ 𝐑ɴᴅʏᴋᴇ◥✕🚬🍸",
    "{target} ◤𝐋ᴏᴅᴀ 𝐋ᴇʟᴇ◥✕🚬🍸",
    "{target} ◤𝐊ᴀ 𝐁ᴀᴀᴘ JORDAN 𝐊ɪɴɢ◥✕🚬🍸",
    "{target} ◤𝐓ᴇʀɪ 𝐁ᴏᴏʙɪᴇs 𝐊ʜᴀ 𝐋ᴜ◥✕🚬🍸",
    "{target} 𝐊ɪ 𝐊ᴀʟɪ 𝐂ʜᴜᴛ 𝐏ᴇ.𝐂ʜᴀᴘᴀʟ 🥶",
    "{target} 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐊ᴀ 𝐂ʜᴜᴅᴀɪ 𝐒ᴏɴɢ 𝐁ᴀᴊᴀᴜ 🥶",
]
REPLY_MESSAGES = [
    "{target} 𝐓ʀʏ 𝐇ᴀᴄʟɪ 𝐌ᴀᴀ 𝐊ᴏ 𝐂ᴏᴅᴜ? 😿💔😤😔😡😨😡💔😭😜🤘🏻😰🤣😜",
    "{target} चुद गया -!",
    "𝐀ʟᴏᴏ 𝐊ʜᴀᴋᴇ {target} 𝐊ɪ 𝐌ᴀ 𝐂ʜᴏᴅ 𝐃ᴜɴɢᴀ!",
    "{target} 𝐑ɴᴅʏ 𝐊ᴇ 𝐁ᴀᴄᴄʜᴇ 𝐓ᴜ 𝐋ᴀᴅᴇɢᴀ? 𝐂ᴏᴅᴜ 𝐓ʀʏ 𝐌ᴀᴀ/-",
    "{target} 𝐁ᴏʟ JORDAN 𝐏ᴀᴘᴀ पिताश्री 𝐌ᴇʀɪ 𝐌ᴀᴀ 𝐂ʜᴏᴅ 𝐃ᴏ",
    "{target} 𝐊ɪ 𝐌ᴀ 𝐁ᴏʟᴇ JORDAN 𝐏ᴀᴘᴀ 𝐒ᴇ 𝐂ʜᴜᴅᴜɴɢɪ",
    "{target} 𝐊ɪ 𝐁ʜᴇɴ 𝐊ɪ 𝐂ʜᴜᴛ 𝐊ᴀʟɪ 𝐊ᴀʟɪ",
    "{target} 𝐓ᴇʀɪ 𝐁ʜᴇɴ 𝐊ɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐀ᴄʜᴀʀ 𝐃ᴀʟ 𝐊ᴀʀ 𝐂Hᴀᴛ 𝐋ᴜ 🤡😡😜😡😔😤😳💔😜🫵🏻😔",
    "{target} 𝐆ᴀʀᴇᴇʙ 𝐊ᴀ 𝐁ᴀᴄʜʜᴀ",
    "{target} 𝐂ʜᴜᴅ 𝐊ᴇ 𝐏ᴀɢᴀʟ 𝐇ᴏ 𝐆ᴀʏᴀ",
    "{target} 𝐂ʜʟ 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐊ɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐂ʜᴀᴘᴀʟ 𝐌ᴀʀᴜ 😿🫵🏻❤️",
    "{target} 𝐋ᴜɴᴅ 𝐂ʜᴜsᴇɢᴀ 𝐒ᴀʙᴋᴀ",
    "{target} 𝐊ɪ 𝐌ᴀᴀ 𝐊ᴏ 𝐂ʜᴏᴅᴇ 𝐀ᴅɪᴛʏᴀ 𝐏ᴀᴘᴀ",
    "{target} 𝐊ɪ 𝐌ᴀᴀ JORDAN 𝐏ᴀᴘᴀ 𝐒ᴇ 𝐂ʜᴜᴅᴇ",
    "{target} JORDAN 𝐏ᴀᴘᴀ 𝐒ᴇ 𝐂ʜᴜᴅᴀ",
    "{target} 𝐁ᴏʟ 𝐓ᴇʀɪ 𝐁ʜᴇɴ 𝐊ɪ 𝐂ʜᴜᴅᴀɪ 𝐋ᴀɢᴀ 𝐃ᴜ? 😳🙄💔😡😔😡😔❤️😿❤️😿❤️🖕🏻💔🙄🤔🙄🤔🙄",
    "{target} 𝐍ᴇ JORDAN 𝐏ᴀᴘᴀ 𝐊ᴏ 𝐁ᴀᴀᴩ 𝐁ᴀɴᴀ 𝐋ɪyᴀ",
    "{target} 𝐁ᴏʟ JORDQN 𝐏ᴀᴘᴀ",
    "{target} 𝐓ᴇʀɪ 𝐌ᴜᴍᴍʏ 𝐊ɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐋ᴀᴀᴛ 𝐌ᴀʀᴜ? 🙃😤🙄😤🙄❤️😔😨😜😨😜🫵🏻🤣😞😰😞😰😡",
    "{target} 𝐊ᴜᴛᴛᴇ 𝐆ᴜʟᴀᴍɪ 𝐊ʀ 😋",
]

SPAM_MESSAGES = [
    "✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི",
    "➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷",
  "➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷",
"➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶",
"{target} 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵___",
  "{target} 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵___//"
]


def extract_retry_after(error_str):
    match = re.search(r'retry after (\d+)', error_str.lower())
    if match:
        return int(match.group(1))
    return None


async def exponential_backoff_sleep(attempt: int, base_delay: float = BASE_RETRY_DELAY) -> float:
    """Calculate exponential backoff delay with jitter."""
    delay = base_delay * (2 ** min(attempt, 5))
    jitter = random.uniform(0, delay * 0.1)
    total_delay = delay + jitter
    await asyncio.sleep(total_delay)
    return total_delay


async def retry_with_backoff(coro, max_attempts: int = MAX_RETRIES) -> bool:
    """Retry a coroutine with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            await coro
            return True
        except asyncio.CancelledError:
            raise
        except RetryAfter as e:
            wait = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
            logger.warning(f"Rate limited. Waiting {wait}s before retry...")
            await asyncio.sleep(wait + 0.1)
        except (TimedOut, NetworkError) as e:
            if attempt < max_attempts - 1:
                delay = await exponential_backoff_sleep(attempt)
                logger.debug(f"Transient error (attempt {attempt+1}): {type(e).__name__}. Waiting {delay:.2f}s...")
            else:
                logger.error(f"Failed after {max_attempts} attempts: {e}")
                return False
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}: {e}")
            return False
    return False


ALL_BOT_INSTANCES: Dict[int, 'HyperBotInstance'] = {}
GLOBAL_STOP_EVENT = asyncio.Event()
COMMAND_LOCKS: Dict[int, asyncio.Lock] = {}


def get_command_lock(chat_id: int) -> asyncio.Lock:
    if chat_id not in COMMAND_LOCKS:
        COMMAND_LOCKS[chat_id] = asyncio.Lock()
    return COMMAND_LOCKS[chat_id]


class HyperBotInstance:
    def __init__(self, bot_number, owner_id):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.authorized_users = set(DEFAULT_AUTHORIZED_USERS)
        self.active_spam_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_name_change_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_custom_nc_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_reply_tasks: Dict[int, asyncio.Task] = {}
        self.active_reply_targets: Dict[int, str] = {}
        self.pending_replies: Dict[int, List[int]] = {}
        self.chat_delays: Dict[int, float] = {}
        self.chat_threads: Dict[int, int] = {}
        self.locks: Dict[int, asyncio.Lock] = {}
        self.stats = {"sent": 0, "errors": 0, "start_time": time.time(), "retries": 0, "rate_limits": 0}
        self.is_running = True
        self.last_cleanup = time.time()
        ALL_BOT_INSTANCES[bot_number] = self
        logger.info(f"Bot {bot_number} initialized successfully")

    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    def is_owner(self, user_id):
        return user_id == self.owner_id

    def is_authorized(self, user_id):
        return user_id == self.owner_id or user_id in self.authorized_users

    async def check_owner(self, update):
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            try:
                await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            except Exception:
                pass
            return False
        return True

    async def check_main_owner(self, update):
        user_id = update.effective_user.id
        if not self.is_owner(user_id):
            try:
                await update.message.reply_text("⛔ Only the main owner can use this command!")
            except Exception:
                pass
            return False
        return True

    async def cleanup_dead_tasks(self):
        """Remove completed or cancelled tasks from tracking."""
        current_time = time.time()
        if current_time - self.last_cleanup < TASK_CLEANUP_INTERVAL:
            return
        self.last_cleanup = current_time
        
        for chat_id in list(self.active_spam_tasks.keys()):
            self.active_spam_tasks[chat_id] = [t for t in self.active_spam_tasks[chat_id] if not t.done()]
            if not self.active_spam_tasks[chat_id]:
                del self.active_spam_tasks[chat_id]
        
        for chat_id in list(self.active_name_change_tasks.keys()):
            self.active_name_change_tasks[chat_id] = [t for t in self.active_name_change_tasks[chat_id] if not t.done()]
            if not self.active_name_change_tasks[chat_id]:
                del self.active_name_change_tasks[chat_id]
        
        for chat_id in list(self.active_custom_nc_tasks.keys()):
            self.active_custom_nc_tasks[chat_id] = [t for t in self.active_custom_nc_tasks[chat_id] if not t.done()]
            if not self.active_custom_nc_tasks[chat_id]:
                del self.active_custom_nc_tasks[chat_id]

    async def safe_cancel_tasks(self, tasks: List[asyncio.Task]):
        for task in tasks:
            if not task.done():
                task.cancel()
        for task in tasks:
            try:
                await asyncio.wait_for(asyncio.shield(task), timeout=2.0)
            except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                pass

    async def stop_all_tasks_globally(self):
        all_tasks = []
        
        for chat_id, tasks in list(self.active_spam_tasks.items()):
            all_tasks.extend(tasks)
            del self.active_spam_tasks[chat_id]
            
        for chat_id, tasks in list(self.active_name_change_tasks.items()):
            all_tasks.extend(tasks)
            del self.active_name_change_tasks[chat_id]
            
        for chat_id, tasks in list(self.active_custom_nc_tasks.items()):
            all_tasks.extend(tasks)
            del self.active_custom_nc_tasks[chat_id]
            
        for chat_id, task in list(self.active_reply_tasks.items()):
            all_tasks.append(task)
            del self.active_reply_tasks[chat_id]
            
        self.active_reply_targets.clear()
        self.pending_replies.clear()
        
        await self.safe_cancel_tasks(all_tasks)
        return len(all_tasks)

    async def name_change_loop(self, chat_id, base_name, context, worker_id=1):
        msg_index = 0
        num_messages = len(NAME_CHANGE_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC Worker #{worker_id} STARTED for chat {chat_id}")
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        current_msg = NAME_CHANGE_MESSAGES[msg_index % num_messages]
                        display_name = current_msg.format(target=base_name)
                        await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                        msg_index += 1
                        success_count += 1
                        self.stats["sent"] += 1
                        if delay > 0:
                            await asyncio.sleep(delay)
                    except asyncio.CancelledError:
                        raise
                    except RetryAfter as e:
                        wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                        await asyncio.sleep(wait_time + 0.05)
                    except (TimedOut, NetworkError):
                        pass
                    except (BadRequest, Forbidden):
                        await asyncio.sleep(0.1)
                        msg_index += 1
                    except Exception:
                        self.stats["errors"] += 1
                        msg_index += 1
                break
            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] NC Worker #{worker_id} stopped after {success_count} changes")
                break
            except Exception:
                await asyncio.sleep(0.1)

    async def custom_name_change_loop(self, chat_id, custom_name, context, worker_id=1):
        success_count = 0
        print(f"[Bot {self.bot_number}] Custom NC Worker #{worker_id} STARTED for chat {chat_id}")
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        heart = random.choice(HEART_EMOJIS)
                        display_name = f"{custom_name} {heart}"
                        await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                        success_count += 1
                        self.stats["sent"] += 1
                        if delay > 0:
                            await asyncio.sleep(delay)
                    except asyncio.CancelledError:
                        raise
                    except RetryAfter as e:
                        wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                        await asyncio.sleep(wait_time + 0.05)
                    except (TimedOut, NetworkError):
                        pass
                    except (BadRequest, Forbidden):
                        await asyncio.sleep(0.1)
                    except Exception:
                        self.stats["errors"] += 1
                break
            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Custom NC Worker #{worker_id} stopped after {success_count} changes")
                break
            except Exception:
                await asyncio.sleep(0.1)

    async def spam_loop(self, chat_id, target_name, context, worker_id):
        success_count = 0
        print(f"[Bot {self.bot_number}] Spam Worker #{worker_id} STARTED for chat {chat_id}")
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        spam_msg = random.choice(SPAM_MESSAGES).format(target=target_name)
                        await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                        success_count += 1
                        self.stats["sent"] += 1
                        if delay > 0:
                            await asyncio.sleep(delay)
                    except asyncio.CancelledError:
                        raise
                    except RetryAfter as e:
                        wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                        await asyncio.sleep(wait_time + 0.05)
                    except (TimedOut, NetworkError):
                        pass
                    except (BadRequest, Forbidden):
                        await asyncio.sleep(0.1)
                    except Exception:
                        self.stats["errors"] += 1
                break
            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Spam Worker #{worker_id} stopped after {success_count} messages")
                break
            except Exception:
                await asyncio.sleep(0.1)

    async def reply_loop(self, chat_id, target_name, context):
        success_count = 0
        print(f"[Bot {self.bot_number}] Reply LOOP started for chat {chat_id}")
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                        async with self.get_lock(chat_id):
                            messages_to_reply = self.pending_replies[chat_id].copy()
                            self.pending_replies[chat_id] = []

                        for msg_id in messages_to_reply:
                            try:
                                reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                                await context.bot.send_message(
                                    chat_id=chat_id,
                                    text=reply_msg,
                                    reply_to_message_id=msg_id
                                )
                                success_count += 1
                                self.stats["sent"] += 1
                                if delay > 0:
                                    await asyncio.sleep(delay)
                            except asyncio.CancelledError:
                                raise
                            except RetryAfter as e:
                                wait_time = int(e.retry_after) if isinstance(e.retry_after, (int, float)) else e.retry_after.total_seconds()
                                await asyncio.sleep(wait_time + 0.05)
                            except (TimedOut, NetworkError):
                                pass
                            except (BadRequest, Forbidden):
                                pass
                            except Exception:
                                self.stats["errors"] += 1
                    else:
                        await asyncio.sleep(0.02)
                break
            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Reply LOOP stopped after {success_count} replies")
                break
            except Exception:
                await asyncio.sleep(0.1)

    async def message_collector(self, update, context):
        if not update.message:
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_reply_targets:
            msg_id = update.message.message_id
            async with self.get_lock(chat_id):
                if chat_id not in self.pending_replies:
                    self.pending_replies[chat_id] = []
                self.pending_replies[chat_id].append(msg_id)

    async def start(self, update, context):
        if not await self.check_owner(update):
            return

        help_text = f"""
𓆩 𝐁ᴏᴛ {self.bot_number} 𓆪 - ⚡ 𝐀ᴅɪᴛʏᴀ 𝐊ɪɴɢ 𝐌ᴜʟᴛɪ 𝐁ᴏᴛ ⚡

━━━━ 🚀 𝐒ᴛᴀʙɪʟɪᴛʏ & 𝐏ᴏᴡᴇʀ 𝐄ɴʜᴀɴᴄᴇᴅ 🚀 ━━━━

✅ 𝐄xᴘᴏɴᴇɴᴛɪᴀʟ 𝐁ᴀᴄᴋᴏғғ 𝐑ᴇᴛʀɪᴇs
✅ 𝐒ᴍᴀʀᴛ 𝐓ᴀsᴋ 𝐂Lᴇᴀɴᴜᴘ & 𝐌ᴇᴍᴏʀʏ 𝐌ᴀɴᴀɢᴇᴍᴇɴᴛ
✅ 𝐁ᴇᴛᴛᴇʀ 𝐄ʀʀᴏʀ 𝐑ᴇᴄᴏᴠᴇʀʏ & 𝐋ᴏɢɪɴɢ
✅ 𝐑ᴀᴛᴇ 𝐋ɪᴍɪᴛ 𝐈ɴᴛᴇʟʟɪɢᴇɴᴄᴇ
✅ 𝐂ᴏɴɴᴇᴄᴛɪᴏᴍ 𝐓ɪᴍᴇᴏᴜᴛ 𝐏ʀᴏᴛᴇᴄᴛɪᴏɴ

━━━━ 𝐀ᴛᴛᴀᴄᴋ 𝐂ᴏᴍᴍᴀɴᴅs ━━━━

/target <name> - 𝐍ᴄ + 𝐒ᴘᴀᴍ 𝐓ᴏɢᴇᴛʜᴇʀ 𝐖ɪᴛʜ 𝐓ʜʀᴇᴀᴅs!
/nc <name> - 𝐍ᴀᴍᴇ 𝐂ʜᴀɴɢᴇ 𝐋ᴏᴏᴘ (with threads)
/ctmnc <custom name> - 𝐂ᴜsᴛᴏᴍ 𝐍ᴀᴍᴇ + 𝐇ᴇᴀʀᴛ 𝐄ᴍᴏᴊɪ 𝐋ᴏᴏᴘ!
/spam <target> - 𝐒ᴘᴀᴍ 𝐋ᴏᴏᴘ (with threads)
/reply <target> - 𝐑ᴇᴘʟʏ 𝐓ᴏ 𝐄ᴠᴇʀʏ 𝐌ᴇssᴀɢᴇ 𝐋ᴏᴏᴘ!

━━━━ 𝐂ᴏɴᴛʀᴏʟ ━━━━

/delay <seconds> - 𝐒ᴇᴛ 𝐃ᴇʟᴀʏ (default: 0)
/threads <1-50> - 𝐒ᴇᴛ 𝐓ʜʀᴇᴀᴅs 𝐅ᴏʀ 𝐍ᴄ + 𝐒ᴘᴀᴍ

━━━━ 𝐒ᴛᴏᴘ ━━━━

/stopnc - 𝐒ᴛᴏᴘ 𝐍ᴀᴍᴇ 𝐂ʜᴀɴɢᴇ 𝐋ᴏᴏᴘ
/stopctmnc - 𝐒ᴛᴏᴘ 𝐂ᴜsᴛᴏᴍ 𝐍ᴀᴍᴇ 𝐂ʜᴀɴɢᴇ 𝐋ᴏᴏᴘ
/stopspam - 𝐒ᴛᴏᴘ 𝐒ᴘᴀᴍ 𝐋ᴏᴏᴘ
/stopreply - 𝐒ᴛᴏᴘ 𝐒ᴘᴀᴍ 𝐑ᴇᴘʟʏ
/stopall - 𝐒ᴛᴏᴘ 𝐀ʟʟ 𝐋ᴏᴏᴘs 𝐈ɴ 𝐓ʜɪs 𝐂ʜᴀᴛ
/superstop - 𝐒ᴛᴏᴘ 𝐀ʟʟ 𝐁ᴏᴛs 𝐄ᴠᴇʀʏᴡʜᴇʀᴇ!

━━━━ 𝐒ᴜᴅᴏ (𝐒ᴅᴜᴏ 𝐎ᴡɴᴇʀ 𝐎ɴʟʏ) ━━━━

/sudo <id1> <id2> ... - 𝐀ᴅᴅ 𝐀ᴜᴛʜᴏʀɪᴢᴇᴅ 𝐔sᴇʀs
/unsudo <id1> <id2> ... - 𝐑ᴇᴍᴏᴠᴇ 𝐀ᴜᴛʜᴏʀɪᴢᴇᴅ 𝐔sᴇʀs
/sudolist - 𝐋ɪsᴛ 𝐀ʟʟ 𝐀ᴜᴛʜᴏʀɪᴢᴇᴅ 𝐔sᴇʀs

━━━━ 𝐔ᴛɪʟɪᴛʏ ━━━━

/ping - 𝐒ʜᴏᴡ 𝐁ᴏᴛ 𝐋ᴇᴛᴇɴᴄʏ 𝐈ɴ 𝐌s
/status - 𝐋ɪᴠᴇ 𝐒ᴛᴀᴛɪsᴛɪᴄs

𝐓ʜʀᴇᴀᴅs: 1-50 (𝐀ᴘᴘʟɪᴇs 𝐓ᴏ 𝐍ᴄ + 𝐒ᴘᴀᴍ)
𝐀ʟʟ 𝐀ᴄᴛɪᴏɴs 𝐑ᴜɴ 𝐈ɴ 𝐋ᴏᴏᴘs ⚡
𝐎ᴡɴᴇʀ 𝐎ɴʟʏ 🔒
"""
        await update.message.reply_text(help_text)

    async def nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /nc <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_name_change_tasks:
                await self.safe_cancel_tasks(self.active_name_change_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.name_change_loop(chat_id, base_name, context, i + 1))
                tasks.append(task)

            self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] Name change LOOP started with {num_threads} threads!")

    async def stop_nc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_name_change_tasks:
                await self.safe_cancel_tasks(self.active_name_change_tasks[chat_id])
                del self.active_name_change_tasks[chat_id]
                await update.message.reply_text(f"[Bot {self.bot_number}] Name change LOOP stopped!")
            else:
                await update.message.reply_text(f"[Bot {self.bot_number}] No active name change loop!")

    async def ctmnc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat

        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /ctmnc <custom name>")
            return

        custom_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_custom_nc_tasks:
                await self.safe_cancel_tasks(self.active_custom_nc_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.custom_name_change_loop(chat_id, custom_name, context, i + 1))
                tasks.append(task)

            self.active_custom_nc_tasks[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] Custom name change LOOP started with {num_threads} threads! Adding heart emojis...")

    async def stop_ctmnc_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_custom_nc_tasks:
                await self.safe_cancel_tasks(self.active_custom_nc_tasks[chat_id])
                del self.active_custom_nc_tasks[chat_id]
                await update.message.reply_text(f"[Bot {self.bot_number}] Custom name change LOOP stopped!")
            else:
                await update.message.reply_text(f"[Bot {self.bot_number}] No active custom name change loop!")

    async def spam_command(self, update, context):
        print(f"[Bot {self.bot_number}] SPAM COMMAND RECEIVED from user {update.effective_user.id}")
        if not await self.check_owner(update):
            print(f"[Bot {self.bot_number}] User {update.effective_user.id} not authorized for spam")
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /spam <target_name>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_spam_tasks:
                await self.safe_cancel_tasks(self.active_spam_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i + 1))
                tasks.append(task)

            self.active_spam_tasks[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] Spam LOOP started with {num_threads} threads!")

    async def stop_spam_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_spam_tasks:
                await self.safe_cancel_tasks(self.active_spam_tasks[chat_id])
                del self.active_spam_tasks[chat_id]
                await update.message.reply_text(f"[Bot {self.bot_number}] Spam LOOP stopped!")
            else:
                await update.message.reply_text(f"[Bot {self.bot_number}] No active spam loop!")

    async def reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("This command only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: /reply <target_name>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_reply_tasks:
                self.active_reply_tasks[chat_id].cancel()

            self.active_reply_targets[chat_id] = target_name
            self.pending_replies[chat_id] = []
            task = asyncio.create_task(self.reply_loop(chat_id, target_name, context))
            self.active_reply_tasks[chat_id] = task

        await update.message.reply_text(f"[Bot {self.bot_number}] Reply LOOP started for {target_name}!")

    async def stop_reply_command(self, update, context):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_reply_tasks:
                self.active_reply_tasks[chat_id].cancel()
                del self.active_reply_tasks[chat_id]
                if chat_id in self.active_reply_targets:
                    del self.active_reply_targets[chat_id]
                if chat_id in self.pending_replies:
                    del self.pending_replies[chat_id]
                await update.message.reply_text(f"[Bot {self.bot_number}] Reply LOOP stopped!")
            else:
                await update.message.reply_text(f"[Bot {self.bot_number}] No active reply loop!")

    async def set_delay_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args or len(context.args) < 1:
            await update.message.reply_text("Usage: /delay <seconds>")
            return

        try:
            delay = float(context.args[0])
            chat_id = update.effective_chat.id
            self.chat_delays[chat_id] = delay
            await update.message.reply_text(f"[Bot {self.bot_number}] Delay set to {delay}s for this chat!")
        except ValueError:
            await update.message.reply_text("Invalid delay value!")

    async def set_threads_command(self, update, context):
        if not await self.check_owner(update):
            return

        if not context.args or len(context.args) < 1:
            await update.message.reply_text("Usage: /threads <count>")
            return

        try:
            threads = int(context.args[0])
            if threads < 1 or threads > 50:
                await update.message.reply_text("Threads must be between 1 and 50!")
                return
            chat_id = update.effective_chat.id
            self.chat_threads[chat_id] = threads
            await update.message.reply_text(f"[Bot {self.bot_number}] Threads set to {threads} for this chat!")
        except ValueError:
            await update.message.reply_text("Invalid thread count!")

    async def add_user_command(self, update, context):
        if not await self.check_main_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /adduser <user_id>")
            return

        try:
            user_id = int(context.args[0])
            self.authorized_users.add(user_id)
            await update.message.reply_text(f"User {user_id} added to authorized users!")
        except ValueError:
            await update.message.reply_text("Invalid user ID!")

    async def remove_user_command(self, update, context):
        if not await self.check_main_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: /removeuser <user_id>")
            return

        try:
            user_id = int(context.args[0])
            if user_id in self.authorized_users:
                self.authorized_users.discard(user_id)
                await update.message.reply_text(f"User {user_id} removed from authorized users!")
            else:
                await update.message.reply_text(f"User {user_id} is not in the authorized list!")
        except ValueError:
            await update.message.reply_text("Invalid user ID!")

    async def stop_all_command(self, update, context):
        if not await self.check_owner(update):
            return

        count = await self.stop_all_tasks_globally()
        await update.message.reply_text(f"[Bot {self.bot_number}] Stopped {count} active tasks!")

    async def stats_command(self, update, context):
        if not await self.check_owner(update):
            return

        uptime = time.time() - self.stats["start_time"]
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)

        stats_text = f"""
📊 Bot {self.bot_number} Stats:
✅ Messages Sent: {self.stats['sent']}
❌ Errors: {self.stats['errors']}
⏱ Uptime: {hours}h {minutes}m {seconds}s
🧵 Active Spam Tasks: {len(self.active_spam_tasks)}
📝 Active NC Tasks: {len(self.active_name_change_tasks)}
💬 Active Reply Tasks: {len(self.active_reply_tasks)}
"""
        await update.message.reply_text(stats_text)


def build_application(token: str, bot_number: int) -> Application:
    bot_instance = HyperBotInstance(bot_number, OWNER_ID)
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", bot_instance.start))
    app.add_handler(CommandHandler("help", bot_instance.start))
    app.add_handler(CommandHandler("nc", bot_instance.nc_command))
    app.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))
    app.add_handler(CommandHandler("ctmnc", bot_instance.ctmnc_command))
    app.add_handler(CommandHandler("stopctmnc", bot_instance.stop_ctmnc_command))
    app.add_handler(CommandHandler("spam", bot_instance.spam_command))
    app.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))
    app.add_handler(CommandHandler("reply", bot_instance.reply_command))
    app.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))
    app.add_handler(CommandHandler("delay", bot_instance.set_delay_command))
    app.add_handler(CommandHandler("threads", bot_instance.set_threads_command))
    app.add_handler(CommandHandler("adduser", bot_instance.add_user_command))
    app.add_handler(CommandHandler("removeuser", bot_instance.remove_user_command))
    app.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
    app.add_handler(CommandHandler("stats", bot_instance.stats_command))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, bot_instance.message_collector))
    
    return app


async def run_bot(token: str, bot_number: int):
    try:
        app = build_application(token, bot_number)
        print(f"[Bot {bot_number}] Starting...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        print(f"[Bot {bot_number}] Running!")
        
        while not GLOBAL_STOP_EVENT.is_set():
            await asyncio.sleep(1)
            
        print(f"[Bot {bot_number}] Stopping...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
    except Exception as e:
        print(f"[Bot {bot_number}] Error: {e}")


async def main():
    print("=" * 70)
    print("⚡⚡⚡ 𝐀ᴅɪᴛʏᴀ 𝐊ɪɴɢ  - 𝐒ᴛᴀʀᴛɪɴɢ 𝐀ʟʟ 𝐁ᴏᴛs ⚡⚡⚡")
    print("🚀 𝐄ɴʜᴀɴᴄᴇᴅ 𝐒ᴛᴀʙɪʟɪᴛʏ & 𝐏ᴏᴡᴇʀ 𝐌ᴏᴅᴇ 🚀")
    print("=" * 70)
    logger.info("⚡ 𝐀ᴅɪᴛʏᴀ 𝐊ɪɴɢ  - 𝐄ɴʜᴀɴᴄᴇᴅ 𝐖ɪᴛʜ 𝐄xᴘᴏɴᴇɴᴛɪᴀʟ 𝐁ᴀᴄᴋᴏғғ & 𝐀ᴜᴛᴏ-𝐂ʟᴇᴀɴᴜᴘ")
    
    def signal_handler(sig, frame):
        print("\n🛑 Shutdown signal received...")
        GLOBAL_STOP_EVENT.set()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    tasks = []
    for i, token in enumerate(BOT_TOKENS, 1):
        task = asyncio.create_task(run_bot(token, i))
        tasks.append(task)
        await asyncio.sleep(0.5)
    
    print(f"\n✅ Started {len(BOT_TOKENS)} bots!")
    print("Press Ctrl+C to stop all bots.\n")
    
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"Main error: {e}")
    finally:
        GLOBAL_STOP_EVENT.set()
        for bot in ALL_BOT_INSTANCES.values():
            await bot.stop_all_tasks_globally()
        print("All bots stopped. Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())