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

# Video Merge Feature - Merge up to 10 videos using FFmpeg
# Uses concat demuxer with -c copy for fast, lossless merging
# PREMIUM ONLY FEATURE

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from helper.database import roxy_bot
from helper.ffmpeg_merge import merge_videos, cleanup_merge_files, get_video_duration
from helper.utils import progress_for_pyrogram, humanbytes, send_reaction
from config import Config
from PIL import Image
import os, time, asyncio, math

# Store merge queues per user
merge_queues = {}

MAX_MERGE_FILES = 10

# Premium required message
PREMIUM_REQUIRED_MSG = """<blockquote>🚫 <b>Pʀᴇᴍɪᴜᴍ Fᴇᴀᴛᴜʀᴇ Oɴʟʏ!</b>

Gᴏ ᴀᴡᴀʏ ʙʀᴏᴛʜᴇʀ, ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴘʀᴇᴛᴛʏ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ ᴡʜᴏ sᴜᴘᴘᴏʀᴛ ᴍᴇ! 😢

Iꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴘʀᴇᴍɪᴜᴍ, ᴄʜᴇᴄᴋᴏᴜᴛ ᴏᴜʀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 👇</blockquote>"""


async def check_premium_access(client, message, user_id):
    """Check if user has premium access. Returns True if premium, False otherwise."""
    # Admins always have access
    if user_id in Config.ADMIN:
        return True
    
    # Check premium status
    is_premium = await roxy_bot.has_premium_access(user_id)
    if not is_premium:
        await message.reply_text(
            PREMIUM_REQUIRED_MSG,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💸 Cʜᴇᴄᴋᴏᴜᴛ Pʟᴀɴs", callback_data="upgrade")],
                [InlineKeyboardButton("💬 Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ", url="https://t.me/roxybasicneed1")]
            ])
        )
        return False
    return True


def get_user_merge_queue(user_id):
    """Get or create merge queue for user"""
    if user_id not in merge_queues:
        merge_queues[user_id] = {
            'files': [], 
            'mode': False, 
            'filenames': [],
            'merged_file': None,
            'pending_upload': False,
            'status_message_id': None,
            'chat_id': None
        }
    return merge_queues[user_id]


def clear_user_merge_queue(user_id):
    """Clear user's merge queue"""
    if user_id in merge_queues:
        # Cleanup downloaded files
        for f in merge_queues[user_id].get('files', []):
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass
        # Cleanup merged file
        merged = merge_queues[user_id].get('merged_file')
        if merged and os.path.exists(merged):
            try:
                os.remove(merged)
            except:
                pass
        merge_queues[user_id] = {
            'files': [], 
            'mode': False, 
            'filenames': [],
            'merged_file': None,
            'pending_upload': False,
            'status_message_id': None,
            'chat_id': None
        }


