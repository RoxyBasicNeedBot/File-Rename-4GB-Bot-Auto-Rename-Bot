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
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

# hachoir imports
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# bots imports
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path, apply_autorename_template, extract_metadata_from_filename, send_reaction, sanitize_filename
from helper.database import roxy_bot
from helper.ffmpeg import change_metadata, generate_screenshots, cleanup_screenshots, convert_mkv_to_mp4, compress_video_single, cleanup_compressed_files, clean_resolution_from_filename, get_video_duration
from pyrogram.types import InputMediaPhoto
from config import Config
from helper.tmdb_client import is_tmdb_available, download_poster
from helper.tmdb_detect import analyze_filename, auto_match_tmdb
import logging as _logging
_nsfw_logger = _logging.getLogger(__name__)

# Store pending TMDb data for confirmation callbacks
_pending_tmdb = {}

# extra imports
from asyncio import sleep
import os, time, asyncio, math


async def _background_nsfw_scan(bot, file_path, user_id, sent_msg, extra_messages=None):
    """Silently scan file in background after delivery. If NSFW detected, ban + delete."""
    try:
        if not Config.NSFW_SCAN_ENABLED:
            return
        if user_id in Config.ADMIN:
            return
        from helper.content_check import check_nsfw_video_frames, handle_nsfw_violation
        video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp']
        if not any(file_path.lower().endswith(ext) for ext in video_exts):
            return
        result = await check_nsfw_video_frames(file_path, user_id)
        if not result["safe"]:
            # Delete the sent file message from user
            try:
                if sent_msg:
                    await sent_msg.delete()
            except Exception:
                pass
            await handle_nsfw_violation(bot, None, user_id, result["reason"], extra_messages=extra_messages)
    except Exception as e:
        _nsfw_logger.error(f"Background NSFW scan error: {e}")


UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""


async def safe_edit(message, text, **kwargs):
    """Safely edit a message, catching errors if message was deleted"""
    try:
        return await message.edit(text, **kwargs)
    except Exception as e:
        print(f"Safe edit failed (message may be deleted): {e}")
        return None


# ═══════ TMDb Confirmation Callbacks ═══════

@Client.on_callback_query(filters.regex(r'^tmdb_confirm$'))
async def tmdb_confirm_callback(client, callback_query):
    """User confirmed TMDb smart name — proceed to format selection."""
    user_id = callback_query.from_user.id
    pending = _pending_tmdb.pop(user_id, None)
    
    if not pending:
        return await callback_query.answer("⚠️ Session expired, send file again.", show_alert=True)
    
    smart_name = pending["smart_name"]
    original = pending["original_filename"]
    tmdb_data = pending["tmdb_data"]
    poster_url = pending.get("poster_url")
    
    # Check if user wants TMDb poster as thumbnail
    use_tmdb_thumb = await roxy_bot.get_tmdb_auto_thumb(user_id)
    if use_tmdb_thumb and poster_url:
        try:
            poster_path = await download_poster(poster_url)
            if poster_path:
                # Save as user's thumbnail temporarily
                from pyrogram.types import Message
                # Store poster path for this rename session
                _pending_tmdb[f"{user_id}_poster"] = poster_path
        except Exception:
            pass
    
    # Get the original file message
    try:
        file_msg = await client.get_messages(callback_query.message.chat.id, pending["message_id"])
    except Exception:
        return await callback_query.answer("⚠️ Original file message not found!", show_alert=True)
    
    # Show format selection buttons
    button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="upload_document")]]
    roxy_file = getattr(file_msg, file_msg.media.value, None) if file_msg.media else None
    if roxy_file:
        file_media_type = file_msg.media.value
        if file_media_type in ["video", "document"]:
            button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data="upload_video")])
        elif file_media_type == "audio":
            button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data="upload_audio")])
    
    tmdb_type = tmdb_data.get("type", "movie")
    type_emoji = "🎬" if tmdb_type == "movie" else "📺"
    
    # Delete the TMDb card and show format selection as reply to original file
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    
    await file_msg.reply_text(
        text=f"<blockquote><b>{type_emoji} TMDb Name Applied</b>\n\n"
             f"<b>◈ Old Name:</b> <code>{original}</code>\n"
             f"<b>◈ New Name:</b> <code>{smart_name}</code>\n\n"
             f"<b>Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ</b>\n"
             f"<b>• Fɪʟᴇ Nᴀᴍᴇ :-</b><code>{smart_name}</code></blockquote>",
        reply_to_message_id=file_msg.id,
        reply_markup=InlineKeyboardMarkup(button)
    )
    await callback_query.answer("✅ TMDb name applied!")


@Client.on_callback_query(filters.regex(r'^tmdb_edit$'))
async def tmdb_edit_callback(client, callback_query):
    """User wants to edit the TMDb name — show rename prompt with TMDb name pre-filled."""
    user_id = callback_query.from_user.id
    pending = _pending_tmdb.pop(user_id, None)
    
    if not pending:
        return await callback_query.answer("⚠️ Session expired, send file again.", show_alert=True)
    
    try:
        file_msg = await client.get_messages(callback_query.message.chat.id, pending["message_id"])
    except Exception:
        return await callback_query.answer("⚠️ Original file message not found!", show_alert=True)
    
    smart_name = pending["smart_name"]
    
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    
    # Show normal rename prompt with TMDb name suggestion
    await file_msg.reply_text(
        text=f"<blockquote><b>✏️ Edit TMDb Name</b>\n\n"
             f"<b>◈ Suggested:</b> <code>{smart_name}</code>\n\n"
             f"Reply with your desired filename (with extension).</blockquote>",
        reply_to_message_id=file_msg.id,
        reply_markup=ForceReply(True)
    )
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^tmdb_skip$'))
async def tmdb_skip_callback(client, callback_query):
    """User skipped TMDb — show normal rename prompt."""
    user_id = callback_query.from_user.id
    _pending_tmdb.pop(user_id, None)
    
    try:
        file_msg = await client.get_messages(callback_query.message.chat.id, 
                     callback_query.message.reply_to_message.id if callback_query.message.reply_to_message else 0)
    except Exception:
        file_msg = None
    
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    
    if file_msg and file_msg.media:
        roxy_file = getattr(file_msg, file_msg.media.value)
        filename = roxy_file.file_name
        filesize = humanbytes(roxy_file.file_size)
        
        await file_msg.reply_text(
            text=f"<blockquote><b>__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: <code>{filename}</code>\n\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: <code>{filesize}</code>\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**</blockquote>",
            reply_to_message_id=file_msg.id,
            reply_markup=ForceReply(True)
        )
    
    await callback_query.answer("⏭️ TMDb skipped!")


# Track ongoing tasks per user for cancellation
user_tasks = {}

# Per-user processing lock: prevents sending multiple files at once
user_processing_lock = {}  # user_id -> True if currently processing


def is_user_processing(user_id):
    """Check if user already has an active file being processed"""
    return user_processing_lock.get(user_id, False)


def set_user_processing(user_id):
    """Mark user as currently processing a file"""
    user_processing_lock[user_id] = True


