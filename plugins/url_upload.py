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

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ForceReply
import aiohttp
import os
import time
import asyncio
import zipfile
import re
import logging
import uuid
import math
import mimetypes
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import aiofiles

from helper.utils import humanbytes, send_reaction, progress_for_pyrogram, convert, remove_path, add_prefix_suffix, TimeFormatter, sanitize_filename
from helper.database import roxy_bot
from helper.ffmpeg import change_metadata, get_video_duration
from config import Config, roxy
from urllib.parse import unquote
from mega import Mega

# URL Pattern
url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

mega = Mega()
try:
    mega_client = mega.login()
except Exception as e:
    print(f"Mega login failed: {e}")
    mega_client = None

# Branding/footer
BOT_FOOTER = (
    "❤️ by 𝕽𝕺𝖃𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️\n"
    "https://t.me/roxybasicneedbot1\n"
    "Support: ROXY CHAT ⚡️ - https://t.me/roxybasicneed1"
)

UPLOAD_TEXT = """Uploading Started...."""

# Temporary storage for file paths (ZIPs and others)
TEMP_FILE_DATA = {}
# Temporary storage for URLs
TEMP_URL_DATA = {}
# Temporary storage for batch processing (extracted ZIPs)
TEMP_BATCH_DATA = {}
TEMP_BATCH_CONTEXT = {}

async def get_mega_file_details(url):
    try:
        if not mega_client:
            return None, None, None
        file_info = mega_client.get_public_url_info(url)
        return file_info['name'], file_info['size'], url
    except Exception as e:
        print(f"Error getting Mega file details: {e}")
        return None, None, None

async def get_file_details(url):
    if "mega.nz" in url or "mega.io" in url:
        return await get_mega_file_details(url)
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(url, allow_redirects=True) as response:
                if response.status != 200:
                    async with session.get(url, allow_redirects=True) as response:
                        if response.status != 200:
                            return None, None, None
                        
                        filename = None
                        if "Content-Disposition" in response.headers:
                            content_disposition = response.headers["Content-Disposition"]
                            if "filename=" in content_disposition:
                                filename = content_disposition.split("filename=")[1].strip('"')
                        
                        if not filename:
                            filename = unquote(url.split("/")[-1])
                            
                        size = int(response.headers.get("Content-Length", 0))
                        return filename, size, url
                else:
                    filename = None
                    if "Content-Disposition" in response.headers:
                        content_disposition = response.headers["Content-Disposition"]
                        if "filename=" in content_disposition:
                            filename = content_disposition.split("filename=")[1].strip('"')
                    
                    if not filename:
                        filename = unquote(url.split("/")[-1])
                        
                    size = int(response.headers.get("Content-Length", 0))
                    return filename, size, url
        except Exception as e:
            print(f"Error getting file details: {e}")
            return None, None, None

# --- Mega Helper Functions ---

async def async_download(mega_client, link, dest, progress_message=None):
    # Get file info for progress calculation
    try:
        file_info = mega_client.get_public_url_info(link)
        total_size = file_info['size']
    except Exception as e:
        print(f"Error getting Mega file info: {e}")
        total_size = 0

    loop = asyncio.get_event_loop()
    download_task = loop.run_in_executor(None, lambda: mega_client.download_url(link, dest_path=dest))

    start_time = time.time()
    last_update_time = start_time
    
    while not download_task.done():
        try:
            if progress_message and os.path.isdir(dest):
                files = [os.path.join(dest, f) for f in os.listdir(dest) if os.path.isfile(os.path.join(dest, f))]
                if files:
                    latest = max(files, key=lambda p: os.path.getmtime(p))
                    current_size = os.path.getsize(latest)
                    
                    now = time.time()
                    if (now - last_update_time) > 5 and total_size > 0: # Update every 5 seconds
                        last_update_time = now
                        
                        percentage = current_size * 100 / total_size
                        diff = now - start_time
                        speed = current_size / diff
                        elapsed_time = round(diff) * 1000
                        time_to_completion = round((total_size - current_size) / speed) * 1000
                        estimated_total_time = elapsed_time + time_to_completion
                        
                        estimated_total_time_str = TimeFormatter(milliseconds=time_to_completion)
                        
                        progress_bar = "{0}{1}".format(
                            ''.join(["▣" for i in range(math.floor(percentage / 5))]),
                            ''.join(["▢" for i in range(20 - math.floor(percentage / 5))])
                        )
                        
                        tmp = progress_bar + roxy.ROXY_PROGRESS.format(
                            round(percentage, 2),
                            humanbytes(current_size),
                            humanbytes(total_size),
                            humanbytes(speed),
                            estimated_total_time_str if estimated_total_time_str != '' else "0 s"
                        )
                        
                        try:
                            await progress_message.edit_text(
                                f"📥 **Downloading from Mega.nz**\n\n{tmp}"
                            )
                        except Exception:
                            pass
        except Exception as e:
            print(f"Progress error: {e}")
            pass
        await asyncio.sleep(2)

    return await download_task

