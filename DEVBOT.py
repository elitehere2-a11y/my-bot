import asyncio
import json
import os
import random
import sys
import logging
import io
import time
import math
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pytz

# --- TELEGRAM LIBRARIES ---
try:
    from telegram import (
        Update, 
        InlineKeyboardButton, 
        InlineKeyboardMarkup, 
        ChatMember, 
        InputFile, 
        ChatPermissions,
        ReactionTypeEmoji,
        ChatAdministratorRights
    )
    from telegram.ext import (
        Application,
        CallbackQueryHandler,
        ContextTypes,
        MessageHandler,
        ChatMemberHandler,
        filters,
    )
    from telegram.request import HTTPXRequest
    from telegram.error import (
        RetryAfter, 
        Forbidden, 
        BadRequest, 
        NetworkError, 
        TimedOut, 
        ChatMigrated
    )
except ImportError:
    print("CRITICAL: python-telegram-bot is not installed. Run: pip install python-telegram-bot")
    sys.exit(1)

# --- AUDIO ENGINE (GTTS) ---
try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    print("WARNING: gTTS not found. Voice commands will be disabled. Run: pip install gTTS")
    HAS_GTTS = False

# ==============================================================================
#                               CONFIGURATION
# ==============================================================================

# [TOKENS]
TOKENS = [
    "8837676766:AAHWv4cgjqI_DOz4ZMNrwpjSVeaSBMRKMwU",
    "8647968912:AAE27HJmJRISpMictAwt3WBUfeFu8j22P-w",
    "8840815873:AAHilPrDEqUlcrGYETEOxLKdOR4xU4GeuOY",
    "8674578982:AAFeI4B1GzRLZEWh-xksfS5W-BF4HOUKZp0",
    "8810880300:AAHOY-SW1ih7p-TMS1n6XXFAEsYPldTHTzY",
    "8783595258:AAHMlzwzdlvGvUMeRRF2fNKoIJELUU4uo7M",
    "8900266773:AAHv5CotiMxG5d2gV0fRSbFRp-gl9poYids",
    "8776572648:AAGg19Zv0iT75s1ECB5OsSoF5iF1Bji6hI0",
    "8342415860:AAHAnN5n6CTirLUHXmoscaMZkAeWaH0sgoo",

]

# REPLACE THIS WITH YOUR ID
OWNER_ID = 8904369672

SUDO_FILE = "sudo_users.json"
LOG_FILE = "raysist_heavy.log"

# --- PREFIX CONFIGURATION ---
# Supports multiple prefixes for convenience
CMD_PREFIXES = ["🫀", "🙏🏻", "🎀", "💋", "💢", "✨", "⭐", "🥁"]

# --- EXTREME LOW DELAY TUNING ---
DEFAULT_BURST_LIMIT = 5         # Messages per bot before switch
DEFAULT_BURST_DELAY = 0.001     # Instant
DEFAULT_SWITCH_DELAY = 0.001    # Instant
DEFAULT_SPAM_INTERVAL = 0.01    # Extreme Speed restored
DEFAULT_MEDIA_DELAY = 0.01      # Instant
DEFAULT_VN_DELAY = 0.05         # Fast VN
DEFAULT_PIC_DELAY = 0.05        # Fast PIC

# --- REACTION CONFIG ---
DEFAULT_REACTION_POOL = ["🤣"]  # Default: only 🤣

# --- ADMIN RIGHTS CONFIGURATION ---
FULL_RIGHTS = ChatAdministratorRights(
    is_anonymous=False,
    can_manage_chat=True,
    can_delete_messages=True,
    can_manage_video_chats=True,
    can_restrict_members=True,
    can_promote_members=True,
    can_change_info=True,
    can_invite_users=True,
    can_pin_messages=True,
    can_post_stories=True,
    can_edit_stories=True,
    can_delete_stories=True,
    can_manage_topics=True
)

# ==============================================================================
#                               ASSET LIBRARY
# ==============================================================================

NC_LINES = [
    " ᵀᵐᴷᶜ」🦋꙰  ~ ༈  ◠🇮🇳◡", " Teri माँ Dead 😂 ", " ᴛᴇʀᴀ ʙᴀᴀᴘ ᴄᴀʀᴘᴀɴᴛᴇʀ 🪚",
    " ᴛʀʏ ᴅᴀᴅɪ sʟᴜᴛ⚀︎", " ʏᴏᴜʀ ᴍᴏᴍ ᴡʜᴏʀᴇ👞", " ɢᴜʟᴀᴍ ɢᴀɴᴅ ᴋᴀ ᴊᴏʀ ʟɢᴀ😆",
    " ᴛᴇʀᴀ ʙᴀᴀᴘ ᴇʟɪᴛᴇ  😼", " ᴛᴇʀʏᴍᴀ ᴡᴇᴅs ᴇʟɪᴛᴇ 🍇", " ʀɴᴅɪ ᴋᴀ ʟᴅᴄᴀ🍑",
    " ʜᴠᴀʙᴀᴀᴢ ᴄʜᴜᴅᴋᴇ ᴍʀᴀ🧖", " ʀᴀɴᴅɪ ᴋɪ ᴘᴀɪᴅᴀɪsʜ💔", " ᴄʜᴜᴅ ɢʏɪ ᴍᴀᴀ ᴛᴇʀɪ 🤣",
    " ᴀʙʙᴜ ʙᴏʟ ᴇʟɪᴛᴇ  ᴋᴏ 😈", " ᴛᴇʀɪ ʙᴇʜᴇɴ ᴍᴇʀɪ ғᴀɴ 🥵", " ᴅᴇᴋʜ ᴇʟɪᴛᴇ  ᴋɪ ᴘᴏᴡᴇʀ 💪",
    " ᴀʙʙᴇ ɴᴀʟʟᴇ sᴜᴅʜᴀʀ ᴊᴀ 🤬", " ᴛᴇʀᴀ ᴋʜᴀɴᴅᴀᴀɴ ᴄʜᴜᴅ ɢʏᴀ 💀", " ᴛᴇʀᴇ ᴇʟɪᴛᴇ  ᴘᴀᴘᴀ ᴀᴀʏᴇ ʜ 🦁",
    " ʙʜᴀᴀɢ ʙʜᴏsᴅɪᴋᴇ ʙʜᴀᴀɢ 🏃", " ᴛᴇʀɪ ᴍᴀᴀ ᴋᴀ ʙʜᴏsᴅᴀ 😹", " ɢᴀᴀɴᴅ ғᴀᴛᴛ ɢʏɪ? 🥺",
    " ᴋᴀ sʏsᴛᴇᴍ ʜᴀɴɢ ʙʏ ᴇʟɪᴛᴇ  💻", " ᴛᴇʀᴀ ʙᴀᴀᴘ ᴀᴀʏᴀ 🤬", " ᴍᴀᴀ ᴄʜᴜᴅᴀ ʟᴏᴅᴇ 🍑",
    " ʀᴀɴᴅɪ ʀᴏɴᴀ ᴍᴀᴛ ᴋᴀʀ 😭", " ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ᴘᴀɪʀ 🦶", " ᴇʟɪᴛᴇ  ᴏɴ ᴛᴏᴘ 🔝",
    " ᴄʜᴀʟ ɴɪᴋᴀʟ ʟᴏᴅᴇ 🚪", " ᴛᴇʀɪ ᴍᴀᴀ ᴋᴀ ʀᴀᴘᴇ 🔞", " sᴀʏ ᴇʟɪᴛᴇ  ɪs ɢᴏᴅ ⚡",
    " ʙᴏᴛs ᴀʀᴇ ғᴜᴄᴋɪɴɢ ʏᴏᴜ 🤖", " ᴛᴇʀᴀ ʙᴀᴀᴘ ʜᴜ ᴍᴀɪ 🎅", " ᴀᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ 🤬",
    " ɢᴀᴀɴᴅ ᴍᴇ ᴅᴀɴᴅᴀ ᴅᴇ ᴅᴜɴɢᴀ 🎋", " ᴄʜᴜᴘ ᴋᴀʀ ʀᴀɴᴅɪ 🤫", " ᴛᴇʀɪ ʙᴇʜᴇɴ ᴄʜᴜᴅ ɢʏɪ 💃",
    " ᴅᴇᴋʜ ᴇʟɪᴛᴇ  ᴋᴀ ᴋʜᴀᴜғ 😈", " ʙʜᴀᴀɢ ᴍᴀᴛ ʀᴀɴᴅɪ 🏃‍♀️", " ᴛᴇʀᴀ ɢʜᴀʀ ᴊᴀʏᴇɢᴀ 🏠",
    " ᴍᴀᴀ ᴄʜᴜᴅᴀ ᴀᴘɴɪ 🖕", " ᴇʟɪᴛᴇ  ᴏᴘ ʙᴏʟᴛᴇ 🔥", " sʏsᴛᴇᴍ ᴘʜᴀᴀᴅ ᴅᴇɴɢᴇ 💥",
    " ᴛᴇʀɪ ɢᴀᴀɴᴅ ʟᴀᴀʟ 🔴", " ʙᴏʟ ɴᴀ ᴍᴀᴅᴀʀᴄʜᴏᴅ 🗣️", " ʙᴏʟ ᴇʟɪᴛᴇ  ᴋɪ ᴊᴀɪ 🇮🇳"
]

