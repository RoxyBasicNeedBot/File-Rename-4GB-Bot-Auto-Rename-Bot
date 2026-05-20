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

# Watermark Plugin (Premium)
# Set/view/delete text watermark with position selection

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import roxy_bot
from helper.utils import send_reaction


POSITION_LABELS = {
    'top_left': '↖️ Top Left',
    'top_right': '↗️ Top Right',
    'center_left': '⬅️ Center Left',
    'center': '⏺️ Center',
    'center_right': '➡️ Center Right',
    'bottom_left': '↙️ Bottom Left',
    'bottom_right': '↘️ Bottom Right',
}


@Client.on_message(filters.private & filters.command(['set_watermark']))
async def set_watermark_command(client, message):
    """Set text watermark with position selection - Premium only"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    # Check premium
    is_premium = await roxy_bot.has_premium_access(user_id)
    if not is_premium:
        return await message.reply_text(
            "<blockquote>🔒 <b>Premium Feature!</b>\n\n"
            "Watermarking is for Premium users only.\n"
            "Use /plans to upgrade.</blockquote>"
        )
    
    # Get watermark text from command
    if len(message.command) < 2:
        return await message.reply_text(
            "<blockquote><b>🎨 Sᴇᴛ Wᴀᴛᴇʀᴍᴀʀᴋ</b>\n\n"
            "Send your watermark text with the command.\n\n"
            "<b>Usage:</b> <code>/set_watermark @YourChannel</code>\n"
            "<b>Example:</b> <code>/set_watermark @MyMovies</code>\n\n"
            "The watermark will be auto-applied to all your videos!</blockquote>"
        )
    
    watermark_text = message.text.split(None, 1)[1].strip()
    
    if len(watermark_text) > 50:
        return await message.reply_text(
            "<blockquote>❌ Watermark text too long! Maximum 50 characters.</blockquote>"
        )
    
    # Save watermark text
    await roxy_bot.set_watermark(user_id, watermark_text)
    
    # Get current position
    current_pos = await roxy_bot.get_watermark_position(user_id)
    
    # Show position selection buttons
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"{'✅ ' if current_pos == 'top_left' else ''}↖️ Top Left", 
                callback_data="wm_pos_top_left"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if current_pos == 'top_right' else ''}↗️ Top Right", 
                callback_data="wm_pos_top_right"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅ ' if current_pos == 'center_left' else ''}⬅️ Center Left", 
                callback_data="wm_pos_center_left"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if current_pos == 'center' else ''}⏺️ Center", 
                callback_data="wm_pos_center"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if current_pos == 'center_right' else ''}➡️ Center Right", 
                callback_data="wm_pos_center_right"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅ ' if current_pos == 'bottom_left' else ''}↙️ Bottom Left", 
                callback_data="wm_pos_bottom_left"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if current_pos == 'bottom_right' else ''}↘️ Bottom Right", 
                callback_data="wm_pos_bottom_right"
            )
        ],
    ])
    
    await message.reply_text(
        f"<blockquote><b>🎨 Wᴀᴛᴇʀᴍᴀʀᴋ Sᴇᴛ!</b>\n\n"
        f"<b>📝 Text:</b> <code>{watermark_text}</code>\n"
        f"<b>📍 Position:</b> {POSITION_LABELS.get(current_pos, 'Bottom Right')}\n\n"
        f"Choose where you want the watermark to appear on your videos:</blockquote>",
        reply_markup=buttons
    )


@Client.on_callback_query(filters.regex(r'^wm_pos_'))
async def watermark_position_callback(client, callback_query):
    """Handle watermark position selection"""

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

    user_id = callback_query.from_user.id
    
    # Extract position from callback data
    position = callback_query.data.replace("wm_pos_", "")
    
    if position not in POSITION_LABELS:
        return await callback_query.answer("❌ Invalid position!", show_alert=True)
    
    # Save position
    await roxy_bot.set_watermark_position(user_id, position)
    
    # Get watermark text
    watermark_text = await roxy_bot.get_watermark(user_id)
    
    # Rebuild buttons with updated checkmark
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"{'✅ ' if position == 'top_left' else ''}↖️ Top Left", 
                callback_data="wm_pos_top_left"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if position == 'top_right' else ''}↗️ Top Right", 
                callback_data="wm_pos_top_right"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅ ' if position == 'center_left' else ''}⬅️ Center Left", 
                callback_data="wm_pos_center_left"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if position == 'center' else ''}⏺️ Center", 
                callback_data="wm_pos_center"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if position == 'center_right' else ''}➡️ Center Right", 
                callback_data="wm_pos_center_right"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅ ' if position == 'bottom_left' else ''}↙️ Bottom Left", 
                callback_data="wm_pos_bottom_left"
            ),
            InlineKeyboardButton(
                f"{'✅ ' if position == 'bottom_right' else ''}↘️ Bottom Right", 
                callback_data="wm_pos_bottom_right"
            )
        ],
    ])
    
    await callback_query.message.edit_text(
        f"<blockquote><b>🎨 Wᴀᴛᴇʀᴍᴀʀᴋ Uᴘᴅᴀᴛᴇᴅ!</b>\n\n"
        f"<b>📝 Text:</b> <code>{watermark_text}</code>\n"
        f"<b>📍 Position:</b> {POSITION_LABELS[position]}\n\n"
        f"✅ Watermark will be applied to all your videos automatically!</blockquote>",
        reply_markup=buttons
    )
    
    await callback_query.answer(f"✅ Position set to {POSITION_LABELS[position]}!")


@Client.on_message(filters.private & filters.command(['see_watermark']))
async def see_watermark_command(client, message):
    """View current watermark settings"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    watermark_text = await roxy_bot.get_watermark(user_id)
    
    if not watermark_text:
        return await message.reply_text(
            "<blockquote><b>🎨 Wᴀᴛᴇʀᴍᴀʀᴋ</b>\n\n"
            "❌ No watermark set.\n\n"
            "Use <code>/set_watermark your text</code> to set one.</blockquote>"
        )
    
    position = await roxy_bot.get_watermark_position(user_id)
    pos_label = POSITION_LABELS.get(position, "Bottom Right")
    
    await message.reply_text(
        f"<blockquote><b>🎨 Yᴏᴜʀ Wᴀᴛᴇʀᴍᴀʀᴋ</b>\n\n"
        f"<b>📝 Text:</b> <code>{watermark_text}</code>\n"
        f"<b>📍 Position:</b> {pos_label}\n\n"
        f"This watermark is auto-applied to all your renamed videos.\n"
        f"Use <code>/del_watermark</code> to remove it.</blockquote>"
    )


@Client.on_message(filters.private & filters.command(['del_watermark']))
async def del_watermark_command(client, message):
    """Delete watermark"""
    await send_reaction(client, message)
    user_id = message.from_user.id
    
    watermark_text = await roxy_bot.get_watermark(user_id)
    
    if not watermark_text:
        return await message.reply_text(
            "<blockquote>❌ No watermark set to delete!</blockquote>"
        )
    
    await roxy_bot.set_watermark(user_id, None)
    
    await message.reply_text(
        "<blockquote>✅ <b>Watermark Deleted!</b>\n\n"
        "Your videos will no longer have a watermark.</blockquote>"
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