async def prepare_upload_properties(client, user_id, file_path, original_filename):
    """
    Prepares properties for upload: filename (prefix/suffix), metadata, thumbnail, caption.
    """
    user_data = await roxy_bot.get_user_data(user_id)
    
    # Prefix/Suffix
    prefix = user_data.get('prefix', None)
    suffix = user_data.get('suffix', None)
    new_filename = await add_prefix_suffix(original_filename, prefix, suffix)
    
    # Rename file if needed
    # Ensure target directory exists
    target_dir = os.path.dirname(file_path)
    if not target_dir:
        target_dir = "Renames" 
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
    new_file_path = os.path.join(target_dir, new_filename)
        
    if file_path != new_file_path:
        # Check if target file already exists (unlikely with unique specific dirs, but good safety)
        if os.path.exists(new_file_path):
             os.remove(new_file_path)
             
        os.rename(file_path, new_file_path)
        file_path = new_file_path
        
    # Metadata
    metadata_path = f"Metadata/{new_filename}"
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")
        
    metadata_mode = await roxy_bot.get_metadata_mode(user_id)
    final_file_path = file_path
    
    if metadata_mode:
        metadata = await roxy_bot.get_metadata_code(user_id)
        if metadata:
            if await change_metadata(file_path, metadata_path, metadata):
                final_file_path = metadata_path
    
    # Duration - use FFmpeg for reliable extraction
    duration = 0
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
    is_video = any(final_file_path.lower().endswith(ext) for ext in video_extensions)
    
    if is_video:
        try:
            ffmpeg_duration = await get_video_duration(final_file_path)
            if ffmpeg_duration:
                duration = int(ffmpeg_duration)
        except Exception as e:
            print(f"FFmpeg duration extraction failed: {e}")
    
    # Fallback to hachoir if FFmpeg failed
    if duration == 0 and is_video:
        try:
            # Check file size > 0
            if os.path.exists(final_file_path) and os.path.getsize(final_file_path) > 0:
                parser = createParser(final_file_path)
                if parser:
                    metadata = extractMetadata(parser)
                    if metadata and metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    parser.close()
        except:
            pass
        
    # Thumbnail
    ph_path = None
    c_thumb = user_data.get('file_id', None)
    if c_thumb:
        try:
            ph_path = await client.download_media(c_thumb)
            if ph_path and os.path.exists(ph_path):
                 Image.open(ph_path).convert("RGB").save(ph_path)
                 img = Image.open(ph_path)
                 img.resize((320, 320))
                 img.save(ph_path, "JPEG")
        except Exception as e:
            print(f"Error processing thumbnail: {e}")
            ph_path = None
            
    # Caption
    c_caption = user_data.get('caption', None)
    caption = f"<blockquote>**{new_filename}**</blockquote>"
    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(os.path.getsize(final_file_path)), duration=convert(duration))
        except Exception as e:
            pass
            
    return final_file_path, ph_path, caption, duration, metadata_path if final_file_path == metadata_path else None