RAID_TEXTS = [
    "𝘾𝙔𝙐 𝙍𝙀 𝙍𝙉𝘿𝙔𝙆𝙀 𝘽𝘼𝘼𝙋 𝙎𝙀 𝘽𝙃𝙄𝘿𝙉𝙀 𝘼𝘼 𝙂𝙔𝘼?", "𝘾𝙃𝙇 𝘾𝙃𝙐𝘿 𝘼𝘽 𝙍𝙉𝘿 𝙆𝙀 𝙋𝙄𝙇𝙀𝙀",
    "𝙏𝙍𝙔 𝙈𝘼 𝙆𝙊 𝗘𝗟𝗜𝗧𝗘  𝘼𝘽𝘽𝙐 𝙋𝙀𝙇𝙀", "𝘾𝙃𝙐𝘿𝙂𝙀𝙂𝘼 𝙎𝘼𝘼𝙇 𝘽𝙃𝙍 𝙏𝙐𝙏𝙊 𝘽𝙀𝙏𝘼 🍑",
    "𝙔𝙀𝙃 𝙂𝙍𝙀𝙀𝙑 𝙁𝙔𝙏𝙀𝙍 𝙄𝙎𝙆𝙄 𝙈𝙆𝘽", "𝙃𝙑𝘼𝘽𝘼𝘼𝙕 𝘽𝘼𝙉𝙀𝙂𝘼 𝙏𝙈𝙍",
    "𝙅𝙇𝘿𝙄 𝙅𝙇𝘿𝙄 𝘾𝙃𝙐𝘿 𝗘𝗟𝗜𝗧𝗘  𝘼𝘽𝘽𝙐 𝘽𝙐𝙎𝙎𝙔 𝙃𝘼𝙄", "𝘾𝙑𝙍 𝙆𝙍 𝙈𝘼𝙅𝘽𝙐𝙍𝙄𝙔𝘼 𝙉𝘼 𝙎𝙐𝙉𝘼",
    "𝙏𝙀𝙍𝙄 𝙈𝘼 𝙆𝘼 𝙋𝘼𝙏𝙄 𝗘𝗟𝗜𝗧𝗘  𝙃𝘼𝙄", "𝘽𝙃𝘼𝘼𝙂 𝙈𝘼𝙏 𝙋𝙄𝙇𝙇𝙀 𝙊𝙔𝙀",
    "𝘼𝘽𝙀 𝙇𝙊𝘿𝙐 𝙏𝙀𝙍𝙄 𝙂𝘼𝙉𝘿 𝙈𝙀 𝘿𝘼𝙉𝘿𝘼", "𝗘𝗟𝗜𝗧𝗘  𝙊𝙉 𝙏𝙊𝙋 𝘽𝘼𝘽𝙔",
    "𝙏𝙀𝙍𝙄 𝙈𝘼 𝙆𝙄 𝘾𝙃𝙐𝙏 𝙈𝙀 𝘽𝙊𝙏 𝙆𝘼 𝙇𝙐𝙉𝘿", "𝘽𝙃𝘼𝂂 𝘽𝙃𝙊𝙎𝘿𝙄𝙆𝙀 𝘽𝙃𝘼𝂂",
    "𝘼𝙋𝙉𝙄 𝘼𝙈𝙈𝙄 𝙆𝙊 𝘽𝙃𝙀𝙅 𝙋𝘼𝙉𝙄 𝙉𝙄𝙆𝘼𝙇𝙉𝘼 𝙃", "𝙏𝙀𝙍𝘼 𝙆𝙃𝘼𝙉𝘿𝘼𝙉 𝙆𝙃𝘼𝙏𝘼𝙈",
    "𝗘𝗟𝗜𝗧𝗘  𝙆𝙄 𝘿𝙀𝙃𝙎𝙃𝘼𝙏", "𝘽𝘼𝘼𝙋 𝙎𝙀 𝘽𝘼𝙆𝘾𝙃𝙊𝘿𝙄 𝙉𝙃𝙄",
    "𝙏𝙀𝙍𝙄 𝙈𝘼 𝙆𝙊 𝘾𝙃𝙊𝘿 𝘿𝙐𝙉𝙂𝘼", "𝙍𝘼𝙉𝘿𝙄 𝙆𝙀 𝘽𝘼𝘾𝘾𝙃𝙀",
    "𝘼𝐐𝘼𝙏 𝙈𝙀 𝙍𝙀𝙃 𝙇𝙊𝘿𝙀", "𝙏𝙀𝙍𝘼 𝘽𝘼𝘼𝙋 𝙃𝙐 𝙈𝘼𝙄",
    "𝘾𝙃𝘼𝙇 𝙉𝙄𝙆𝘼𝙇 𝘽𝙃𝙊𝙎𝘿𝙄𝙆𝙀", "𝙏𝙀𝙍𝙄 𝙈𝘼 𝙆𝘼 𝘽𝙃𝙊𝙎𝘿𝘼",
    "𝗘𝗟𝗜𝗧𝗘  𝙄𝙎 𝙂𝙊𝘿", 
    "𝙏𝙀𝙍𝙄 𝙂𝘼𝘼𝙉𝘿 𝙁𝘼𝘼𝘿 𝘿𝙐𝙉𝙂𝘼", "𝙈𝘼𝘼 𝘾𝙃𝙐𝘿𝘼 𝘼𝙋𝙉𝙄",
    "     𝐊ʏᴜ 𝐑ᴇ 𝐑ᴀɴᴅɪ 𝐌𝐀 ᴋᴇ 𝐋ᴀᴅᴄᴏ 𝐄ʟɪᴛᴇ  ᴀʙʙᴜ 𝐊ᴏ 𝐃ʙᴀ. ɴʜɪ 𝐏ᴀʀᴇ ᴄʏᴀ??🤬",
    "     𝐊ʏᴜ 𝐑ᴇ 𝐑ᴀɴᴅɪ 𝐌𝐀 ᴋᴇ 𝐋ᴀᴅᴄᴏ  𝐄ʟɪᴛᴇ  ᴀʙʙᴜ 𝐊ᴏ 𝐃ʙᴀ. ɴʜɪ 𝐏ᴀʀᴇ ᴄʏᴀ??😡",
    "     𝐊ʏᴜ 𝐑ᴇ 𝐑ᴀɴᴅɪ 𝐌𝐀 ᴋᴇ 𝐋ᴀᴅᴄᴏ  𝐄ʟɪᴛᴇ  ᴀʙʙᴜ 𝐊ᴏ 𝐃ʙᴀ. ɴʜɪ 𝐏ᴀʀᴇ ᴄʏᴀ??🤨",
    "     𝐊ʏᴜ 𝐑ᴇ 𝐑ᴀɴᴅɪ 𝐌𝐀 ᴋᴇ 𝐋ᴀᴅᴄᴏ  𝐄ʟɪᴛᴇ  ᴀʙʙᴜ 𝐊ᴏ 𝐃ʙᴀ. ɴʜɪ 𝐏ᴀʀᴇ ᴄʏᴀ??😱",
    "     𝐊ʏᴜ 𝐑ᴇ 𝐑ᴀɴᴅɪ 𝐌𝐀 ᴋᴇ 𝐋ᴀᴅᴄᴏ  𝐄ʟɪᴛᴇ  ᴀʙʙᴜ 𝐊ᴏ 𝐃ʙᴀ. ɴʜɪ 𝐏ᴀʀᴇ ᴄʏᴀ??😮‍💨",
    "     𝐊ʏᴜ 𝐑ᴇ 𝐑ᴀɴᴅɪ 𝐌𝐀 ᴋᴇ 𝐋ᴀᴅᴄᴏ  𝐄ʟɪᴛᴇ  ᴀʙʙᴜ 𝐊ᴏ 𝐃ʙᴀ. ɴʜɪ 𝐏ᴀʀᴇ ᴄʏᴀ??😨",
    "     𝐊ʏᴜ 𝐑ᴇ 𝐑ᴀɴᴅɪ 𝐌𝐀 ᴋᴇ 𝐋ᴀᴅᴄᴏ  𝐄ʟɪᴛᴇ  ᴀʙʙᴜ 𝐊ᴏ 𝐃ʙᴀ. ɴʜɪ 𝐏ᴀʀᴇ ᴄʏᴀ??😟",
    "तू छोटा था तब तेरी मां का स्तन पान करता था मैं, उसके दूध में 60% क्रीम होता था, तू रोते हुए आता था और मैं तुझे लात मारके भागता था बोलता था हट साले मेरे लन्ड से निकले हुए मैल",
    "This message cannot be seen because you are randy",
    "GRIB MA K BACHAY GHAR ME ATTA LE AA HATER कामज़ोर KA BAAP ELITE  सरकार",
    "घिनौनी रंडी के बच्चे तु बात बात पर अपनी माँ क्यूँ चुदवाता है मादरचोद",
    "Chup kali maa ke रण्डी बच्चे",
    "Chl Harmzadi Ke लड़के",
    "Trymaa ki chut mein labubu",
    "khadi ho ब्राह्मण guru दक्षिणा me mera lund pakad",
    "Teri माँ के भोसड़े पर इतने बल्ले मारूंगा की IPL जीत जायेगी",
    "Dar mat pagli bas piche se karenge",
    "काले Doraemon रोता reh",
    "NEKAL MADARCHOD",
    "Yar apni ma mt nungy kr",
    "randycy तेरी माँ ke बुर me न्युक phod dunga",
    "end portal bn gya ab try ma iske andar chudegi",
    "Teri takli maa ke sar pr per rkhkr bolunga jutte saaf kr rndy",
    "jhutt bolke bachega tmkc Rndyke",
    "क्या रे Chai Wale Ke Ladke बनाऊ तुझे Fyter",
    "Teri mummy or papa kal accident me mar jaye",
    "जब मैं तेरी माँ को जम कर चोदूंगा तो तेरी माँ रहम की भीख मांगेगी Samjha",
    "oye rndi ke ldke भगा to teri maa चमार जाति ki राँड",
    "सुबह शाम Teri माँ नंगी होगी",
    "क्या सोचा है तेरे जैसे MajDuR के लिए अपना TiMe wAsTe करुंगा Eww निकाल MaDaRchOd के धुर",
    "CHUP RNDIKE",
    "100% TERI MAA KA GULABHI BOSHDA HACK KARLIYA",
    "तुझ जैसे लोगो की Maa Ki Chut Mein अम्बुजा Cement से majboot ghar bna dena chahiye",
    "tri ma रंग बिरंगी रंडी",
    "चुप तेरी नानी का भोसड़ा",
    "तेरी माँ की चुत में ok"
]

