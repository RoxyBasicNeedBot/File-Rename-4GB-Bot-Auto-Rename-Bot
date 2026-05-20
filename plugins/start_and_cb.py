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
import random, asyncio, datetime, pytz, time, psutil, shutil, aiohttp

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery

# bots imports
from helper.database import roxy_bot
from config import Config, roxy
from helper.utils import humanbytes, send_reaction
from helper.stickers import STICKERS
from plugins import __version__ as _bot_version_, __developer__, __database__, __library__, __language__, __programer__
from plugins.file_rename import upload_doc
from plugins.wallhaven_helper import get_random_pic

upgrade_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('💸 Buy Premium ✓', url='https://t.me/roxybasicneedbot1'),
         ],[
        InlineKeyboardButton("🔙 Back", callback_data = "start")
]])

upgrade_trial_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('💸 Buy Premium ✓', url='https://t.me/roxybasicneedbot1'),
         ],[
        InlineKeyboardButton("🔙 Back", callback_data = "start")
]])


@Client.on_message(filters.private & filters.command("free"))
async def free_command(client, message):
    """Send sticker for free users - just sticker, no message"""
    await send_reaction(client, message)
    await client.send_sticker(message.chat.id, STICKERS["free_user"])


@Client.on_message(filters.private & filters.command("features"))
async def features_command(client, message):
    """List all bot features with premium features marked"""
    await send_reaction(client, message)
    
    features_text = """<blockquote><b>✨ Bᴏᴛ Fᴇᴀᴛᴜʀᴇs</b>

<b>📁 Fɪʟᴇ Mᴀɴᴀɢᴇᴍᴇɴᴛ:</b>
• ✏️ Rᴇɴᴀᴍᴇ ꜰɪʟᴇs
• 🔄 Aᴜᴛᴏ Rᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴛᴇᴍᴘʟᴀᴛᴇ
• 📝 Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ
• 🔖 Pʀᴇꜰɪx & Sᴜꜰꜰɪx
• 🖼️ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ
• 💾 Mᴇᴛᴀᴅᴀᴛᴀ Eᴅɪᴛɪɴɢ

<b>📝 Sᴜʙᴛɪᴛʟᴇ Sᴜᴘᴘᴏʀᴛ:</b>
• 🌐 Mᴜʟᴛɪ-Lᴀɴɢᴜᴀɢᴇ Sᴜʙᴛɪᴛʟᴇ Mᴜx
• 📄 Sᴜᴘᴘᴏʀᴛs: .srt, .ass, .ssa, .vtt, .sub
• 🎬 Sᴏꜰᴛ Sᴜʙs (Tᴏɢɢʟᴇᴀʙʟᴇ ɪɴ Pʟᴀʏᴇʀ)
• ⚡ Fᴀsᴛ — Nᴏ Rᴇ-ᴇɴᴄᴏᴅɪɴɢ!

<b>🎬 Mᴇᴅɪᴀ Cᴏɴᴠᴇʀsɪᴏɴ:</b>
• 🎥 MKV ᴛᴏ MP4 Cᴏɴᴠᴇʀᴛ
• 📸 Sᴄʀᴇᴇɴsʜᴏᴛ Gᴇɴᴇʀᴀᴛɪᴏɴ
• 📊 Mᴇᴅɪᴀ Tyᴘᴇ Sᴇʟᴇᴄᴛɪᴏɴ

<b>📺 Cʜᴀɴɴᴇʟ Fᴇᴀᴛᴜʀᴇs:</b>
• 🎯 Dᴜᴍᴘ Cʜᴀɴɴᴇʟ Sᴜᴘᴘᴏʀᴛ
• 📤 Aᴜᴛᴏ Fᴏʀᴡᴀʀᴅ ᴛᴏ Cʜᴀɴɴᴇʟ

<b>📦 Dᴀɪʟʏ Lɪᴍɪᴛ:</b>
• 📊 2GB Fʀᴇᴇ Dᴀɪʟʏ Uᴘʟᴏᴀᴅ
• ♻️ Aᴜᴛᴏ Rᴇsᴇᴛ Eᴠᴇʀʏ 24 Hᴏᴜʀs

<b>💎 Pʀᴇᴍɪᴜᴍ Fᴇᴀᴛᴜʀᴇs:</b>
• 💎 Vɪᴅᴇᴏ Mᴇʀɢᴇ (ᴜᴘ ᴛᴏ 10 ꜰɪʟᴇs)
• 💎 Vɪᴅᴇᴏ Cᴏᴍᴘʀᴇss
• 💎 Vɪᴅᴇᴏ Tʀɪᴍ (Aᴜᴛᴏ & Mᴀɴᴜᴀʟ)
• 💎 Hɪɢʜᴇʀ Uᴘʟᴏᴀᴅ Lɪᴍɪᴛs
• 💎 Pʀɪᴏʀɪᴛʏ Sᴜᴘᴘᴏʀᴛ
• 💎 Fᴀsᴛᴇʀ Pʀᴏᴄᴇssɪɴɢ

<b>⏳ Fʀᴇᴇ Tʀɪᴀʟ:</b>
• 4 Hᴏᴜʀs Fʀᴇᴇ Tʀɪᴀʟ Aᴠᴀɪʟᴀʙʟᴇ!</blockquote>"""
    
    await message.reply_text(
        features_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Gᴇᴛ Pʀᴇᴍɪᴜᴍ", callback_data="upgrade")],
            [InlineKeyboardButton("💬 Sᴜᴘᴘᴏʀᴛ", url="https://t.me/roxybasicneed1")]
        ])
    )

        
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await send_reaction(client, message)
    
    user_id = message.from_user.id
    
    # ===== BAN CHECK =====
    ban_status = await roxy_bot.get_ban_status(user_id)
    if ban_status.get('is_banned') and user_id not in Config.ADMIN:
        from config import roxy as roxy_config
        await message.reply_text(
            roxy_config.BANNED_TXT.format(ban_status.get('ban_reason', 'Policy violation')),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📞 Contact Support", url="https://t.me/roxycontactbot")
            ]])
        )
        return
    
    # Check maintenance mode (skip for admins)
    if user_id not in Config.ADMIN:
        is_maintenance, maintenance_msg = await roxy_bot.get_maintenance_mode()
        if is_maintenance:
            await message.reply_text(f"<blockquote>{maintenance_msg}</blockquote>")
            return
    
    start_button = [[        
        InlineKeyboardButton('⚙️ Sᴇᴛᴛɪɴɢs', callback_data='settings_menu'),
        InlineKeyboardButton('📋 Hᴇʟᴘ', callback_data='help')
        ],[
        InlineKeyboardButton('🎬 Sᴇᴛ Mᴇᴅɪᴀ', callback_data='media_menu')
        ],[
        InlineKeyboardButton('📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/roxybasicneedbot1'),
        InlineKeyboardButton('💬 Sᴜᴘᴘᴏʀᴛ', url='https://t.me/roxybasicneed1')
         ]]
        
    if client.premium:
        start_button.append([InlineKeyboardButton('💎 Pʀᴇᴍɪᴜᴍ Pʟᴀɴs 💎', callback_data='upgrade')])
            
    user = message.from_user
    await roxy_bot.add_user(client, message) 
    
    pic_url = await get_random_pic()
    
    # Try to send photo with wallhaven URL, fallback to static image if fails
    try:
        await message.reply_photo(pic_url, caption=roxy.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button))
    except Exception as e:
        # Fallback to static image if Telegram can't fetch the URL
        fallback_image = "https://i.ibb.co/27SZFvzv/file-29500.jpg"
        try:
            await message.reply_photo(fallback_image, caption=roxy.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button))
        except:
            # If photo completely fails, send text only
            await message.reply_text(roxy.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button))