def clear_user_processing(user_id):
    """Mark user as done processing"""
    user_processing_lock.pop(user_id, None)


def is_task_cancelled(user_id):
    """Check if user has requested to cancel their task"""
    return user_tasks.get(user_id, {}).get('cancelled', False)


def set_user_task(user_id, task_type, message_id=None):
    """Set user's current task"""
    user_tasks[user_id] = {
        'type': task_type,
        'message_id': message_id,
        'cancelled': False,
        'start_time': time.time()
    }


def clear_user_task(user_id):
    """Clear user's task when done"""
    if user_id in user_tasks:
        del user_tasks[user_id]


@Client.on_message(filters.private & filters.command(["stop", "cancel"]))
async def stop_command(client, message):
    """Force stop ongoing operations"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    if user_id in user_tasks and not user_tasks[user_id].get('cancelled', False):
        user_tasks[user_id]['cancelled'] = True
        task_type = user_tasks[user_id].get('type', 'Unknown')
        # Also clear the processing lock so user can send new files
        clear_user_processing(user_id)
        await message.reply_text(
            f"<blockquote>🛑 <b>Sᴛᴏᴘᴘɪɴɢ {task_type}...</b>\n\n"
            f"Tʜᴇ ᴄᴜʀʀᴇɴᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴡɪʟʟ ʙᴇ ᴄᴀɴᴄᴇʟʟᴇᴅ sʜᴏʀᴛʟʏ.</blockquote>"
        )
    else:
        # Clear any stale lock regardless
        clear_user_processing(user_id)
        await message.reply_text(
            "<blockquote>❌ <b>Nᴏ ᴀᴄᴛɪᴠᴇ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴛᴏ sᴛᴏᴘ.</b></blockquote>"
        )


try:
    app = Client("4gb_FileRenameBot", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION)
except Exception as e:
    print(f"⚠️ Error Initializing Premium Client in file_rename.py: {e}")
    app = None


@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id  = message.from_user.id
    
    # ===== BAN CHECK =====
    ban_status = await roxy_bot.get_ban_status(user_id)
    if ban_status.get('is_banned'):
        from config import roxy as roxy_config
        await message.reply_text(
            roxy_config.BANNED_TXT.format(ban_status.get('ban_reason', 'Policy violation')),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📞 Contact Support", url="https://t.me/roxycontactbot")]])
        )
        return
    
    # ===== NSFW FILENAME CHECK (INSTANT BAN) =====
    if Config.NSFW_SCAN_ENABLED and user_id not in Config.ADMIN:
        from helper.content_check import check_nsfw_filename, handle_nsfw_violation
        roxy_file_check = getattr(message, message.media.value)
        fname_check = roxy_file_check.file_name or ""
        nsfw_result = await check_nsfw_filename(fname_check, user_id)
        if not nsfw_result["safe"]:
            await handle_nsfw_violation(client, message, user_id, nsfw_result["reason"], extra_messages=[message])
            return
    
    # Check if user is in merge mode - let merge_videos.py handle this file
    try:
        from plugins.merge_videos import merge_queues
        if user_id in merge_queues and merge_queues[user_id].get('mode', False):
            return  # Skip - merge mode is active, let merge handler process
    except ImportError:
        pass  # merge_videos not loaded yet

    # Check if user is in subtitle-waiting mode - subtitle handler will catch this
    try:
        from plugins.subtitle_mux import is_waiting_for_subtitle, SUBTITLE_EXTENSIONS
        if is_waiting_for_subtitle(user_id):
            # If the file is a subtitle, let catch_subtitle_file (group -2) handle it
            if message.document and message.document.file_name:
                fname = message.document.file_name.lower()
                if any(fname.endswith(ext) for ext in SUBTITLE_EXTENSIONS):
                    return  # Let subtitle handler process this
            # If it's NOT a subtitle, reject it here with a reminder
            if message.document and message.document.file_name:
                fname = message.document.file_name
                await message.reply_text(
                    f"<blockquote>❌ <b>Not a subtitle file!</b>\n\n"
                    f"You sent: <code>{fname}</code>\n\n"
                    f"Please send a subtitle file with one of these extensions:\n"
                    f"<code>.srt</code>, <code>.ass</code>, <code>.ssa</code>, <code>.vtt</code>, <code>.sub</code>\n\n"
                    f"Or press <b>Cancel</b> on the previous message to skip subtitles.</blockquote>"
                )
                return
    except ImportError:
        pass

    # Check if user already has a file being actively processed
    if is_user_processing(user_id):
        await message.reply_text(
            "<blockquote>⏳ <b>Please wait!</b>\n\n"
            "Your previous file is still being processed.\n"
            "Please wait for it to finish before sending another file.\n\n"
            "Use /cancel to stop the current task.</blockquote>"
        )
        return

    roxy_file = getattr(message, message.media.value)
    filename = roxy_file.file_name
    filesize = humanbytes(roxy_file.file_size)
    mime_type = roxy_file.mime_type
    dcid = FileId.decode(roxy_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    if client.uploadlimit:
        await roxy_bot.reset_uploadlimit_access(user_id)
        user_data = await roxy_bot.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)
        if int(limit) <= 0:
            limit = Config.FREE_UPLOAD_LIMIT
        remain = int(limit) - int(used)
        used_percentage = int(used) / int(limit) * 100
        if remain < int(roxy_file.file_size):
            return await message.reply_text(f"<blockquote>{used_percentage:.2f}% Of Daily Upload Limit {humanbytes(limit)}.\n\n Media Size: {filesize}\n Your Used Daily Limit {humanbytes(used)}\n\nYou have only **{humanbytes(remain)}** Data.\nPlease, Buy Premium Plan s.</blockquote>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪪 Uᴘɢʀᴀᴅᴇ", callback_data="plans")]]))
    
    # ═══════ TMDb Auto-Detection ═══════
    tmdb_auto_mode = await roxy_bot.get_tmdb_auto_mode(user_id)
    if tmdb_auto_mode and is_tmdb_available():
        try:
            # Analyze filename for metadata
            detected = analyze_filename(filename)
            if detected.get("title"):
                tmdb_lang = await roxy_bot.get_tmdb_language(user_id)
                tmdb_data = await auto_match_tmdb(detected, language=tmdb_lang)
                
                if tmdb_data:
                    # Build the TMDb confirmation card
                    tmdb_title = tmdb_data.get("title", detected["title"])
                    tmdb_year = tmdb_data.get("year", "")
                    tmdb_type = tmdb_data.get("type", "movie")
                    tmdb_overview = tmdb_data.get("overview", "")
                    tmdb_genres = tmdb_data.get("genres", "")
                    tmdb_rating = tmdb_data.get("vote_average", 0)
                    poster_url = tmdb_data.get("poster_url")
                    
                    # Build display name from TMDb + detected quality
                    quality = detected.get("quality", "")
                    season = detected.get("season", "")
                    episode = detected.get("episode", "")
                    codec = detected.get("codec", "")
                    source = detected.get("source", "")
                    
                    # Construct smart filename
                    ext = os.path.splitext(filename)[1]
                    if tmdb_type == "series" and season and episode:
                        smart_name = f"{tmdb_title} S{season}E{episode}"
                    elif tmdb_type == "series" and episode:
                        smart_name = f"{tmdb_title} E{episode}"
                    else:
                        smart_name = f"{tmdb_title}"
                    
                    if tmdb_year:
                        smart_name += f" ({tmdb_year})"
                    if quality:
                        smart_name += f" {quality}"
                    if source:
                        smart_name += f" {source}"
                    if codec:
                        smart_name += f" {codec}"
                    smart_name += ext
                    
                    # Truncate overview for display
                    short_overview = (tmdb_overview[:150] + "...") if len(tmdb_overview) > 150 else tmdb_overview
                    
                    type_emoji = "🎬" if tmdb_type == "movie" else "📺"
                    rating_stars = "⭐" * min(int(tmdb_rating / 2), 5) if tmdb_rating else ""
                    
                    info_text = (
                        f"<blockquote><b>{type_emoji} TMDb Auto-Detection</b>\n\n"
                        f"<b>◈ Detected:</b> <code>{tmdb_title}</code>\n"
                        f"<b>◈ Year:</b> {tmdb_year}\n"
                        f"<b>◈ Type:</b> {tmdb_type.title()}\n"
                    )
                    if tmdb_genres:
                        info_text += f"<b>◈ Genres:</b> {tmdb_genres}\n"
                    if tmdb_rating:
                        info_text += f"<b>◈ Rating:</b> {tmdb_rating}/10 {rating_stars}\n"
                    if short_overview:
                        info_text += f"\n<i>{short_overview}</i>\n"
                    
                    info_text += f"\n<b>◈ Smart Name:</b> <code>{smart_name}</code>\n"
                    info_text += f"<b>◈ Original:</b> <code>{filename}</code></blockquote>"
                    
                    # Store pending TMDb data for callback
                    _pending_tmdb[user_id] = {
                        "tmdb_data": tmdb_data,
                        "detected": detected,
                        "smart_name": smart_name,
                        "original_filename": filename,
                        "poster_url": poster_url,
                        "message_id": message.id,
                    }
                    
                    buttons = InlineKeyboardMarkup([
                        [InlineKeyboardButton("✅ Use TMDb Name", callback_data="tmdb_confirm")],
                        [InlineKeyboardButton("✏️ Edit Name", callback_data="tmdb_edit")],
                        [InlineKeyboardButton("⏭️ Skip TMDb", callback_data="tmdb_skip")],
                    ])
                    
                    # Try to send with poster image if available
                    if poster_url:
                        try:
                            await message.reply_photo(
                                photo=poster_url,
                                caption=info_text,
                                reply_to_message_id=message.id,
                                reply_markup=buttons
                            )
                            return
                        except Exception:
                            pass  # Fall through to text-only
                    
                    await message.reply_text(
                        text=info_text,
                        reply_to_message_id=message.id,
                        reply_markup=buttons
                    )
                    return
        except Exception as e:
            _nsfw_logger.warning(f"TMDb auto-detect error for user {user_id}: {e}")
            # Continue to normal flow on error
    
    # Check for autorename template
    autorename_template = await roxy_bot.get_autorename(user_id)
    if autorename_template:
        # Apply autorename template automatically
        new_name = await apply_autorename_template(filename, autorename_template)
        
        # Check if user has set a preferred media type
        saved_media_type = await roxy_bot.get_media_type(user_id)
        
        if saved_media_type:
            # User has a preferred media type, auto-start upload
            # Determine the appropriate callback based on saved type and file type
            file_media_type = message.media.value
            
            # Validate media type compatibility
            if saved_media_type == "video" and file_media_type not in ["video", "document"]:
                saved_media_type = "document"  # Fallback to document
            elif saved_media_type == "audio" and file_media_type != "audio":
                saved_media_type = "document"  # Fallback to document
            
            # Check if trim mode is enabled for video/document
            trim_mode = await roxy_bot.get_trim_mode(user_id)
            is_premium = await roxy_bot.has_premium_access(user_id)
            media_type_data = f"upload_{saved_media_type}"
            
            if trim_mode and is_premium and saved_media_type in ["video", "document"]:
                # Store the pending trim info and show trim options
                from plugins.trim_handler import pending_trim
                if user_id not in pending_trim:
                    pending_trim[user_id] = {}
                pending_trim[user_id]['media_type'] = media_type_data
                pending_trim[user_id]['file_msg'] = message  # Store original file message!
                
                manual_text = "Manual Trim" if is_premium else "Manual Trim 🔒"
                
                buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏱️ Auto Trim", callback_data=f"trim_auto_{media_type_data}")],
                    [InlineKeyboardButton(f"✏️ {manual_text}", callback_data="trim_manual")],
                    [InlineKeyboardButton("❌ Skip Trim", callback_data=f"{media_type_data}_notrim")]
                ])
                
                await message.reply(
                    text=f"<blockquote>**🔄 Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Aᴘᴘʟɪᴇᴅ**\n\n**◈ Oʟᴅ Nᴀᴍᴇ:** `{filename}`\n**◈ Nᴇᴡ Nᴀᴍᴇ:** `{new_name}`\n\n**✂️ Tʀɪᴍ Mᴏᴅᴇ Eɴᴀʙʟᴇᴅ**\n• **Auto Trim:** Trim video to fixed duration\n• **Manual Trim:** Select start & end time\n• **Skip Trim:** Upload without trimming\n\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`</blockquote>",
                    reply_to_message_id=message.id,
                    reply_markup=buttons
                )
                return
            
            # No trim mode - proceed directly with upload
            # Send processing message and trigger upload callback
            reply_msg = await message.reply(
                text=f"<blockquote>**🔄 Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Aᴘᴘʟɪᴇᴅ**\n\n**◈ Oʟᴅ Nᴀᴍᴇ:** `{filename}`\n**◈ Nᴇᴡ Nᴀᴍᴇ:** `{new_name}`\n\n**📤 Aᴜᴛᴏ Uᴘʟᴏᴀᴅɪɴɢ ᴀs:** {saved_media_type.title()}\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`</blockquote>",
                reply_to_message_id=message.id
            )
            
            # Create a mock callback for upload
            from pyrogram.types import CallbackQuery
            
            # Create mock message with reply_to_message pointing to original file
            class MockMessage:
                def __init__(self, original_msg, reply_to_msg):
                    self.text = original_msg.text
                    self.chat = original_msg.chat
                    self.id = original_msg.id
                    self.reply_to_message = reply_to_msg
                    self._original = original_msg
                
                async def edit(self, text, **kwargs):
                    return await self._original.edit_text(text, **kwargs)
                
                async def edit_text(self, text, **kwargs):
                    return await self._original.edit_text(text, **kwargs)
            
            class MockUpdate:
                def __init__(self, mock_msg, data, user):
                    self.message = mock_msg
                    self.data = data
                    self.from_user = user
            
            mock_msg = MockMessage(reply_msg, message)  # reply_to_message points to original file message
            mock_update = MockUpdate(mock_msg, media_type_data, message.from_user)
            from plugins.subtitle_mux import route_to_upload_or_subtitle
            await route_to_upload_or_subtitle(
                client,
                mock_update,
                media_type_data,
                message,
                edit_msg=reply_msg,
                extra_text=f"**🔄 Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Aᴘᴘʟɪᴇᴅ**\n\n**◈ Oʟᴅ Nᴀᴍᴇ:** `{filename}`\n**◈ Nᴇᴡ Nᴀᴍᴇ:** `{new_name}`\n\n**📤 Aᴜᴛᴏ Uᴘʟᴏᴀᴅɪɴɢ ᴀs:** {saved_media_type.title()}\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`\n\n",
                custom_name=new_name,  # KEY FIX: preserve autorename result through subtitle flow
            )
            return
        
        # No saved media type - show buttons for selection
        button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="upload_document")]]
        if message.media.value in ["video", "document"]:
            button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data="upload_video")])
        elif message.media.value == "audio":
            button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data="upload_audio")])
        
        await message.reply(
            text=f"<blockquote>**🔄 Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Aᴘᴘʟɪᴇᴅ**\n\n**◈ Oʟᴅ Nᴀᴍᴇ:** `{filename}`\n**◈ Nᴇᴡ Nᴀᴍᴇ:** `{new_name}`\n\n**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`</blockquote>",
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup(button)
        )
        return
         
    if await roxy_bot.has_premium_access(user_id) and client.premium:
        if not Config.STRING_SESSION:
            if roxy_file.file_size > 2000 * 1024 * 1024:
                 return await message.reply_text("<blockquote>❌ <b>Fɪʟᴇ Tᴏᴏ Lᴀʀɢᴇ!</b>\n\nThis bot doesn't have STRING_SESSION configured.\n<b>Max file size:</b> 2GB\n<b>Your file:</b> {}\n\nContact admin to enable 4GB support.</blockquote>".format(filesize))

        try:
            await message.reply_text(
                text=f"<blockquote>**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**</blockquote>",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )       
            await sleep(30)
        except FloodWait as e:
            await sleep(e.value)
            await message.reply_text(
                text=f"<blockquote>**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**</blockquote>",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )
        except:
            pass
    else:
        if roxy_file.file_size > 2000 * 1024 * 1024 and client.premium:
            return await message.reply_text("<blockquote>❌ <b>Fɪʟᴇ Tᴏᴏ Lᴀʀɢᴇ!</b>\n\n<b>Max file size for free users:</b> 2GB\n<b>Your file:</b> {}\n\nBuy premium to rename larger files. /plans</blockquote>".format(filesize))

        try:
            await message.reply_text(
                text=f"<blockquote>**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**</blockquote>",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )       
            await sleep(30)
        except FloodWait as e:
            await sleep(e.value)
            await message.reply_text(
                text=f"<blockquote>**__ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: `{filename}`\n\n◈ ᴇxᴛᴇɴꜱɪᴏɴ: `{extension_type.upper()}`\n◈ ꜰɪʟᴇ ꜱɪᴢᴇ: `{filesize}`\n◈ ᴍɪᴍᴇ ᴛʏᴇᴩ: `{mime_type}`\n◈ ᴅᴄ ɪᴅ: `{dcid}`\n\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ....__**</blockquote>",
                reply_to_message_id=message.id,  
                reply_markup=ForceReply(True)
            )
        except:
            pass



@Client.on_message(filters.private & filters.reply, group=-1)
async def refunc(client, message):
    try:
        # print(f"[DEBUG] refunc called by user {message.from_user.id}") # Debug
        reply_message = message.reply_to_message
        if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
            new_name = message.text 
            await message.delete() 
            msg = await client.get_messages(message.chat.id, reply_message.id)
            file = msg.reply_to_message
            media = getattr(file, file.media.value)
            if not "." in new_name:
                if "." in media.file_name:
                    extn = media.file_name.rsplit('.', 1)[-1]
                else:
                    extn = "mkv"
                new_name = new_name + "." + extn
            await reply_message.delete()

            button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ",callback_data = "upload_document")]]
            if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
                button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data = "upload_video")])
            elif file.media == MessageMediaType.AUDIO:
                button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data = "upload_audio")])
            
            await message.reply(
                text=f"<blockquote>**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`</blockquote>",
                reply_to_message_id=file.id,
                reply_markup=InlineKeyboardMarkup(button)
            )
    except Exception as e:
        print(f"Error in refunc: {e}")
    
    # Allow other handlers to process this message (e.g., /broadcast)
    await message.continue_propagation()


async def upload_doc(bot, update):
    user_id = int(update.message.chat.id)
    media_type = update.data  # upload_video, upload_document, upload_audio
    
    roxy_processing = await update.message.edit("<blockquote>`Processing...`</blockquote>")
    
    # Creating Directory for Metadata
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")
    
    # Set task tracking for /stop command AND per-user processing lock
    set_user_task(user_id, "File Processing", update.message.id)
    set_user_processing(user_id)

    new_name = update.message.text
    try:
        import re as _re
        new_filename_ = new_name.split(":-", 1)[1].strip().strip('`').strip()
        # Remove any trailing HTML/blockquote artifacts from Telegram text rendering
        new_filename_ = _re.sub(r'[\s_]*(/?blockquote)[\s_]*$', '', new_filename_, flags=_re.IGNORECASE).strip()
    except:
        clear_user_processing(user_id)
        return await roxy_processing.edit("<blockquote>❌ Error parsing filename. Please try again.</blockquote>")
    
    user_data = await roxy_bot.get_user_data(user_id)


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
        # adding prefix and suffix
        prefix = user_data.get('prefix', None)
        suffix = user_data.get('suffix', None)
        new_filename = await add_prefix_suffix(new_filename_, prefix, suffix)
        # Sanitize filename to prevent "File name too long" errors
        new_filename = sanitize_filename(new_filename)
    except Exception as e:
        clear_user_processing(user_id)
        return await roxy_processing.edit(f"<blockquote>⚠️ Something went wrong can't able to set Prefix or Suffix ☹️ \n\n❄️ Contact My Creator -> @roxybasicneedbot1\nError: {e}</blockquote>")

    # msg file location 
    file = update.message.reply_to_message
    media = getattr(file, file.media.value)
    
    # file downloaded path
    # Use unique temporary path to prevent race conditions
    import time
    unique_id = f"{user_id}_{int(time.time())}"
    file_path = f"Renames/{unique_id}_{new_filename}"
    metadata_path = f"Metadata/{unique_id}_{new_filename}"    

    await roxy_processing.edit("<blockquote>`Try To Download....`</blockquote>")
    if bot.uploadlimit:
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)
        total_used = int(used) + int(media.file_size)
        await roxy_bot.set_used_limit(user_id, total_used)
    
    try:
        dl_path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(DOWNLOAD_TEXT, roxy_processing, time.time()))
        
        # Validate download success
        if not dl_path or not os.path.exists(dl_path):
            clear_user_processing(user_id)
            return await roxy_processing.edit("<blockquote>❌ **Download Failed!**\n\nFile not found after download.</blockquote>")
            
        if os.path.getsize(dl_path) == 0:
            clear_user_processing(user_id)
            return await roxy_processing.edit("<blockquote>❌ **Download Failed!**\n\nFile is empty (0 bytes). Check your session string or file integrity.</blockquote>")
            
    except Exception as e:
        if bot.uploadlimit:
            used_remove = max(0, int(used) - int(media.file_size))
            await roxy_bot.set_used_limit(user_id, used_remove)
        clear_user_processing(user_id)
        return await roxy_processing.edit(f"<blockquote>Download Error: {e}</blockquote>")

    # NSFW scan moved to background — runs silently after file is sent to user

    # ===== TRIM VIDEO AFTER DOWNLOAD =====
    trim_mode = await roxy_bot.get_trim_mode(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    if trim_mode and is_premium and media_type in ["upload_video", "upload_document"]:
        from plugins.trim_handler import get_pending_trim, clear_pending_trim
        from helper.ffmpeg_trim import trim_video, get_video_duration
        
        pending = get_pending_trim(user_id)
        trim_type = pending.get('trim_type')
        
        if trim_type == 'auto':
            trim_duration = pending.get('duration', 0)
            if trim_duration > 0:
                # Get video duration to validate
                video_duration = await get_video_duration(dl_path)
                
                if video_duration and trim_duration > video_duration:
                    await safe_edit(roxy_processing, f"<blockquote>⚠️ <b>Video too short!</b>\n\nYour video is {int(video_duration // 60)} min {int(video_duration % 60)} sec.\nCan't trim to {trim_duration // 60} min.\n\nUploading full video...</blockquote>")
                else:
                    # Perform trim
                    trim_output = dl_path.rsplit('.', 1)[0] + "_trimmed." + dl_path.rsplit('.', 1)[1]
                    
                    async def trim_progress(percent, status):
                        try:
                            bar = "⬢" * int(percent / 5) + "⬡" * (20 - int(percent / 5))
                            await safe_edit(roxy_processing, f"<blockquote>✂️ <b>Trimming Video...</b>\n\n{bar} {percent:.0f}%</blockquote>")
                        except:
                            pass
                    
                    await safe_edit(roxy_processing, "<blockquote>✂️ <b>Trimming video...</b>\n\nPlease wait...</blockquote>")
                    
                    success = await trim_video(dl_path, trim_output, duration=trim_duration, progress_callback=trim_progress)
                    
                    if success and os.path.exists(trim_output):
                        # Remove original and use trimmed
                        try:
                            os.remove(dl_path)
                        except:
                            pass
                        dl_path = trim_output
                        file_path = trim_output  # Update file_path too for upload!
                        await safe_edit(roxy_processing, f"<blockquote>✅ Video trimmed to {trim_duration // 60} min!</blockquote>")
                    else:
                        await safe_edit(roxy_processing, "<blockquote>⚠️ Trim failed, uploading original...</blockquote>")
        
        elif trim_type == 'manual':
            start_time = pending.get('start_time')
            end_time = pending.get('end_time')
            
            if start_time and end_time:
                # Perform manual trim
                trim_output = dl_path.rsplit('.', 1)[0] + "_trimmed." + dl_path.rsplit('.', 1)[1]
                
                async def trim_progress(percent, status):
                    try:
                        bar = "⬢" * int(percent / 5) + "⬡" * (20 - int(percent / 5))
                        await safe_edit(roxy_processing, f"<blockquote>✂️ <b>Trimming Video...</b>\n\n{bar} {percent:.0f}%</blockquote>")
                    except:
                        pass
                
                await safe_edit(roxy_processing, f"<blockquote>✂️ <b>Trimming video...</b>\n\nFrom {start_time} to {end_time}...</blockquote>")
                
                success = await trim_video(dl_path, trim_output, start_time=start_time, end_time=end_time, progress_callback=trim_progress)
                
                if success and os.path.exists(trim_output):
                    # Remove original and use trimmed
                    try:
                        os.remove(dl_path)
                    except:
                        pass
                    dl_path = trim_output
                    file_path = trim_output  # Update file_path too for upload!
                    await safe_edit(roxy_processing, f"<blockquote>✅ Video trimmed from {start_time} to {end_time}!</blockquote>")
                else:
                    await safe_edit(roxy_processing, "<blockquote>⚠️ Trim failed, uploading original...</blockquote>")
        
        # Clear pending trim
        clear_pending_trim(user_id)

    # MKV to MP4 conversion if enabled
    mkv_converted = False
    original_dl_path = dl_path
    convert_mkv = await roxy_bot.get_convert_mkv_to_mp4(user_id)
    if convert_mkv and dl_path.lower().endswith('.mkv'):
        await safe_edit(roxy_processing, "<blockquote>🎬 Cᴏɴᴠᴇʀᴛɪɴɢ MKV ᴛᴏ MP4...</blockquote>")
        mp4_path = dl_path[:-4] + '.mp4'
        new_filename_mp4 = new_filename[:-4] + '.mp4' if new_filename.lower().endswith('.mkv') else new_filename
        if await convert_mkv_to_mp4(dl_path, mp4_path):
            # Remove original MKV file
            try:
                if os.path.exists(dl_path):
                    os.remove(dl_path)
            except:
                pass
            dl_path = mp4_path
            file_path = f"Renames/{unique_id}_{new_filename_mp4}"
            new_filename = new_filename_mp4
            metadata_path = f"Metadata/{unique_id}_{new_filename_mp4}"
            mkv_converted = True
            await safe_edit(roxy_processing, "<blockquote>✅ MKV ᴄᴏɴᴠᴇʀᴛᴇᴅ ᴛᴏ MP4 sᴜᴄᴄᴇssꜰᴜʟʟʏ!</blockquote>")
        else:
            await safe_edit(roxy_processing, "<blockquote>⚠️ MKV ᴄᴏɴᴠᴇʀsɪᴏɴ ꜰᴀɪʟᴇᴅ, ᴜᴘʟᴏᴀᴅɪɴɢ ᴏʀɪɢɪɴᴀʟ ꜰɪʟᴇ...</blockquote>")

    # ===== SUBTITLE MUXING (Multi-language, MKV output) =====
    video_extensions_check = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
    is_video_for_sub = any(new_filename.lower().endswith(ext) for ext in video_extensions_check)

    from plugins.subtitle_mux import get_pending_subtitles, clear_pending_subtitle
    pending_subs = get_pending_subtitles(user_id)

    if pending_subs and is_video_for_sub:
        # Check all subtitle files exist
        valid_subs = [s for s in pending_subs if os.path.exists(s['path'])]

        if not valid_subs:
            await safe_edit(roxy_processing, "<blockquote>⚠️ Subtitle files missing, uploading original video...</blockquote>")
            clear_pending_subtitle(user_id)
        else:
            sub_count = len(valid_subs)
            lang_names = ', '.join([s.get('title', '?') for s in valid_subs])
            await safe_edit(roxy_processing, f"<blockquote>📝 <b>Adding {sub_count} Subtitle(s)...</b>\n\n🌐 {lang_names}\n\nPlease wait...</blockquote>")

            # Sub output path — always MKV for subtitle support
            ext_idx = dl_path.rfind('.')
            sub_output_base = dl_path[:ext_idx] if ext_idx > -1 else dl_path
            sub_output = sub_output_base + "_subb.mkv"

            from helper.subtitle_ffmpeg import mux_subtitles

            success = False
            actual_output = sub_output
            try:
                success, actual_output = await mux_subtitles(dl_path, valid_subs, sub_output)
            except Exception as sub_err:
                print(f"[SubtitleMux] Exception: {sub_err}")
                import traceback
                traceback.print_exc()
                success = False

            if success and os.path.exists(actual_output) and os.path.getsize(actual_output) > 0:
                try:
                    os.remove(dl_path)
                except:
                    pass
                dl_path = actual_output    # update download path
                file_path = actual_output  # CRITICAL: final upload uses muxed file

                # Force filename extension to .mkv since output is always MKV
                name_base, name_ext = os.path.splitext(new_filename)
                if name_ext.lower() != '.mkv':
                    new_filename = name_base + '.mkv'
                    print(f"[SubtitleMux] Forced filename to MKV: {new_filename}")

                await safe_edit(roxy_processing, f"<blockquote>✅ {sub_count} subtitle(s) added successfully!\n\n🌐 {lang_names}</blockquote>")
            else:
                # Cleanup failed output
                for p in [sub_output, actual_output]:
                    if p and os.path.exists(p):
                        try:
                            os.remove(p)
                        except:
                            pass
                await safe_edit(roxy_processing, "<blockquote>⚠️ Subtitle mux failed, uploading original video...</blockquote>")

            clear_pending_subtitle(user_id)

    metadata_mode = await roxy_bot.get_metadata_mode(user_id)
    if metadata_mode:        
        metadata = await roxy_bot.get_metadata_code(user_id)
        if metadata:
            await safe_edit(roxy_processing, "<blockquote>I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**</blockquote>")            
            if await change_metadata(dl_path, metadata_path, metadata):            
                await safe_edit(roxy_processing, "<blockquote>Metadata Added.....</blockquote>")
                print("Metadata Added.....")
            else:
                await safe_edit(roxy_processing, "<blockquote>Failed to add metadata, uploading original file...</blockquote>")
                metadata_mode = False
        else:
            await safe_edit(roxy_processing, "<blockquote>No metadata found, uploading original file...</blockquote>")
            metadata_mode = False
    else:
        await safe_edit(roxy_processing, "<blockquote>`Try To Uploading....`</blockquote>")

    # ===== WATERMARK VIDEO (Premium) =====
    watermark_text = await roxy_bot.get_watermark(user_id)
    watermark_path = None
    if watermark_text and is_premium:
        video_extensions_wm = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
        is_video_wm = any(new_filename.lower().endswith(ext) for ext in video_extensions_wm)
        if is_video_wm:
            from helper.ffmpeg import add_text_watermark
            watermark_position = await roxy_bot.get_watermark_position(user_id)
            source_for_wm = metadata_path if metadata_mode and os.path.exists(metadata_path) else dl_path
            watermark_path = source_for_wm + "_watermarked.mp4"
            await safe_edit(roxy_processing, "<blockquote>🎨 Aᴅᴅɪɴɢ Wᴀᴛᴇʀᴍᴀʀᴋ...</blockquote>")
            if await add_text_watermark(source_for_wm, watermark_path, watermark_text, watermark_position):
                # Use watermarked file as the source for upload
                if metadata_mode and os.path.exists(metadata_path):
                    metadata_path = watermark_path
                else:
                    dl_path = watermark_path
                await safe_edit(roxy_processing, f"<blockquote>✅ Watermark '{watermark_text}' added!</blockquote>")
            else:
                await safe_edit(roxy_processing, "<blockquote>⚠️ Watermark failed, uploading without watermark...</blockquote>")
                watermark_path = None
        
    # Get video duration using FFmpeg (more reliable than hachoir)
    duration = 0
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
    is_video = any(new_filename.lower().endswith(ext) for ext in video_extensions)
    
    if is_video:
        try:
            ffmpeg_duration = await get_video_duration(dl_path)
            if ffmpeg_duration:
                duration = int(ffmpeg_duration)
                print(f"Got video duration from FFmpeg: {duration} seconds")
        except Exception as e:
            print(f"FFmpeg duration extraction failed: {e}")
    
    # Fallback to hachoir if FFmpeg failed
    if duration == 0 and is_video:
        try:
             # Check file size > 0
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                parser = createParser(file_path)
                if parser:
                    metadata_info = extractMetadata(parser)
                    if metadata_info and metadata_info.has("duration"):
                        duration = metadata_info.get('duration').seconds
                    parser.close()
        except Exception as e:
            print(f"Error extracting metadata with hachoir: {e}")
        
    ph_path = None
    c_caption = user_data.get('caption', None)
    c_thumb = user_data.get('file_id', None)

    if c_caption:
         try:
             # Extract metadata from the original filename for caption placeholders
             # Get original filename from media
             original_filename = media.file_name if media.file_name else new_filename
             metadata = extract_metadata_from_filename(original_filename)
             
             # adding custom caption with extended placeholder support
             caption = c_caption.format(
                 filename=new_filename, 
                 filesize=humanbytes(media.file_size), 
                 duration=convert(duration),
                 episode=metadata.get('episode', ''),
                 season=metadata.get('season', ''),
                 chapter=metadata.get('chapter', ''),
                 quality=metadata.get('quality', ''),
                 audio=metadata.get('audio', ''),
                 # Also support capitalized versions
                 Episode=metadata.get('episode', ''),
                 Season=metadata.get('season', ''),
                 Chapter=metadata.get('chapter', ''),
                 Quality=metadata.get('quality', ''),
                 Audio=metadata.get('audio', '')
             )
         except KeyError as e:
             if bot.uploadlimit:
                 used_remove = max(0, int(used) - int(media.file_size))
                 await roxy_bot.set_used_limit(user_id, used_remove)
             return await roxy_processing.edit(text=f"<blockquote>Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ: Iɴᴠᴀʟɪᴅ Pʟᴀᴄᴇʜᴏʟᴅᴇʀ ●> {e}\n\n<b>Sᴜᴘᴘᴏʀᴛᴇᴅ:</b> {{filename}}, {{filesize}}, {{duration}}, {{episode}}, {{season}}, {{chapter}}, {{quality}}, {{audio}}</blockquote>")
         except Exception as e:
             if bot.uploadlimit:
                 used_remove = max(0, int(used) - int(media.file_size))
                 await roxy_bot.set_used_limit(user_id, used_remove)
             return await roxy_processing.edit(text=f"<blockquote>Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ ●> ({e})</blockquote>")             
    else:
         caption = f"<blockquote>**{new_filename}**</blockquote>"
 
    if (media.thumbs or c_thumb):
         # downloading thumbnail path
         try:
             if c_thumb:
                 ph_path = await bot.download_media(c_thumb) 
             else:
                 ph_path = await bot.download_media(media.thumbs[0].file_id)
             
             if ph_path and os.path.exists(ph_path):
                 img = Image.open(ph_path).convert("RGB")
                 # Preserve aspect ratio: fit within 320x320 without stretching
                 # For 16:9 video (1280x720) → becomes 320x180, NOT 320x320
                 img.thumbnail((320, 320), Image.LANCZOS)
                 img.save(ph_path, "JPEG")
         except Exception as e:
             print(f"Error processing thumbnail: {e}")
             ph_path = None

    # ===== TMDb Auto-Thumbnail Override =====
    tmdb_auto_thumb = await roxy_bot.get_tmdb_auto_thumb(user_id)
    if tmdb_auto_thumb and is_tmdb_available():
        # Check if a poster was saved during TMDb confirm callback
        tmdb_poster_key = f"{user_id}_poster"
        tmdb_poster_path = _pending_tmdb.pop(tmdb_poster_key, None)
        
        if not tmdb_poster_path:
            # No poster from callback — try to detect and download now
            try:
                original_fn = media.file_name if media.file_name else new_filename
                detected = analyze_filename(original_fn)
                if detected.get("title"):
                    tmdb_lang = await roxy_bot.get_tmdb_language(user_id)
                    tmdb_data = await auto_match_tmdb(detected, language=tmdb_lang)
                    if tmdb_data and tmdb_data.get("poster_url"):
                        tmdb_poster_path = await download_poster(tmdb_data["poster_url"])
            except Exception as e:
                print(f"[TMDb Thumb] Auto-fetch error: {e}")
        
        if tmdb_poster_path and os.path.exists(tmdb_poster_path):
            try:
                img = Image.open(tmdb_poster_path).convert("RGB")
                img.thumbnail((320, 320), Image.LANCZOS)
                img.save(tmdb_poster_path, "JPEG")
                # Override existing thumbnail with TMDb poster
                if ph_path and os.path.exists(ph_path) and ph_path != tmdb_poster_path:
                    try:
                        os.remove(ph_path)
                    except:
                        pass
                ph_path = tmdb_poster_path
                print(f"[TMDb Thumb] ✅ Using TMDb poster as thumbnail")
            except Exception as e:
                print(f"[TMDb Thumb] Poster processing error: {e}")
                # Keep original thumbnail if TMDb poster fails

    type = update.data.split("_")[1]
    
    # Use the correct file path based on metadata mode
    final_file_path = metadata_path if metadata_mode and os.path.exists(metadata_path) else file_path
    
    if app and media.file_size > 2000 * 1024 * 1024:
        try:
            if type == "document":
                filw = await app.send_document(
                    Config.LOG_CHANNEL,
                    document=final_file_path,
                    file_name=new_filename,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, roxy_processing, time.time()))
            elif type == "video":
                filw = await app.send_video(
                    Config.LOG_CHANNEL,
                    video=final_file_path,
                    file_name=new_filename,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, roxy_processing, time.time()))
            elif type == "audio":
                filw = await app.send_audio(
                    Config.LOG_CHANNEL,
                    audio=final_file_path,
                    file_name=new_filename,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, roxy_processing, time.time()))

            from_chat = filw.chat.id
            mg_id = filw.id
            await asyncio.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await bot.delete_messages(from_chat, mg_id)
            
            # Log upload activity
            await roxy_bot.log_upload(user_id, media.file_size)
            
            # Silent background NSFW scan after delivery
            asyncio.create_task(_background_nsfw_scan(bot, dl_path, user_id, None, extra_messages=[]))
            
        except Exception as e:
            if bot.uploadlimit:
                used_remove = max(0, int(used) - int(media.file_size))
                await roxy_bot.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            clear_user_processing(user_id)
            return await roxy_processing.edit(f"<blockquote>Upload Error: {e}</blockquote>")
    else:
        # Check if user has set a dump channel
        dump_channel = await roxy_bot.get_dump_channel(user_id)
        target_chat = dump_channel if dump_channel else update.message.chat.id
        
        # Check screenshot settings BEFORE upload
        screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
        screenshot_task = None
        
        # Start screenshot generation in parallel with upload if enabled and video
        if screenshot_mode and type == "video":
            screenshot_task = asyncio.create_task(generate_screenshots(final_file_path, interval=300))
        
        try:
            if type == "document":
                sent_msg = await bot.send_document(
                    target_chat,
                    document=final_file_path,
                    file_name=new_filename,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, roxy_processing, time.time()))
            elif type == "video":
                sent_msg = await bot.send_video(
                    target_chat,
                    video=final_file_path,
                    file_name=new_filename,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, roxy_processing, time.time()))
            elif type == "audio":
                sent_msg = await bot.send_audio(
                    target_chat,
                    audio=final_file_path,
                    file_name=new_filename,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, roxy_processing, time.time()))
            
            # Log upload activity
            await roxy_bot.log_upload(user_id, media.file_size)
            
            # Silent background NSFW scan after delivery
            asyncio.create_task(_background_nsfw_scan(bot, dl_path, user_id, sent_msg, extra_messages=[roxy_processing]))
            
            # Wait for screenshots if task was started
            screenshot_paths = []
            if screenshot_task:
                try:
                    screenshot_paths = await screenshot_task
                    if screenshot_paths:
                        # Send screenshots to same target as file
                        for i in range(0, len(screenshot_paths), 10):
                            batch = screenshot_paths[i:i+10]
                            media_group = [InputMediaPhoto(path) for path in batch]
                            await bot.send_media_group(target_chat, media_group)
                        await cleanup_screenshots(screenshot_paths)
                except Exception as ss_err:
                    print(f"Screenshot error: {ss_err}")
                    screenshot_paths = []
            
        except Exception as e:
            if bot.uploadlimit:
                used_remove = max(0, int(used) - int(media.file_size))
                await roxy_bot.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            clear_user_processing(user_id)
            
            # Provide helpful error message for dump channel issues
            if dump_channel:
                return await roxy_processing.edit(f"<blockquote>Upload Error: {e}\n\n⚠️ Mᴀᴋᴇ sᴜʀᴇ I ᴀᴍ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ᴅᴜᴍᴘ ᴄʜᴀɴɴᴇʟ!</blockquote>")
            return await roxy_processing.edit(f"<blockquote>Upload Error: {e}</blockquote>")
    
    # Video compression for Premium users (after main upload is done)
    compress_mode = await roxy_bot.get_compress_video(user_id)
    is_premium = await roxy_bot.has_premium_access(user_id)
    compressed_count = 0
    
    # Use the already downloaded file for compression (no need to re-download!)
    # The file to compress is either metadata_path (if metadata was added) or dl_path
    compress_source_file = metadata_path if metadata_mode and os.path.exists(metadata_path) else dl_path
    
    # Check if file is a video by extension (works even when uploaded as "document")
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
    is_video_file = any(new_filename.lower().endswith(ext) for ext in video_extensions)
    
    if compress_mode and is_premium and is_video_file and os.path.exists(compress_source_file):
        try:
            await safe_edit(roxy_processing, "<blockquote>📦 Sᴛᴀʀᴛɪɴɢ ᴠɪᴅᴇᴏ ᴄᴏᴍᴘʀᴇssɪᴏɴ...</blockquote>")
            
            # Get base filename without extension and CLEAN existing resolution tags
            base_filename_raw = os.path.splitext(new_filename)[0]
            base_filename = clean_resolution_from_filename(base_filename_raw)
            
            # Get video duration for progress tracking
            video_duration = await get_video_duration(compress_source_file)
            
            # Create output directory
            if not os.path.exists("Compressed"):
                os.makedirs("Compressed")
            
            # Resolutions to compress - process and send each one immediately
            resolutions = [
                ('720p', 720),
                ('480p', 480),
                ('360p', 360)
            ]
            
            for res_name, height in resolutions:
                # Check for cancellation from /stop command
                if is_task_cancelled(user_id):
                    await safe_edit(roxy_processing, "<blockquote>🛑 <b>Cᴏᴍᴘʀᴇssɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ ʙʏ ᴜsᴇʀ.</b></blockquote>")
                    break
                
                output_file = os.path.join("Compressed", f"{base_filename}_{res_name}.mp4")
                
                # Progress callback with hexagon progress bar
                async def compression_progress(percentage, eta_str):
                    # Build hexagon progress bar (⬢ filled, ⬡ empty)
                    filled = math.floor(percentage / 5)
                    progress_bar = ''.join(["⬢" for _ in range(filled)]) + ''.join(["⬡" for _ in range(20 - filled)])
                    
                    progress_text = f"""<blockquote><b>📦 Cᴏᴍᴘʀᴇssɪɴɢ ᴛᴏ {res_name}...