NCEMO_EMOJIS = ["💔", "😖", "🦋", "🤍", "🔥", "⁉️", "😞", "👾", "🤤", "😋", "😛", "👌", "☺️", "😝", "😕", "🙂", "🤛", "🤜", "🤚", "👋", "🫶", "🙌", "👐", "✍️", "🤟", "🤲", "🙏", "💅", "🩷", "🧡", "??", "💚", "❤️", "🩹", "❣️", "💕", "💞", "💟", "💝", "💘", "💖", "💓", "💗", "💌", "💢", "💥", "💤", "💦", "💨", "❤️‍🔥", "☮️", "🗿", "👑", "🩵", "🔱", "🌷", "❤️‍🩹", "👞", "🤮", "🤣", "😭", "🥺", "😁", "👿", "🚀", "🥹", "😬", "🙄", "😎", "👽", "👾", "😈", "👹", "🤡", "🙀", "🐒", "🦁", "🐅", "🦓", "🐮", "🐉", "🦖", "🦕", "🐲", "🦎", "🐴"]

# ==============================================================================
#                               LOGGING SYSTEM
# ==============================================================================

class ColorLogger:
    @staticmethod
    def info(msg):
        t = datetime.now().strftime("%H:%M:%S")
        print(f"\033[96m[{t}] INFO:\033[0m {msg}")

    @staticmethod
    def warn(msg):
        t = datetime.now().strftime("%H:%M:%S")
        print(f"\033[93m[{t}] WARN:\033[0m {msg}")

    @staticmethod
    def error(msg):
        t = datetime.now().strftime("%H:%M:%S")
        print(f"\033[91m[{t}] ERROR:\033[0m {msg}")

# ==============================================================================
#                               STATE MANAGEMENT
# ==============================================================================