@Client.on_message(filters.private & filters.command("merge"))
async def start_merge_mode(client, message: Message):
    """Start merge mode to collect video files - PREMIUM ONLY"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    # Premium check
    if not await check_premium_access(client, message, user_id):
        return
    
    queue = get_user_merge_queue(user_id)
    queue['mode'] = True
    queue['files'] = []
    queue['filenames'] = []
    queue['merged_file'] = None
    queue['pending_upload'] = False
    queue['chat_id'] = message.chat.id
    
    # Send pinned status message with cancel button
    status_msg = await message.reply_text(
        "<blockquote><b>🎬 Mᴇʀɢᴇ Mᴏᴅᴇ Eɴᴀʙʟᴇᴅ!</b>\n\n"
        "📤 Sᴇɴᴅ ᴜᴘ ᴛᴏ <b>10 ᴠɪᴅᴇᴏ ꜰɪʟᴇs</b> ᴛᴏ ᴍᴇʀɢᴇ.\n\n"
        "📊 <b>Qᴜᴇᴜᴇ:</b> 0/10 ꜰɪʟᴇs\n\n"
        "<b>Cᴏᴍᴍᴀɴᴅs:</b>\n"
        "• /mergeall - Mᴇʀɢᴇ ᴀʟʟ ꜰɪʟᴇs\n"
        "• /mergestatus - Vɪᴇᴡ ǫᴜᴇᴜᴇ\n"
        "• /clearmerge - Cʟᴇᴀʀ ǫᴜᴇᴜᴇ\n"
        "• /exitmerge - Exɪᴛ ᴍᴇʀɢᴇ ᴍᴏᴅᴇ\n\n"
        "⚡ Usᴇs ꜰᴀsᴛ sᴛʀᴇᴀᴍ ᴄᴏᴘʏ (ɴᴏ ʀᴇ-ᴇɴᴄᴏᴅɪɴɢ)</blockquote>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ Mᴇʀɢᴇ", callback_data="cancel_merge_queue")]
        ])
    )
    queue['status_message_id'] = status_msg.id


@Client.on_message(filters.private & filters.command("clearmerge"))
async def clear_merge(client, message: Message):
    """Clear the merge queue - PREMIUM ONLY"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    # Premium check
    if not await check_premium_access(client, message, user_id):
        return
    
    queue = get_user_merge_queue(user_id)
    file_count = len(queue.get('files', []))
    clear_user_merge_queue(user_id)
    
    await message.reply_text(
        f"<blockquote>🗑️ <b>Mᴇʀɢᴇ Qᴜᴇᴜᴇ Cʟᴇᴀʀᴇᴅ!</b>\n\n"
        f"Rᴇᴍᴏᴠᴇᴅ {file_count} ꜰɪʟᴇ(s) ꜰʀᴏᴍ ǫᴜᴇᴜᴇ.\n\n"
        f"Bᴏᴛ ɪs ɴᴏᴡ ɪɴ ɴᴏʀᴍᴀʟ ʀᴇɴᴀᴍᴇ ᴍᴏᴅᴇ.</blockquote>"
    )


@Client.on_message(filters.private & filters.command("exitmerge"))
async def exit_merge_mode(client, message: Message):
    """Exit merge mode and return to normal rename mode - PREMIUM ONLY"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    queue = get_user_merge_queue(user_id)
    
    if not queue.get('mode', False):
        await message.reply_text(
            "<blockquote>❌ <b>Nᴏᴛ ɪɴ Mᴇʀɢᴇ Mᴏᴅᴇ!</b>\n\n"
            "Yᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ɪɴ ɴᴏʀᴍᴀʟ ʀᴇɴᴀᴍᴇ ᴍᴏᴅᴇ.</blockquote>"
        )
        return
    
    file_count = len(queue.get('files', []))
    clear_user_merge_queue(user_id)
    
    await message.reply_text(
        f"<blockquote>✅ <b>Exɪᴛᴇᴅ Mᴇʀɢᴇ Mᴏᴅᴇ!</b>\n\n"
        f"🗑️ Cʟᴇᴀʀᴇᴅ {file_count} ꜰɪʟᴇ(s) ꜰʀᴏᴍ ǫᴜᴇᴜᴇ.\n\n"
        f"📝 Bᴏᴛ ɪs ɴᴏᴡ ɪɴ ɴᴏʀᴍᴀʟ ʀᴇɴᴀᴍᴇ ᴍᴏᴅᴇ.\n"
        f"Sᴇɴᴅ ꜰɪʟᴇs ᴛᴏ ʀᴇɴᴀᴍᴇ ᴛʜᴇᴍ!</blockquote>"
    )


@Client.on_callback_query(filters.regex("^cancel_merge_queue$"))
async def cancel_merge_queue_callback(client, query):
    """Handle cancel merge button click"""
    user_id = query.from_user.id
    queue = get_user_merge_queue(user_id)
    
    if not queue.get('mode', False) and not queue.get('files', []):
        await query.answer("❌ No active merge queue!", show_alert=True)
        return
    
    file_count = len(queue.get('files', []))
    clear_user_merge_queue(user_id)
    
    await query.message.edit(
        f"<blockquote>✅ <b>Mᴇʀɢᴇ Cᴀɴᴄᴇʟʟᴇᴅ!</b>\n\n"
        f"🗑️ Cʟᴇᴀʀᴇᴅ {file_count} ꜰɪʟᴇ(s) ꜰʀᴏᴍ ǫᴜᴇᴜᴇ.\n\n"
        f"📝 Bᴏᴛ ɪs ɴᴏᴡ ɪɴ ɴᴏʀᴍᴀʟ ʀᴇɴᴀᴍᴇ ᴍᴏᴅᴇ.</blockquote>"
    )
    await query.answer("Merge cancelled!", show_alert=False)


@Client.on_callback_query(filters.regex("^merge_now_btn$"))
async def merge_now_button_callback(client, query):
    """Handle merge all button click from pinned status"""
    user_id = query.from_user.id
    queue = get_user_merge_queue(user_id)
    
    files = queue.get('files', [])
    
    if len(files) < 2:
        await query.answer("❌ Need at least 2 files to merge!", show_alert=True)
        return
    
    await query.answer("Starting merge...", show_alert=False)
    
    # Trigger the merge process
    # Create a mock message for the merge function
    class MockMessage:
        def __init__(self, original_msg, user):
            self.chat = original_msg.chat
            self.from_user = user
            self.id = original_msg.id
        
        async def reply_text(self, text, **kwargs):
            return await query.message.edit(text, **kwargs)
    
    mock_msg = MockMessage(query.message, query.from_user)
    await do_merge_files(client, mock_msg, user_id)


@Client.on_message(filters.private & filters.command("mergestatus"))
async def merge_status(client, message: Message):
    """Show current merge queue status - PREMIUM ONLY"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    # Premium check
    if not await check_premium_access(client, message, user_id):
        return
    
    queue = get_user_merge_queue(user_id)
    files = queue.get('filenames', [])
    mode = queue.get('mode', False)
    
    if not files:
        status = "❌ Eᴍᴘᴛʏ" if mode else "❌ Nᴏᴛ Aᴄᴛɪᴠᴇ"
        await message.reply_text(
            f"<blockquote><b>📋 Mᴇʀɢᴇ Qᴜᴇᴜᴇ Sᴛᴀᴛᴜs</b>\n\n"
            f"Sᴛᴀᴛᴜs: {status}\n\n"
            f"Usᴇ /merge ᴛᴏ sᴛᴀʀᴛ ᴍᴇʀɢᴇ ᴍᴏᴅᴇ.</blockquote>"
        )
        return
    
    file_list = ""
    for i, name in enumerate(files, 1):
        file_list += f"{i}. {name}\n"
    
    await message.reply_text(
        f"<blockquote><b>📋 Mᴇʀɢᴇ Qᴜᴇᴜᴇ Sᴛᴀᴛᴜs</b>\n\n"
        f"<b>Fɪʟᴇs:</b> {len(files)}/{MAX_MERGE_FILES}\n\n"
        f"{file_list}\n"
        f"Usᴇ /mergeall ᴛᴏ ᴍᴇʀɢᴇ ᴛʜᴇsᴇ ꜰɪʟᴇs.</blockquote>"
    )


