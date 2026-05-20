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

# Video Trim Handler - Premium Feature

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Message, CallbackQuery
from helper.database import roxy_bot
from helper.ffmpeg_trim import trim_video, get_video_duration
from helper.utils import humanbytes
import os, time, asyncio


# Store pending trim operations
pending_trim = {}  # user_id -> {file_path, filename, message_id, stage, start_time, file_msg}


# ===== Settings Callbacks =====

@Client.on_callback_query(filters.regex(r'^settings_trim_info$'))
async def trim_info_callback(client, callback_query):
    await callback_query.answer(
        "✂️ Trim videos before upload. Premium feature only!",
        show_alert=True
    )


@Client.on_callback_query(filters.regex(r'^settings_toggle_trim$'))
async def toggle_trim_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Check premium access
    is_premium = await roxy_bot.has_premium_access(user_id)
    if not is_premium:
        return await callback_query.answer(
            "🔒 Trim is for Premium users only! Use /plans to upgrade.",
            show_alert=True
        )
    
    # Get current mode and toggle
    current_mode = await roxy_bot.get_trim_mode(user_id)
    new_mode = not current_mode
    await roxy_bot.set_trim_mode(user_id, new_mode)
    
    # Get other settings for button refresh
    dump_channel = await roxy_bot.get_dump_channel(user_id)
    screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
    mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    
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
    compress_status = "✅ ON" if compress_mode else "❌ OFF"
    trim_status = "✅ ON" if new_mode else "❌ OFF"
    
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
    
    status_text = "enabled" if new_mode else "disabled"
    await callback_query.answer(f"✂️ Trim mode {status_text}!")


# ===== Trim Selection Callbacks =====

