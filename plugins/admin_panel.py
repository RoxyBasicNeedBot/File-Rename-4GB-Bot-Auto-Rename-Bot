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
from helper.utils import get_seconds, humanbytes, send_reaction
import os, sys, time, asyncio, logging, datetime, pytz, traceback

# pyrogram imports
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    await send_reaction(bot, message)
    total_users = await roxy_bot.total_users_count()
    if bot.premium:
        total_premium_users = await roxy_bot.total_premium_users_count()
    else:
        total_premium_users = "Disabled ✅"
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))    
    start_t = time.time()
    roxy = await message.reply('<blockquote>**ᴘʀᴏᴄᴇssɪɴɢ.....**</blockquote>')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await roxy.edit(text=f"<blockquote>**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`\n**💸 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs:** `{total_premium_users}`</blockquote>")

# bot logs process 
@Client.on_message(filters.command('logs') & filters.user(Config.ADMIN))
async def log_file(b, m):
    await send_reaction(b, m)
    try:
        await m.reply_document('BotLog.txt')
    except Exception as e:
        await m.reply(str(e))

@Client.on_message(filters.command(["addpremium", "add_premium"]) & filters.user(Config.ADMIN))
async def add_premium(client, message):
    await send_reaction(client, message)
    if not client.premium:
        return await message.reply_text("<blockquote>premium mode disabled ✅</blockquote>")
    
    # Simple format: /add_premium user_id days gb
    if len(message.command) < 4:
        return await message.reply_text(
            "<blockquote><b>📋 Usage:</b> /add_premium user_id days gb\n\n"
            "<b>Example:</b>\n"
            "<code>/add_premium 123456789 30 10</code>\n"
            "↳ Gives user 30 days premium with 10GB daily limit\n\n"
            "<code>/add_premium 123456789 7 50</code>\n"
            "↳ Gives user 7 days premium with 50GB daily limit</blockquote>", 
            quote=True
        )

    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
        gb_limit = int(message.command[3])
    except ValueError:
        return await message.reply_text(
            "<blockquote>❌ Invalid input! All values must be numbers.\n\n"
            "<b>Usage:</b> /add_premium user_id days gb</blockquote>", 
            quote=True
        )

    if days <= 0:
        return await message.reply_text("<blockquote>❌ Days must be greater than 0!</blockquote>", quote=True)
    
    if gb_limit <= 0:
        return await message.reply_text("<blockquote>❌ GB limit must be greater than 0!</blockquote>", quote=True)

    try:
        user = await client.get_users(user_id)
    except Exception as e:
        return await message.reply_text(f"<blockquote>❌ User not found: {e}</blockquote>", quote=True)

    # Calculate expiry time and limit in bytes
    time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p")
    
    expiry_time = datetime.datetime.now() + datetime.timedelta(days=days)
    limit_bytes = gb_limit * 1024 * 1024 * 1024  # Convert GB to bytes

    # Save to database
    user_data = {"id": user_id, "expiry_time": expiry_time}
    await roxy_bot.add_premium(user_id, user_data, limit_bytes, "Premium")

    # Get expiry formatted
    expiry_str_in_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")

    # Send confirmation to admin
    await message.reply_text(
        f"<blockquote>✅ <b>Pʀᴇᴍɪᴜᴍ Aᴅᴅᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n"
        f"👤 <b>Usᴇʀ:</b> {user.mention}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"📅 <b>Dᴜʀᴀᴛɪᴏɴ:</b> <code>{days} days</code>\n"
        f"📦 <b>Dᴀɪʟʏ Lɪᴍɪᴛ:</b> <code>{gb_limit} GB</code>\n\n"
        f"⏳ <b>Jᴏɪɴɪɴɢ:</b> {current_time}\n\n"
        f"⌛️ <b>Exᴘɪʀʏ:</b> {expiry_str_in_ist}</blockquote>", 
        quote=True, 
        disable_web_page_preview=True
    )

    # Notify the user
    try:
        await client.send_message(
            chat_id=user_id,
            text=f"<blockquote>🎉 <b>Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs {user.mention}!</b>\n\n"
                 f"✨ Yᴏᴜ ɴᴏᴡ ʜᴀᴠᴇ <b>Premium Access!</b>\n\n"
                 f"📅 <b>Dᴜʀᴀᴛɪᴏɴ:</b> <code>{days} days</code>\n"
                 f"📦 <b>Dᴀɪʟʏ Lɪᴍɪᴛ:</b> <code>{gb_limit} GB</code>\n\n"
                 f"⏳ <b>Jᴏɪɴɪɴɢ:</b> {current_time}\n\n"
                 f"⌛️ <b>Exᴘɪʀʏ:</b> {expiry_str_in_ist}\n\n"
                 f"Eɴᴊᴏʏ! 🚀</blockquote>", 
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Could not notify user {user_id}: {e}")



@Client.on_message(filters.command(["removepremium", "remove_premium"]) & filters.user(Config.ADMIN))
async def remove_premium(bot, message):
    await send_reaction(bot, message)
    if not bot.premium:
        return await message.reply_text("<blockquote>premium mode disabled ✅</blockquote>")
     
    if len(message.command) == 2:
        try:
            user_id = int(message.command[1])  # Convert the user_id to integer
            user = await bot.get_users(user_id)
            
            if await roxy_bot.has_premium_access(user_id):
                await roxy_bot.remove_premium(user_id)
                
                # Send confirmation to admin
                await message.reply_text(
                    f"<blockquote>✅ <b>Pʀᴇᴍɪᴜᴍ Rᴇᴍᴏᴠᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n"
                    f"👤 <b>Usᴇʀ:</b> {user.mention}\n"
                    f"🆔 <b>ID:</b> <code>{user_id}</code></blockquote>",
                    quote=True
                )
                
                # Notify the user
                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"<blockquote><b>ʜᴇʏ {user.mention},</b>\n\n"
                             f"❌ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.\n\n"
                             f"ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʟᴀɴ ʜᴇʀᴇ 👉 /myplan</blockquote>"
                    )
                except Exception as e:
                    print(f"Could not notify user {user_id}: {e}")
            else:
                await message.reply_text(
                    "<blockquote>❌ <b>Uɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ!</b>\n\n"
                    "Tʜɪs ᴜsᴇʀ ᴅᴏᴇs ɴᴏᴛ ʜᴀᴠᴇ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ.</blockquote>",
                    quote=True
                )
        except ValueError:
            await message.reply_text("<blockquote>❌ Iɴᴠᴀʟɪᴅ ᴜsᴇʀ ID!</blockquote>", quote=True)
        except Exception as e:
            await message.reply_text(f"<blockquote>❌ Eʀʀᴏʀ: {str(e)}</blockquote>", quote=True)
    else:
        await message.reply_text("<blockquote>ᴜsᴀɢᴇ: /remove_premium ᴜsᴇʀ_ɪᴅ</blockquote>", quote=True)


# Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await send_reaction(b, m)
    roxy = await b.send_message(text="<blockquote>**🔄 ᴘʀᴏᴄᴇssᴇs sᴛᴏᴘᴘᴇᴅ. ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛɪɴɢ.....**</blockquote>", chat_id=m.chat.id)
    failed = 0
    success = 0
    deactivated = 0
    blocked = 0
    start_time = time.time()
    total_users = await roxy_bot.total_users_count()
    all_users = await roxy_bot.get_all_users()
    async for user in all_users:
        try:
            restart_msg = f"<blockquote>ʜᴇʏ, {(await b.get_users(user['_id'])).mention}\n\n**🔄 ᴘʀᴏᴄᴇssᴇs sᴛᴏᴘᴘᴇᴅ. ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛɪɴɢ.....\n\n✅️ ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ. ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ.**</blockquote>"
            await b.send_message(user['_id'], restart_msg)
            success += 1
        except InputUserDeactivated:
            deactivated +=1
            await roxy_bot.delete_user(user['_id'])
        except UserIsBlocked:
            blocked +=1
            await roxy_bot.delete_user(user['_id'])
        except Exception as e:
            failed += 1
            await roxy_bot.delete_user(user['_id'])
            print(e)
            pass
        try:
            await roxy.edit(f"<blockquote><u>ʀᴇsᴛᴀʀᴛ ɪɴ ᴩʀᴏɢʀᴇꜱꜱ:</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}</blockquote>")
        except FloodWait as e:
            await asyncio.sleep(e.value)
    completed_restart = datetime.timedelta(seconds=int(time.time() - start_time))
    await roxy.edit(f"<blockquote>ᴄᴏᴍᴘʟᴇᴛᴇᴅ ʀᴇsᴛᴀʀᴛ: {completed_restart}\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}</blockquote>")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.ADMIN))