@Client.on_message(filters.private & (filters.video | filters.document), group=5)
async def collect_merge_files(client, message: Message):
    """Collect video files when merge mode is active"""
    user_id = message.from_user.id
    queue = get_user_merge_queue(user_id)
    
    # Check if merge mode is active
    if not queue.get('mode', False):
        return  # Let other handlers process this
    
    # Get file info
    media = message.video or message.document
    if not media:
        return
    
    # Check if it's a video file
    filename = media.file_name or "video.mp4"
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
    is_video = any(filename.lower().endswith(ext) for ext in video_extensions)
    
    if not is_video:
        await message.reply_text("<blockquote>❌ Pʟᴇᴀsᴇ sᴇɴᴅ ᴠɪᴅᴇᴏ ꜰɪʟᴇs ᴏɴʟʏ!</blockquote>")
        message.stop_propagation()
        return
    
    # Check queue limit
    if len(queue['files']) >= MAX_MERGE_FILES:
        await message.reply_text(
            f"<blockquote>❌ Mᴀxɪᴍᴜᴍ {MAX_MERGE_FILES} ꜰɪʟᴇs ʀᴇᴀᴄʜᴇᴅ!\n\n"
            f"Usᴇ /mergeall ᴛᴏ ᴍᴇʀɢᴇ ᴏʀ /clearmerge ᴛᴏ sᴛᴀʀᴛ ᴏᴠᴇʀ.</blockquote>"
        )
        message.stop_propagation()
        return
    
    # Download the file
    status_msg = await message.reply_text("<blockquote>⬇️ Dᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰɪʟᴇ...</blockquote>")
    
    try:
        # Create merge directory
        if not os.path.exists("MergeFiles"):
            os.makedirs("MergeFiles")
        
        file_path = f"MergeFiles/{user_id}_{len(queue['files'])+1}_{filename}"
        
        dl_path = await client.download_media(
            message=message,
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=("⬇️ Downloading...", status_msg, time.time())
        )
        
        # Add to queue
        queue['files'].append(dl_path)
        queue['filenames'].append(filename)
        
        await status_msg.edit(
            f"<blockquote>✅ <b>Fɪʟᴇ Aᴅᴅᴇᴅ!</b>\n\n"
            f"📂 {filename}\n"
            f"📊 Qᴜᴇᴜᴇ: {len(queue['files'])}/{MAX_MERGE_FILES}\n\n"
            f"Sᴇɴᴅ ᴍᴏʀᴇ ꜰɪʟᴇs ᴏʀ /mergeall ᴛᴏ ᴍᴇʀɢᴇ.</blockquote>"
        )
        
        # Update the pinned status message with current queue
        if queue.get('status_message_id') and queue.get('chat_id'):
            try:
                file_list = "\n".join([f"  {i}. {name}" for i, name in enumerate(queue['filenames'], 1)])
                await client.edit_message_text(
                    chat_id=queue['chat_id'],
                    message_id=queue['status_message_id'],
                    text=f"<blockquote><b>🎬 Mᴇʀɢᴇ Mᴏᴅᴇ Aᴄᴛɪᴠᴇ</b>\n\n"
                         f"📊 <b>Qᴜᴇᴜᴇ:</b> {len(queue['files'])}/{MAX_MERGE_FILES} ꜰɪʟᴇs\n\n"
                         f"<b>Fɪʟᴇs:</b>\n{file_list}\n\n"
                         f"<b>Cᴏᴍᴍᴀɴᴅs:</b>\n"
                         f"• /mergeall - Mᴇʀɢᴇ ᴀʟʟ ꜰɪʟᴇs\n"
                         f"• /exitmerge - Exɪᴛ ᴍᴇʀɢᴇ ᴍᴏᴅᴇ</blockquote>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔗 Mᴇʀɢᴇ Aʟʟ", callback_data="merge_now_btn")],
                        [InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ Mᴇʀɢᴇ", callback_data="cancel_merge_queue")]
                    ])
                )
            except Exception as e:
                print(f"Could not update pinned status: {e}")
        
    except Exception as e:
        await status_msg.edit(f"<blockquote>❌ Dᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ: {e}</blockquote>")
    
    # Stop propagation to prevent other handlers
    message.stop_propagation()