{progress_bar}

✘ Dᴏɴᴇ: {percentage:.1f}%
✘ ETA: {eta_str}</b></blockquote>"""
                    try:
                        await roxy_processing.edit(progress_text)
                    except:
                        pass
                
                # Compress this resolution
                success = await compress_video_single(
                    compress_source_file, 
                    output_file, 
                    height, 
                    video_duration, 
                    compression_progress
                )
                
                if success and os.path.exists(output_file):
                    compressed_count += 1
                    
                    # Send immediately with thumbnail!
                    await safe_edit(roxy_processing, f"<blockquote>📤 Uᴘʟᴏᴀᴅɪɴɢ {res_name}...</blockquote>")
                    comp_caption = f"<blockquote><b>{base_filename}_{res_name}.mp4</b>\n📦 Compressed to {res_name}</blockquote>"
                    
                    try:
                        await bot.send_video(
                            target_chat,
                            video=output_file,
                            caption=comp_caption,
                            thumb=ph_path,  # Include thumbnail!
                            progress=progress_for_pyrogram,
                            progress_args=(f"Uploading {res_name}...", roxy_processing, time.time())
                        )
                        print(f"Uploaded {res_name} successfully")
                    except Exception as upload_err:
                        print(f"Error uploading {res_name}: {upload_err}")
                    
                    # Cleanup this compressed file immediately after upload
                    try:
                        if os.path.exists(output_file):
                            os.remove(output_file)
                    except:
                        pass
                else:
                    print(f"Compression to {res_name} failed")
                    await safe_edit(roxy_processing, f"<blockquote>⚠️ {res_name} ᴄᴏᴍᴘʀᴇssɪᴏɴ ꜰᴀɪʟᴇᴅ, sᴋɪᴘᴘɪɴɢ...</blockquote>")
                    await asyncio.sleep(1)
                
        except Exception as e:
            print(f"Compression error: {e}")
            import traceback
            traceback.print_exc()
    
    # Clean up original files (after compression is done)
    await remove_path(ph_path, file_path, dl_path, metadata_path)
    # Clean up watermark temp file if exists
    if watermark_path and os.path.exists(watermark_path):
        try:
            os.remove(watermark_path)
        except:
            pass
    
    # Clear task tracking and per-user processing lock
    clear_user_task(user_id)
    clear_user_processing(user_id)
    
    # Check if task was cancelled
    if is_task_cancelled(user_id):
        return
    
    # Success message
    if dump_channel:
        try:
            chat = await bot.get_chat(dump_channel)
            ss_text = f"\n📸 Screenshots: {len(screenshot_paths)}" if screenshot_paths else ""
            comp_text = f"\n📦 Compressed: {compressed_count} versions" if compressed_count > 0 else ""
            return await safe_edit(roxy_processing, f"<blockquote>✅ Uᴘʟᴏᴀᴅᴇᴅ Sᴜᴄᴄᴇssꜰᴜʟʟʏ!\n\n📺 Dᴜᴍᴘᴇᴅ ᴛᴏ: <b>{chat.title}</b>{ss_text}{comp_text}</blockquote>")
        except:
            return await safe_edit(roxy_processing, "<blockquote>✅ Uᴘʟᴏᴀᴅᴇᴅ Sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴛᴏ ᴅᴜᴍᴘ ᴄʜᴀɴɴᴇʟ!</blockquote>")
    
    ss_text = f"\n📸 Screenshots: {len(screenshot_paths)}" if screenshot_paths else ""
    comp_text = f"\n📦 Compressed: {compressed_count} versions" if compressed_count > 0 else ""
    await safe_edit(roxy_processing, f"<blockquote>Uploaded Successfully....{ss_text}{comp_text}</blockquote>")
    
    # ===== AUTO-DELETE NOTICE + SCHEDULING =====
    import datetime as _dt
    from config import roxy as roxy_config
    delete_hours = Config.AUTO_DELETE_HOURS
    delete_at = _dt.datetime.now() + _dt.timedelta(hours=delete_hours)
    
    try:
        auto_del_msg = await bot.send_message(
            update.message.chat.id if hasattr(update, 'message') else user_id,
            roxy_config.AUTO_DELETE_TXT.format(delete_hours)
        )
        # Schedule auto-delete for the notice message
        await roxy_bot.schedule_auto_delete(auto_del_msg.chat.id, auto_del_msg.id, delete_at)
    except:
        pass
    
    # Schedule auto-delete for the processing message
    try:
        await roxy_bot.schedule_auto_delete(roxy_processing.chat.id, roxy_processing.id, delete_at)
    except:
        pass
    
    # Schedule auto-delete for the sent file message (if not dump channel)
    if not dump_channel:
        try:
            if 'sent_msg' in dir() and sent_msg:
                await roxy_bot.schedule_auto_delete(sent_msg.chat.id, sent_msg.id, delete_at)
        except:
            pass

    # Clean up after short delay
    await asyncio.sleep(5)
    try:
        await roxy_processing.delete()
    except:
        pass
    try:
        if update.message:
            await update.message.delete()
    except:
        pass
    # Delete user's original file message
    try:
        if file:
            await file.delete()
    except:
        pass


# ✅ Team-RoxyBasicNeedBot

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