async def ban(c: Client, m: Message):
    await send_reaction(c, m)
    if len(m.command) == 1:
        await m.reply_text(
            f"<blockquote>Use this command to ban any user from the bot.\n\n"
            f"Usage:\n\n"
            f"`/ban user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban 1234567 28 You misused me.`\n"
            f"This will ban user with id `1234567` for `28` days for the reason `You misused me`.</blockquote>",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(user_id,              
                f"<blockquote><b>Sorry Sir, 😔 You are Banned!..</b>\n\n"
                f"📝 <b>Reason:</b> {ban_reason}\n\n"
                f"📞 <b>Please Contact - @roxycontactbot</b></blockquote>",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📞 Contact Support", url="https://t.me/roxycontactbot")
                ]])
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await roxy_bot.ban_user(user_id, ban_duration, ban_reason)
        await m.reply_text(f"<blockquote>{ban_log_text}</blockquote>", quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"<blockquote>Error occoured! Traceback given below\n\n`{traceback.format_exc()}`</blockquote>",
            quote=True
        )


@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.ADMIN))
async def unban(c: Client, m: Message):
    await send_reaction(c, m)
    if len(m.command) == 1:
        await m.reply_text(
            f"<blockquote>Use this command to unban any user.\n\n"
            f"Usage:\n\n`/unban user_id`\n\n"
            f"Eg: `/unban 1234567`\n"
            f"This will unban user with id `1234567`.</blockquote>",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(user_id, f"<blockquote>Your ban was lifted!</blockquote>")
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await roxy_bot.remove_ban(user_id)
        await m.reply_text(f"<blockquote>{unban_log_text}</blockquote>", quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"<blockquote>Error occurred! Traceback given below\n\n`{traceback.format_exc()}`</blockquote>",
            quote=True
        )


@Client.on_message(filters.private & filters.command("banned_users") & filters.user(Config.ADMIN))
async def _banned_users(client, m: Message):
    await send_reaction(client, m)
    all_banned_users = await roxy_bot.get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"<blockquote>Total banned user(s): `{banned_usr_count}`\n\n{text}</blockquote>"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)

     

 


