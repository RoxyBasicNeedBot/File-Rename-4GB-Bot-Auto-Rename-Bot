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
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import roxy_bot
from helper.utils import send_reaction
from helper.stickers import send_success_sticker

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    await send_reaction(client, message)
    roxy = await message.reply_text("<blockquote>__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__</blockquote>")
    if len(message.command) == 1:
       return await roxy.edit("<blockquote>**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__**\n\n<b>Sᴜᴘᴘᴏʀᴛᴇᴅ Pʟᴀᴄᴇʜᴏʟᴅᴇʀs:</b>\n• {filename} - File name\n• {filesize} - File size\n• {duration} - Duration\n• {episode} - Episode number\n• {season} - Season number\n• {quality} - Video quality\n• {audio} - Audio language\n• {chapter} - Chapter number\n\n<b>Exᴀᴍᴩʟᴇ:</b>\n<code>/set_caption 📕 {filename}\n\n📺 S{season} E{episode}\n💾 Size: {filesize}\n🎧 Audio: {audio}\n📹 Quality: {quality}\n\n@your_channel</code></blockquote>")
    caption = message.text.split(" ", 1)[1]
    await roxy_bot.set_caption(message.from_user.id, caption=caption)
    await roxy.edit("<blockquote>__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__</blockquote>")
    await send_success_sticker(client, message.chat.id, "caption_set")
   
@Client.on_message(filters.private & filters.command(['del_caption', 'delete_caption', 'delcaption']))
async def delete_caption(client, message):
    await send_reaction(client, message)
    roxy = await message.reply_text("<blockquote>__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__</blockquote>")
    caption = await roxy_bot.get_caption(message.from_user.id)  
    if not caption:
       return await roxy.edit("<blockquote>__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__</blockquote>")
    await roxy_bot.set_caption(message.from_user.id, caption=None)
    await roxy.edit("<blockquote>__**❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ**__</blockquote>")
                                       
@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    await send_reaction(client, message)
    roxy = await message.reply_text("<blockquote>__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__</blockquote>")
    caption = await roxy_bot.get_caption(message.from_user.id)  
    if caption:
       await roxy.edit(f"<blockquote>**Yᴏᴜ'ʀᴇ Cᴀᴩᴛɪᴏɴ:-**\n\n`{caption}`</blockquote>")
    else:
       await roxy.edit("<blockquote>__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__</blockquote>")

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):
    await send_reaction(client, message)
    roxy = await message.reply_text("<blockquote>__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__</blockquote>")
    thumb = await roxy_bot.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
        await roxy.delete()
    else:
        await roxy.edit("<blockquote>😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__</blockquote>") 
		
@Client.on_message(filters.private & filters.command(['del_thumb', 'delete_thumb', 'delthumb']))
async def removethumb(client, message):
    await send_reaction(client, message)
    roxy = await message.reply_text("<blockquote>__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__</blockquote>")
    thumb = await roxy_bot.get_thumbnail(message.from_user.id)
    if thumb:
        await roxy_bot.set_thumbnail(message.from_user.id, file_id=None)
        await roxy.edit("<blockquote>❌️ __**Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ**__</blockquote>")
        return
    await roxy.edit("<blockquote>😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__</blockquote>")


@Client.on_message(filters.private & filters.photo)

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

async def addthumbs(client, message):
    await send_reaction(client, message)
    roxy = await message.reply_text("<blockquote>__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__</blockquote>")
    await roxy_bot.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await roxy.edit("<blockquote>✅️ __**Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ**__</blockquote>")
    await send_success_sticker(client, message.chat.id, "thumbnail_set")