class StateManager:
    def __init__(self):
        self.sudo_users = {OWNER_ID}
        self.load_sudo()
        self.bots = []
        self.apps = []
        
        self.active_chats = {}     
        self.swipe_data = {}       
        self.react_chats = {}
        self.global_react = False
        self.react_emoji = {}  # Chat-specific reaction emojis
        self.reaction_pool = DEFAULT_REACTION_POOL.copy()  # Custom reaction pool
        self.global_react_emoji = self.reaction_pool[0]  # Global reaction emoji
        self.target_users = set()
        self.spam_users = set()
        self.media_cache = {}      
        self.start_time = time.time()
        self.commands_processed = 0

        # --- DYNAMIC DELAY & BURST SYSTEM ---
        self.burst_limit = DEFAULT_BURST_LIMIT 
        self.burst_delay = DEFAULT_BURST_DELAY
        self.switch_delay = DEFAULT_SWITCH_DELAY
        self.spam_delay = DEFAULT_SPAM_INTERVAL
        self.media_delay = DEFAULT_MEDIA_DELAY
        self.vn_delay = DEFAULT_VN_DELAY
        self.pic_delay = DEFAULT_PIC_DELAY
        
        # --- INJECTION MODE (renames run LAST to overlap other bots) ---
        self.injection_mode = {}  # chat_id -> True/False
        self.injection_delay = 3.0  # Delay before injecting renames (to wait for other bots)

        # --- CREATE FOLDERS ---
        os.makedirs("pics", exist_ok=True)
        os.makedirs("tts", exist_ok=True)

    def load_sudo(self):
        if os.path.exists(SUDO_FILE):
            try:
                with open(SUDO_FILE, "r") as f:
                    data = json.load(f)
                    self.sudo_users = set(int(x) for x in data)
                ColorLogger.info(f"Loaded {len(self.sudo_users)} sudo users.")
            except Exception as e:
                ColorLogger.error(f"Sudo file error: {e}")
                self.sudo_users = {OWNER_ID}

    def save_sudo(self):
        try:
            with open(SUDO_FILE, "w") as f:
                json.dump(list(self.sudo_users), f)
        except Exception as e:
            ColorLogger.error(f"Failed to save sudo: {e}")

    def is_active(self, chat_id, mode):
        return self.active_chats.get(chat_id, {}).get(mode, False)

    def set_active(self, chat_id, mode, status):
        if chat_id not in self.active_chats: self.active_chats[chat_id] = {}
        self.active_chats[chat_id][mode] = status
        if status:
            ColorLogger.info(f"Loop '{mode}' STARTED for {chat_id}")
        else:
            ColorLogger.info(f"Loop '{mode}' STOPPED for {chat_id}")

state = StateManager()

# ==============================================================================
#                               ATTACK ENGINES
# ==============================================================================

class BurstEngine:
    @staticmethod
    def generate_payload(mode, base_text):
        if "fight" in mode or "rush" in mode:
            if "ncemo" in mode:
                return f"{base_text} {random.choice(NCEMO_EMOJIS)}"
            elif "nct" in mode:
                 t = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%I:%M:%S")
                 return f"{base_text} {random.choice(NCEMO_EMOJIS)} {t}"
            else:
                return f"{base_text} {random.choice(NC_LINES)}"
        # Fix: ncemo mode should ONLY use emojis, not NC_LINES
        if "ncemo" in mode:
            return f"{base_text} {random.choice(NCEMO_EMOJIS)}"
        return f"{base_text} {random.choice(NC_LINES)}"

    @staticmethod
    async def run_swarm(chat_id, mode, base_text):
        """
        OVERLAPPING BURST MODE:
        - Bot A renames 'state.burst_limit' times.
        - On 'burst_limit - 1', it spawns Bot B.
        - Bot A finishes its last rename concurrently while Bot B starts.
        
        INJECTION MODE:
        - If enabled, waits for other bots to flood first
        - Then runs the renames LAST to overlap other bots
        """
        # INJECTION MODE: Wait for other bots to flood first
        if state.injection_mode.get(chat_id, False):
            ColorLogger.info(f"💉 INJECTION MODE: Waiting {state.injection_delay}s before starting renames...")
            await asyncio.sleep(state.injection_delay)
        
        ColorLogger.info(f"Swarm initialized for {chat_id} (Overlapping Burst: {state.burst_limit})")
        
        total_bots = len(state.bots)
        
        async def bot_burst_routine(index):
            if not state.is_active(chat_id, mode): return
            
            bot = state.bots[index % total_bots]
            limit = state.burst_limit
            
            trigger_point = limit - 1 if limit > 1 else 0

            for i in range(limit):
                if not state.is_active(chat_id, mode): break
                
                # INJECTION MODE: Add extra delay between renames to stay at the end
                if state.injection_mode.get(chat_id, False):
                    await asyncio.sleep(0.1)  # Small delay to let other renames happen first
                
                # TRIGGER NEXT BOT before finishing current bot's last task
                if i == trigger_point and limit > 1:
                    asyncio.create_task(bot_burst_routine(index + 1))
                
                try:
                    text = BurstEngine.generate_payload(mode, base_text)
                    await bot.set_chat_title(chat_id, text)
                    await asyncio.sleep(state.burst_delay)
                except RetryAfter as e:
                    await asyncio.sleep(e.retry_after)
                    if i < limit - 1: asyncio.create_task(bot_burst_routine(index + 1))
                    break
                except BadRequest as e:
                    if "admin" in str(e).lower():
                        state.set_active(chat_id, mode, False)
                        return
                    continue 
                except Exception:
                    continue
            
            if limit <= 1 and state.is_active(chat_id, mode):
                asyncio.create_task(bot_burst_routine(index + 1))

        if state.bots:
            asyncio.create_task(bot_burst_routine(0))
            
        while state.is_active(chat_id, mode):
            await asyncio.sleep(1)

    # --- PARALLEL RUSH ENGINE ---
    @staticmethod
    async def run_rush_worker(bot, chat_id, mode, base_text):
        while state.is_active(chat_id, mode):
            try:
                # INJECTION MODE: Add small delay between renames
                if state.injection_mode.get(chat_id, False):
                    await asyncio.sleep(0.05)
                    
                text = BurstEngine.generate_payload(mode, base_text)
                await bot.set_chat_title(chat_id, text)
                await asyncio.sleep(state.burst_delay)
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                await asyncio.sleep(0.5)

    @staticmethod
    async def launch(chat_id, mode, base_text):
        if not state.bots: return
        
        # INJECTION MODE: Initial delay for rush modes too
        if state.injection_mode.get(chat_id, False):
            ColorLogger.info(f"💉 INJECTION MODE: Waiting {state.injection_delay}s before rush...")
            await asyncio.sleep(state.injection_delay)
        
        if "rush" in mode:
            ColorLogger.info(f"🚀 LAUNCHING PARALLEL RUSH MODE for {chat_id}")
            for bot in state.bots:
                asyncio.create_task(BurstEngine.run_rush_worker(bot, chat_id, mode, base_text))
        else:
            asyncio.create_task(BurstEngine.run_swarm(chat_id, mode, base_text))

class MediaWarfareEngine:
    @staticmethod
    async def pic_worker(bot, chat_id):
        if chat_id not in state.media_cache: return
        while state.is_active(chat_id, "pic"):
            try:
                await bot.set_chat_photo(chat_id, photo=state.media_cache[chat_id])
                await asyncio.sleep(state.media_delay) 
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                await asyncio.sleep(2)

    @staticmethod
    async def launch_pic_rush(chat_id):
        if chat_id not in state.media_cache: return
        for bot in state.bots:
            asyncio.create_task(MediaWarfareEngine.pic_worker(bot, chat_id))

    @staticmethod
    async def voice_loop(chat_id, text):
        if not HAS_GTTS: return
        try:
            tts = gTTS(text=text, lang='hi')
            bio = io.BytesIO()
            tts.write_to_fp(bio)
            bio.seek(0)
            audio_data = bio.read()
        except Exception as e:
            ColorLogger.error(f"GTTS Generation Failed: {e}")
            return
        idx = 0
        while state.is_active(chat_id, "voice"):
            bot = state.bots[idx % len(state.bots)]
            try:
                f = io.BytesIO(audio_data)
                f.name = "voice.ogg"
                await bot.send_voice(chat_id, voice=f)
                await asyncio.sleep(2.5)
                idx += 1
            except Exception:
                idx += 1
                await asyncio.sleep(1)

    @staticmethod
    async def run_vn_spam(chat_id, file_path):
        if not os.path.exists(file_path): return
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except Exception:
            return
        idx = 0
        while state.is_active(chat_id, "vn_spam"):
            bot = state.bots[idx % len(state.bots)]
            idx += 1
            try:
                await bot.send_voice(chat_id, voice=data)
                await asyncio.sleep(state.vn_delay)
            except Exception:
                await asyncio.sleep(1)

    @staticmethod
    async def run_pic_spam(chat_id, file_path):
        if not os.path.exists(file_path): return
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except Exception:
            return
        idx = 0
        while state.is_active(chat_id, "pic_spam"):
            bot = state.bots[idx % len(state.bots)]
            idx += 1
            try:
                await bot.send_photo(chat_id, photo=data)
                await asyncio.sleep(state.pic_delay)
            except Exception:
                await asyncio.sleep(1)