@Client.on_message(filters.private & filters.command(["premium_list", "premiumlist"]) & filters.user(Config.ADMIN))
async def premium_list(client, m: Message):
    await send_reaction(client, m)
    if not client.premium:
        return await m.reply_text("<blockquote>premium mode disabled ✅</blockquote>")
    
    processing_msg = await m.reply_text("<blockquote>**🔄 Fetching premium users...**</blockquote>", quote=True)
    
    all_premium_users = await roxy_bot.get_all_premium_users()
    premium_usr_count = 0
    text = ''
    
    async for premium_user in all_premium_users:
        user_id = premium_user.get('id')
        expiry_time = premium_user.get('expiry_time')
        has_free_trial = premium_user.get('has_free_trial', False)
        
        # Try to get user info
        try:

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

            user = await client.get_users(user_id)
            user_name = user.first_name if user.first_name else "Unknown"
            user_mention = user.mention
        except:
            user_name = "Unknown"
            user_mention = f"[User](tg://user?id={user_id})"
        
        # Get upload limit
        user_data = await roxy_bot.get_user_data(user_id)
        upload_limit = user_data.get('uploadlimit', 0) if user_data else 0
        limit_gb = round(upload_limit / (1024 * 1024 * 1024), 1) if upload_limit else 0
        
        # Format expiry time
        if expiry_time:
            time_left = expiry_time - datetime.datetime.now()
            if time_left.total_seconds() > 0:
                days = time_left.days
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                time_left_str = f"{days}d {hours}h {minutes}m"
            else:
                time_left_str = "Expired"
            expiry_str = expiry_time.strftime("%d-%m-%Y %I:%M %p")
        else:
            expiry_str = "N/A"
            time_left_str = "N/A"
        
        plan_type = "Trial" if has_free_trial else "Premium"
        
        premium_usr_count += 1
        text += f"**{premium_usr_count}.** {user_mention}\n"
        text += f"   ├ **ID:** `{user_id}`\n"
        text += f"   ├ **Plan:** `{plan_type}`\n"
        text += f"   ├ **Daily Limit:** `{limit_gb} GB`\n"
        text += f"   ├ **Expiry:** `{expiry_str}`\n"
        text += f"   └ **Time Left:** `{time_left_str}`\n\n"
    
    if premium_usr_count == 0:
        reply_text = "<blockquote>**📋 Premium Users List**\n\n❌ No premium users found!</blockquote>"
    else:
        reply_text = f"<blockquote>**📋 Premium Users List**\n\n**Total Premium Users:** `{premium_usr_count}`\n\n{text}</blockquote>"
    
    await processing_msg.delete()
    
    if len(reply_text) > 4096:
        with open('premium-users.txt', 'w') as f:
            f.write(reply_text.replace('<blockquote>', '').replace('</blockquote>', '').replace('**', '').replace('`', ''))
        await m.reply_document('premium-users.txt', True, caption=f"<blockquote>**📋 Total Premium Users:** `{premium_usr_count}`</blockquote>")
        os.remove('premium-users.txt')
        return
    await m.reply_text(reply_text, True)


# ===== Maintenance Mode Commands =====
@Client.on_message(filters.private & filters.command(["on_maintenance", "maintenance_on"]) & filters.user(Config.ADMIN))
async def enable_maintenance(client, message: Message):
    """Enable maintenance mode"""
    await send_reaction(client, message)
    
    # Get custom message if provided
    custom_msg = None
    if len(message.command) > 1:
        custom_msg = " ".join(message.command[1:])
    
    # Default maintenance message
    default_msg = """🔧 <b>Bᴏᴛ Uɴᴅᴇʀ Mᴀɪɴᴛᴇɴᴀɴᴄᴇ</b>

ʜᴇʏ ʙʀᴏᴛʜᴇʀ, sɪsᴛᴇʀ, ᴀɴᴅ ꜰʀɪᴇɴᴅs! 👋

ᴛʜᴇ ʙᴏᴛ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ɪɴ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ.

ᴡᴇ ᴀʀᴇ ᴀᴅᴅɪɴɢ ɴᴇᴡ ᴇxᴄɪᴛɪɴɢ ꜰᴇᴀᴛᴜʀᴇs ꜰᴏʀ ʏᴏᴜ! 🚀

ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ. ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ʏᴏᴜʀ ᴘᴀᴛɪᴇɴᴄᴇ! 🙏"""
    
    await roxy_bot.set_maintenance_mode(True, custom_msg or default_msg)
    
    await message.reply_text(
        "<blockquote>🔧 <b>Mᴀɪɴᴛᴇɴᴀɴᴄᴇ Mᴏᴅᴇ Eɴᴀʙʟᴇᴅ!</b>\n\n"
        "✅ Aʟʟ ᴜsᴇʀs ᴡɪʟʟ sᴇᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴇssᴀɢᴇ.\n"
        "✅ Oɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ.\n\n"
        "Tᴏ ᴅɪsᴀʙʟᴇ: /off_maintenance</blockquote>",
        quote=True
    )