@Client.on_callback_query(filters.regex(r'^trim_select$'))
async def trim_select_callback(client, callback_query):
    """Show Auto Trim / Manual Trim options - Premium only"""
    user_id = callback_query.from_user.id
    
    # Check premium access
    is_premium = await roxy_bot.has_premium_access(user_id)
    if not is_premium:
        return await callback_query.answer(
            "🔒 Trim is for Premium users only! Use /plans to upgrade.",
            show_alert=True
        )
    
    # IMPORTANT: Store file_msg NOW before editing message (reply_to_message can become None after edit)
    if user_id not in pending_trim:
        pending_trim[user_id] = {}
    if not pending_trim[user_id].get('file_msg'):
        pending_trim[user_id]['file_msg'] = callback_query.message.reply_to_message
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱️ Auto Trim", callback_data="trim_auto")],
        [InlineKeyboardButton("✏️ Manual Trim", callback_data="trim_manual")],
        [InlineKeyboardButton("❌ Skip Trim", callback_data="trim_skip")]
    ])
    
    await callback_query.message.edit_text(
        text="<blockquote><b>✂️ Sᴇʟᴇᴄᴛ Tʀɪᴍ Mᴏᴅᴇ</b>\n\n"
             "• <b>Auto Trim:</b> Trim video to fixed duration from start\n"
             "• <b>Manual Trim:</b> Select start & end time</blockquote>",
        reply_markup=buttons
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^trim_auto'))
async def trim_auto_callback(client, callback_query):
    """Show duration options for auto trim - Premium only"""
    user_id = callback_query.from_user.id
    
    # Check premium access
    is_premium = await roxy_bot.has_premium_access(user_id)
    if not is_premium:
        return await callback_query.answer(
            "🔒 Trim is for Premium users only! Use /plans to upgrade.",
            show_alert=True
        )
    
    # Extract media type from callback if present (trim_auto_upload_video or trim_auto_upload_document)
    data = callback_query.data
    if "upload_video" in data:
        media_type = "upload_video"
    elif "upload_document" in data:
        media_type = "upload_document"
    else:
        media_type = "upload_video"  # default
    
    # Store media type and file message for later
    if user_id not in pending_trim:
        pending_trim[user_id] = {}
    pending_trim[user_id]['media_type'] = media_type
    # Only set file_msg if not already stored (reply_to_message may be None after edits)
    if not pending_trim[user_id].get('file_msg'):
        pending_trim[user_id]['file_msg'] = callback_query.message.reply_to_message
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("1 min", callback_data="trim_dur_60"),
         InlineKeyboardButton("2 min", callback_data="trim_dur_120"),
         InlineKeyboardButton("3 min", callback_data="trim_dur_180")],
        [InlineKeyboardButton("4 min", callback_data="trim_dur_240"),
         InlineKeyboardButton("5 min", callback_data="trim_dur_300")],
        [InlineKeyboardButton("10 min", callback_data="trim_dur_600"),
         InlineKeyboardButton("20 min", callback_data="trim_dur_1200")],
        [InlineKeyboardButton("30 min", callback_data="trim_dur_1800"),
         InlineKeyboardButton("1 hour", callback_data="trim_dur_3600")],
        [InlineKeyboardButton("⬅️ Back", callback_data="trim_select")]
    ])
    
    await callback_query.message.edit_text(
        text="<blockquote><b>⏱️ Sᴇʟᴇᴄᴛ Vɪᴅᴇᴏ Dᴜʀᴀᴛɪᴏɴ</b>\n\n"
             "Video will be trimmed from start to selected duration.</blockquote>",
        reply_markup=buttons
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^trim_manual$'))
async def trim_manual_callback(client, callback_query):
    """Handle manual trim - Premium only"""
    user_id = callback_query.from_user.id
    
    # Check premium access
    is_premium = await roxy_bot.has_premium_access(user_id)
    if not is_premium:
        return await callback_query.answer(
            "🔒 Trim is for Premium users only! Use /plans to upgrade.",
            show_alert=True
        )
    
    # Set user to manual trim mode - awaiting start time
    if user_id not in pending_trim:
        pending_trim[user_id] = {}
    pending_trim[user_id]['stage'] = 'awaiting_start'
    pending_trim[user_id]['message_id'] = callback_query.message.id
    # Only set file_msg if not already stored
    if not pending_trim[user_id].get('file_msg'):
        pending_trim[user_id]['file_msg'] = callback_query.message.reply_to_message
    
    await callback_query.message.edit_text(
        text="<blockquote><b>✏️ Manual Trim</b>\n\n"
             "Enter the <b>start time</b> in format:\n"
             "<code>MM:SS</code> or <code>HH:MM:SS</code>\n\n"
             "Example: <code>00:01:30</code> for 1 minute 30 seconds</blockquote>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="trim_cancel")]
        ])
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^trim_skip$'))
async def trim_skip_callback(client, callback_query):
    """Skip trimming and proceed with upload"""
    user_id = callback_query.from_user.id
    
    # Clear any pending trim
    if user_id in pending_trim:
        del pending_trim[user_id]
    
    await callback_query.answer("Skipping trim, proceeding with upload...")
    # This will be handled by file_rename.py to continue upload