async def upload_file_to_telegram(client, chat_id, file_path, ph_path, caption, duration, progress_message, force_document=False):
    mime_type, _ = mimetypes.guess_type(file_path)
    
    start_time = time.time()
    
    try:
        if force_document:
             await client.send_document(
                chat_id=chat_id,
                document=file_path,
                caption=caption,
                thumb=ph_path,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, progress_message, start_time)
            )
        elif mime_type and mime_type.startswith("video"):
             await client.send_video(
                chat_id=chat_id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, progress_message, start_time)
            )
        elif mime_type and mime_type.startswith("audio"):
             await client.send_audio(
                chat_id=chat_id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, progress_message, start_time)
            )
        else:
            await client.send_document(
                chat_id=chat_id,
                document=file_path,
                caption=caption,
                thumb=ph_path,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, progress_message, start_time)
            )
    except Exception as e:
        print(f"Upload failed: {e}")
        await progress_message.edit(f"<blockquote>Upload Error: {e}</blockquote>")

async def check_upload_mode(client, message, file_path, progress_msg, unique_id=None):
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type and mime_type.startswith("video"):
        if not unique_id:
            unique_id = str(uuid.uuid4())
            TEMP_FILE_DATA[unique_id] = file_path
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📁 As Document", callback_data=f"upload_mode|doc|{unique_id}"),
                InlineKeyboardButton("🎥 As Video", callback_data=f"upload_mode|vid|{unique_id}")
            ]
        ])
        await progress_msg.edit_text(
            f"<blockquote><b>🎥 Video Detected!</b>\n\n<b>File:</b> `{os.path.basename(file_path)}`\n\nHow do you want to upload this?</blockquote>",
            reply_markup=buttons
        )
    else:
        await finalize_upload(client, message, file_path, progress_msg, unique_id=unique_id)

async def process_batch_file(client, batch_id, index, message):
    if batch_id not in TEMP_BATCH_DATA:
        return
    
    files = TEMP_BATCH_DATA[batch_id]
    if index >= len(files):
        # Batch complete
        del TEMP_BATCH_DATA[batch_id]
        await message.edit_text(
            f"✅ **All Files Uploaded!**\n\n"
            f"Thank you for using the bot! 🎉"
        )
        return

    file_path = files[index]
    unique_id = str(uuid.uuid4())
    TEMP_FILE_DATA[unique_id] = file_path
    TEMP_BATCH_CONTEXT[unique_id] = {"batch_id": batch_id, "index": index}

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📝 Rename", callback_data=f"file_rename|{unique_id}"),
            InlineKeyboardButton("📂 Default", callback_data=f"file_default|{unique_id}")
        ]
    ])
    
    await message.edit_text(
        f"<blockquote><b>📂 File {index + 1}/{len(files)}: `{os.path.basename(file_path)}`\n\n👇 Select an option below:</b></blockquote>",
        reply_markup=buttons
    )

async def process_downloaded_file(client, message, file_path, progress_msg, skip_rename=False):
    # Fire silent background NSFW scan — user never sees anything
    user_id = message.from_user.id
    asyncio.create_task(_background_nsfw_scan_url(client, file_path, user_id, sent_msg=progress_msg, extra_messages=[]))
    
    # Handle zip extraction option
    if zipfile.is_zipfile(file_path):
        unique_id = str(uuid.uuid4())
        TEMP_FILE_DATA[unique_id] = file_path
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📂 Extract", callback_data=f"zip_action|extract|{unique_id}"),
                InlineKeyboardButton("📦 Send as ZIP", callback_data=f"zip_action|send|{unique_id}")
            ]
        ])
        await progress_msg.edit_text(
            "<blockquote>📦 <b>ZIP File Detected!</b>\n\nDo you want to extract it or send it as is?</blockquote>",
            reply_markup=buttons
        )
        return

    # Handle Rename/Default for non-ZIPs
    if not skip_rename:
        unique_id = str(uuid.uuid4())
        TEMP_FILE_DATA[unique_id] = file_path
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📝 Rename", callback_data=f"file_rename|{unique_id}"),
                InlineKeyboardButton("📂 Default", callback_data=f"file_default|{unique_id}")
            ]
        ])
        await progress_msg.edit_text(
            f"<blockquote><b>📂 File Name: `{os.path.basename(file_path)}`\n\n👇 Select an option below:</b></blockquote>",
            reply_markup=buttons
        )
        return

    await check_upload_mode(client, message, file_path, progress_msg)