@Client.on_message(filters.private & filters.command(["off_maintenance", "maintenance_off"]) & filters.user(Config.ADMIN))
async def disable_maintenance(client, message: Message):
    """Disable maintenance mode"""
    await send_reaction(client, message)
    
    await roxy_bot.set_maintenance_mode(False)
    
    await message.reply_text(
        "<blockquote>✅ <b>Mᴀɪɴᴛᴇɴᴀɴᴄᴇ Mᴏᴅᴇ Dɪsᴀʙʟᴇᴅ!</b>\n\n"
        "Aʟʟ ᴜsᴇʀs ᴄᴀɴ ɴᴏᴡ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ ɴᴏʀᴍᴀʟʟʏ. 🎉</blockquote>",
        quote=True
    )


# ===== Top Uploaders Command =====
@Client.on_message(filters.private & filters.command("use") & filters.user(Config.ADMIN))
async def top_uploaders_12h(client, message: Message):
    """
    Show top uploaders in last 12 hours.
    Usage:
      /use          — Show top 10 uploaders in last 12 hours
      /use user_id  — Show specific user's 12hr usage + daily limit info
    """
    await send_reaction(client, message)
    
    processing_msg = await message.reply_text(
        "<blockquote>🔄 <b>Fᴇᴛᴄʜɪɴɢ ᴜsᴀɢᴇ ᴅᴀᴛᴀ...</b></blockquote>",
        quote=True
    )
    
    try:
        # ── Single user lookup: /use user_id ──
        if len(message.command) >= 2:
            try:
                target_user_id = int(message.command[1])
            except ValueError:
                await processing_msg.edit(
                    "<blockquote>❌ Invalid user ID! Usage: <code>/use user_id</code></blockquote>"
                )
                return
            
            # Get user info
            try:
                target_user = await client.get_users(target_user_id)
                user_mention = target_user.mention
            except:
                user_mention = f"<code>{target_user_id}</code>"
            
            # Get 12hr upload activity from activity collection
            user_activity = await roxy_bot.get_user_uploads(target_user_id, hours=12)
            upload_count_12h = user_activity.get('upload_count', 0)
            upload_size_12h = user_activity.get('total_size', 0)
            
            # Get daily limit info from user data
            user_data = await roxy_bot.get_user_data(target_user_id)
            daily_limit = user_data.get('uploadlimit', 0) if user_data else 0
            used_limit = user_data.get('used_limit', 0) if user_data else 0
            usertype = user_data.get('usertype', 'Free') if user_data else 'Free'
            remain = max(0, int(daily_limit) - int(used_limit))
            
            # Premium status
            is_premium = await roxy_bot.has_premium_access(target_user_id)
            premium_status = "✅ Active" if is_premium else "❌ No"
            
            await processing_msg.edit(
                f"<blockquote>📊 <b>Usᴇʀ Usᴀɢᴇ Rᴇᴘᴏʀᴛ</b>\n\n"
                f"👤 <b>User:</b> {user_mention}\n"
                f"🆔 <b>ID:</b> <code>{target_user_id}</code>\n"
                f"💎 <b>Premium:</b> {premium_status}\n"
                f"📋 <b>Plan:</b> <code>{usertype}</code>\n\n"
                f"━━ <b>Lᴀsᴛ 12 Hᴏᴜʀs</b> ━━\n"
                f"📤 <b>Uploads:</b> <code>{upload_count_12h}</code>\n"
                f"📦 <b>Size:</b> <code>{humanbytes(upload_size_12h)}</code>\n\n"
                f"━━ <b>Dᴀɪʟʏ Lɪᴍɪᴛ</b> ━━\n"
                f"📊 <b>Limit:</b> <code>{humanbytes(daily_limit)}</code>\n"
                f"📈 <b>Used:</b> <code>{humanbytes(used_limit)}</code>\n"
                f"📉 <b>Remain:</b> <code>{humanbytes(remain)}</code></blockquote>"
            )
            return
        
        # ── Default: top 10 uploaders in last 12 hours ──
        top_users = await roxy_bot.get_top_uploaders(hours=12, limit=10)
        
        if not top_users:
            await processing_msg.edit(
                "<blockquote>📊 <b>Tᴏᴘ 10 Uᴘʟᴏᴀᴅᴇʀs (Lᴀsᴛ 12 Hᴏᴜʀs)</b>\n\n"
                "❌ Nᴏ ᴜᴘʟᴏᴀᴅs ɪɴ ᴛʜᴇ ʟᴀsᴛ 12 ʜᴏᴜʀs!</blockquote>"
            )
            return
        
        text = ""
        total_uploads = 0
        total_size = 0
        
        for i, user_data in enumerate(top_users, 1):
            user_id = user_data['user_id']
            upload_count = user_data['upload_count']
            upload_size = user_data['total_size']
            
            total_uploads += upload_count
            total_size += upload_size
            
            # Get daily limit info
            ud = await roxy_bot.get_user_data(user_id)
            daily_limit = ud.get('uploadlimit', 0) if ud else 0
            used_today = ud.get('used_limit', 0) if ud else 0
            
            # Try to get username
            try:
                user = await client.get_users(user_id)
                user_name = user.first_name or "Unknown"
                if len(user_name) > 15:
                    user_name = user_name[:15] + "..."
            except:
                user_name = "Unknown"
            
            size_str = humanbytes(upload_size) if upload_size > 0 else "0 B"
            limit_str = humanbytes(daily_limit) if daily_limit > 0 else "2 GB"
            used_str = humanbytes(used_today) if used_today > 0 else "0 B"
            text += f"{i}. <b>{user_name}</b>\n   ├ 📤 {upload_count} uploads ({size_str})\n   └ 📊 Used: {used_str} / {limit_str}\n\n"
        
        total_size_str = humanbytes(total_size) if total_size > 0 else "0 B"
        
        await processing_msg.edit(
            f"<blockquote>📊 <b>Tᴏᴘ 10 Uᴘʟᴏᴀᴅᴇʀs (Lᴀsᴛ 12 Hᴏᴜʀs)</b>\n\n"
            f"{text}"
            f"━━━━━━━━━━━━━━━\n"
            f"<b>Tᴏᴛᴀʟ:</b> {total_uploads} uploads | {total_size_str}\n\n"
            f"💡 <b>Tip:</b> <code>/use user_id</code> for detailed user report</blockquote>"
        )
        
    except Exception as e:
        print(f"Error fetching top uploaders: {e}")
        import traceback
        traceback.print_exc()
        await processing_msg.edit(
            f"<blockquote>❌ <b>Eʀʀᴏʀ:</b> {str(e)}</blockquote>"
        )