# Set Media Type Command
@Client.on_message(filters.private & filters.command(['setmedia', 'set_media']))
async def set_media_type(client, message):
    await send_reaction(client, message)
    user_id = message.from_user.id
    current_type = await roxy_bot.get_media_type(user_id)
    
    # Build buttons with checkmark on selected option
    doc_text = "✅ Dᴏᴄᴜᴍᴇɴᴛ" if current_type == "document" else "📁 Dᴏᴄᴜᴍᴇɴᴛ"
    vid_text = "✅ Vɪᴅᴇᴏ" if current_type == "video" else "🎥 Vɪᴅᴇᴏ"
    aud_text = "✅ Aᴜᴅɪᴏ" if current_type == "audio" else "🎵 Aᴜᴅɪᴏ"
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(doc_text, callback_data="setmedia_document"),
            InlineKeyboardButton(vid_text, callback_data="setmedia_video")
        ],
        [
            InlineKeyboardButton(aud_text, callback_data="setmedia_audio")
        ]
    ])
    
    await message.reply_text(
        text="<blockquote><b>Sᴇʟᴇᴄᴛ Yᴏᴜʀ Pʀᴇꜰᴇʀʀᴇᴅ Mᴇᴅɪᴀ Tyᴩᴇ:</b>\n\nTʜɪs ᴡɪʟʟ ᴅᴇᴛᴇʀᴍɪɴᴇ ʜᴏᴡ ʏᴏᴜʀ ꜰɪʟᴇs ᴀʀᴇ ʜᴀɴᴅʟᴇᴅ ʙʏ ᴛʜᴇ ʙᴏᴛ.</blockquote>",
        reply_markup=buttons
    )


# Delete media type command
@Client.on_message(filters.private & filters.command(['delmedia', 'del_media', 'deletemedia']))
async def delete_media_type(client, message):
    user_id = message.from_user.id
    
    # Check if user has a saved media type
    current_type = await roxy_bot.get_media_type(user_id)
    
    if current_type:
        # Remove the media type by setting it to None
        await roxy_bot.set_media_type(user_id, None)
        await message.reply_text(
            "<blockquote>✅ <b>Mᴇᴅɪᴀ Tyᴩᴇ Dᴇʟᴇᴛᴇᴅ!</b>\n\nYᴏᴜ ᴡɪʟʟ ɴᴏᴡ ʙᴇ ᴀsᴋᴇᴅ ᴛᴏ sᴇʟᴇᴄᴛ ᴏᴜᴛᴘᴜᴛ ᴛʏᴘᴇ ᴇᴀᴄʜ ᴛɪᴍᴇ.</blockquote>"
        )
    else:
        await message.reply_text(
            "<blockquote>❌ Nᴏ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ ɪs sᴇᴛ.\n\nUsᴇ /setmedia ᴛᴏ sᴇᴛ ᴏɴᴇ.</blockquote>"
        )


# Callback handler for setmedia buttons
@Client.on_callback_query(filters.regex(r'^setmedia_(document|video|audio)$'))
async def setmedia_callback(client, callback_query):
    user_id = callback_query.from_user.id
    media_type = callback_query.data.split("_")[1]
    
    # Save the media type preference
    await roxy_bot.set_media_type(user_id, media_type)
    
    # Update buttons to show new selection
    doc_text = "✅ Dᴏᴄᴜᴍᴇɴᴛ" if media_type == "document" else "📁 Dᴏᴄᴜᴍᴇɴᴛ"
    vid_text = "✅ Vɪᴅᴇᴏ" if media_type == "video" else "🎥 Vɪᴅᴇᴏ"
    aud_text = "✅ Aᴜᴅɪᴏ" if media_type == "audio" else "🎵 Aᴜᴅɪᴏ"
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(doc_text, callback_data="setmedia_document"),
            InlineKeyboardButton(vid_text, callback_data="setmedia_video")
        ],
        [
            InlineKeyboardButton(aud_text, callback_data="setmedia_audio")
        ]
    ])
    
    type_names = {"document": "📁 Dᴏᴄᴜᴍᴇɴᴛ", "video": "🎥 Vɪᴅᴇᴏ", "audio": "🎵 Aᴜᴅɪᴏ"}
    
    await callback_query.message.edit_text(
        text=f"<blockquote><b>Sᴇʟᴇᴄᴛ Yᴏᴜʀ Pʀᴇꜰᴇʀʀᴇᴅ Mᴇᴅɪᴀ Tyᴩᴇ:</b>\n\nTʜɪs ᴡɪʟʟ ᴅᴇᴛᴇʀᴍɪɴᴇ ʜᴏᴡ ʏᴏᴜʀ ꜰɪʟᴇs ᴀʀᴇ ʜᴀɴᴅʟᴇᴅ ʙʏ ᴛʜᴇ ʙᴏᴛ.\n\n✅ <b>Sᴇʟᴇᴄᴛᴇᴅ:</b> {type_names[media_type]}</blockquote>",
        reply_markup=buttons
    )
    await callback_query.answer(f"✅ Media type set to {media_type.title()}")
    await send_success_sticker(callback_query._client, callback_query.message.chat.id, "media_set")

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
