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
NSFW Content Check Orchestrator for Roxy Rename Bot
- Filename keyword check (instant ban)
- Video frame extraction + API scan (≤200MB, 10 frames)
- URL keyword check
- Ban handling with contact button + message cleanup
"""

import os
import asyncio
import logging
import datetime
import tempfile
import shutil

from config import Config
from helper.content_scanner import content_scanner
from helper.adult_filter import contains_adult_keywords, validate_url_file
from helper.database import roxy_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def is_admin_user(user_id: int) -> bool:
    """Check if user is an admin (bypasses all NSFW checks)"""
    try:
        if user_id in Config.ADMIN:
            return True
    except:
        pass
    return False


async def check_nsfw_filename(filename: str, user_id: int) -> dict:
    """
    Check filename for NSFW keywords.
    Returns: {"safe": bool, "reason": str}
    """
    # Filename NSFW check has been disabled as requested
    return {"safe": True, "reason": "Filename check disabled"}


async def check_nsfw_video_frames(file_path: str, user_id: int) -> dict:
    """
    Extract frames from video (≤200MB) and scan each via NSFW API.
    Returns: {"safe": bool, "reason": str}
    """
    try:
        if await is_admin_user(user_id):
            return {"safe": True, "reason": "Admin bypass"}
        
        # Check file extension
        ext = os.path.splitext(file_path)[1].lower()
        video_extensions = ['.mp4', '.mkv', '.avi', '.webm', '.mov', '.flv', '.wmv', '.3gp', '.m4v']
        if ext not in video_extensions:
            return {"safe": True, "reason": "Not a video file"}
        
        # Check size (≤ 200MB)
        file_size = os.path.getsize(file_path)
        size_limit = Config.NSFW_VIDEO_SIZE_LIMIT
        if file_size > size_limit:
            logger.info(f"⏭️ [NSFW] {os.path.basename(file_path)} > {size_limit // (1024*1024)}MB ({file_size / 1024 / 1024:.1f}MB), skipping scan")
            return {"safe": True, "reason": "File too large for scanning - skipped"}
        
        logger.info(f"🎬 [NSFW] Starting scan: {os.path.basename(file_path)} ({file_size / 1024 / 1024:.1f}MB)")
        
        # Create temp directory for frames
        temp_dir = tempfile.mkdtemp(prefix="nsfw_frames_")
        
        try:
            # Step 1: Get video duration using ffprobe
            probe_cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ]
            
            try:
                proc = await asyncio.create_subprocess_exec(
                    *probe_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
            except asyncio.TimeoutError:
                logger.warning("⚠️ [NSFW] ffprobe timed out")
                return {"safe": True, "reason": "ffprobe timeout - skipped"}
            except FileNotFoundError:
                logger.warning("⚠️ [NSFW] ffprobe not found")
                return {"safe": True, "reason": "ffprobe not available - skipped"}
            
            if proc.returncode != 0:
                logger.warning(f"⚠️ [NSFW] ffprobe failed")
                return {"safe": True, "reason": "ffprobe failed - skipped"}
            
            try:
                duration = float(stdout.decode().strip())
            except (ValueError, AttributeError):
                logger.warning("⚠️ [NSFW] Could not parse duration")
                return {"safe": True, "reason": "Duration parse error - skipped"}
            
            if duration <= 0:
                return {"safe": True, "reason": "Zero duration - skipped"}
            
            logger.info(f"📹 [NSFW] Video duration: {duration:.1f}s")
            
            # Step 2: Extract frames at evenly spaced intervals
            frames_to_extract = Config.NSFW_FRAME_COUNT
            frame_files = []
            
            for i in range(frames_to_extract):
                timestamp = (duration / (frames_to_extract + 1)) * (i + 1)
                frame_path = os.path.join(temp_dir, f"frame_{i}.jpg")
                
                extract_cmd = [
                    'ffmpeg', '-y',
                    '-ss', f'{timestamp:.2f}',
                    '-i', file_path,
                    '-frames:v', '1',
                    '-q:v', '2',
                    '-loglevel', 'error',
                    frame_path
                ]
                
                try:
                    proc = await asyncio.create_subprocess_exec(
                        *extract_cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
                except asyncio.TimeoutError:
                    logger.warning(f"⚠️ [NSFW] ffmpeg timed out extracting frame {i+1}")
                    continue
                except FileNotFoundError:
                    logger.warning("⚠️ [NSFW] ffmpeg not found")
                    return {"safe": True, "reason": "ffmpeg not available - skipped"}
                
                if proc.returncode == 0 and os.path.exists(frame_path) and os.path.getsize(frame_path) > 0:
                    frame_files.append(frame_path)
                    logger.info(f"✅ [NSFW] Frame {i+1}/{frames_to_extract} extracted")
                else:
                    logger.warning(f"⚠️ [NSFW] Frame {i+1} extraction failed")
            
            if not frame_files:

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

                logger.warning("⚠️ [NSFW] No frames extracted")
                return {"safe": True, "reason": "No frames extracted - skipped"}
            
            logger.info(f"📊 [NSFW] Extracted {len(frame_files)}/{frames_to_extract} frames, scanning...")
            
            # Step 3: Scan each frame via NSFW API
            for idx, frame_path in enumerate(frame_files):
                with open(frame_path, 'rb') as f:
                    image_bytes = f.read()
                
                result = await content_scanner.scan_image_bytes(image_bytes)
                logger.info(f"🔍 [NSFW] Frame {idx+1} scan: safe={result['safe']}, reason={result['reason']}")
                
                if not result["safe"]:
                    logger.warning(f"🚫 [NSFW] NSFW DETECTED in frame {idx+1} of {os.path.basename(file_path)}")
                    return {
                        "safe": False,
                        "reason": f"NSFW content detected in video frame {idx+1}: {result['reason']}"
                    }
            
            logger.info(f"✅ [NSFW] Scan complete: {os.path.basename(file_path)} - ALL FRAMES SAFE")
            return {"safe": True, "reason": "All frames safe"}
            
        finally:
            # Clean up temp directory
            try:
                shutil.rmtree(temp_dir)
            except Exception as cleanup_err:
                logger.debug(f"Could not clean temp dir: {cleanup_err}")
                
    except Exception as e:
        logger.error(f"❌ [NSFW] Error scanning video: {e}", exc_info=True)
        return {"safe": True, "reason": "Scan error - allowed"}


async def check_nsfw_url(url: str, user_id: int) -> dict:
    """
    Check URL for NSFW content (keywords in URL + filename).
    Returns: {"safe": bool, "reason": str}
    """
    try:
        if await is_admin_user(user_id):
            return {"safe": True, "reason": "Admin bypass"}
        
        is_safe, reason = await validate_url_file(url)
        if not is_safe:
            logger.warning(f"🚫 NSFW URL detected from user {user_id}: {url[:100]}")
            return {"safe": False, "reason": reason}
        
        return {"safe": True, "reason": "URL is safe"}
    
    except Exception as e:
        logger.error(f"Error checking URL: {e}")
        return {"safe": True, "reason": "Check error - allowed"}


async def handle_nsfw_violation(bot, message, user_id, reason, extra_messages=None):
    """
    Handle NSFW violation: instant ban + log + notify with contact button + delete messages.
    extra_messages: list of additional message objects to delete (e.g. processing msg, user file msg)
    """
    from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    
    try:
        # Detect violation type for logging
        if "video frame" in reason.lower():
            detection_type = "🎬 Video Frame Scan"
        elif "filename" in reason.lower() or "file name" in reason.lower():
            detection_type = "📄 Filename Check"
        elif "url" in reason.lower():
            detection_type = "🔗 URL Check"
        else:
            detection_type = "🔍 Content Scan"
        
        # 1. Ban user in database (permanent = 99999 days)
        await roxy_bot.ban_user(user_id, 99999, f"NSFW: {reason}")
        logger.warning(f"🚫 BANNED user {user_id} for NSFW [{detection_type}]: {reason}")
        
        # 2. Log to LOG_CHANNEL with full details
        if Config.LOG_CHANNEL:
            try:
                user = message.from_user if message and hasattr(message, 'from_user') and message.from_user else None
                if user:
                    user_info = f"👤 <b>User:</b> {user.mention}\n🆔 <b>ID:</b> <code>{user_id}</code>\n📛 <b>Username:</b> @{user.username or 'N/A'}"
                else:
                    user_info = f"🆔 <b>ID:</b> <code>{user_id}</code>"
                
                log_text = (
                    f"<blockquote><b>🚫 NSFW AUTO-BAN</b>\n\n"
                    f"{user_info}\n\n"
                    f"🔎 <b>Detection:</b> {detection_type}\n"
                    f"📝 <b>Reason:</b> {reason}\n\n"
                    f"⏰ <b>Time:</b> {datetime.datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n"
                    f"🔨 <b>Action:</b> Permanent Ban</blockquote>\n\n"
                    f"<blockquote><b><u>⚠️ 18+ Content Strictly Prohibited ⚠️</u></b></blockquote>"
                )
                await bot.send_message(Config.LOG_CHANNEL, log_text)
            except Exception as e:
                logger.error(f"Error logging NSFW ban: {e}")
        
        # 3. Notify user with contact button
        try:
            from config import roxy
            ban_text = roxy.BANNED_TXT.format(reason)
            await bot.send_message(
                user_id,
                ban_text,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📞 Contact Support", url="https://t.me/roxycontactbot")
                ]])
            )
        except Exception as e:
            logger.error(f"Error notifying banned user: {e}")
        
        # 4. Delete the offending message 
        try:
            if message:
                await message.delete()
        except Exception as e:
            logger.debug(f"Could not delete offending message: {e}")
        
        # 5. Delete extra messages (processing msg, user file msg, etc.)
        if extra_messages:
            for msg in extra_messages:
                try:
                    if msg:
                        await msg.delete()
                except:
                    pass
        
        # 6. Try to delete recent bot messages to this user (cleanup)
        try:
            tracked_msgs = await roxy_bot.get_user_bot_messages(user_id)
            if tracked_msgs:
                async for msg_record in tracked_msgs:
                    try:
                        await bot.delete_messages(
                            msg_record['chat_id'],
                            msg_record['message_id']
                        )
                    except:
                        pass
        except Exception as e:
            logger.debug(f"Could not cleanup messages: {e}")
        
    except Exception as e:
        logger.error(f"Error handling NSFW violation: {e}", exc_info=True)

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