@Client.on_message(filters.private & filters.command("myplan"))
async def myplan(client, message):
    await send_reaction(client, message)
    if not client.premium:
        return # premium mode disabled ✓

    user_id = message.from_user.id
    user = message.from_user.mention
    
    if await roxy_bot.has_premium_access(user_id):
        data = await roxy_bot.get_user(user_id)
        expiry_str_in_ist = data.get("expiry_time")
        time_left_str = expiry_str_in_ist - datetime.datetime.now()

        text = f"<blockquote>ᴜꜱᴇʀ :- {user}\nᴜꜱᴇʀ ɪᴅ :- <code>{user_id}</code>\n</blockquote>"

        if client.uploadlimit:
            await roxy_bot.reset_uploadlimit_access(user_id)                
            user_data = await roxy_bot.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")

            text += f"<blockquote>ᴘʟᴀɴ :- `{type}`\nᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :- `{humanbytes(limit)}`\nᴛᴏᴅᴀʏ ᴜsᴇᴅ :- `{humanbytes(used)}`\nʀᴇᴍᴀɪɴ :- `{humanbytes(remain)}`\n</blockquote>"

        text += f"<blockquote>ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\nᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}</blockquote>"

        await message.reply_text(text, quote=True)

    else:
        if client.uploadlimit:
            await roxy_bot.reset_uploadlimit_access(user_id)
            user_data = await roxy_bot.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")

            text = f"<blockquote>ᴜꜱᴇʀ :- {user}\nᴜꜱᴇʀ ɪᴅ :- <code>{user_id}</code>\nᴘʟᴀɴ :- `{type}`\nᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :- `{humanbytes(limit)}`\nᴛᴏᴅᴀʏ ᴜsᴇᴅ :- `{humanbytes(used)}`\nʀᴇᴍᴀɪɴ :- `{humanbytes(remain)}`\nᴇxᴘɪʀᴇᴅ ᴅᴀᴛᴇ :- ʟɪғᴇᴛɪᴍᴇ\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ 👇</blockquote>"

            await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ 💸", callback_data='upgrade')]]), quote=True)

        else:
            m=await message.reply_sticker("CAACAgIAAxkBAAIBTGVjQbHuhOiboQsDm35brLGyLQ28AAJ-GgACglXYSXgCrotQHjibHgQ")
            await message.reply_text(f"<blockquote>ʜᴇʏ {user},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs, ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ 👇</blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ 💸", callback_data='upgrade')]]))			 
            await asyncio.sleep(2)
            await m.delete()