@Client.on_callback_query(filters.regex(r'^trim_cancel$'))
async def trim_cancel_callback(client, callback_query):
    """Cancel trimming"""
    user_id = callback_query.from_user.id
    
    if user_id in pending_trim:
        del pending_trim[user_id]
    
    await callback_query.message.edit_text(
        "<blockquote>❌ Trim cancelled.</blockquote>"
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^trim_dur_(\d+)$'))
async def trim_duration_callback(client, callback_query):
    """Handle auto trim with specific duration"""
    import re
    match = re.match(r'^trim_dur_(\d+)$', callback_query.data)
    if not match:
        return
    
    duration = int(match.group(1))
    user_id = callback_query.from_user.id
    
    # Store the selected duration
    if user_id not in pending_trim:
        pending_trim[user_id] = {}
    
    pending_trim[user_id]['duration'] = duration
    pending_trim[user_id]['trim_type'] = 'auto'
    
    duration_text = f"{duration // 60} min" if duration >= 60 else f"{duration} sec"
    
    # Get the already-chosen media type
    media_type = pending_trim[user_id].get('media_type', 'upload_video')
    
    # Get the original filename from file message
    file_msg = pending_trim[user_id].get('file_msg') or callback_query.message.reply_to_message

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

    if file_msg:
        try:
            media = getattr(file_msg, file_msg.media.value)
            filename = media.file_name
        except:
            filename = "video.mp4"
    else:
        filename = "video.mp4"
    
    # Store file_msg if not already stored
    pending_trim[user_id]['file_msg'] = file_msg
    
    # Show confirmation with filename in correct format for upload_doc parsing
    await callback_query.message.edit_text(
        f"<blockquote>✅ <b>Trim set to {duration_text}</b>\n\nProceeding...\n\n• Fɪʟᴇ Nᴀᴍᴇ :-`{filename}`</blockquote>"
    )
    await callback_query.answer(f"Trim: {duration_text}")

    # Extract custom_name from pending_trim if stored, else use the filename shown in the message
    custom_name = pending_trim[user_id].get('custom_name', filename)

    # Create mock message with reply_to_message pointing to original file
    class MockMessage:
        def __init__(self, original_msg, file_message, text_override=None):
            self.text = text_override if text_override is not None else original_msg.text
            self.chat = original_msg.chat
            self.id = original_msg.id
            self.reply_to_message = file_message
            self._original = original_msg

        async def edit(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

        async def edit_text(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

    class MockCallback:
        def __init__(self, mock_msg, data, user):
            self.message = mock_msg
            self.data = data
            self.from_user = user

    text_for_upload = f"📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-{custom_name}"
    mock_msg = MockMessage(callback_query.message, file_msg, text_override=text_for_upload)
    mock_callback = MockCallback(mock_msg, media_type, callback_query.from_user)

    # Trigger upload
    from plugins.subtitle_mux import route_to_upload_or_subtitle
    await route_to_upload_or_subtitle(client, mock_callback, media_type, file_msg, edit_msg=callback_query.message, custom_name=custom_name)


@Client.on_callback_query(filters.regex(r'^upload_video_notrim$'))
async def skip_trim_video_callback(client, callback_query):
    """Skip trim and proceed with normal video upload"""
    user_id = callback_query.from_user.id
    
    # Get the original filename from reply message
    file_msg = callback_query.message.reply_to_message
    if file_msg:
        try:
            media = getattr(file_msg, file_msg.media.value)
            filename = media.file_name
        except:
            filename = "video.mp4"
    else:
        filename = "video.mp4"
    
    # Set a flag to indicate no trim
    pending_trim[user_id] = {'trim_type': 'skip', 'media_type': 'upload_video'}

    # Extract stored custom_name or fall back to original filename
    custom_name = pending_trim[user_id].get('custom_name', filename)

    # Update message with correct filename format for upload_doc parsing
    await callback_query.message.edit_text(
        f"<blockquote>📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-`{custom_name}`</blockquote>"
    )

    class MockMessage:
        def __init__(self, original_msg, file_message, text_override=None):
            self.text = text_override if text_override is not None else original_msg.text
            self.chat = original_msg.chat
            self.id = original_msg.id
            self.reply_to_message = file_message
            self._original = original_msg

        async def edit(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

        async def edit_text(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

    class MockCallback:
        def __init__(self, mock_msg, data, user):
            self.message = mock_msg
            self.data = data
            self.from_user = user

    text_for_upload = f"📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-{custom_name}"
    mock_msg = MockMessage(callback_query.message, file_msg, text_override=text_for_upload)
    mock_callback = MockCallback(mock_msg, "upload_video", callback_query.from_user)

    from plugins.subtitle_mux import route_to_upload_or_subtitle
    await route_to_upload_or_subtitle(client, mock_callback, "upload_video", file_msg, edit_msg=callback_query.message, custom_name=custom_name)


@Client.on_callback_query(filters.regex(r'^upload_document_notrim$'))
async def skip_trim_document_callback(client, callback_query):
    """Skip trim and proceed with normal document upload"""
    user_id = callback_query.from_user.id
    
    # Get the original filename from reply message
    file_msg = callback_query.message.reply_to_message
    if file_msg:
        try:
            media = getattr(file_msg, file_msg.media.value)
            filename = media.file_name
        except:
            filename = "file.mp4"
    else:
        filename = "file.mp4"
    
    # Set a flag to indicate no trim
    pending_trim[user_id] = {'trim_type': 'skip', 'media_type': 'upload_document'}

    # Extract stored custom_name or fall back to original filename
    custom_name = pending_trim[user_id].get('custom_name', filename)

    # Update message with correct filename format for upload_doc parsing
    await callback_query.message.edit_text(
        f"<blockquote>📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-`{custom_name}`</blockquote>"
    )

    class MockMessage:
        def __init__(self, original_msg, file_message, text_override=None):
            self.text = text_override if text_override is not None else original_msg.text
            self.chat = original_msg.chat
            self.id = original_msg.id
            self.reply_to_message = file_message
            self._original = original_msg

        async def edit(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

        async def edit_text(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

    class MockCallback:
        def __init__(self, mock_msg, data, user):
            self.message = mock_msg
            self.data = data
            self.from_user = user

    text_for_upload = f"📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-{custom_name}"
    mock_msg = MockMessage(callback_query.message, file_msg, text_override=text_for_upload)
    mock_callback = MockCallback(mock_msg, "upload_document", callback_query.from_user)

    from plugins.subtitle_mux import route_to_upload_or_subtitle
    await route_to_upload_or_subtitle(client, mock_callback, "upload_document", file_msg, edit_msg=callback_query.message, custom_name=custom_name)


# ===== Manual Trim Time Handler =====

@Client.on_message(filters.private & filters.text & filters.regex(r'^\d{1,2}:\d{2}(:\d{2})?$'), group=4)
async def receive_trim_time(client, message):
    """Handle time input for manual trim"""
    user_id = message.from_user.id
    
    if user_id not in pending_trim:
        return
    
    stage = pending_trim[user_id].get('stage')
    time_input = message.text.strip()
    
    if stage == 'awaiting_start':
        pending_trim[user_id]['start_time'] = time_input
        pending_trim[user_id]['stage'] = 'awaiting_end'
        
        await message.reply_text(
            text="<blockquote><b>✏️ Manual Trim</b>\n\n"
                 f"Start time: <code>{time_input}</code>\n\n"
                 "Now enter the <b>end time</b> in format:\n"
                 "<code>MM:SS</code> or <code>HH:MM:SS</code></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel", callback_data="trim_cancel")]
            ])
        )
        await message.delete()
        
    elif stage == 'awaiting_end':
        pending_trim[user_id]['end_time'] = time_input
        pending_trim[user_id]['stage'] = 'ready'
        pending_trim[user_id]['trim_type'] = 'manual'
        
        start = pending_trim[user_id]['start_time']
        media_type = pending_trim[user_id].get('media_type', 'upload_video')
        file_msg = pending_trim[user_id].get('file_msg')
        
        # Get filename from file message
        if file_msg:
            try:
                media = getattr(file_msg, file_msg.media.value)
                filename = media.file_name
            except:
                filename = "video.mp4"
        else:
            filename = "video.mp4"
        
        # Use stored custom_name or fall back to original filename
        custom_name = pending_trim[user_id].get('custom_name', filename)

        # Send confirmation with filename in correct format for upload_doc
        reply_msg = await message.reply_text(
            f"<blockquote>✅ Manual trim set:\n"
            f"<b>Start:</b> {start}\n"
            f"<b>End:</b> {time_input}\n\n"
            f"• Fɪʟᴇ Nᴀᴍᴇ :-`{custom_name}`</blockquote>",
            reply_to_message_id=file_msg.id if file_msg else None
        )
        await message.delete()

        class MockMessage:
            def __init__(self, original_reply, file_message, text_override=None):
                self.text = text_override if text_override is not None else original_reply.text
                self.chat = original_reply.chat
                self.id = original_reply.id
                self.reply_to_message = file_message
                self._original = original_reply

            async def edit(self, text, **kwargs):
                return await self._original.edit_text(text, **kwargs)

            async def edit_text(self, text, **kwargs):
                return await self._original.edit_text(text, **kwargs)

        class MockCallback:
            def __init__(self, mock_msg, data, user):
                self.message = mock_msg
                self.data = data
                self.from_user = user

        text_for_upload = f"📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-{custom_name}"
        mock_msg = MockMessage(reply_msg, file_msg, text_override=text_for_upload)
        mock_callback = MockCallback(mock_msg, media_type, message.from_user)

        # Trigger upload
        from plugins.subtitle_mux import route_to_upload_or_subtitle
        await route_to_upload_or_subtitle(client, mock_callback, media_type, file_msg, edit_msg=reply_msg, custom_name=custom_name)


def get_pending_trim(user_id):
    """Get pending trim settings for a user"""
    return pending_trim.get(user_id, {})


def clear_pending_trim(user_id):
    """Clear pending trim for a user"""
    if user_id in pending_trim:
        del pending_trim[user_id]

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
