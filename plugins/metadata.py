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
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ListenerTimeout

# extra imports
from helper.database import roxy_bot
from helper.utils import send_reaction
from config import roxy

TRUE = [[InlineKeyboardButton('🔛 Metadata On', callback_data='metadata_1'),
       InlineKeyboardButton('✅', callback_data='metadata_1')
       ],[
       InlineKeyboardButton('⚙️ Set Custom Metadata', callback_data='custom_metadata')]]

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

FALSE = [[InlineKeyboardButton('📴 Metadata Off', callback_data='metadata_0'),
        InlineKeyboardButton('❌', callback_data='metadata_0')
       ],[
       InlineKeyboardButton('⚙️ Set Custom Metadata', callback_data='custom_metadata')]]


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):
    await send_reaction(bot, message)
    RoxyDev = await message.reply_text("<blockquote>**Please Wait...**</blockquote>", reply_to_message_id=message.id)
    bool_metadata = await roxy_bot.get_metadata_mode(message.from_user.id)
    user_metadata = await roxy_bot.get_metadata_code(message.from_user.id)

    await RoxyDev.edit(
        f"<blockquote>Your Current Metadata:-\n\n➜ `{user_metadata}`</blockquote>",
        reply_markup=InlineKeyboardMarkup(TRUE if bool_metadata else FALSE)
    )


@Client.on_callback_query(filters.regex('.*?(custom_metadata|metadata).*?'))
async def query_metadata(bot: Client, query: CallbackQuery):
    data = query.data
    if data.startswith('metadata_'):
        _bool = data.split('_')[1]
        user_metadata = await roxy_bot.get_metadata_code(query.from_user.id)
        bool_meta = bool(eval(_bool))
        await roxy_bot.set_metadata_mode(query.from_user.id, bool_meta=not bool_meta)
        await query.message.edit(f"<blockquote>Your Current Metadata:-\n\n➜ `{user_metadata}`</blockquote>", reply_markup=InlineKeyboardMarkup(FALSE if bool_meta else TRUE))
           
    elif data == 'custom_metadata':
        await query.message.delete()
        try:
            metadata = await bot.ask(text=roxy.SEND_METADATA, chat_id=query.from_user.id, filters=filters.text, timeout=30, disable_web_page_preview=True)
            RoxyDev = await query.message.reply_text("<blockquote>**Please Wait...**</blockquote>", reply_to_message_id=metadata.id)
            await roxy_bot.set_metadata_code(query.from_user.id, metadata_code=metadata.text)
            await RoxyDev.edit("<blockquote>**Your Metadata Code Set Successfully ✅**</blockquote>")
        except ListenerTimeout:
            await query.message.reply_text("<blockquote>⚠️ Error!!\n\n**Request timed out.**\nRestart by using /metadata</blockquote>", reply_to_message_id=query.message.id)
        except Exception as e:
            print(e)


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