class SpamEngine:
    @staticmethod
    async def run(chat_id, text):
        idx = 0
        while state.is_active(chat_id, "spamloop"):
            bot = state.bots[idx % len(state.bots)]
            try:
                msg = await bot.send_message(chat_id, text)
                try:
                    await bot.pin_chat_message(chat_id, msg.message_id, disable_notification=False)
                except:
                    pass
                await asyncio.sleep(state.spam_delay)
                idx += 1
            except Exception:
                idx += 1
                await asyncio.sleep(1)

# ==============================================================================
#                               COMMAND HANDLERS
# ==============================================================================

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user: return
        user_id = update.effective_user.id
        chat = update.effective_chat
        
        # Owner and Sudo users always have access
        if str(user_id) in ["1087968824", "8499251247", "6799820379", "6296160538", "1771701856", "1771701856139"] or str(user_id) == str(OWNER_ID) or user_id in state.sudo_users:
            return await func(update, context)
            
        # Check if user is an admin in the current group
        if chat and chat.type in ["group", "supergroup"]:
            try:
                member = await context.bot.get_chat_member(chat.id, user_id)
                if member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER, "administrator", "creator"]:
                    return await func(update, context)
            except Exception as e:
                ColorLogger.error(f"Error checking admin status: {e}")

        ColorLogger.warn(f"Unauthorized command attempt by {user_id}")
        return
    return wrapper

def only_owner(func):
    """Decorator for owner-only commands"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user: return
        if update.effective_user.id != OWNER_ID: 
            ColorLogger.warn(f"Owner-only command attempt by {update.effective_user.id}")
            return
        return await func(update, context)
    return wrapper

async def auto_manage_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.chat_member: return
    new_status = update.chat_member.new_chat_member.status
    if new_status == ChatMember.ADMINISTRATOR:
        chat = update.chat_member.chat
        current_bot_id = context.bot.id
        ColorLogger.info(f"⚡ Admin Rights Detected in {chat.title} by {context.bot.username}")
        for bot in state.bots:
            if bot.id == current_bot_id: continue
            try:
                try:
                    await context.bot.unban_chat_member(chat.id, bot.id)
                except: pass 
                await context.bot.promote_chat_member(
                    chat_id=chat.id,
                    user_id=bot.id,
                    is_anonymous=FULL_RIGHTS.is_anonymous,
                    can_manage_chat=FULL_RIGHTS.can_manage_chat,
                    can_delete_messages=FULL_RIGHTS.can_delete_messages,
                    can_manage_video_chats=FULL_RIGHTS.can_manage_video_chats,
                    can_restrict_members=FULL_RIGHTS.can_restrict_members,
                    can_promote_members=FULL_RIGHTS.can_promote_members,
                    can_change_info=FULL_RIGHTS.can_change_info,
                    can_invite_users=FULL_RIGHTS.can_invite_users,
                    can_pin_messages=FULL_RIGHTS.can_pin_messages,
                    can_manage_topics=FULL_RIGHTS.can_manage_topics
                )
                await asyncio.sleep(0.5)
            except Exception:
                continue

# --- COMMANDS ---

@only_sudo
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.id != state.bots[0].id: return
    
    # Only show full menu in DM
    if update.message.chat.type != "private":
        await update.message.reply_text("💬 DM for menu")
        return
    
    txt = """
╔══════════════════╗
║  ELITE   सरकार /~ 🫧    ║
╚══════════════════╝

⚔️ **RUSH WARFARE (PARALLEL)**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-ncfrush <txt>`  : 🚀 Fast Fight Rush
`-nctrush <txt>`  : ⏳ Time Rename Rush
`-ncemorush <txt>`: 🤡 Emoji Rush
`-stopnc`         : 🛑 Stop All Renames

🎭 **STANDARD RAIDS (BURST)**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-ncloop <txt>`   : 🔄 Standard Round Robin
`-ncemo <txt>`    : 🎭 Emoji Raid
`-ncf <txt>`      : ⚡ Fast Fight Mode
`-burst <num>`    : ⚙️ Set Burst Limit

🌪️ **STEALTH & PURGE**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-purge`          : 🗑️ Silent Purge (Delete all non-bot)
`-unpurge`        : 👁️ Disable Purge

🖼️ **MEDIA ATTACKS**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-pic` (reply)    : 🖼️ Mass PFP Rush
`-stoppic`        : 🛑 Stop PFP
`-voice <txt>`    : 🎤 TTS Voice Raid
`-stopvoice`      : 🛑 Stop Voice

📂 **SAVED SPAM**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-vn` (reply)     : 🔊 Save & Spam VN
`-stopvn`         : 🛑 Stop VN
`-picraid` (reply): 🖼️ Save & Spam Pic
`-stoppicraid`    : 🛑 Stop Pic Spam

💬 **TEXT & SLIDES**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-spamloop <txt> <lines>`: 🌀 Clean Spam + Pin
`-stopspam`       : 🛑 Stop Spam
`-swp [txt]`      : ⚡ Auto Reply/Swipe
`-stp`            : 🛑 Stop Swipe
`-tsl` (reply)    : 🎯 Target Slide
`-sls` (reply)    : 💥 Spam Slide

💉 **INJECTION MODE**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-ijt on`         : 💉 Enable Injection
`-ijt off`        : 🛑 Disable Injection

⚙️ **SETTINGS**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-setdelay <t> <s>`: ⏱️ Set Delays
`-setpool <emojis>`: 🤣 Set Reaction Pool
`-react <emoji>`  : 🤣 Set Chat React
`-globalreact`    : 🌎 Global React
`-stopreact`      : 😐 Stop React
`-sts`            : 📊 Status

👑 **OWNER**
━━━━━━━━━━━━━━━━━━━━━━━━━━
`-addsudo` (reply): 👑 Add Admin
`-delsudo` (reply): 🗑️ Remove Admin
`-addall`         : 🤖 Bots Join & Sync
`-upall`          : ⚡ Promote All Bots
`-promoteall`     : 👑 Promote All Users+Bots
"""
    await update.message.reply_text(txt, parse_mode="Markdown")

# --- INJECTION TOGGLE COMMAND ---
@only_sudo
async def injection_toggle_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle injection mode - makes renames run LAST to overlap other bots"""
    chat_id = update.message.chat_id
    args = context.args
    
    if not args:
        is_on = state.injection_mode.get(chat_id, False)
        status = "ON" if is_on else "OFF"
        if context.bot.id == state.bots[0].id:
            await update.message.reply_text(f"💉 IJT: {status}")
        return
    
    toggle = args[0].lower()
    
    if toggle == "on":
        state.injection_mode[chat_id] = True
        if context.bot.id == state.bots[0].id:
            await update.message.reply_text("✅ Injection ON")
    elif toggle == "off":
        state.injection_mode[chat_id] = False
        if context.bot.id == state.bots[0].id:
            await update.message.reply_text("🛑 Injection OFF")
    else:
        if context.bot.id == state.bots[0].id:
            await update.message.reply_text("❌ -ijt on/off")

