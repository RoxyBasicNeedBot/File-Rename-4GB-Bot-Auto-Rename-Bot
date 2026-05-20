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
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChannelPrivate, ChannelInvalid, MessageNotModified
from helper.database import roxy_bot
from helper.utils import send_reaction
from helper.tmdb_client import is_tmdb_available
from config import Config


# Settings command
@Client.on_message(filters.private & filters.command(['settings']))
async def settings_command(client, message):
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    # Get current settings
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
    mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    trim_mode = await roxy_bot.get_trim_mode(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    
    # TMDb settings
    tmdb_auto = await roxy_bot.get_tmdb_auto_mode(user_id)
    tmdb_thumb = await roxy_bot.get_tmdb_auto_thumb(user_id)
    tmdb_lang = await roxy_bot.get_tmdb_language(user_id)
    tmdb_available = is_tmdb_available()
    
    if dump_channel:
        try:
            chat = await client.get_chat(dump_channel)
            channel_name = chat.title
            dump_status = f"✅ {channel_name}"
        except:
            dump_status = f"⚠️ ID: {dump_channel}"
    else:
        dump_status = "❌ Nᴏᴛ Sᴇᴛ"
    
    # Screenshot status
    ss_status = "✅ ON" if screenshot_mode else "❌ OFF"
    # MKV to MP4 status
    mkv_status = "✅ ON" if mkv_to_mp4_mode else "❌ OFF"
    # Compress Video status (Premium only)
    if is_premium:
        compress_status = "✅ ON" if compress_mode else "❌ OFF"
    else:
        compress_status = "🔒 Premium"
    # Trim status (Premium only)
    if is_premium:
        trim_status = "✅ ON" if trim_mode else "❌ OFF"
    else:
        trim_status = "🔒 Premium"
    
    # TMDb status
    if tmdb_available:
        tmdb_auto_status = "✅ ON" if tmdb_auto else "❌ OFF"
        tmdb_thumb_status = "✅ ON" if tmdb_thumb else "❌ OFF"
    else:
        tmdb_auto_status = "⚠️ No API Key"
        tmdb_thumb_status = "⚠️ No API Key"
    
    # Find language display name
    lang_display = tmdb_lang
    for code, name in Config.TMDB_LANGUAGES:
        if code == tmdb_lang:
            lang_display = name
            break
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
        [InlineKeyboardButton(f"📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ: {dump_status}", callback_data="settings_viewdump")],
        [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
         InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
        [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
         InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
        [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss Vɪᴅᴇᴏ", callback_data="settings_compress_info"), 
         InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
        [InlineKeyboardButton(f"✂️ Tʀɪᴍ Vɪᴅᴇᴏ", callback_data="settings_trim_info"), 
         InlineKeyboardButton(f"{trim_status}", callback_data="settings_toggle_trim")],
        [InlineKeyboardButton(f"🎬 TMDb Aᴜᴛᴏ-Dᴇᴛᴇᴄᴛ", callback_data="settings_tmdb_info"),
         InlineKeyboardButton(f"{tmdb_auto_status}", callback_data="settings_toggle_tmdb")],
        [InlineKeyboardButton(f"🖼️ TMDb Tʜᴜᴍʙɴᴀɪʟ", callback_data="settings_tmdb_thumb_info"),
         InlineKeyboardButton(f"{tmdb_thumb_status}", callback_data="settings_toggle_tmdb_thumb")],
        [InlineKeyboardButton(f"🌐 TMDb Lᴀɴɢ: {lang_display}", callback_data="settings_tmdb_lang")],
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_removedump")],
        [InlineKeyboardButton("✖️ Cʟᴏsᴇ", callback_data="close")]
    ])
    
    await message.reply_text(
        text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
        reply_markup=buttons
    )



# Callback for Set Dump Channel button
@Client.on_callback_query(filters.regex(r'^settings_setdump$'))
async def setdump_callback(client, callback_query):
    await callback_query.message.edit_text(
        text="<blockquote><b>🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ</b>\n\nSᴇɴᴅ ᴍᴇ ᴛʜᴇ Cʜᴀɴɴᴇʟ ID ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴜᴍᴘ ʀᴇɴᴀᴍᴇᴅ ꜰɪʟᴇs.\n\n<b>📌 Hᴏᴡ ᴛᴏ ɢᴇᴛ Cʜᴀɴɴᴇʟ ID:</b>\n1️⃣ Fᴏʀᴡᴀʀᴅ ᴀɴʏ ᴍᴇssᴀɢᴇ ꜰʀᴏᴍ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ @useridroxybot\n2️⃣ Iᴛ ᴡɪʟʟ sʜᴏᴡ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ID (ʟɪᴋᴇ -1001234567890)\n\n<b>⚠️ Iᴍᴘᴏʀᴛᴀɴᴛ:</b> Mᴀᴋᴇ sᴜʀᴇ I ᴀᴍ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ ᴡɪᴛʜ ᴘᴏsᴛ ᴘᴇʀᴍɪssɪᴏɴs!</blockquote>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="settings_back")]
        ])
    )
    
    # Set a flag to listen for channel ID
    await roxy_bot.col.update_one(
        {'_id': callback_query.from_user.id},
        {'$set': {'awaiting_dump_channel': True}}
    )
    await callback_query.answer()