async def do_merge_files(client, message, user_id):

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

    """
    Helper function to perform the actual merge operation.
    Called from both /mergeall command and merge_now_btn callback.
    """
    queue = get_user_merge_queue(user_id)
    files = queue.get('files', [])
    
    if len(files) < 2:
        await message.reply_text(
            "<blockquote>❌ <b>Nᴇᴇᴅ ᴀᴛ ʟᴇᴀsᴛ 2 ꜰɪʟᴇs ᴛᴏ ᴍᴇʀɢᴇ!</b>\n\n"
            f"Cᴜʀʀᴇɴᴛ ǫᴜᴇᴜᴇ: {len(files)} ꜰɪʟᴇ(s)\n\n"
            "Usᴇ /merge ᴛᴏ sᴛᴀʀᴛ ᴄᴏʟʟᴇᴄᴛɪɴɢ ꜰɪʟᴇs.</blockquote>"
        )
        return
    
    # Disable merge mode
    queue['mode'] = False
    
    status_msg = await message.reply_text(
        f"<blockquote>🔄 <b>Mᴇʀɢɪɴɢ {len(files)} ꜰɪʟᴇs...</b>\n\n"
        f"⏳ Pʟᴇᴀsᴇ ᴡᴀɪᴛ...</blockquote>"
    )
    
    try:
        # Create output file
        timestamp = int(time.time())
        output_file = f"MergeFiles/merged_{user_id}_{timestamp}.mp4"
        
        # Progress callback
        async def merge_progress(percentage, status):
            filled = math.floor(percentage / 5)
            progress_bar = ''.join(["⬢" for _ in range(filled)]) + ''.join(["⬡" for _ in range(20 - filled)])
            
            try:
                await status_msg.edit(
                    f"<blockquote><b>🔄 Mᴇʀɢɪɴɢ {len(files)} ꜰɪʟᴇs...</b>\n\n"
                    f"{progress_bar}\n\n"
                    f"✘ Dᴏɴᴇ: {percentage:.1f}%\n"
                    f"✘ {status}</blockquote>"
                )
            except:
                pass
        
        # Merge videos
        success = await merge_videos(files, output_file, merge_progress)
        
        if not success or not os.path.exists(output_file):
            await status_msg.edit("<blockquote>❌ <b>Mᴇʀɢᴇ ꜰᴀɪʟᴇᴅ!</b>\n\nVɪᴅᴇᴏ ꜰᴏʀᴍᴀᴛs ᴍᴀʏ ɴᴏᴛ ʙᴇ ᴄᴏᴍᴘᴀᴛɪʙʟᴇ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.</blockquote>")
            clear_user_merge_queue(user_id)
            return
        
        # Store merged file path
        queue['merged_file'] = output_file
        queue['pending_upload'] = True
        queue['file_count'] = len(files)
        
        # Clean up source files now
        for f in queue.get('files', []):
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass
        queue['files'] = []
        
        # Get file size
        file_size = os.path.getsize(output_file)
        duration = int(await get_video_duration(output_file))
        queue['duration'] = duration
        queue['file_size'] = file_size
        
        # Ask for rename option
        await status_msg.edit(
            f"<blockquote>✅ <b>Mᴇʀɢᴇ Cᴏᴍᴘʟᴇᴛᴇ!</b>\n\n"
            f"📊 Fɪʟᴇs ᴍᴇʀɢᴇᴅ: {queue['file_count']}\n"
            f"📦 Sɪᴢᴇ: {humanbytes(file_size)}\n"
            f"⏱️ Dᴜʀᴀᴛɪᴏɴ: {duration}s\n\n"
            f"<b>Wᴀɴᴛ ᴛᴏ ʀᴇɴᴀᴍᴇ ᴛʜᴇ ꜰɪʟᴇ?</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ Rᴇɴᴀᴍᴇ", callback_data="merge_rename")],
                [InlineKeyboardButton("⏩ Sᴋɪᴘ (Uᴘʟᴏᴀᴅ Nᴏᴡ)", callback_data="merge_skip_rename")]
            ])
        )
        
    except Exception as e:
        print(f"Merge error: {e}")
        import traceback
        traceback.print_exc()
        await status_msg.edit(f"<blockquote>❌ <b>Eʀʀᴏʀ:</b> {str(e)}</blockquote>")
        clear_user_merge_queue(user_id)