# ===== Current Active Users Command =====
@Client.on_message(filters.private & filters.command("current") & filters.user(Config.ADMIN))
async def current_active_users(client, message: Message):
    """Show all users currently uploading or downloading files"""
    await send_reaction(client, message)
    
    try:
        from plugins.file_rename import user_tasks
        
        if not user_tasks:
            await message.reply_text(
                "<blockquote>📊 <b>Cᴜʀʀᴇɴᴛ Aᴄᴛɪᴠᴇ Usᴇʀs</b>\n\n"
                "❌ Nᴏ ᴀᴄᴛɪᴠᴇ ᴜsᴇʀs ʀɪɢʜᴛ ɴᴏᴡ!</blockquote>",
                quote=True
            )
            return
        
        text = ""
        count = 0
        current_time = time.time()
        
        for user_id, task_info in user_tasks.items():
            if task_info.get('cancelled'):
                continue  # Skip cancelled tasks
            
            count += 1
            task_type = task_info.get('type', 'Unknown')
            start_time = task_info.get('start_time', current_time)
            duration_secs = int(current_time - start_time)
            
            # Format duration
            if duration_secs < 60:
                duration_str = f"{duration_secs}s"
            else:
                mins = duration_secs // 60
                secs = duration_secs % 60
                duration_str = f"{mins}m {secs}s"
            
            # Try to get user name
            try:
                user = await client.get_users(user_id)
                user_name = user.first_name or "Unknown"
                if len(user_name) > 15:
                    user_name = user_name[:15] + "..."
            except:
                user_name = "Unknown"
            
            text += f"{count}. <b>{user_name}</b> (ID: <code>{user_id}</code>)\n"
            text += f"   └ {task_type} - {duration_str}\n\n"
        
        if count == 0:
            await message.reply_text(
                "<blockquote>📊 <b>Cᴜʀʀᴇɴᴛ Aᴄᴛɪᴠᴇ Usᴇʀs</b>\n\n"
                "❌ Nᴏ ᴀᴄᴛɪᴠᴇ ᴜsᴇʀs ʀɪɢʜᴛ ɴᴏᴡ!</blockquote>",
                quote=True
            )
            return
        
        await message.reply_text(
            f"<blockquote>📊 <b>Cᴜʀʀᴇɴᴛ Aᴄᴛɪᴠᴇ Usᴇʀs</b>\n\n"
            f"{text}"
            f"━━━━━━━━━━━━━━━\n"
            f"<b>Tᴏᴛᴀʟ:</b> {count} ᴀᴄᴛɪᴠᴇ ᴜsᴇʀ(s)</blockquote>",
            quote=True
        )
        
    except ImportError:
        await message.reply_text(
            "<blockquote>❌ Cᴏᴜʟᴅ ɴᴏᴛ ʟᴏᴀᴅ ᴛᴀsᴋ ᴛʀᴀᴄᴋᴇʀ!</blockquote>",
            quote=True
        )
    except Exception as e:
        print(f"Error fetching active users: {e}")
        await message.reply_text(
            f"<blockquote>❌ <b>Eʀʀᴏʀ:</b> {str(e)}</blockquote>",
            quote=True
        )


