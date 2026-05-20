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

# imports
from pyrogram import Client, filters, enums
from helper.database import roxy_bot
from helper.utils import send_reaction

# prefix commond ✨
@Client.on_message(filters.private & filters.command('set_prefix'))
async def add_prefix(client, message):
    await send_reaction(client, message)
    if len(message.command) == 1:
        return await message.reply_text("<blockquote>**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @roxybasicneedbot1`**</blockquote>")
    prefix = message.text.split(" ", 1)[1]
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    await roxy_bot.set_prefix(message.from_user.id, prefix)
    await RoxyDev.edit("<blockquote>__**✅ ᴘʀᴇꜰɪx ꜱᴀᴠᴇᴅ**__</blockquote>")

@Client.on_message(filters.private & filters.command('del_prefix'))
async def delete_prefix(client, message):
    await send_reaction(client, message)
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    prefix = await roxy_bot.get_prefix(message.from_user.id)

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

    if not prefix:
        return await RoxyDev.edit("<blockquote>__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__</blockquote>")
    await roxy_bot.set_prefix(message.from_user.id, None)
    await RoxyDev.edit("<blockquote>__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__</blockquote>")

@Client.on_message(filters.private & filters.command('see_prefix'))
async def see_prefix(client, message):
    await send_reaction(client, message)
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    prefix = await roxy_bot.get_prefix(message.from_user.id)
    if prefix:
        await RoxyDev.edit(f"<blockquote>**ʏᴏᴜʀ ᴘʀᴇꜰɪx:-**\n\n`{prefix}`</blockquote>")
    else:
        await RoxyDev.edit("<blockquote>__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__</blockquote>")

# SUFFIX COMMOND ✨
@Client.on_message(filters.private & filters.command('set_suffix'))
async def add_suffix(client, message):
    await send_reaction(client, message)
    if len(message.command) == 1:
        return await message.reply_text("<blockquote>**__Give The Suffix__\n\nExᴀᴍᴩʟᴇ:- `/set_suffix @roxybasicneedbot1`**</blockquote>")
    suffix = message.text.split(" ", 1)[1]
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    await roxy_bot.set_suffix(message.from_user.id, suffix)
    await RoxyDev.edit("<blockquote>__**✅ ꜱᴜꜰꜰɪx ꜱᴀᴠᴇᴅ**__</blockquote>")

@Client.on_message(filters.private & filters.command('del_suffix'))
async def delete_suffix(client, message):
    await send_reaction(client, message)
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    suffix = await roxy_bot.get_suffix(message.from_user.id)
    if not suffix:
        return await RoxyDev.edit("<blockquote>__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__</blockquote>")
    await roxy_bot.set_suffix(message.from_user.id, None)
    await RoxyDev.edit("<blockquote>__**❌️ ꜱᴜꜰꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__</blockquote>")

@Client.on_message(filters.private & filters.command('see_suffix'))
async def see_suffix(client, message):
    await send_reaction(client, message)
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    suffix = await roxy_bot.get_suffix(message.from_user.id)
    if suffix:
        await RoxyDev.edit(f"<blockquote>**ʏᴏᴜʀ ꜱᴜꜰꜰɪx:-**\n\n`{suffix}`</blockquote>")
    else:
        await RoxyDev.edit("<blockquote>__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__</blockquote>")


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