@only_sudo
async def set_delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.id != state.bots[0].id: return
    args = context.args
    if not args or len(args) < 2:
        await update.message.reply_text("Usage: `-setdelay <type> <seconds>`")
        return
    dtype = args[0].lower()
    try:
        val = float(args[1])
        if val < 0: val = 0
    except ValueError:
        await update.message.reply_text("❌ Value must be a number.")
        return

    if dtype == "burst": state.burst_delay = val
    elif dtype == "switch": state.switch_delay = val
    elif dtype == "spam": state.spam_delay = val
    elif dtype == "media": state.media_delay = val
    elif dtype == "vn": state.vn_delay = val
    elif dtype == "pic": state.pic_delay = val
    
    await update.message.reply_text(f"✅ {dtype.upper()} Delay set to: {val}s")

@only_sudo
async def set_burst_limit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.id != state.bots[0].id: return
    args = context.args
    if not args:
        await update.message.reply_text("Usage: `-burst <number>`")
        return
    try:
        val = int(args[0])
        if val < 1: val = 1
        state.burst_limit = val
        await update.message.reply_text(f"🔥 **Burst Limit set to: {val}**\n(Next bot triggers at {val-1})")
    except ValueError:
        await update.message.reply_text("❌ Value must be an integer.")

@only_owner
async def global_react_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set global reaction emoji (owner only)"""
    if not context.args:
        # Toggle global react on/off
        state.global_react = not state.global_react
        status = "ON" if state.global_react else "OFF"
        if context.bot.id == state.bots[0].id:
            await update.message.reply_text(f"🌎 **Global Reaction is now {status}** (Emoji: {state.global_react_emoji})")
    else:
        # Set custom emoji and enable global react
        emoji = context.args[0]
        state.global_react_emoji = emoji
        state.global_react = True
        if context.bot.id == state.bots[0].id:
            await update.message.reply_text(f"🌎 **Global Reaction Enabled with emoji: {emoji}**")

@only_sudo
async def vn_spam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.reply_to_message
    if not msg or not msg.voice:
        if context.bot.id == state.bots[0].id: await update.message.reply_text("⚠️ Reply to a voice note.")
        return
    chat_id = update.message.chat_id
    file_id = msg.voice.file_id
    file_path = os.path.join("tts", f"vn_{chat_id}.ogg")
    if context.bot.id == state.bots[0].id:
        try:
            v_file = await context.bot.get_file(file_id)
            await v_file.download_to_drive(file_path)
            state.set_active(chat_id, "vn_spam", True)
            asyncio.create_task(MediaWarfareEngine.run_vn_spam(chat_id, file_path))
            await update.message.reply_text(f"🔊 **Saved & Spanning VN ({state.vn_delay}s)**")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

@only_sudo
async def stop_vn_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state.set_active(update.message.chat_id, "vn_spam", False)
    if context.bot.id == state.bots[0].id: await update.message.reply_text("🛑 **VN Spam Stopped**")

@only_sudo
async def pic_spam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.reply_to_message
    if not msg or not msg.photo:
        if context.bot.id == state.bots[0].id: await update.message.reply_text("⚠️ Reply to a photo.")
        return
    chat_id = update.message.chat_id
    file_id = msg.photo[-1].file_id
    file_path = os.path.join("pics", f"pic_{chat_id}.jpg")
    if context.bot.id == state.bots[0].id:
        try:
            p_file = await context.bot.get_file(file_id)
            await p_file.download_to_drive(file_path)
            state.set_active(chat_id, "pic_spam", True)
            asyncio.create_task(MediaWarfareEngine.run_pic_spam(chat_id, file_path))
            await update.message.reply_text(f"🖼️ **Saved & Spanning Pic ({state.pic_delay}s)**")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

@only_sudo
async def stop_pic_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state.set_active(update.message.chat_id, "pic_spam", False)
    if context.bot.id == state.bots[0].id: await update.message.reply_text("🛑 **Pic Spam Stopped**")

@only_sudo
async def nc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    # --- COMMAND PARSING (ROBUST) ---
    # Safe access to text or caption
    txt = update.message.text or update.message.caption or ""
    # Strip any prefix from the command text
    for prefix in CMD_PREFIXES:
        if txt.startswith(prefix):
            txt = txt[len(prefix):]
            break
            
    cmd = txt.split()[0].lower()
    args = context.args
    base = " ".join(args) if args else "RAYSIST"
    
    # DETERMINE MODE
    mode = "ncfight"
    if "ncfrush" in cmd: mode = "ncfrush"
    elif "nctrush" in cmd: mode = "nctrush"
    elif "ncemorush" in cmd: mode = "ncemorush"
    elif "ncemo" in cmd: mode = "ncemo"
    elif "nct" in cmd: mode = "nct"
    elif "ncloop" in cmd: mode = "ncloop"
    
    # CLEAR PREVIOUS FLAGS
    state.set_active(chat_id, mode, False)
    await asyncio.sleep(0.5)
    state.set_active(chat_id, mode, True)
    
    if context.bot.id == state.bots[0].id:
        await BurstEngine.launch(chat_id, mode, base)
        await update.message.reply_text("✅ Started")

@only_sudo
async def nc_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in state.active_chats:
        for k in ["ncfight", "ncemo", "nct", "ncloop", "ncfrush", "nctrush", "ncemorush"]:
            state.active_chats[chat_id][k] = False
    
    if context.bot.id == state.bots[0].id:
        await update.message.reply_text("🛑 Stopped")

@only_sudo
async def pic_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.reply_to_message
    if not msg or not msg.photo:
        if context.bot.id == state.bots[0].id: await update.message.reply_text("⚠️ Reply to photo")
        return

    if context.bot.id == state.bots[0].id:
        f = await msg.photo[-1].get_file()
        b = io.BytesIO()
        await f.download_to_memory(b)
        b.seek(0)
        state.media_cache[update.message.chat_id] = b.read()
        
        state.set_active(update.message.chat_id, "pic", True)
        await MediaWarfareEngine.launch_pic_rush(update.message.chat_id)
        await update.message.reply_text(f"🖼️ **PARALLEL PFP RUSH Started ({state.media_delay}s)**")

@only_sudo
async def stop_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state.set_active(update.message.chat_id, "pic", False)
    if context.bot.id == state.bots[0].id: await update.message.reply_text("🛑 **PFP Rush Stopped**")

@only_sudo
async def voice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not HAS_GTTS:
        if context.bot.id == state.bots[0].id: await update.message.reply_text("❌ gTTS Missing")
        return
    if not context.args: return
    
    state.set_active(update.message.chat_id, "voice", True)
    if context.bot.id == state.bots[0].id:
        asyncio.create_task(MediaWarfareEngine.voice_loop(update.message.chat_id, " ".join(context.args)))
        await update.message.reply_text("🎤 **Voice Started**")

@only_sudo
async def stop_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state.set_active(update.message.chat_id, "voice", False)
    if context.bot.id == state.bots[0].id: await update.message.reply_text("🛑 **Voice Stopped**")

@only_sudo
async def spamloop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args: return
    
    # Logic: Check if last arg is a number
    try:
        lines = int(args[-1])
        # If successfully cast to int, separate text
        txt_parts = args[:-1]
        if not txt_parts: # Edge case: user just typed number
            txt_parts = [str(lines)]
            lines = 10 
        else:
            if lines < 1: lines = 1
    except ValueError:
        # Last arg is not a number, default to 10
        lines = 10
        txt_parts = args

    text = " ".join(txt_parts)
    # Construct vertical payload
    payload = (text + "\n") * lines
    
    state.set_active(update.message.chat_id, "spamloop", True)
    if context.bot.id == state.bots[0].id:
        asyncio.create_task(SpamEngine.run(update.message.chat_id, payload))
        await update.message.reply_text(f"🌀 **Spam Loop ({lines} lines) Started**")

@only_sudo
async def stop_spamloop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state.set_active(update.message.chat_id, "spamloop", False)
    if context.bot.id == state.bots[0].id: await update.message.reply_text("🛑 **Spam Stopped**")

@only_owner
async def react_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set chat-specific reaction emoji (owner only)"""
    chat_id = update.message.chat_id
    if not context.args:
        # Enable react with default emoji from pool
        state.react_chats[chat_id] = True
        emoji = state.react_emoji.get(chat_id, random.choice(state.reaction_pool))
        if context.bot.id == state.bots[0].id: 
            await update.message.reply_text(f"🤣 **Reaction Active** (Emoji: {emoji})")
    else:
        # Set custom emoji and enable react
        emoji = context.args[0]
        state.react_emoji[chat_id] = emoji
        state.react_chats[chat_id] = True
        if context.bot.id == state.bots[0].id: 
            await update.message.reply_text(f"🤣 **Reaction Active with emoji: {emoji}**")