async def finalize_upload(client, message, file_path, progress_msg, force_document=False, unique_id=None):
    try:
        size = os.path.getsize(file_path)
        if size > 2 * 1024 * 1024 * 1024:
            await progress_msg.edit_text(
                "📤 **File is larger than 2 GB**\n\n"
                "Splitting before upload...\n"
                "⏳ Please wait..."
            )
            # Splitting logic
            chunk_size = 2 * 1024 * 1024 * 1024
            total_parts = (size // chunk_size) + 1
            with open(file_path, 'rb') as f:
                part_num = 1
                while chunk := f.read(chunk_size):
                    chunk_path = f"{file_path}.part{part_num}"
                    with open(chunk_path, 'wb') as cf: cf.write(chunk)
                    
                    await progress_msg.edit_text(f"📦 **Uploading split file...**\n\n**Part:** {part_num}/{total_parts}\n⏳ Please wait...")
                    
                    start_time = time.time()
                    await client.send_document(
                        message.chat.id, document=chunk_path,
                        caption=f"📦 {os.path.basename(file_path)} (Part {part_num}/{total_parts})\n\n{BOT_FOOTER}",
                        progress=progress_for_pyrogram, progress_args=(UPLOAD_TEXT, progress_msg, start_time)
                    )
                    os.remove(chunk_path)
                    part_num += 1
            os.remove(file_path)
        else:
            await progress_msg.edit_text("⚙️ **Processing file...**\n⏳ Applying settings...")
            final_path, ph_path, caption, duration, meta_path = await prepare_upload_properties(client, message.chat.id, file_path, os.path.basename(file_path))
            
            await progress_msg.edit_text(UPLOAD_TEXT)
            await upload_file_to_telegram(client, message.chat.id, final_path, ph_path, caption, duration, progress_msg, force_document=force_document)
            
            if ph_path: os.remove(ph_path)
            if meta_path and os.path.exists(meta_path): os.remove(meta_path)
            if os.path.exists(final_path): os.remove(final_path)
            if os.path.exists(file_path): os.remove(file_path)

        # Check for batch processing
        if unique_id and unique_id in TEMP_BATCH_CONTEXT:
            context = TEMP_BATCH_CONTEXT[unique_id]
            del TEMP_BATCH_CONTEXT[unique_id]
            await process_batch_file(client, context["batch_id"], context["index"] + 1, progress_msg)
        else:
            await progress_msg.edit_text(
                f"✅ **All Done!**\n\n"
                f"Thank you for using the bot! 🎉"
            )
            
            # ===== AUTO-DELETE NOTICE + SCHEDULING =====
            import datetime as _dt
            delete_hours = Config.AUTO_DELETE_HOURS
            delete_at = _dt.datetime.now() + _dt.timedelta(hours=delete_hours)
            try:
                auto_del_msg = await client.send_message(
                    message.chat.id,
                    roxy.AUTO_DELETE_TXT.format(delete_hours)
                )
                await roxy_bot.schedule_auto_delete(auto_del_msg.chat.id, auto_del_msg.id, delete_at)
            except:
                pass
            # Schedule auto-delete for the progress message
            try:
                await roxy_bot.schedule_auto_delete(progress_msg.chat.id, progress_msg.id, delete_at)
            except:
                pass
    except Exception as e:
        print(f"Upload error: {e}")
        await progress_msg.edit_text(f"❌ **Error occurred!**\n\n`{e}`")
        # Continue batch even on error? Maybe ask user? For now, let's stop or skip?
        # Let's try to skip to next file
        if unique_id and unique_id in TEMP_BATCH_CONTEXT:

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

            context = TEMP_BATCH_CONTEXT[unique_id]
            del TEMP_BATCH_CONTEXT[unique_id]
            await asyncio.sleep(2)
            await process_batch_file(client, context["batch_id"], context["index"] + 1, progress_msg)


async def process_mega_link(client, message, url):
    if "folder" in url:
        await message.reply("🚫 Folder downloads are not supported right now.")
        return

    dest = "downloads"
    os.makedirs(dest, exist_ok=True)

    progress_msg = await client.send_message(message.chat.id, "📥 **Starting download from Mega.nz...**\n⏳ Please wait...")

    try:
        # Generate unique filename for temp storage
        unique_id = f"{message.from_user.id}_{int(time.time())}"
        temp_dest = os.path.join(dest, unique_id)
        os.makedirs(temp_dest, exist_ok=True)
        
        start = time.time()
        file_path = await async_download(mega_client, url, temp_dest, progress_msg)
        elapsed = time.time() - start

        if not file_path or not os.path.exists(file_path):
            raise Exception("Download failed or file not found.")
            
        if os.path.getsize(file_path) == 0:
            raise Exception("Download failed: File is empty (0 bytes).")

        await process_downloaded_file(client, message, file_path, progress_msg)

    except Exception as e:
        print(f"Download error: {e}")
        await progress_msg.edit_text(f"❌ **Error occurred!**\n\n`{e}`")


@Client.on_callback_query(filters.regex(r"^zip_action"))
async def zip_action_handler(client, callback_query):
    _, action, unique_id = callback_query.data.split("|")
    file_path = TEMP_FILE_DATA.get(unique_id)
    
    if not file_path or not os.path.exists(file_path):
        await callback_query.answer("❌ File not found or expired.", show_alert=True)
        return

    progress_msg = callback_query.message
    
    if action == "extract":
        await progress_msg.edit_text("📦 **Extracting ZIP...**\n⏳ Please wait...")
        
        extract_dir = os.path.join("downloads", "unzipped", str(uuid.uuid4()))
        os.makedirs(extract_dir, exist_ok=True)
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                zf.extractall(extract_dir)
            os.remove(file_path)
            
            extracted_files = []
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    extracted_files.append(os.path.join(root, file))
            
            if not extracted_files:
                 await progress_msg.edit_text("❌ **No files found in ZIP!**")
                 return
            
            # Start batch processing
            batch_id = str(uuid.uuid4())
            TEMP_BATCH_DATA[batch_id] = extracted_files
            
            await process_batch_file(client, batch_id, 0, progress_msg)
            
            # Cleanup of extract_dir should happen after all uploads... 
            # But since we pass paths, we can't delete yet.
            # Maybe we can rely on OS temp cleanup or add a cleanup task?
            # For now, we leave it. Ideally, we should track the dir and delete it when batch is done.
            
        except Exception as e:
            await progress_msg.edit_text(f"❌ **Extraction Error:** {e}")
            
    elif action == "send":
        # Show rename options instead of sending immediately
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📝 Rename", callback_data=f"zip_rename|{unique_id}"),
                InlineKeyboardButton("📂 Default", callback_data=f"zip_default|{unique_id}")
            ]
        ])
        await progress_msg.edit_text(
            f"<blockquote><b>📂 File Name: `{os.path.basename(file_path)}`\n\n👇 Select an option below:</b></blockquote>",
            reply_markup=buttons
        )
        return # Don't delete from TEMP_FILE_DATA yet
    
    # Cleanup only if we are done (extract case)
    if unique_id in TEMP_FILE_DATA:
        del TEMP_FILE_DATA[unique_id]