@Client.on_message(filters.private & filters.command("plans"))
async def plans(client, message):
    await send_reaction(client, message)
    if not client.premium:
        return # premium mode disabled ✓

    user = message.from_user
    upgrade_msg = roxy.UPGRADE_PLAN.format(user.mention) if client.uploadlimit else roxy.UPGRADE_PREMIUM.format(user.mention)
    
    free_trial_status = await roxy_bot.get_free_trial_status(user.id)
    if not await roxy_bot.has_premium_access(user.id):
        if not free_trial_status:
            await message.reply_text(text=upgrade_msg, reply_markup=upgrade_trial_button, disable_web_page_preview=True)
        else:
            await message.reply_text(text=upgrade_msg, reply_markup=upgrade_button, disable_web_page_preview=True)
    else:
        await message.reply_text(text=upgrade_msg, reply_markup=upgrade_button, disable_web_page_preview=True)
   
  
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    
    # Helper function to handle both photo and text messages
    async def smart_edit(text, reply_markup, disable_web_page_preview=True):
        """Edit message - for photo: edit caption, for text: edit text"""
        if query.message.photo:
            # It's a photo message, edit the caption
            try:
                await query.message.edit_caption(
                    caption=text,
                    reply_markup=reply_markup
                )
            except Exception as e:
                # If edit_caption fails, delete and send new text
                try:
                    await query.message.delete()
                except:
                    pass
                await client.send_message(
                    query.from_user.id,
                    text=text,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup
                )
        else:
            # It's a text message, just edit
            await query.message.edit_text(
                text=text,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup
            )
    
    if data == "start":
        start_button = [[        
        InlineKeyboardButton('⚙️ Sᴇᴛᴛɪɴɢs', callback_data='settings_menu'),
        InlineKeyboardButton('📋 Hᴇʟᴘ', callback_data='help')
        ],[
        InlineKeyboardButton('🎬 Sᴇᴛ Mᴇᴅɪᴀ', callback_data='media_menu')
        ],[
        InlineKeyboardButton('📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/roxybasicneedbot1'),
        InlineKeyboardButton('💬 Sᴜᴘᴘᴏʀᴛ', url='https://t.me/roxybasicneed1')
         ]]

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

            
        if client.premium:
            start_button.append([InlineKeyboardButton('💎 Pʀᴇᴍɪᴜᴍ Pʟᴀɴs 💎', callback_data='upgrade')])
            
        await smart_edit(
            text=roxy.START_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(start_button))
        
    elif data == "help":
        await smart_edit(
            text=roxy.HELP_TXT,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("🖼️ Thumbnail", callback_data = "thumbnail"),
                InlineKeyboardButton("📝 Caption", callback_data = "caption")
                ],[          
                InlineKeyboardButton("✏️ Custom File Name", callback_data = "custom_file_name"),
                InlineKeyboardButton("🔄 Auto Rename", callback_data = "autorename_help")
                ],[          
                InlineKeyboardButton("ℹ️ About", callback_data = "about"),
                InlineKeyboardButton("💾 Metadata", callback_data = "roxy_meta_data")
                                     ],[
                InlineKeyboardButton("🔙 Back", callback_data = "start")
                  ]]))         
        
    elif data == "about":
        about_button = [[
         #⚠️ don't change source code & source link ⚠️ #
        InlineKeyboardButton("💻 Source", callback_data = "source_code"), #Whoever is deploying this repo is given a warning ⚠️ not to remove this repo link #first & last warning ⚠️
        InlineKeyboardButton("📊 Bot Status", callback_data = "bot_status")
        ],[
        InlineKeyboardButton("🟢 Live Status", callback_data = "live_status")           
        ]]
        if client.premium:
            about_button[-1].append(InlineKeyboardButton("⬆️ Upgrade", callback_data = "upgrade"))
            about_button.append([InlineKeyboardButton("🔙 Back", callback_data = "start")])
        else:
            about_button[-1].append(InlineKeyboardButton("🔙 Back", callback_data = "start"))
            
        await smart_edit(
            text=roxy.ABOUT_TXT.format(client.mention, __developer__, __programer__, __library__, __language__, __database__, _bot_version_),
            reply_markup=InlineKeyboardMarkup(about_button))    
        
    elif data == "upgrade":
        if not client.premium:
            return await query.message.delete()
                
        user = query.from_user
        upgrade_msg = roxy.UPGRADE_PLAN.format(user.mention) if client.uploadlimit else roxy.UPGRADE_PREMIUM.format(user.mention)
    
        free_trial_status = await roxy_bot.get_free_trial_status(query.from_user.id)
        if not await roxy_bot.has_premium_access(query.from_user.id):
            if not free_trial_status:
                await smart_edit(text=upgrade_msg, reply_markup=upgrade_trial_button)   
            else:
                await smart_edit(text=upgrade_msg, reply_markup=upgrade_button)
        else:
            await smart_edit(text=upgrade_msg, reply_markup=upgrade_button)
           
    elif data == "give_trial":
        if not client.premium:
            return await query.message.delete()
                
        await query.message.delete()
        free_trial_status = await roxy_bot.get_free_trial_status(query.from_user.id)
        if not free_trial_status:            
            await roxy_bot.give_free_trial(query.from_user.id)
            new_text = "**<blockquote>✅ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴛʀɪᴀʟ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ғᴏʀ 4 ʜᴏᴜʀs.\n\nʏᴏᴜ ᴄᴀɴ ᴜsᴇ ꜰʀᴇᴇ ᴛʀɪᴀʟ ꜰᴏʀ 4 ʜᴏᴜʀs ꜰʀᴏᴍ ɴᴏᴡ 😀\n\nआप अब से 4 घण्टा के लिए निःशुल्क ट्रायल का उपयोग कर सकते हैं 😀</blockquote>**"
        else:
            new_text = "**<blockquote>🤣 ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴜsᴇᴅ ғʀᴇᴇ ɴᴏ ᴍᴏʀᴇ ғʀᴇᴇ ᴛʀᴀɪʟ. ᴘʟᴇᴀsᴇ ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʜᴇʀᴇ ᴀʀᴇ ᴏᴜʀ 👉 /plans</blockquote>**"
        await client.send_message(query.from_user.id, text=new_text)

    elif data == "thumbnail":
        await smart_edit(
            text=roxy.THUMBNAIL,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "help")]])) 
      
    elif data == "caption":
        await smart_edit(
            text=roxy.CAPTION,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "help")]])) 
      
    elif data == "custom_file_name":
        await smart_edit(
            text=roxy.CUSTOM_FILE_NAME,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "help")]])) 
      
    elif data == "roxy_meta_data":
        await smart_edit(
            text=roxy.ROXY_METADATA,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "help")]])) 

    elif data == "autorename_help":
        await smart_edit(
            text=roxy.AUTORENAME_TXT,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Bᴀᴄᴋ", callback_data = "help")]])) 
      
    elif data == "bot_status":
        total_users = await roxy_bot.total_users_count()
        if client.premium:
            total_premium_users = await roxy_bot.total_premium_users_count()
        else:
            total_premium_users = "Disabled ✅"
        
        uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        await smart_edit(
            text=roxy.BOT_STATUS.format(uptime, total_users, total_premium_users, sent, recv),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("🔙 Back", callback_data = "about")]])) 
      
    elif data == "live_status":
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await smart_edit(
            text=roxy.LIVE_STATUS.format(currentTime, cpu_usage, ram_usage, total, used, disk_usage, free, sent, recv),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("🔙 Back", callback_data = "about")]])) 
      
    elif data == "source_code":
        await smart_edit(
            text=roxy.DEV_TXT,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
           #Whoever is deploying this repo is given a warning ⚠️ not to remove this repo link #first & last warning ⚠️   
                InlineKeyboardButton("💞 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 💞", url="https://github.com/RoxyBasicNeedBot")
            ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("🔙 Back", callback_data = "start")
                 ]])          
        )
    
    elif data == "settings_menu":
        # Open settings menu
        user_id = query.from_user.id
        
        dump_channel = await roxy_bot.get_dump_channel(user_id)
        screenshot_mode = await roxy_bot.get_screenshot_mode(user_id)
        mkv_to_mp4_mode = await roxy_bot.get_convert_mkv_to_mp4(user_id)
        compress_mode = await roxy_bot.get_compress_video(user_id)
        trim_mode = await roxy_bot.get_trim_mode(user_id)
        is_premium = await roxy_bot.has_premium_access(user_id)
        
        if dump_channel:
            try:
                chat = await client.get_chat(dump_channel)
                dump_status = f"✅ {chat.title}"
            except:
                dump_status = f"⚠️ ID: {dump_channel}"
        else:
            dump_status = "❌ Not Set"
        
        ss_status = "✅ ON" if screenshot_mode else "❌ OFF"
        mkv_status = "✅ ON" if mkv_to_mp4_mode else "❌ OFF"
        compress_status = ("✅ ON" if compress_mode else "❌ OFF") if is_premium else "🔒 Premium"
        trim_status = ("✅ ON" if trim_mode else "❌ OFF") if is_premium else "🔒 Premium"
        
        await smart_edit(
            text="<blockquote><b>⚙️ Sᴇᴛᴛɪɴɢs</b>\n\nCᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ʙᴏᴛ sᴇᴛᴛɪɴɢs ʜᴇʀᴇ.</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"🎯 Sᴇᴛ Dᴜᴍᴘ Cʜᴀɴɴᴇʟ", callback_data="settings_setdump")],
                [InlineKeyboardButton(f"📺 Dᴜᴍᴘ: {dump_status}", callback_data="settings_viewdump")],
                [InlineKeyboardButton(f"📸 Sᴄʀᴇᴇɴsʜᴏᴛs", callback_data="settings_ss_info"), 
                 InlineKeyboardButton(f"{ss_status}", callback_data="settings_toggle_ss")],
                [InlineKeyboardButton(f"🎬 MKV → MP4", callback_data="settings_mkv_info"), 
                 InlineKeyboardButton(f"{mkv_status}", callback_data="settings_toggle_mkv")],
                [InlineKeyboardButton(f"📦 Cᴏᴍᴘʀᴇss", callback_data="settings_compress_info"), 
                 InlineKeyboardButton(f"{compress_status}", callback_data="settings_toggle_compress")],
                [InlineKeyboardButton(f"✂️ Tʀɪᴍ", callback_data="settings_trim_info"), 
                 InlineKeyboardButton(f"{trim_status}", callback_data="settings_toggle_trim")],
                [InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="start")]
            ])
        )

    
    elif data == "media_menu":
        # Show media type selection menu
        user_id = query.from_user.id
        
        current_type = await roxy_bot.get_media_type(user_id)
        
        doc_text = "✅ Dᴏᴄᴜᴍᴇɴᴛ" if current_type == "document" else "📁 Dᴏᴄᴜᴍᴇɴᴛ"
        vid_text = "✅ Vɪᴅᴇᴏ" if current_type == "video" else "🎥 Vɪᴅᴇᴏ"
        aud_text = "✅ Aᴜᴅɪᴏ" if current_type == "audio" else "🎵 Aᴜᴅɪᴏ"
        
        await smart_edit(
            text="<blockquote><b>🎬 Sᴇᴛ Mᴇᴅɪᴀ Tyᴘᴇ</b>\n\nSᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘʀᴇꜰᴇʀʀᴇᴅ ᴏᴜᴛᴘᴜᴛ ꜰᴏʀᴍᴀᴛ ꜰᴏʀ ʀᴇɴᴀᴍᴇᴅ ꜰɪʟᴇs.</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(doc_text, callback_data="setmedia_document"),
                    InlineKeyboardButton(vid_text, callback_data="setmedia_video")
                ],
                [
                    InlineKeyboardButton(aud_text, callback_data="setmedia_audio")
                ],
                [InlineKeyboardButton("🔙 Bᴀᴄᴋ", callback_data="start")]
            ])
        )
            
    elif data.startswith("upload"):
        user_id = query.from_user.id
        
        # Check if trim mode is enabled for video/document uploads
        trim_mode = await roxy_bot.get_trim_mode(user_id)
        
        # Only show trim options for video/document, not for audio or notrim variants
        if trim_mode and data in ["upload_video", "upload_document"]:
            # Store the selected media type for later use
            from plugins.trim_handler import pending_trim
            if user_id not in pending_trim:
                pending_trim[user_id] = {}
            pending_trim[user_id]['media_type'] = data
            
            # Show trim selection options
            is_premium = await roxy_bot.has_premium_access(user_id)
            manual_text = "Manual Trim" if is_premium else "Manual Trim 🔒"
            
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("⏱️ Auto Trim", callback_data=f"trim_auto_{data}")],
                [InlineKeyboardButton(f"✏️ {manual_text}", callback_data="trim_manual")],
                [InlineKeyboardButton("❌ Skip Trim", callback_data=f"{data}_notrim")]
            ])
            
            await query.message.edit_text(
                text="<blockquote><b>✂️ Tʀɪᴍ Mᴏᴅᴇ Eɴᴀʙʟᴇᴅ</b>\n\n"
                     "• <b>Auto Trim:</b> Trim video to fixed duration from start\n"
                     "• <b>Manual Trim:</b> Select start & end time (Premium only)\n"
                     "• <b>Skip Trim:</b> Upload without trimming</blockquote>",
                reply_markup=buttons
            )
        else:
            # No trim mode or audio - proceed directly
            from plugins.subtitle_mux import route_to_upload_or_subtitle
            file_msg = query.message.reply_to_message

            # KEY FIX: Extract the user's custom rename BEFORE the message gets edited.
            # The button message text contains: "• Fɪʟᴇ Nᴀᴍᴇ :-`filename.ext`"
            # If we don't extract it now, show_subtitle_option() will overwrite the text.
            custom_name = None
            try:
                msg_text = query.message.text or ""
                if ":-" in msg_text:
                    import re as _re
                    part = msg_text.split(":-", 1)[1].strip().strip("`").strip()
                    # Take only the first line in case there is trailing text
                    part = part.split("\n")[0].strip().strip("`").strip()
                    # Remove any trailing HTML/blockquote artifacts from Telegram text rendering
                    part = _re.sub(r'[\s_]*(/?blockquote)[\s_]*$', '', part, flags=_re.IGNORECASE).strip()
                    if part:
                        custom_name = part
                        print(f"[UploadCB] user={query.from_user.id} | extracted custom_name: {custom_name}")
            except Exception as _e:
                print(f"[UploadCB] Could not extract custom_name: {_e}")

            await route_to_upload_or_subtitle(
                client, query, data, file_msg,
                edit_msg=query.message,
                custom_name=custom_name
            )
            
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

    else:
        await query.continue_propagation()

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