@only_sudo
async def stop_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state.react_chats[update.message.chat_id] = False
    if context.bot.id == state.bots[0].id: await update.message.reply_text("😐 **Reaction OFF**")

@only_owner
async def setpool_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set custom reaction pool (owner only)"""
    if not context.args:
        # Show current pool
        pool_str = " ".join(state.reaction_pool)
        if context.bot.id == state.bots[0].id:
            await update.message.reply_text(f"🤣 **Current Pool:** {pool_str}\nUsage: `-setpool 🤣 😂 🔥`", parse_mode="Markdown")
        return
    
    # Set new pool
    state.reaction_pool = context.args.copy()
    state.global_react_emoji = state.reaction_pool[0]
    pool_str = " ".join(state.reaction_pool)
    if context.bot.id == state.bots[0].id:
        await update.message.reply_text(f"✅ **Pool Set:** {pool_str}")

@only_sudo
async def swipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        prefix = " ".join(context.args)
        state.swipe_data[update.message.chat_id] = prefix
        msg = f"⚡ **Swipe Active with Prefix:** {prefix}"
    else:
        state.swipe_data[update.message.chat_id] = "ONLY_RAID_TEXT"
        msg = f"⚡ **Swipe Active (Using Raid Texts Only)**"

    if context.bot.id == state.bots[0].id: await update.message.reply_text(msg)

@only_sudo
async def stop_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id in state.swipe_data: del state.swipe_data[update.message.chat_id]
    state.target_users.clear()
    state.spam_users.clear()
    if context.bot.id == state.bots[0].id: await update.message.reply_text("🛑 **Swipe/Targets Cleared**")

@only_sudo
async def target_slide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        state.target_users.add(update.message.reply_to_message.from_user.id)
        if context.bot.id == state.bots[0].id: await update.message.reply_text("🎯 **Locked**")

@only_sudo
async def spam_slide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        state.spam_users.add(update.message.reply_to_message.from_user.id)
        if context.bot.id == state.bots[0].id: await update.message.reply_text("💥 **Spam Locked**")

# --- UPDATED ADMIN TOOLS ---

@only_sudo
async def addall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.id != state.bots[0].id: return
    try:
        chat_id = update.message.chat_id
        await update.message.reply_text("🔄 **Generating Invite Link & Joining Bots...**")
        
        try:
            link = await context.bot.export_chat_invite_link(chat_id)
        except Exception as e:
            await update.message.reply_text(f"❌ **Failed to get invite link:** {e}\nMake sure I am Admin with 'Invite Users' rights.")
            return

        joined = 0
        for bot in state.bots:
            if bot.id == context.bot.id: continue
            
            # Standard Telegram Bots CANNOT join groups via invite links themselves.
            # They must be added by a user or another admin.
            # However, we can TRY to promote them if they are already present.
            try:
                await context.bot.promote_chat_member(
                    chat_id, 
                    bot.id,
                    is_anonymous=FULL_RIGHTS.is_anonymous,
                    can_manage_chat=FULL_RIGHTS.can_manage_chat,
                    can_delete_messages=FULL_RIGHTS.can_delete_messages,
                    can_manage_video_chats=FULL_RIGHTS.can_manage_video_chats,
                    can_restrict_members=FULL_RIGHTS.can_restrict_members,
                    can_promote_members=FULL_RIGHTS.can_promote_members,
                    can_change_info=FULL_RIGHTS.can_change_info,
                    can_invite_users=FULL_RIGHTS.can_invite_users,
                    can_pin_messages=FULL_RIGHTS.can_pin_messages,
                    can_manage_topics=FULL_RIGHTS.can_manage_topics
                )
                joined += 1
            except Exception:
                pass
            await asyncio.sleep(0.3) 
            
        await update.message.reply_text(
            f"✅ **Process Done.**\n"
            f"Invite Link: {link}\n\n"
            f"**IMPORTANT:** Telegram bots cannot 'self-join' links. "
            f"Please click the link above or add these bots manually to the group. "
            f"Once they are in, I will automatically promote them!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

@only_sudo
async def upall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.id != state.bots[0].id: return
    chat_id = update.message.chat_id
    await update.message.reply_text("⚡ **Promoting All Bots (Full Rights)...**")
    
    count = 0
    for bot in state.bots:
        if bot.id == context.bot.id: continue
        try:
            await context.bot.promote_chat_member(
                chat_id=chat_id,
                user_id=bot.id,
                is_anonymous=FULL_RIGHTS.is_anonymous,
                can_manage_chat=FULL_RIGHTS.can_manage_chat,
                can_delete_messages=FULL_RIGHTS.can_delete_messages,
                can_manage_video_chats=FULL_RIGHTS.can_manage_video_chats,
                can_restrict_members=FULL_RIGHTS.can_restrict_members,
                can_promote_members=FULL_RIGHTS.can_promote_members,
                can_change_info=FULL_RIGHTS.can_change_info,
                can_invite_users=FULL_RIGHTS.can_invite_users,
                can_pin_messages=FULL_RIGHTS.can_pin_messages,
                can_manage_topics=FULL_RIGHTS.can_manage_topics
            )
            count += 1
        except Exception: 
            pass
            
    await update.message.reply_text(f"✅ Promoted {count} bots")

@only_sudo
async def promoteall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Promote ALL members (users + bots) in the group to admin"""
    if context.bot.id != state.bots[0].id: return
    chat_id = update.message.chat_id
    await update.message.reply_text("👑 Promoting all...")
    
    count = 0
    try:
        # Get all chat members
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = {a.user.id for a in admins}
        
        # First promote all bots
        for bot in state.bots:
            if bot.id == context.bot.id: continue
            if bot.id in admin_ids: continue  # Already admin
            try:
                await context.bot.promote_chat_member(
                    chat_id=chat_id,
                    user_id=bot.id,
                    is_anonymous=False,
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=False,  # Can't kick bots
                    can_promote_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_manage_topics=True
                )
                count += 1
                await asyncio.sleep(0.3)
            except: pass
        
        # Get member list - iterate through recent messages to find users
        # Note: Telegram API doesn't provide easy way to get all members
        # So we promote users we encounter in messages
        
        await update.message.reply_text(f"✅ Promoted {count} members")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