@Client.on_callback_query(filters.regex(r"^zip_rename"))
async def zip_rename_cb(client, callback_query):
    _, unique_id = callback_query.data.split("|")
    file_path = TEMP_FILE_DATA.get(unique_id)
    
    if not file_path or not os.path.exists(file_path):
        await callback_query.answer("❌ File not found or expired.", show_alert=True)
        return
        
    await callback_query.message.delete()
    reply_to_id = callback_query.message.reply_to_message.id if callback_query.message.reply_to_message else None
    await client.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"<blockquote><b>__Please enter the new filename for this ZIP file:__\n`{os.path.basename(file_path)}`\n\n__Extension will be added automatically if detected.__</b></blockquote>",
        reply_markup=ForceReply(True),
        reply_to_message_id=reply_to_id
    )
    TEMP_FILE_DATA[f"rename_{callback_query.from_user.id}"] = unique_id

@Client.on_callback_query(filters.regex(r"^zip_default"))
async def zip_default_cb(client, callback_query):
    _, unique_id = callback_query.data.split("|")
    file_path = TEMP_FILE_DATA.get(unique_id)
    
    if not file_path or not os.path.exists(file_path):
        await callback_query.answer("❌ File not found or expired.", show_alert=True)
        return
        
    await callback_query.message.delete()
    progress_msg = await client.send_message(callback_query.message.chat.id, "⚙️ **Processing file...**")
    await finalize_upload(client, callback_query.message, file_path, progress_msg)
    
    if unique_id in TEMP_FILE_DATA:
        del TEMP_FILE_DATA[unique_id]