# Callback for View Dump Channel
@Client.on_callback_query(filters.regex(r'^settings_viewdump$'))
async def viewdump_callback(client, callback_query):
    user_id = callback_query.from_user.id
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    
    if dump_channel:
        try:
            chat = await client.get_chat(dump_channel)
            info_text = f"<blockquote><b>📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ Iɴꜰᴏ</b>\n\n<b>Nᴀᴍᴇ:</b> {chat.title}\n<b>ID:</b> <code>{dump_channel}</code>\n<b>Sᴛᴀᴛᴜs:</b> ✅ Aᴄᴛɪᴠᴇ</blockquote>"
        except Exception as e:
            info_text = f"<blockquote><b>📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ Iɴꜰᴏ</b>\n\n<b>ID:</b> <code>{dump_channel}</code>\n<b>Sᴛᴀᴛᴜs:</b> ⚠️ Cᴀɴɴᴏᴛ ᴀᴄᴄᴇss (Mᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ)</blockquote>"
    else:
        info_text = "<blockquote><b>📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ</b>\n\n❌ Nᴏ ᴅᴜᴍᴘ ᴄʜᴀɴɴᴇʟ sᴇᴛ.\n\nUse <b>Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ</b> ᴛᴏ ᴄᴏɴꜰɪɢᴜʀᴇ.</blockquote>"
    
    await callback_query.message.edit_text(
        text=info_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="settings_back")]
        ])
    )
    await callback_query.answer()