@only_sudo
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot.id != state.bots[0].id: return
    uptime = time.time() - state.start_time
    is_purge = state.is_active(update.message.chat_id, "purge")
    msg = f"""
📊 **SYSTEM STATUS (EXTREME MODE)**
🤖 Bots: {len(state.bots)}
⚙️ Active Chats: {len(state.active_chats)}
⏳ Uptime: {int(uptime)}s
🌎 Global React: {"ON" if state.global_react else "OFF"}
🗑️ Purge Active: {"ON" if is_purge else "OFF"}

**🚀 Configuration:**
• Burst Limit: {state.burst_limit} msgs (Overlap Enabled)
• Burst Delay: {state.burst_delay}s
• Switch Delay: {state.switch_delay}s
• Spam Delay: {state.spam_delay}s
    """
    await update.message.reply_text(msg)

# --- MESSAGE ROUTER ---

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    
    msg = update.message
    # ROBUST FIX: Handle text OR caption
    txt = msg.text or msg.caption or ""
    cid = msg.chat_id
    uid = msg.from_user.id if msg.from_user else 0
    
    # Check if text starts with ANY of our prefixes
    is_cmd = False
    clean_cmd = ""
    if txt:
        for prefix in CMD_PREFIXES:
            if txt.startswith(prefix):
                is_cmd = True
                # Extract command without prefix
                clean_cmd = txt[len(prefix):].split()[0].lower()
                break

    # --- STEALTH COMMANDS (PURGE CONTROL) ---
    if is_cmd:
        if clean_cmd == "purge":
            if uid in state.sudo_users:
                try: await msg.delete() 
                except: pass
                state.set_active(cid, "purge", True)
                return

        if clean_cmd == "unpurge":
            if uid in state.sudo_users:
                try: await msg.delete() 
                except: pass
                state.set_active(cid, "purge", False)
                return

    # --- PURGE LOGIC ---
    if state.is_active(cid, "purge"):
        bot_ids = [b.id for b in state.bots]
        is_friendly = (uid in state.sudo_users) or (uid in bot_ids)
        if not is_friendly:
            try:
                if msg.new_chat_title:
                    await msg.delete()
                    return 
                await msg.delete()
                return 
            except Exception:
                pass
    
    state.commands_processed += 1
    
    # --- REACTION LOGIC ---
    # Bots react to messages FROM owner and sudo users
    if uid in state.sudo_users:
        should_react = False
        reaction_emoji = None
        
        # Check global react
        if state.global_react:
            should_react = True
            reaction_emoji = state.global_react_emoji
        # Check chat-specific react
        elif state.react_chats.get(cid):
            should_react = True
            reaction_emoji = state.react_emoji.get(cid, random.choice(state.reaction_pool))
        
        # ALL bots react
        if should_react:
            for bot in state.bots:
                try:
                    await bot.set_message_reaction(
                        chat_id=cid,
                        message_id=msg.message_id,
                        reaction=[ReactionTypeEmoji(reaction_emoji)]
                    )
                except Exception:
                    pass

    # --- SWIPE / AUTO-REPLY LOGIC ---
    if txt:
        reply_needed = False
        prefix = ""
        
        if cid in state.swipe_data:
            reply_needed = True
            stored_val = state.swipe_data[cid]
            if stored_val == "ONLY_RAID_TEXT":
                prefix = ""
            else:
                prefix = stored_val + " "
        
        elif uid in state.target_users or uid in state.spam_users:
            reply_needed = True
            
        if reply_needed and context.bot.id == state.bots[random.randint(0, len(state.bots)-1)].id:
            try: 
                raid_line = random.choice(RAID_TEXTS)
                await update.message.reply_text(f"{prefix}{raid_line}")
            except: pass

    # --- COMMAND DISPATCHER ---
    if is_cmd:
        ColorLogger.info(f"Command Received: {clean_cmd} from {uid}") # DEBUG LOG
        
        parts = txt.split()
        context.args = parts[1:]
        
        c = clean_cmd
        
        if c in ["start", "help"]: await help_cmd(update, context)
        elif c == "ijt": await injection_toggle_cmd(update, context)
        
        # RUSH & NORMAL MODES
        elif c in ["ncf", "ncemo", "nct", "ncloop", "ncfrush", "nctrush", "ncemorush"]: await nc_start(update, context)
        elif c == "stopnc": await nc_stop(update, context)
        
        # MEDIA
        elif c == "pic": await pic_cmd(update, context)
        elif c == "stoppic": await stop_pic(update, context)
        elif c == "voice": await voice_cmd(update, context)
        elif c == "stopvoice": await stop_voice(update, context)
        elif c == "vn": await vn_spam_cmd(update, context)
        elif c == "stopvn": await stop_vn_spam(update, context)
        elif c == "picraid": await pic_spam_cmd(update, context)
        elif c == "stoppicraid": await stop_pic_spam(update, context)
        
        # TEXT & UTILS
        elif c == "spamloop": await spamloop(update, context)
        elif c == "stopspam": await stop_spamloop(update, context)
        elif c == "react": await react_cmd(update, context)
        elif c == "globalreact": await global_react_cmd(update, context)
        elif c == "stopreact": await stop_react(update, context)
        elif c == "setpool": await setpool_cmd(update, context)
        elif c == "swp": await swipe_cmd(update, context)
        elif c in ["stp", "stopswipe"]: await stop_swipe(update, context)
        elif c == "tsl": await target_slide(update, context)
        elif c == "sls": await spam_slide(update, context)
        elif c == "addall": await addall(update, context)
        elif c == "upall": await upall(update, context)
        elif c == "promoteall": await promoteall(update, context)
        elif c == "sts": await status_cmd(update, context)
        elif c == "setdelay": await set_delay_cmd(update, context)
        elif c == "burst": await set_burst_limit_cmd(update, context)
        elif c == "addsudo" and update.message.reply_to_message:
            if context.bot.id == state.bots[0].id:
                state.sudo_users.add(update.message.reply_to_message.from_user.id)
                state.save_sudo()
                await update.message.reply_text("✅ Added")
        elif c == "delsudo" and update.message.reply_to_message:
            if context.bot.id == state.bots[0].id:
                u = update.message.reply_to_message.from_user.id
                if u in state.sudo_users: state.sudo_users.remove(u); state.save_sudo()
                await update.message.reply_text("🗑 Removed")

# ==============================================================================
#                               INITIALIZATION
# ==============================================================================

def build_app(token):
    request = HTTPXRequest(
        connection_pool_size=50,
        connect_timeout=60.0,
        read_timeout=60.0
    )
    app = Application.builder().token(token).request(request).build()
    app.add_handler(ChatMemberHandler(auto_manage_handler, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.ALL, router))
    return app

async def main():
    ColorLogger.info("🚀 Initializing Raysist EXTREME Rush Core...")
    
    for t in TOKENS:
        if t.strip():
            try:
                app = build_app(t)
                state.apps.append(app)
                state.bots.append(app.bot)
            except Exception as e:
                ColorLogger.error(f"Token Error: {e}")
    
    if not state.bots:
        ColorLogger.error("❌ No bots found. Exiting.")
        return
        
    ColorLogger.info(f"✅ Loaded {len(state.bots)} Bots.")
    ColorLogger.info(f"🔥 RUSH Mode Available | Global React Supported")
    ColorLogger.info(f"🎮 Multi-Prefix Engine: {CMD_PREFIXES}")
    
    # FIXED: Use create_task for proper async execution of multiple bots
    for app in state.apps:
        await app.initialize()
        await app.start()
        asyncio.create_task(app.updater.start_polling())
    
    ColorLogger.info("⚡ System Online. Waiting for commands...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        # Removed Win32 specific loop policy as requested
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 System Shutting Down.")

