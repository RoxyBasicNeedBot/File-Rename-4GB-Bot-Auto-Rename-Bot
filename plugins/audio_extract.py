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

# Audio Extraction Plugin
# Extract audio (MP3) from video files

import os, time, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import roxy_bot
from helper.utils import send_reaction
from helper.ffmpeg import extract_audio_from_video


@Client.on_message(filters.private & filters.command(['extract_audio']))
async def extract_audio_command(client, message):
    """Extract audio from a video file - reply to a video with /extract_audio"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    # Must be a reply to a video/document
    replied = message.reply_to_message
    if not replied:
        return await message.reply_text(
            "<blockquote><b>🎵 Exᴛʀᴀᴄᴛ Aᴜᴅɪᴏ</b>\n\n"
            "Reply to a <b>video file</b> with /extract_audio to extract its audio as MP3.\n\n"
            "<b>Usage:</b> Reply to a video → <code>/extract_audio</code></blockquote>"
        )
    
    # Check if the replied message contains a video or document
    media = replied.video or replied.document
    if not media:
        return await message.reply_text(
            "<blockquote>❌ <b>No video found!</b>\n\n"
            "Please reply to a <b>video file</b> to extract audio.</blockquote>"
        )
    
    # Check file extension for documents
    if replied.document:
        file_name = replied.document.file_name or ""
        video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
        if not any(file_name.lower().endswith(ext) for ext in video_exts):
            return await message.reply_text(
                "<blockquote>❌ <b>Not a video file!</b>\n\n"
                "Please reply to a video file (.mp4, .mkv, .avi, etc.)</blockquote>"
            )
    
    # Show processing message
    processing_msg = await message.reply_text(
        "<blockquote>🎵 <b>Exᴛʀᴀᴄᴛɪɴɢ Aᴜᴅɪᴏ...</b>\n\n"
        "⏳ Downloading video...</blockquote>"
    )
    
    dl_path = None
    output_path = None
    
    try:
        # Download the video
        dl_path = await replied.download(
            file_name=f"downloads/{user_id}_{int(time.time())}_audio_extract"
        )
        
        if not dl_path or not os.path.exists(dl_path):
            return await processing_msg.edit(
                "<blockquote>❌ <b>Download failed!</b></blockquote>"
            )
        
        await processing_msg.edit(
            "<blockquote>🎵 <b>Exᴛʀᴀᴄᴛɪɴɢ Aᴜᴅɪᴏ...</b>\n\n"
            "🔄 Converting to MP3...</blockquote>"
        )
        
        # Generate output filename
        if replied.video:
            orig_name = replied.video.file_name or "video"

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

        else:
            orig_name = replied.document.file_name or "video"
        
        base_name = os.path.splitext(orig_name)[0]
        output_path = f"downloads/{user_id}_{int(time.time())}_{base_name}.mp3"
        
        # Progress callback
        async def progress(percentage, status):
            try:
                await processing_msg.edit(
                    f"<blockquote>🎵 <b>Exᴛʀᴀᴄᴛɪɴɢ Aᴜᴅɪᴏ...</b>\n\n"
                    f"📊 Progress: <b>{percentage:.0f}%</b>\n"
                    f"📝 Status: {status}</blockquote>"
                )
            except:
                pass
        
        # Extract audio
        success = await extract_audio_from_video(
            dl_path, output_path, 
            audio_format="mp3", bitrate="192k",
            progress_callback=progress
        )
        
        if not success or not os.path.exists(output_path):
            return await processing_msg.edit(
                "<blockquote>❌ <b>Audio extraction failed!</b>\n\n"
                "The video may not contain an audio track.</blockquote>"
            )
        
        await processing_msg.edit(
            "<blockquote>🎵 <b>Exᴛʀᴀᴄᴛɪɴɢ Aᴜᴅɪᴏ...</b>\n\n"
            "📤 Uploading MP3...</blockquote>"
        )
        
        # Upload the MP3
        file_size = os.path.getsize(output_path)
        duration_sec = 0
        
        # Try to get audio duration
        try:
            from helper.ffmpeg import get_video_duration
            duration_sec = int(await get_video_duration(output_path))
        except:
            pass
        
        await client.send_audio(
            chat_id=message.chat.id,
            audio=output_path,
            file_name=f"{base_name}.mp3",
            caption=f"<blockquote>🎵 <b>Audio Extracted!</b>\n\n"
                    f"📁 <b>File:</b> <code>{base_name}.mp3</code>\n"
                    f"📊 <b>Size:</b> {file_size / (1024*1024):.1f} MB</blockquote>",
            duration=duration_sec,
            reply_to_message_id=message.id
        )
        
        await processing_msg.delete()
        
    except Exception as e:
        try:
            await processing_msg.edit(f"<blockquote>❌ <b>Error:</b> {str(e)[:200]}</blockquote>")
        except:
            pass
    finally:
        # Cleanup
        for path in [dl_path, output_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
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