# Global force stop flag
FORCE_STOP_ACTIVE = False
FORCE_STOP_USERS = set()


@Client.on_message(filters.private & filters.command(["forcestop", "force_stop"]) & filters.user(Config.ADMIN))
async def force_stop_all(client, message: Message):
    """Force stop all ongoing processes and notify users"""
    global FORCE_STOP_ACTIVE, FORCE_STOP_USERS
    await send_reaction(client, message)
    
    status_msg = await message.reply_text("<blockquote>🛑 <b>Sᴛᴏᴘᴘɪɴɢ ᴀʟʟ ᴘʀᴏᴄᴇssᴇs...</b></blockquote>")
    
    # Set global force stop flag
    FORCE_STOP_ACTIVE = True
    stopped_count = 0
    
    # Try to clear merge queues
    try:
        from plugins.merge_videos import merge_queues, clear_user_merge_queue
        for user_id in list(merge_queues.keys()):
            if merge_queues[user_id].get('mode') or merge_queues[user_id].get('files'):
                FORCE_STOP_USERS.add(user_id)
                clear_user_merge_queue(user_id)
                stopped_count += 1
                # Notify user
                try:
                    await client.send_message(
                        user_id,
                        "<blockquote>🛑 <b>Pʀᴏᴄᴇss Sᴛᴏᴘᴘᴇᴅ!</b>\n\n"
                        "Bᴏᴛ ɪs ᴜᴘᴅᴀᴛɪɴɢ ᴀɴᴅ ʏᴏᴜʀ ᴘʀᴏᴄᴇss ɪs sᴛᴏᴘᴘᴇᴅ.\n\n"
                        "Tʜᴀɴᴋs ʏᴏᴜ! 🙏</blockquote>"
                    )
                except:
                    pass
    except Exception as e:
        print(f"Error clearing merge queues: {e}")
    
    # Reset force stop flag after a delay
    await asyncio.sleep(5)
    FORCE_STOP_ACTIVE = False
    FORCE_STOP_USERS.clear()
    
    await status_msg.edit(
        f"<blockquote>✅ <b>Fᴏʀᴄᴇ Sᴛᴏᴘ Cᴏᴍᴘʟᴇᴛᴇ!</b>\n\n"
        f"🛑 Sᴛᴏᴘᴘᴇᴅ: <code>{stopped_count}</code> ᴘʀᴏᴄᴇss(ᴇs)\n"
        f"📨 Usᴇʀs ɴᴏᴛɪꜰɪᴇᴅ: <code>{stopped_count}</code></blockquote>"
    )

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