@Client.on_message(filters.private & filters.command("mergeall"))
async def merge_all_files(client, message: Message):
    """Merge all collected video files - Step 1: Merge and show rename option - PREMIUM ONLY"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    # Premium check
    if not await check_premium_access(client, message, user_id):
        return
    
    # Use the helper function
    await do_merge_files(client, message, user_id)


@Client.on_callback_query(filters.regex("^merge_rename$"))
async def merge_rename_callback(client, query):
    """Handle rename button - ask for new filename"""
    user_id = query.from_user.id
    queue = get_user_merge_queue(user_id)
    
    if not queue.get('pending_upload') or not queue.get('merged_file'):
        await query.answer("❌ No merged file pending!", show_alert=True)
        return
    
    await query.message.edit(
        "<blockquote><b>✏️ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ</b>\n\n"
        "Rᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴇ ɴᴇᴡ ꜰɪʟᴇɴᴀᴍᴇ (ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ):\n\n"
        "Exᴀᴍᴘʟᴇ: `My_Merged_Video.mp4`</blockquote>",
        reply_markup=ForceReply(True)
    )


@Client.on_callback_query(filters.regex("^merge_skip_rename$"))
async def merge_skip_rename_callback(client, query):
    """Handle skip rename - show media type selection"""
    user_id = query.from_user.id
    queue = get_user_merge_queue(user_id)
    
    if not queue.get('pending_upload') or not queue.get('merged_file'):
        await query.answer("❌ No merged file pending!", show_alert=True)
        return
    
    # Check if user has saved media preference
    saved_media_type = await roxy_bot.get_media_type(user_id)
    
    if saved_media_type:
        # Use saved preference - upload directly
        await query.message.edit("<blockquote>📤 <b>Uᴘʟᴏᴀᴅɪɴɢ ᴍᴇʀɢᴇᴅ ᴠɪᴅᴇᴏ...</b></blockquote>")
        await upload_merged_video(client, query.message, user_id, saved_media_type)
    else:
        # Show media type selection
        await query.message.edit(
            "<blockquote><b>🎬 Sᴇʟᴇᴄᴛ Oᴜᴛᴘᴜᴛ Tyᴘᴇ</b>\n\n"
            "Cʜᴏᴏsᴇ ʜᴏᴡ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ᴍᴇʀɢᴇᴅ ᴠɪᴅᴇᴏ:</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="merge_upload_document")],
                [InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data="merge_upload_video")]
            ])
        )


@Client.on_callback_query(filters.regex("^merge_upload_(document|video)$"))
async def merge_upload_type_callback(client, query):
    """Handle media type selection and upload"""
    user_id = query.from_user.id
    media_type = query.data.split("_")[2]  # document or video
    
    await query.message.edit("<blockquote>📤 <b>Uᴘʟᴏᴀᴅɪɴɢ ᴍᴇʀɢᴇᴅ ᴠɪᴅᴇᴏ...</b></blockquote>")
    await upload_merged_video(client, query.message, user_id, media_type)


@Client.on_message(filters.private & filters.reply, group=6)
async def handle_merge_rename_reply(client, message: Message):
    """Handle reply for merge rename"""
    user_id = message.from_user.id
    queue = get_user_merge_queue(user_id)
    
    # Check if this is a rename reply for merge
    if not queue.get('pending_upload') or not queue.get('merged_file'):
        return  # Not a merge rename reply
    
    reply_msg = message.reply_to_message
    if not reply_msg or not reply_msg.reply_markup:
        return
    if not isinstance(reply_msg.reply_markup, ForceReply):
        return
    
    # Get new filename
    new_name = message.text.strip()
    if not new_name:
        await message.reply_text("<blockquote>❌ Pʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ꜰɪʟᴇɴᴀᴍᴇ!</blockquote>")
        return
    
    # Add .mp4 if no extension
    if not "." in new_name:
        new_name += ".mp4"
    
    queue['new_filename'] = new_name
    
    await message.delete()
    
    # Check if user has saved media preference
    saved_media_type = await roxy_bot.get_media_type(user_id)
    
    if saved_media_type:
        # Use saved preference - upload directly
        try:
            await reply_msg.edit("<blockquote>📤 <b>Uᴘʟᴏᴀᴅɪɴɢ ᴍᴇʀɢᴇᴅ ᴠɪᴅᴇᴏ...</b></blockquote>")
            status_msg = reply_msg
        except:
            # ForceReply message can't be edited, send new one
            try:
                await reply_msg.delete()
            except:
                pass
            status_msg = await client.send_message(message.chat.id, "<blockquote>📤 <b>Uᴘʟᴏᴀᴅɪɴɢ ᴍᴇʀɢᴇᴅ ᴠɪᴅᴇᴏ...</b></blockquote>")
        await upload_merged_video(client, status_msg, user_id, saved_media_type, new_name)
    else:
        # Show media type selection
        try:
            await reply_msg.edit(
                f"<blockquote><b>🎬 Sᴇʟᴇᴄᴛ Oᴜᴛᴘᴜᴛ Tyᴘᴇ</b>\n\n"
                f"📝 Fɪʟᴇɴᴀᴍᴇ: <code>{new_name}</code>\n\n"
                f"Cʜᴏᴏsᴇ ʜᴏᴡ ᴛᴏ ᴜᴘʟᴏᴀᴅ:</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="merge_upload_document")],
                    [InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data="merge_upload_video")]
                ])
            )
        except:
            # ForceReply message can't be edited, send new one
            try:
                await reply_msg.delete()
            except:
                pass
            await client.send_message(
                message.chat.id,
                f"<blockquote><b>🎬 Sᴇʟᴇᴄᴛ Oᴜᴛᴘᴜᴛ Tyᴘᴇ</b>\n\n"
                f"📝 Fɪʟᴇɴᴀᴍᴇ: <code>{new_name}</code>\n\n"
                f"Cʜᴏᴏsᴇ ʜᴏᴡ ᴛᴏ ᴜᴘʟᴏᴀᴅ:</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="merge_upload_document")],
                    [InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data="merge_upload_video")]
                ])
            )
    
    message.stop_propagation()


async def upload_merged_video(client, status_msg, user_id, media_type, new_filename=None):
    """Upload the merged video with specified media type"""
    queue = get_user_merge_queue(user_id)
    
    if not queue.get('merged_file') or not os.path.exists(queue['merged_file']):
        await status_msg.edit("<blockquote>❌ Mᴇʀɢᴇᴅ ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ!</blockquote>")
        clear_user_merge_queue(user_id)
        return
    
    output_file = queue['merged_file']
    file_size = queue.get('file_size', os.path.getsize(output_file))
    duration = queue.get('duration', 0)
    file_count = queue.get('file_count', 0)
    
    # Use new filename or default
    display_name = new_filename or queue.get('new_filename') or f"merged_{user_id}.mp4"
    
    # Rename file if new name provided
    if new_filename or queue.get('new_filename'):
        new_path = os.path.join(os.path.dirname(output_file), display_name)
        try:
            os.rename(output_file, new_path)
            output_file = new_path
            queue['merged_file'] = new_path
        except:
            pass
    
    try:
        # Get user's thumbnail
        user_data = await roxy_bot.get_user_data(user_id)
        c_thumb = user_data.get('file_id', None) if user_data else None
        
        ph_path = None
        if c_thumb:
            try:
                ph_path = await client.download_media(c_thumb)
                if ph_path and os.path.exists(ph_path):
                    Image.open(ph_path).convert("RGB").save(ph_path)
                    img = Image.open(ph_path)
                    img.resize((320, 320))
                    img.save(ph_path, "JPEG")
            except Exception as e:
                print(f"Thumbnail error: {e}")
                ph_path = None
        
        # Caption
        caption = f"<blockquote><b>🎬 {display_name}</b>\n\n📊 Files: {file_count}\n📦 Size: {humanbytes(file_size)}</blockquote>"
        
        # Check for dump channel
        dump_channel = await roxy_bot.get_dump_channel(user_id)
        target_chat = dump_channel if dump_channel else status_msg.chat.id
        
        # Upload based on media type
        if media_type == "document":
            await client.send_document(
                target_chat,
                document=output_file,
                caption=caption,
                thumb=ph_path,
                file_name=display_name,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", status_msg, time.time())
            )
        else:  # video
            await client.send_video(
                target_chat,
                video=output_file,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                file_name=display_name,
                progress=progress_for_pyrogram,
                progress_args=("📤 Uploading...", status_msg, time.time())
            )
        
        # Success message
        if dump_channel:
            try:
                chat = await client.get_chat(dump_channel)
                await status_msg.edit(
                    f"<blockquote>✅ <b>Uᴘʟᴏᴀᴅ Cᴏᴍᴘʟᴇᴛᴇ!</b>\n\n"
                    f"📝 Fɪʟᴇ: <code>{display_name}</code>\n"
                    f"📦 Sɪᴢᴇ: {humanbytes(file_size)}\n"
                    f"🎬 Tyᴘᴇ: {media_type.title()}\n"
                    f"📺 Dᴜᴍᴘᴇᴅ ᴛᴏ: <b>{chat.title}</b></blockquote>"
                )
            except:
                await status_msg.edit(f"<blockquote>✅ <b>Uᴘʟᴏᴀᴅ Cᴏᴍᴘʟᴇᴛᴇ!</b>\n\n📝 Fɪʟᴇ: <code>{display_name}</code>\n📦 Sɪᴢᴇ: {humanbytes(file_size)}</blockquote>")
        else:
            await status_msg.edit(
                f"<blockquote>✅ <b>Uᴘʟᴏᴀᴅ Cᴏᴍᴘʟᴇᴛᴇ!</b>\n\n"
                f"📝 Fɪʟᴇ: <code>{display_name}</code>\n"
                f"📦 Sɪᴢᴇ: {humanbytes(file_size)}\n"
                f"🎬 Tyᴘᴇ: {media_type.title()}</blockquote>"
            )
        
        # Cleanup
        try:
            if ph_path and os.path.exists(ph_path):
                os.remove(ph_path)
        except:
            pass
        
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        await status_msg.edit(f"<blockquote>❌ <b>Uᴘʟᴏᴀᴅ Eʀʀᴏʀ:</b> {str(e)}</blockquote>")
    
    # Clear queue
    clear_user_merge_queue(user_id)

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