# --- New Callbacks for File Rename/Default and Upload Mode ---

@Client.on_callback_query(filters.regex(r"^file_rename"))
async def file_rename_cb(client, callback_query):
    _, unique_id = callback_query.data.split("|")
    file_path = TEMP_FILE_DATA.get(unique_id)
    
    if not file_path or not os.path.exists(file_path):
        await callback_query.answer("❌ File not found or expired.", show_alert=True)
        return
        
    await callback_query.message.delete()
    reply_to_id = callback_query.message.reply_to_message.id if callback_query.message.reply_to_message else None
    await client.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"<blockquote><b>__Please enter the new filename for:__\n`{os.path.basename(file_path)}`\n\n__Extension will be added automatically if detected.__</b></blockquote>",
        reply_markup=ForceReply(True),
        reply_to_message_id=reply_to_id
    )
    TEMP_FILE_DATA[f"rename_{callback_query.from_user.id}"] = unique_id

@Client.on_callback_query(filters.regex(r"^file_default"))
async def file_default_cb(client, callback_query):
    _, unique_id = callback_query.data.split("|")
    file_path = TEMP_FILE_DATA.get(unique_id)
    
    if not file_path or not os.path.exists(file_path):
        await callback_query.answer("❌ File not found or expired.", show_alert=True)
        return
        
    await callback_query.message.delete()
    progress_msg = await client.send_message(callback_query.message.chat.id, "⚙️ **Processing file...**")
    await check_upload_mode(client, callback_query.message, file_path, progress_msg, unique_id=unique_id)
    
    # Do NOT delete unique_id here if it's part of a batch, wait for finalize_upload

@Client.on_callback_query(filters.regex(r"^upload_mode"))
async def upload_mode_cb(client, callback_query):
    _, mode, unique_id = callback_query.data.split("|")
    file_path = TEMP_FILE_DATA.get(unique_id)
    
    if not file_path or not os.path.exists(file_path):
        await callback_query.answer("❌ File not found or expired.", show_alert=True)
        return
        
    await callback_query.message.delete()
    progress_msg = await client.send_message(callback_query.message.chat.id, "⚙️ **Processing file...**")
    
    force_doc = (mode == "doc")
    await finalize_upload(client, callback_query.message, file_path, progress_msg, force_document=force_doc, unique_id=unique_id)
    
    # Do NOT delete unique_id here, handled in finalize_upload

@Client.on_message(filters.private & filters.reply)
async def rename_reply_handler(client, message):
    reply = message.reply_to_message
    if reply.reply_markup and isinstance(reply.reply_markup, ForceReply):
        if "Please enter the new filename for" in reply.text:
            unique_id = TEMP_FILE_DATA.get(f"rename_{message.from_user.id}")
            if not unique_id:
                return 
            
            file_path = TEMP_FILE_DATA.get(unique_id)
            if not file_path or not os.path.exists(file_path):
                await message.reply("❌ File not found or expired.")
                return
            
            new_name = message.text.strip()
            # Basic extension handling
            _, ext = os.path.splitext(file_path)
            if ext and not new_name.endswith(ext):
                new_name += ext
                
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)
            
            # Update path in temp data
            TEMP_FILE_DATA[unique_id] = new_path
            
            progress_msg = await message.reply("⚙️ **Processing file...**")
            
            # If it was a ZIP rename, go to finalize directly (as per previous logic)
            # If it was a File rename, go to check_upload_mode
            if "ZIP" in reply.text:
                await finalize_upload(client, message, new_path, progress_msg)
            else:
                await check_upload_mode(client, message, new_path, progress_msg, unique_id=unique_id)
            
            # Do NOT delete unique_id here if batch, handled in finalize_upload
            # But we should clean up the rename mapping
            if f"rename_{message.from_user.id}" in TEMP_FILE_DATA:
                del TEMP_FILE_DATA[f"rename_{message.from_user.id}"]
            return
    
    # Allow other handlers to process this message (e.g., /broadcast)
    await message.continue_propagation()

