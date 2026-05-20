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

import asyncio


# ==================== STICKER IDs ====================
# Add your sticker file_ids here
# You can get sticker ID by forwarding sticker to @userinfobot or @RawDataBot

STICKERS = {
    # Success stickers for different actions - each gets a unique sticker
    "caption_set": "CAACAgIAAxkBAAIKu2lLmb0LP36gXA-LyS4SkVrzWxvNAAI5GgAC7bwoSfirS7Hm88FYHgQ",  # 😏 FunnyKids1 (Static)
    "autorename_set": "CAACAgIAAxkBAAIKvWlLmeXRHMSkiCPiBt2wcOUIi6u8AAJAAAOvxlEaV1XfcKI2zaoeBA",  # 👍 TheLittleMole (Animated)
    "thumbnail_set": "CAACAgUAAxkBAAIKv2lLmqKmZHiadh-rGrvPPpDjyOkGAAK9BQACw8txVSr1Xl_z7bGVHgQ",  # 😂 VIDEO_PACK_V2 (Video)
    "prefix_set": "CAACAgUAAxkBAAIKwWlLmtHCGwaik1H_z3U1_1BbndwtAAJDEQACJxf4V8g1oV5RtWGQHgQ",  # 🐱 MAGIC455 (Static)
    "suffix_set": "CAACAgQAAxkBAAIKw2lLmv2qCXvGA39J1OlDl44b8ZvCAAJnDgAC2O1wUONXZ-rprVWYHgQ",  # 😐 MargaretQualleyMood (Static)
    "media_set": "CAACAgUAAxkBAAIKxWlLmyIZJMpPnrXq2KbQNVZrQNzSAALOBgAC50UxVd2o2l28a3FjHgQ",  # 😏 Vieillot (Static)
    "settings_updated": "CAACAgUAAxkBAAIKx2lLm0e-MCbzifuuE2DzjJeE2jv_AALtBAACqRUwVXfqeXOxLe4THgQ",  # 😎 Vieillot (Static)
    "free_user": "CAACAgUAAxkBAAILK2lPyYtbo-O-_tpF2QkNKf8qpCxGAALUCAAC4Tz4VOxMqgy_QNBbHgQ",  # 🆓 Free user sticker
}


async def send_success_sticker(client, chat_id, sticker_type="caption_set"):
    """
    Send a success sticker.
    
    Args:
        client: Pyrogram client instance
        chat_id: Chat ID to send sticker to
        sticker_type: Type of sticker to send (key from STICKERS dict)
    
    Returns:
        The sticker message object or None if failed
    """

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

    try:
        sticker_id = STICKERS.get(sticker_type, STICKERS["caption_set"])
        sticker_msg = await client.send_sticker(chat_id, sticker_id)
        return sticker_msg
    except Exception as e:
        print(f"Error sending sticker: {e}")
        return None


async def send_sticker_with_message(client, chat_id, text, sticker_type="caption_set", delete_sticker_after=3):
    """
    Send a sticker followed by a text message.
    
    Args:
        client: Pyrogram client instance
        chat_id: Chat ID to send to
        text: Text message to send
        sticker_type: Type of sticker to send
        delete_sticker_after: Seconds to wait before deleting sticker
    
    Returns:
        Tuple of (sticker_message, text_message)
    """
    try:
        sticker_id = STICKERS.get(sticker_type, STICKERS["caption_set"])
        sticker_msg = await client.send_sticker(chat_id, sticker_id)
        text_msg = await client.send_message(chat_id, text)
        
        if delete_sticker_after > 0:
            await asyncio.sleep(delete_sticker_after)
            try:
                await sticker_msg.delete()
            except:
                pass
        
        return sticker_msg, text_msg
    except Exception as e:
        print(f"Error sending sticker with message: {e}")
        return None, None

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
