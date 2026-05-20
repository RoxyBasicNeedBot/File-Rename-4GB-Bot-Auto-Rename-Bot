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
from pyrogram import Client, filters
from helper.database import roxy_bot
from helper.utils import send_reaction
from helper.stickers import send_success_sticker

AUTORENAME_HELP = """<blockquote>
📝 <b><u>Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Tᴇᴍᴘʟᴀᴛᴇ</u></b>

Sᴇᴛ ᴀ ᴛᴇᴍᴘʟᴀᴛᴇ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ꜰɪʟᴇs.

➢ /autorename - Sᴇᴛ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ
➢ /see_autorename - Vɪᴇᴡ ʏᴏᴜʀ ᴛᴇᴍᴘʟᴀᴛᴇ
➢ /del_autorename - Dᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴛᴇᴍᴘʟᴀᴛᴇ

<b>Sᴜᴘᴘᴏʀᴛᴇᴅ Pʟᴀᴄᴇʜᴏʟᴅᴇʀs:</b>
• {episode} - Episode number
• {season} - Season number  
• {chapter} - Chapter number
• {quality} - Video quality (480p, 720p, etc.)
• {audio} - Audio language

<b>Exᴀᴍᴩʟᴇs:</b>
➥ Exᴀᴍᴘʟᴇ1: <code>/autorename [WF] [C{chapter}] One Pi @roxybasicneedbot1</code>

➤ Exᴀᴍᴘʟᴇ2: <code>/autorename [S{season} E{episode}] One Pi [{quality}] [{audio}]</code>

Note: Don't put .mkv or .mp4 at the end.
Tʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴜsᴇ ᴛʜɪs ᴛᴇᴍᴘʟᴀᴛᴇ ᴛᴏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ғɪʟᴇs ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.
</blockquote>"""

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



# Set autorename template command
@Client.on_message(filters.private & filters.command('autorename'))
async def set_autorename(client, message):
    await send_reaction(client, message)
    if len(message.command) == 1:
        return await message.reply_text(AUTORENAME_HELP)
    
    template = message.text.split(" ", 1)[1]
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    await roxy_bot.set_autorename(message.from_user.id, template)
    await RoxyDev.edit(f"<blockquote>__**✅ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ ꜱᴀᴠᴇᴅ**__\n\n**Tᴇᴍᴘʟᴀᴛᴇ:** `{template}`</blockquote>")
    await send_success_sticker(client, message.chat.id, "autorename_set")


# View autorename template command
@Client.on_message(filters.private & filters.command('see_autorename'))
async def see_autorename(client, message):
    await send_reaction(client, message)
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    template = await roxy_bot.get_autorename(message.from_user.id)
    if template:
        await RoxyDev.edit(f"<blockquote>**ʏᴏᴜʀ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ:-**\n\n`{template}`</blockquote>")
    else:
        await RoxyDev.edit("<blockquote>__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ**__\n\nUse /autorename to set one.</blockquote>")


# Delete autorename template command
@Client.on_message(filters.private & filters.command('del_autorename'))
async def delete_autorename(client, message):
    await send_reaction(client, message)
    RoxyDev = await message.reply_text("<blockquote>Please Wait ...</blockquote>", reply_to_message_id=message.id)
    template = await roxy_bot.get_autorename(message.from_user.id)
    if not template:
        return await RoxyDev.edit("<blockquote>__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ**__</blockquote>")
    await roxy_bot.set_autorename(message.from_user.id, None)
    await RoxyDev.edit("<blockquote>__**❌️ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ ᴅᴇʟᴇᴛᴇᴅ**__</blockquote>")

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
