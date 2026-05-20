# ═══════════════════════════════════════════════════════════════
# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
#
# Portfolio: https://aratt.ai/@roxybasicneedbot
#
# Bot & Website Developer 🤖
# Creator of RoxyBasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
#
# © 2026 RoxyBasicNeedBot. All Rights Reserved.
# ═══════════════════════════════════════════════════════════════

# pyrogram imports
from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant

# extra imports
from config import Config
from helper.database import roxy_bot
import datetime 

async def not_subscribed(_, client, message):
    await roxy_bot.add_user(client, message)
    
    channels = []
    if hasattr(Config, 'FORCE_SUB') and Config.FORCE_SUB:
        channels.append(Config.FORCE_SUB)
    if hasattr(Config, 'FORCE_SUB2') and Config.FORCE_SUB2:
        channels.append(Config.FORCE_SUB2)
        
    if not channels:
        return False

    for channel in channels:
        try:
            user = await client.get_chat_member(channel, message.from_user.id)
            if user.status not in [enums.ChatMemberStatus.MEMBER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                return True

# ═══════════════════════════════════════════════════════════════
# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
#
# Portfolio: https://aratt.ai/@roxybasicneedbot
#
# Bot & Website Developer 🤖
# Creator of RoxyBasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
#
# © 2026 RoxyBasicNeedBot. All Rights Reserved.
# ═══════════════════════════════════════════════════════════════

        except UserNotParticipant:
            return True
        except Exception as e:
            print(f"Error checking subscription for {channel}: {e}")
            return False

    return False

async def handle_banned_user_status(bot, message):
    await roxy_bot.add_user(bot, message) 
    user_id = message.from_user.id
    ban_status = await roxy_bot.get_ban_status(user_id)
    if ban_status.get("is_banned", False):
        if ( datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await roxy_bot.remove_ban(user_id)
        else:
            return await message.reply_text(
                "<blockquote><b>Sorry Sir, 😔 You are Banned!..</b>\n\n"
                f"📝 <b>Reason:</b> {ban_status.get('ban_reason', 'Policy violation')}\n\n"
                "📞 <b>Please Contact - @roxycontactbot</b></blockquote>\n\n"
                "<blockquote><b><u>⚠️ 18+ Content Strictly Prohibited ⚠️</u></b></blockquote>",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📞 Contact Support", url="https://t.me/roxycontactbot")
                ]])
            ) 
    await message.continue_propagation()
    
async def forces_sub(client, message):
    buttons = []
    if hasattr(Config, 'FORCE_SUB') and Config.FORCE_SUB:
        buttons.append([InlineKeyboardButton(text="📢 Join Update Channel 📢", url="https://t.me/roxybasicneedbot1")])
    if hasattr(Config, 'FORCE_SUB2') and Config.FORCE_SUB2:
        buttons.append([InlineKeyboardButton(text="📢 Join AnimekazeToonskaze 📢", url="https://t.me/AnimekazeToonskaze")])
        
    text = """
<blockquote><b>
𝚂𝚘𝚛𝚛𝚢 𝙳𝚞𝚍𝚎… 😐  
𝙸𝚝 𝚜𝚎𝚎𝚖𝚜 𝚕𝚒𝚔𝚎 𝚢𝚘𝚞 𝚑𝚊𝚟𝚎 𝚗𝚘𝚝 𝚓𝚘𝚒𝚗𝚎𝚍 𝚘𝚞𝚛 𝙾𝚏𝚏𝚒𝚌𝚒𝚊𝚕 𝚄𝚙𝚍𝚊𝚝𝚎 𝙲𝚑𝚊𝚗𝚗𝚎𝚕𝚜 𝚢𝚎𝚝.  

𝙵𝚘𝚛 𝚜𝚎𝚌𝚞𝚛𝚒𝚝𝚢, 𝚚𝚞𝚊𝚕𝚒𝚝𝚢 𝚊𝚗𝚍 𝚜𝚎𝚊𝚖𝚕𝚎𝚜𝚜 𝚜𝚎𝚛𝚟𝚒𝚌𝚎,  
𝚋𝚘𝚝 𝚘𝚗𝚕𝚢 𝚠𝚘𝚛𝚔𝚜 𝚏𝚘𝚛 𝚞𝚜𝚎𝚛𝚜 𝚠𝚑𝚘 𝚊𝚛𝚎 𝚙𝚊𝚛𝚝 𝚘𝚏 𝚘𝚞𝚛 𝚌𝚑𝚊𝚗𝚗𝚎𝚕𝚜.  

𝙺𝚒𝚗𝚍𝚕𝚢 𝚓𝚘𝚒𝚗 𝚝𝚑𝚎 𝚌𝚑𝚊𝚗𝚗𝚎𝚕𝚜 𝚏𝚒𝚛𝚜𝚝 𝚝𝚘 𝚌𝚘𝚗𝚝𝚒𝚗𝚞𝚎  
𝚊𝚗𝚍 𝚞𝚗𝚕𝚘𝚌𝚔 𝚏𝚞𝚕𝚕 𝚏𝚎𝚊𝚝𝚞𝚛𝚎𝚜 ✨  
</b></blockquote>
"""
    if Config.FORCE_SUB_IMAGE:
        return await message.reply_photo(photo=Config.FORCE_SUB_IMAGE, caption=text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
#

# ═══════════════════════════════════════════════════════════════
# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
#
# Portfolio: https://aratt.ai/@roxybasicneedbot
#
# Bot & Website Developer 🤖
# Creator of RoxyBasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
#
# © 2026 RoxyBasicNeedBot. All Rights Reserved.
# ═══════════════════════════════════════════════════════════════
