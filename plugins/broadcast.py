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

# extra imports
from config import Config
from helper.database import roxy_bot
from helper.utils import send_reaction
import time, asyncio, logging, datetime, traceback

# pyrogram imports
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@Client.on_message(filters.private & filters.command("broadcast") & filters.user(Config.ADMIN))
async def broadcast_handler(bot: Client, m: Message):
    print(f"[DEBUG] Broadcast received from: {m.from_user.id}")
    
    # Step 1: React
    try:
        await send_reaction(bot, m)
    except:
        pass
    
    # Step 2: Determine what to broadcast
    if m.reply_to_message:
        print("[DEBUG] Broadcast type: Reply")
        broadcast_msg = m.reply_to_message
    elif m.media:
        print("[DEBUG] Broadcast type: Media (Command message)")
        # If command has media (pasted image/file), broadcast the message itself
        broadcast_msg = m
    elif m.command and len(m.command) > 1:
        print("[DEBUG] Broadcast type: Text (Command message)")
        # If command has text suffix (e.g., /broadcast Hello), broadcast the message itself
        broadcast_msg = m
    else:
        print("[DEBUG] Broadcast rejected: No content")
        # If just "/broadcast" with no reply and no other content, fail.
        return await m.reply_text("<blockquote><b>⚠️ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ sᴇɴᴅ ᴍᴇᴅɪᴀ ᴡɪᴛʜ /broadcast ᴄᴏᴍᴍᴀɴᴅ.</b></blockquote>")
    
    # Step 3: Send initializing message
    print("[DEBUG] Sending initializing message...")
    sts_msg = await m.reply_text("<blockquote>Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴɪᴛɪᴀʟɪᴢɪɴɢ...</blockquote>")
    
    try:
        # Step 4: Log to channel if configured
        if Config.LOG_CHANNEL:
            try:
                await bot.send_message(
                    Config.LOG_CHANNEL, 
                    f"{m.from_user.mention} (ID: {m.from_user.id}) started broadcast..."
                )
            except:
                pass
        
        # Step 5: Get user count and list
        print("[DEBUG] Fetching user count...")
        total_users = await roxy_bot.total_users_count()
        print(f"[DEBUG] Total users: {total_users}")
        await sts_msg.edit(f"<blockquote>Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ! Tᴏᴛᴀʟ Uꜱᴇʀꜱ: {total_users}</blockquote>")
        
        all_users = await roxy_bot.get_all_users()
        
        # Step 6: Broadcast to all users
        done = 0
        failed = 0
        success = 0

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

        start_time = time.time()
        
        # Get bot ID to skip self
        bot_id = bot.me.id
        
        print("[DEBUG] Starting broadcast loop...")
        async for user in all_users:
            user_id = int(user['_id'])
            
            # Skip broadcasting to bot itself
            if user_id == bot_id:
                continue
                
            try:
                sts = await send_msg(user_id, broadcast_msg)
                if sts == 200:
                    success += 1
                else:
                    failed += 1
                if sts == 400:
                    await roxy_bot.delete_user(user_id)
                done += 1
                
                # Update progress every 20 users
                if done % 20 == 0:
                    await sts_msg.edit(
                        f"<blockquote>Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ:\n"
                        f"Tᴏᴛᴀʟ: {total_users}\n"
                        f"Cᴏᴍᴩʟᴇᴛᴇᴅ: {done}/{total_users}\n"
                        f"Sᴜᴄᴄᴇꜱꜱ: {success}\n"
                        f"Fᴀɪʟᴇᴅ: {failed}</blockquote>"
                    )
            except Exception as e:
                logger.error(f"Error broadcasting to user {user_id}: {e}")
                print(f"[DEBUG] Loop Error on user {user_id}: {e}")
                failed += 1
                done += 1
        
        # Step 7: Send completion message
        completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
        print(f"[DEBUG] Broadcast completed in {completed_in}")
        await sts_msg.edit(
            f"<blockquote>✅ Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ!\n"
            f"Tɪᴍᴇ: {completed_in}\n\n"
            f"Tᴏᴛᴀʟ: {total_users}\n"
            f"Sᴜᴄᴄᴇꜱꜱ: {success}\n"
            f"Fᴀɪʟᴇᴅ: {failed}</blockquote>"
        )
        
    except Exception as e:
        logger.error(f"Broadcast error: {e}")
        print(f"[DEBUG] Critical Broadcast Error: {e}")
        traceback.print_exc()
        await sts_msg.edit(f"<blockquote><b>❌ Eʀʀᴏʀ:</b> {str(e)}</blockquote>")


async def send_msg(user_id, message):
    """Send message to a single user"""
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        print(f"[DEBUG] User {user_id} Deactivated")
        return 400
    except UserIsBlocked:
        print(f"[DEBUG] User {user_id} Blocked Bot")
        return 400
    except PeerIdInvalid:
        print(f"[DEBUG] User {user_id} PeerIdInvalid")
        return 400
    except Exception as e:
        print(f"[DEBUG] Error sending to {user_id}: {e}")
        return 500

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