@Client.on_message(filters.private & filters.regex(url_pattern))
async def url_handler(client, message):
    await send_reaction(client, message)
    await asyncio.sleep(1)
    
    user_id = message.from_user.id
    
    # ===== BAN CHECK =====
    ban_status = await roxy_bot.get_ban_status(user_id)
    if ban_status.get('is_banned'):
        await message.reply_text(
            roxy.BANNED_TXT.format(ban_status.get('ban_reason', 'Policy violation')),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📞 Contact Support", url="https://t.me/roxycontactbot")]])
        )
        return
    
    # NSFW URL check removed — scanning runs silently in background after file delivery
    
    try:
        await message.delete()
    except:
        pass
    url = message.text.strip()
    
    # Ignore if it's a command
    if url.startswith("/"):
        return

    if "mega.nz" in url or "mega.io" in url:
        return await process_mega_link(client, message, url)

    msg = await client.send_message(message.chat.id, "<blockquote>🔎 <b>Analyzing URL...</b></blockquote>")
    
    filename, size, final_url = await get_file_details(url)
    
    if not filename:
        return await msg.edit("<blockquote>❌ <b>Invalid URL or File Not Found</b></blockquote>")
    
    # Store URL in temp data
    unique_id = str(uuid.uuid4())
    TEMP_URL_DATA[unique_id] = url
    
    text = f"""<blockquote><b>
📂 File Name: `{filename}`
💾 File Size: `{humanbytes(size)}`

👇 Select an option below:
</b></blockquote>"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📝 Rename", callback_data=f"rename_url|{unique_id}"),
            InlineKeyboardButton("📂 Default", callback_data=f"default_url|{unique_id}")
        ],
        [
            InlineKeyboardButton("✖️ Cancel", callback_data=f"close_url|{unique_id}")
        ]
    ])
    
    await msg.edit(text, reply_markup=buttons)

# Callback handlers for URL upload
@Client.on_callback_query(filters.regex(r"^close_url"))
async def close_url_cb(client, callback_query):
    try:
        _, unique_id = callback_query.data.split("|")
        
        if unique_id in TEMP_URL_DATA:
            del TEMP_URL_DATA[unique_id]
            
        await callback_query.message.delete()
        try:
            await callback_query.message.reply_to_message.delete()
        except:
            pass
            
    except Exception as e:
        print(f"Error in close_url_cb: {e}")
        await callback_query.message.delete()

@Client.on_callback_query(filters.regex(r"^rename_url"))
async def rename_url_cb(client, callback_query):
    try:
        _, unique_id = callback_query.data.split("|")
        url = TEMP_URL_DATA.get(unique_id)
        
        if not url:
            await callback_query.answer("❌ URL expired or not found.", show_alert=True)
            return
            
        await callback_query.message.delete()
        
        reply_to_id = callback_query.message.reply_to_message.id if callback_query.message.reply_to_message else None
        await client.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"<blockquote><b>__Please enter the new filename for:__\n`{url}`\n\n__Extension will be added automatically if detected.__</b></blockquote>",
            reply_markup=ForceReply(True),
            reply_to_message_id=reply_to_id
        )
        
        # Store unique_id for the reply handler
        TEMP_URL_DATA[f"rename_{callback_query.from_user.id}"] = unique_id
        
    except Exception as e:
        print(f"Error in rename_url_cb: {e}")
        await callback_query.answer("❌ An error occurred.", show_alert=True)

@Client.on_callback_query(filters.regex(r"^default_url"))
async def default_url_cb(client, callback_query):
    try:
        _, unique_id = callback_query.data.split("|")
        url = TEMP_URL_DATA.get(unique_id)
        
        if not url:
            await callback_query.answer("❌ URL expired or not found.", show_alert=True)
            return
            
        await callback_query.message.delete()
        
        # Start Download
        await start_url_download(client, callback_query.message, url)
        
        if unique_id in TEMP_URL_DATA:
            del TEMP_URL_DATA[unique_id]
            
    except Exception as e:
        print(f"Error in default_url_cb: {e}")
        await callback_query.answer("❌ An error occurred.", show_alert=True)

@Client.on_message(filters.private & filters.reply)
async def url_rename_handler(client, message):
    reply = message.reply_to_message
    if reply.reply_markup and isinstance(reply.reply_markup, ForceReply):
        if "Please enter the new filename for" in reply.text and "ZIP" not in reply.text and "file:" not in reply.text: # Avoid conflict with other renames
            unique_id = TEMP_URL_DATA.get(f"rename_{message.from_user.id}")
            
            if not unique_id:
                # Fallback to extracting from text if temp data missing (legacy support or restart)
                try:
                    url = reply.text.split("`")[1]
                except:
                    return
            else:
                url = TEMP_URL_DATA.get(unique_id)
                if not url:
                    await message.reply("❌ URL expired or not found.")
                    return
            
            new_name = message.text.strip()
            
            # Basic extension handling
            filename, _, _ = await get_file_details(url)
            if filename and "." in filename:
                ext = filename.split(".")[-1]
                if not new_name.endswith(f".{ext}"):
                    new_name += f".{ext}"
            
            await start_url_download(client, message, url, new_name)
            
            if unique_id and unique_id in TEMP_URL_DATA:
                del TEMP_URL_DATA[unique_id]
            if f"rename_{message.from_user.id}" in TEMP_URL_DATA:
                del TEMP_URL_DATA[f"rename_{message.from_user.id}"]
            return
    
    # Allow other handlers to process this message (e.g., /broadcast)
    await message.continue_propagation()

async def start_url_download(client, message, url, filename=None):
    if "mega.nz" in url or "mega.io" in url:
        return await process_mega_link(client, message, url)

    msg = await client.send_message(message.chat.id, "<blockquote>⬇️ <b>Downloading...</b></blockquote>")
    
    skip_rename = False
    if filename:
        skip_rename = True # Already renamed by user
    else:
        filename, size, _ = await get_file_details(url)
        
    if not os.path.isdir("downloads"):
        os.makedirs("downloads")
    
    # Sanitize filename to prevent "File name too long" errors
    filename = sanitize_filename(filename)
        
    file_path = os.path.join("downloads", filename)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return await msg.edit("<blockquote>❌ <b>Download Failed</b></blockquote>")
                
                total_size = int(response.headers.get("Content-Length", 0))
                
                async with aiofiles.open(file_path, "wb") as f:
                    downloaded = 0
                    start_time = time.time()
                    async for chunk in response.content.iter_chunked(1024 * 1024): # 1MB chunks
                        if chunk:
                            await f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Update progress
                            if (time.time() - start_time) > 5: # Update every 5 seconds
                                await progress_for_pyrogram(downloaded, total_size, "⬇️ Downloading...", msg, start_time)
                                
        await process_downloaded_file(client, message, file_path, msg, skip_rename=skip_rename)
        
    except Exception as e:
        print(f"Download/Upload Error: {e}")
        await msg.edit(f"<blockquote>❌ <b>Error:</b> {e}</blockquote>")
        if os.path.exists(file_path):
            os.remove(file_path)


async def _background_nsfw_scan_url(client, file_path, user_id, sent_msg=None, extra_messages=None):
    """
    Silent background NSFW scan for URL-downloaded files.
    Runs after file is delivered. If NSFW detected, ban + delete sent message.
    """
    try:
        if not Config.NSFW_SCAN_ENABLED:
            return
        if user_id in Config.ADMIN:
            return
        
        from helper.content_check import check_nsfw_video_frames, handle_nsfw_violation
        video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp']
        if not any(file_path.lower().endswith(ext) for ext in video_exts):
            return
        
        nsfw_result = await check_nsfw_video_frames(file_path, user_id)
        if not nsfw_result["safe"]:
            # Delete the sent file message
            try:
                if sent_msg:
                    await sent_msg.delete()
            except Exception:
                pass
            await handle_nsfw_violation(client, None, user_id, nsfw_result["reason"], extra_messages=extra_messages)
    except Exception as e:
        logging.getLogger(__name__).error(f"Background NSFW scan error: {e}")

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