# Callback for Remove Dump Channel
@Client.on_callback_query(filters.regex(r'^settings_removedump$'))
async def removedump_callback(client, callback_query):
    user_id = callback_query.from_user.id
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    
    if dump_channel:
        await roxy_bot.set_dump_channel(user_id, None)
        await callback_query.answer("✅ Dump channel removed!", show_alert=True)
    else:
        await callback_query.answer("❌ No dump channel set!", show_alert=True)
    
    # Refresh settings menu - Get remaining settings for button status
    screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
    mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    ss_status = "✅ ON" if screenshot_mode else "❌ OFF"
    mkv_status = "✅ ON" if mkv_to_mp4_mode else "❌ OFF"
    compress_status = ("✅ ON" if compress_mode else "❌ OFF") if is_premium else "🔒 Premium"
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
        [InlineKeyboardButton(f"📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ: ❌ Nᴏᴛ Sᴇᴛ", callback_data="settings_viewdump")],
        [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
         InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
        [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
         InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
        [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss Vɪᴅᴇᴏ", callback_data="settings_compress_info"), 
         InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_removedump")],
        [InlineKeyboardButton("✖️ Cʟᴏsᴇ", callback_data="close")]
    ])
    
    try:
        await callback_query.message.edit_text(
            text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
            reply_markup=buttons
        )
    except MessageNotModified:
        pass


# Callback for Back to Settings
@Client.on_callback_query(filters.regex(r'^settings_back$'))
async def settings_back_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Clear awaiting flag
    await roxy_bot.col.update_one(
        {'_id': user_id},
        {'$set': {'awaiting_dump_channel': False}}
    )
    
    # Get current settings
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
    mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    trim_mode = await roxy_bot.get_trim_mode(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    
    if dump_channel:
        try:
            chat = await client.get_chat(dump_channel)
            channel_name = chat.title
            dump_status = f"✅ {channel_name}"
        except:
            dump_status = f"⚠️ ID: {dump_channel}"
    else:
        dump_status = "❌ Nᴏᴛ Sᴇᴛ"
    
    ss_status = "✅ ON" if screenshot_mode else "❌ OFF"
    mkv_status = "✅ ON" if mkv_to_mp4_mode else "❌ OFF"
    compress_status = ("✅ ON" if compress_mode else "❌ OFF") if is_premium else "🔒 Premium"
    trim_status = ("✅ ON" if trim_mode else "❌ OFF") if is_premium else "🔒 Premium"
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
        [InlineKeyboardButton(f"📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ: {dump_status}", callback_data="settings_viewdump")],
        [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
         InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
        [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
         InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
        [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss Vɪᴅᴇᴏ", callback_data="settings_compress_info"), 
         InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
        [InlineKeyboardButton(f"✂️ Tʀɪᴍ Vɪᴅᴇᴏ", callback_data="settings_trim_info"), 
         InlineKeyboardButton(f"{trim_status}", callback_data="settings_toggle_trim")],
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_removedump")],
        [InlineKeyboardButton("✖️ Cʟᴏsᴇ", callback_data="close")]
    ])
    
    await callback_query.message.edit_text(
        text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
        reply_markup=buttons
    )
    await callback_query.answer()



# Callback for Screenshot Info
@Client.on_callback_query(filters.regex(r'^settings_ss_info$'))
async def screenshot_info_callback(client, callback_query):
    await callback_query.answer(
        "📸 When enabled, bot will generate screenshots from video every 5 seconds and send them as album.",
        show_alert=True
    )


# Callback for Toggle Screenshot Mode
@Client.on_callback_query(filters.regex(r'^settings_toggle_ss$'))
async def toggle_screenshot_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Get current mode and toggle
    current_mode = await roxy_bot.get_screenshot_mode(user_id)
    new_mode = not current_mode
    await roxy_bot.set_screenshot_mode(user_id, new_mode)
    
    # Get other settings for button refresh
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    
    if dump_channel:
        try:
            chat = await client.get_chat(dump_channel)
            dump_status = f"✅ {chat.title}"
        except:
            dump_status = f"⚠️ ID: {dump_channel}"
    else:
        dump_status = "❌ Nᴏᴛ Sᴇᴛ"
    
    ss_status = "✅ ON" if new_mode else "❌ OFF"
    mkv_status = "✅ ON" if mkv_to_mp4_mode else "❌ OFF"
    compress_status = ("✅ ON" if compress_mode else "❌ OFF") if is_premium else "🔒 Premium"
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
        [InlineKeyboardButton(f"📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ: {dump_status}", callback_data="settings_viewdump")],
        [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
         InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
        [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
         InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
        [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss Vɪᴅᴇᴏ", callback_data="settings_compress_info"), 
         InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_removedump")],
        [InlineKeyboardButton("✖️ Cʟᴏsᴇ", callback_data="close")]
    ])
    
    await callback_query.message.edit_text(
        text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
        reply_markup=buttons
    )
    
    status_text = "enabled" if new_mode else "disabled"
    await callback_query.answer(f"📸 Screenshots {status_text}!")


# Callback for MKV to MP4 Info
@Client.on_callback_query(filters.regex(r'^settings_mkv_info$'))
async def mkv_info_callback(client, callback_query):
    await callback_query.answer(
        "🎬 When enabled, MKV files will be automatically converted to MP4 format using FFmpeg remux (fast, no quality loss).",
        show_alert=True
    )


# Callback for Toggle MKV to MP4 Mode
@Client.on_callback_query(filters.regex(r'^settings_toggle_mkv$'))
async def toggle_mkv_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Get current mode and toggle
    current_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    new_mode = not current_mode
    await roxy_bot.set_convert_mkv_to_mp4(user_id, new_mode)
    
    # Get other settings for button refresh
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    
    if dump_channel:
        try:
            chat = await client.get_chat(dump_channel)

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

            dump_status = f"✅ {chat.title}"
        except:
            dump_status = f"⚠️ ID: {dump_channel}"
    else:
        dump_status = "❌ Nᴏᴛ Sᴇᴛ"
    
    ss_status = "✅ ON" if screenshot_mode else "❌ OFF"
    mkv_status = "✅ ON" if new_mode else "❌ OFF"
    compress_status = ("✅ ON" if compress_mode else "❌ OFF") if is_premium else "🔒 Premium"
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
        [InlineKeyboardButton(f"📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ: {dump_status}", callback_data="settings_viewdump")],
        [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
         InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
        [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
         InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
        [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss Vɪᴅᴇᴏ", callback_data="settings_compress_info"), 
         InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_removedump")],
        [InlineKeyboardButton("✖️ Cʟᴏsᴇ", callback_data="close")]
    ])
    
    await callback_query.message.edit_text(
        text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
        reply_markup=buttons
    )
    
    status_text = "enabled" if new_mode else "disabled"
    await callback_query.answer(f"🎬 MKV to MP4 conversion {status_text}!")


# Callback for Compress Video Info
@Client.on_callback_query(filters.regex(r'^settings_compress_info$'))
async def compress_info_callback(client, callback_query):
    await callback_query.answer(
        "📦 Compresses video to 720p, 480p, 360p after renaming. Takes ~10-35 min for 1GB file. Premium only!",
        show_alert=True
    )


# Callback for Toggle Compress Video Mode (Premium Only)
@Client.on_callback_query(filters.regex(r'^settings_toggle_compress$'))
async def toggle_compress_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Check premium access
    is_premium = await roxy_bot.has_premium_access(user_id)
    if not is_premium:
        return await callback_query.answer("🔒 This feature is for Premium users only! Use /plans to upgrade.", show_alert=True)
    
    # Get current mode and toggle
    current_mode = await roxy_bot.get_compress_video(user_id)
    new_mode = not current_mode
    await roxy_bot.set_compress_video(user_id, new_mode)
    
    # Get other settings for button refresh
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
    mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    
    if dump_channel:
        try:
            chat = await client.get_chat(dump_channel)
            dump_status = f"✅ {chat.title}"
        except:
            dump_status = f"⚠️ ID: {dump_channel}"
    else:
        dump_status = "❌ Nᴏᴛ Sᴇᴛ"
    
    ss_status = "✅ ON" if screenshot_mode else "❌ OFF"
    mkv_status = "✅ ON" if mkv_to_mp4_mode else "❌ OFF"
    compress_status = "✅ ON" if new_mode else "❌ OFF"
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
        [InlineKeyboardButton(f"📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ: {dump_status}", callback_data="settings_viewdump")],
        [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
         InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
        [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
         InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
        [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss Vɪᴅᴇᴏ", callback_data="settings_compress_info"), 
         InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_removedump")],
        [InlineKeyboardButton("✖️ Cʟᴏsᴇ", callback_data="close")]
    ])
    
    await callback_query.message.edit_text(
        text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
        reply_markup=buttons
    )
    
    status_text = "enabled" if new_mode else "disabled"
    await callback_query.answer(f"📦 Video compression {status_text}!")


# Message handler to receive channel ID
@Client.on_message(filters.private & filters.text & ~filters.command([
    'start', 'help', 'settings', 'setmedia', 'autorename', 'set_caption', 
    'del_caption', 'see_caption', 'set_prefix', 'del_prefix', 'see_prefix',
    'set_suffix', 'del_suffix', 'see_suffix', 'metadata', 'view_thumb', 
    'del_thumb', 'see_autorename', 'del_autorename', 'myplan', 'plans',
    'broadcast', 'stats', 'ban', 'unban', 'add_premium', 'remove_premium',
    'premium_list', 'banned_users'
]), group=5)
async def receive_dump_channel_id(client, message):
    user_id = message.from_user.id
    
    # Check if user is awaiting dump channel input
    user_data = await roxy_bot.get_user_data(user_id)
    if not user_data or not user_data.get('awaiting_dump_channel', False):
        return  # Not awaiting input, let other handlers process
    
    # Clear the awaiting flag
    await roxy_bot.col.update_one(
        {'_id': user_id},
        {'$set': {'awaiting_dump_channel': False}}
    )
    
    channel_id_text = message.text.strip()
    
    # Validate channel ID format
    try:
        channel_id = int(channel_id_text)
    except ValueError:
        await message.reply_text(
            "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Cʜᴀɴɴᴇʟ ID!</b>\n\nPʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍᴇʀɪᴄ ᴄʜᴀɴɴᴇʟ ID.\n\nExᴀᴍᴘʟᴇ: <code>-1001234567890</code></blockquote>"
        )
        return
    
    # Verify bot is admin in the channel
    try:
        chat = await client.get_chat(channel_id)
        member = await client.get_chat_member(channel_id, "me")
        
        if member.status.value not in ["administrator", "owner"]:
            await message.reply_text(
                f"<blockquote>❌ <b>Bᴏᴛ ɪs ɴᴏᴛ ᴀᴅᴍɪɴ!</b>\n\nPʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ɪɴ <b>{chat.title}</b> ᴡɪᴛʜ ᴘᴏsᴛ ᴘᴇʀᴍɪssɪᴏɴs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.</blockquote>"
            )
            return
        
        # Save the dump channel
        await roxy_bot.set_dump_channel(user_id, channel_id)
        
        await message.reply_text(
            f"<blockquote>✅ <b>Dᴜᴍᴘ Cʜᴀɴɴᴇʟ Sᴇᴛ!</b>\n\n<b>Cʜᴀɴɴᴇʟ:</b> {chat.title}\n<b>ID:</b> <code>{channel_id}</code>\n\n🎉 Aʟʟ ʏᴏᴜʀ ʀᴇɴᴀᴍᴇᴅ ꜰɪʟᴇs ᴡɪʟʟ ɴᴏᴡ ʙᴇ sᴇɴᴛ ᴛᴏ ᴛʜɪs ᴄʜᴀɴɴᴇʟ!</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ Bᴀᴄᴋ ᴛᴏ Sᴇᴛᴛɪɴɢs", callback_data="settings_back")]
            ])
        )
        
    except ChannelPrivate:
        await message.reply_text(
            "<blockquote>❌ <b>Cʜᴀɴɴᴇʟ ɪs ᴘʀɪᴠᴀᴛᴇ!</b>\n\nI ᴄᴀɴ'ᴛ ᴀᴄᴄᴇss ᴛʜɪs ᴄʜᴀɴɴᴇʟ. Pʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ꜰɪʀsᴛ.</blockquote>"
        )
    except ChannelInvalid:
        await message.reply_text(
            "<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ Cʜᴀɴɴᴇʟ!</b>\n\nTʜɪs ᴄʜᴀɴɴᴇʟ ᴅᴏᴇs ɴᴏᴛ ᴇxɪsᴛ ᴏʀ I ᴄᴀɴ'ᴛ ꜰɪɴᴅ ɪᴛ.</blockquote>"
        )
    except Exception as e:
        await message.reply_text(
            f"<blockquote>❌ <b>Eʀʀᴏʀ!</b>\n\n{str(e)}\n\nMᴀᴋᴇ sᴜʀᴇ I ᴀᴍ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.</blockquote>"
        )


# ===== TMDb Settings Callbacks =====

# TMDb Auto-Detection Info
@Client.on_callback_query(filters.regex(r'^settings_tmdb_info$'))
async def tmdb_info_callback(client, callback_query):
    await callback_query.answer(
        "🎬 TMDb Auto-Detection: When ON, bot scans filename → detects movie/series → shows TMDb poster + metadata before renaming.",
        show_alert=True
    )

# Toggle TMDb Auto-Detection
@Client.on_callback_query(filters.regex(r'^settings_toggle_tmdb$'))
async def toggle_tmdb_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    if not is_tmdb_available():
        return await callback_query.answer("⚠️ TMDb API key not configured! Ask admin to set TMDB_API_KEY.", show_alert=True)
    
    current = await roxy_bot.get_tmdb_auto_mode(user_id)
    new_mode = not current
    await roxy_bot.set_tmdb_auto_mode(user_id, new_mode)
    
    status = "enabled ✅" if new_mode else "disabled ❌"
    await callback_query.answer(f"🎬 TMDb Auto-Detection {status}!")
    
    # Refresh settings menu
    await _refresh_settings_menu(client, callback_query)

# TMDb Auto-Thumbnail Info
@Client.on_callback_query(filters.regex(r'^settings_tmdb_thumb_info$'))
async def tmdb_thumb_info_callback(client, callback_query):
    await callback_query.answer(
        "🖼️ TMDb Thumbnail: When ON, TMDb movie/series poster is automatically used as video thumbnail. Premium only!",
        show_alert=True
    )

# Toggle TMDb Auto-Thumbnail  
@Client.on_callback_query(filters.regex(r'^settings_toggle_tmdb_thumb$'))
async def toggle_tmdb_thumb_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    if not is_tmdb_available():
        return await callback_query.answer("⚠️ TMDb API key not configured!", show_alert=True)
    
    # TMDb Thumbnail is FREE for all users
    
    current = await roxy_bot.get_tmdb_auto_thumb(user_id)
    new_mode = not current
    await roxy_bot.set_tmdb_auto_thumb(user_id, new_mode)
    
    status = "enabled ✅" if new_mode else "disabled ❌"
    await callback_query.answer(f"🖼️ TMDb Auto-Thumbnail {status}!")
    
    await _refresh_settings_menu(client, callback_query)

# TMDb Language Selection Menu
@Client.on_callback_query(filters.regex(r'^settings_tmdb_lang$'))
async def tmdb_lang_menu_callback(client, callback_query):
    user_id = callback_query.from_user.id
    current_lang = await roxy_bot.get_tmdb_language(user_id)
    
    buttons = []
    row = []
    for code, name in Config.TMDB_LANGUAGES:
        mark = "✅ " if code == current_lang else ""
        row.append(InlineKeyboardButton(f"{mark}{name}", callback_data=f"settings_set_tmdb_lang_{code}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="settings_back")])
    
    await callback_query.message.edit_text(
        text="<blockquote><b>🌐 TMDb Language</b>\n\nSelect your preferred language for TMDb metadata (movie/series titles, descriptions).\n\n"
             f"<b>Current:</b> <code>{current_lang}</code></blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()

# Set TMDb Language
@Client.on_callback_query(filters.regex(r'^settings_set_tmdb_lang_'))
async def set_tmdb_lang_callback(client, callback_query):
    user_id = callback_query.from_user.id
    lang_code = callback_query.data.replace("settings_set_tmdb_lang_", "")
    
    await roxy_bot.set_tmdb_language(user_id, lang_code)
    
    # Find display name
    lang_name = lang_code
    for code, name in Config.TMDB_LANGUAGES:
        if code == lang_code:
            lang_name = name
            break
    
    await callback_query.answer(f"🌐 Language set to {lang_name}!")
    await _refresh_settings_menu(client, callback_query)


async def _refresh_settings_menu(client, callback_query):
    """Helper to rebuild and refresh the settings menu after any toggle."""
    user_id = callback_query.from_user.id
    
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
    mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    trim_mode = await roxy_bot.get_trim_mode(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    tmdb_auto = await roxy_bot.get_tmdb_auto_mode(user_id)
    tmdb_thumb = await roxy_bot.get_tmdb_auto_thumb(user_id)
    tmdb_lang = await roxy_bot.get_tmdb_language(user_id)
    tmdb_available = is_tmdb_available()
    
    if dump_channel:
        try:
            chat = await client.get_chat(dump_channel)
            dump_status = f"✅ {chat.title}"
        except:
            dump_status = f"⚠️ ID: {dump_channel}"
    else:
        dump_status = "❌ Nᴏᴛ Sᴇᴛ"
    
    ss_status = "✅ ON" if screenshot_mode else "❌ OFF"
    mkv_status = "✅ ON" if mkv_to_mp4_mode else "❌ OFF"
    compress_status = ("✅ ON" if compress_mode else "❌ OFF") if is_premium else "🔒 Premium"
    trim_status = ("✅ ON" if trim_mode else "❌ OFF") if is_premium else "🔒 Premium"
    
    if tmdb_available:
        tmdb_auto_status = "✅ ON" if tmdb_auto else "❌ OFF"
        tmdb_thumb_status = "✅ ON" if tmdb_thumb else "❌ OFF"
    else:
        tmdb_auto_status = "⚠️ No API Key"
        tmdb_thumb_status = "⚠️ No API Key"
    
    lang_display = tmdb_lang
    for code, name in Config.TMDB_LANGUAGES:
        if code == tmdb_lang:
            lang_display = name
            break
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
        [InlineKeyboardButton(f"📺 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ: {dump_status}", callback_data="settings_viewdump")],
        [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
         InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
        [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
         InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
        [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss Vɪᴅᴇᴏ", callback_data="settings_compress_info"), 
         InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
        [InlineKeyboardButton(f"✂️ Tʀɪᴍ Vɪᴅᴇᴏ", callback_data="settings_trim_info"), 
         InlineKeyboardButton(f"{trim_status}", callback_data="settings_toggle_trim")],
        [InlineKeyboardButton(f"🎬 TMDb Aᴜᴛᴏ-Dᴇᴛᴇᴄᴛ", callback_data="settings_tmdb_info"),
         InlineKeyboardButton(f"{tmdb_auto_status}", callback_data="settings_toggle_tmdb")],
        [InlineKeyboardButton(f"🖼️ TMDb Tʜᴜᴍʙɴᴀɪʟ", callback_data="settings_tmdb_thumb_info"),
         InlineKeyboardButton(f"{tmdb_thumb_status}", callback_data="settings_toggle_tmdb_thumb")],
        [InlineKeyboardButton(f"🌐 TMDb Lᴀɴɢ: {lang_display}", callback_data="settings_tmdb_lang")],
        [InlineKeyboardButton("❌ Rᴇᴍᴏᴠᴇ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_removedump")],
        [InlineKeyboardButton("✖️ Cʟᴏsᴇ", callback_data="close")]
    ])
    
    try:
        await callback_query.message.edit_text(
            text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
            reply_markup=buttons
        )
    except MessageNotModified:
        pass

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
