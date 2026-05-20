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

# Subtitle Muxing Plugin - Multi-language subtitle support
# Supports: .srt, .ass, .ssa, .vtt, .sub subtitle formats
# Flow: User sends subtitles one-by-one, selects language for each, types /done to proceed
# Always outputs MKV for best player compatibility (VLC, MX Player, mpv)

import os, time, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import roxy_bot
from helper.utils import send_reaction

# Supported subtitle extensions
SUBTITLE_EXTENSIONS = ['.srt', '.ass', '.ssa', '.vtt', '.sub']

# Language options for subtitle tracks
LANGUAGE_OPTIONS = [
    ('eng', 'English 🇬🇧'),
    ('hin', 'Hindi 🇮🇳'),
    ('tam', 'Tamil 🇮🇳'),
    ('tel', 'Telugu 🇮🇳'),
    ('jpn', 'Japanese 🇯🇵'),
    ('kor', 'Korean 🇰🇷'),
    ('ara', 'Arabic 🇸🇦'),
    ('custom', '✏️ Custom'),
]

LANGUAGE_TITLES = {
    'eng': 'English',
    'hin': 'Hindi',
    'tam': 'Tamil',
    'tel': 'Telugu',
    'jpn': 'Japanese',
    'kor': 'Korean',
    'ara': 'Arabic',
}

# Per-user subtitle state tracking
# {user_id: {
#     'waiting': True/False,          # waiting for subtitle file
#     'waiting_lang': True/False,     # waiting for language selection
#     'waiting_custom_lang': True/False,  # waiting for custom language text
#     'media_type': 'upload_video',
#     'file_msg': Message,            # original video message
#     'reply_msg': Message,           # bot's reply message
#     'status_msg': Message,          # current status message
#     'custom_name': 'My Movie.mkv',  # preserved user rename
#     'subtitles': [                  # list of queued subtitles
#         {'path': '/path/to/sub', 'lang': 'eng', 'title': 'English', 'format': '.srt', 'filename': 'eng.srt'},
#     ],
#     'pending_sub_path': None,       # temp: subtitle downloaded but not yet assigned language
#     'pending_sub_format': None,     # temp: format of pending subtitle
#     'pending_sub_filename': None,   # temp: original filename of pending subtitle
# }}
pending_subtitle_state = {}


def is_subtitle_file(filename):
    """Check if a filename is a subtitle file"""
    if not filename:
        return False
    return any(filename.lower().endswith(ext) for ext in SUBTITLE_EXTENSIONS)


def get_subtitle_format(filename):
    """Get the subtitle format extension from filename"""
    if not filename:
        return None
    for ext in SUBTITLE_EXTENSIONS:
        if filename.lower().endswith(ext):
            return ext
    return None


def is_waiting_for_subtitle(user_id):
    """Check if user is in any subtitle-related waiting mode"""
    state = pending_subtitle_state.get(user_id, {})
    return state.get('waiting', False) or state.get('waiting_lang', False) or state.get('waiting_custom_lang', False)


def get_pending_subtitles(user_id):
    """Get the list of pending subtitles for the upload pipeline"""
    state = pending_subtitle_state.get(user_id, {})
    subs = state.get('subtitles', [])
    if subs:
        return subs
    return None


def clear_pending_subtitle(user_id):
    """Clear subtitle state and cleanup all downloaded files"""
    state = pending_subtitle_state.pop(user_id, {})
    # Clean up all subtitle files
    for sub in state.get('subtitles', []):
        sub_path = sub.get('path')
        if sub_path and os.path.exists(sub_path):
            try:
                os.remove(sub_path)
            except:
                pass
    # Clean up pending sub
    pending_path = state.get('pending_sub_path')
    if pending_path and os.path.exists(pending_path):
        try:
            os.remove(pending_path)
        except:
            pass


def set_subtitle_waiting(user_id, media_type, file_msg, reply_msg, custom_name=None):
    """Put user in subtitle-waiting mode, preserving their custom rename."""
    pending_subtitle_state[user_id] = {
        'waiting': True,
        'waiting_lang': False,
        'waiting_custom_lang': False,
        'media_type': media_type,
        'file_msg': file_msg,
        'reply_msg': reply_msg,
        'status_msg': None,
        'custom_name': custom_name,
        'subtitles': [],
        'pending_sub_path': None,
        'pending_sub_format': None,
        'pending_sub_filename': None,
    }


def cancel_subtitle_waiting(user_id):
    """Cancel subtitle waiting and cleanup"""
    clear_pending_subtitle(user_id)


def is_video_file(filename):
    """Check if the file is a video based on extension"""
    if not filename:
        return False
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp']
    return any(filename.lower().endswith(ext) for ext in video_extensions)


def _build_subtitle_summary(subtitles):
    """Build a display summary of queued subtitles"""
    if not subtitles:
        return "No subtitles added yet."
    lines = []
    for i, sub in enumerate(subtitles, 1):
        title = sub.get('title', 'Unknown')
        fmt = sub.get('format', '.srt')
        fname = sub.get('filename', 'subtitle')
        lines.append(f"  {i}. 🌐 <b>{title}</b> — <code>{fname}</code>")
    return '\n'.join(lines)


def _build_mock_update(reply_msg, file_msg, media_type, user, custom_name):
    """
    Build a MockMessage/MockUpdate for calling upload_doc.
    The message text must contain ':-' followed by the filename,
    which is how upload_doc parses the filename to use.
    """
    class MockMessage:
        def __init__(self, original_msg, reply_to_msg, text_override=None):
            self.text = text_override if text_override is not None else original_msg.text
            self.chat = original_msg.chat
            self.id = original_msg.id
            self.reply_to_message = reply_to_msg
            self._original = original_msg

        async def edit(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

        async def edit_text(self, text, **kwargs):
            return await self._original.edit_text(text, **kwargs)

    class MockUpdate:
        def __init__(self, mock_msg, data, user_obj):
            self.message = mock_msg
            self.data = data
            self.from_user = user_obj

    # upload_doc parses filename via: new_name.split(":-")[1].strip().strip('`').strip()
    # IMPORTANT: Use plain text (no HTML tags!) because this is set directly on
    # MockMessage.text and NOT rendered by Telegram, so tags would appear in the filename.
    text_for_upload = f"📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-{custom_name}"
    mock_msg = MockMessage(reply_msg, file_msg, text_override=text_for_upload)
    return MockUpdate(mock_msg, media_type, user)


async def show_subtitle_option(client, message, user_id, media_type, file_msg,
                                edit_msg=None, extra_text="", custom_name=None):
    """
    Show subtitle option buttons to user.
    Stores custom_name in state BEFORE editing the message (fixes rename bug).
    """
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Aᴅᴅ Sᴜʙᴛɪᴛʟᴇ(s)", callback_data=f"sub_add_{media_type}")],
        [InlineKeyboardButton("⏭️ Sᴋɪᴘ", callback_data=f"sub_skip_{media_type}")]
    ])

    # Use custom_name for display if available, else fall back to original filename
    display_name = custom_name
    if not display_name:
        try:
            roxy_file = getattr(file_msg, file_msg.media.value)
            display_name = roxy_file.file_name or "video"
        except:
            display_name = "video"

    text = (
        f"<blockquote>{extra_text}<b>📝 Sᴜʙᴛɪᴛʟᴇ Oᴘᴛɪᴏɴ</b>\n\n"
        f"<b>📹 File:</b> <code>{display_name}</code>\n\n"
        f"Would you like to add subtitles to this video?\n\n"
        f"<b>Supported formats:</b> .srt, .ass, .ssa, .vtt, .sub\n\n"
        f"• <b>Multi-Language:</b> Send multiple subtitle files with different languages.\n"
        f"• <b>Soft Sub:</b> Toggleable tracks in your player (VLC, MX Player). <b>(Fast)</b></blockquote>"
    )

    if edit_msg:
        reply_msg = await edit_msg.edit_text(text, reply_markup=buttons)
    else:
        reply_msg = await message.reply(
            text=text,
            reply_to_message_id=file_msg.id,
            reply_markup=buttons
        )

    # Store state with custom_name AFTER getting reply_msg reference
    set_subtitle_waiting(user_id, media_type, file_msg, reply_msg, custom_name=custom_name)
    return reply_msg


async def route_to_upload_or_subtitle(client, mock_update, media_type_data, file_msg,
                                       edit_msg=None, extra_text="", custom_name=None):
    """
    Check if the file is a video and show subtitle options.
    Otherwise proceed directly to upload_doc.
    """
    from plugins.file_rename import upload_doc

    # Detect batch upload (media group) — no subtitle for batch
    is_batch = getattr(file_msg, "media_group_id", None) is not None

    try:
        roxy_file = getattr(file_msg, file_msg.media.value)
        filename = roxy_file.file_name or "video.mp4"
    except:
        filename = "video.mp4"

    if is_video_file(filename) and media_type_data in ["upload_video", "upload_document"] and not is_batch:
        user_id = mock_update.from_user.id
        message_to_use = edit_msg if edit_msg else mock_update.message
        await show_subtitle_option(
            client=client,
            message=message_to_use,
            user_id=user_id,
            media_type=media_type_data,
            file_msg=file_msg,
            edit_msg=edit_msg,
            extra_text=extra_text,
            custom_name=custom_name,
        )
    else:
        await upload_doc(client, mock_update)


def _build_language_buttons(sub_index):
    """Build language selection inline keyboard"""
    rows = []
    for i in range(0, len(LANGUAGE_OPTIONS), 2):
        row = []
        for lang_code, lang_label in LANGUAGE_OPTIONS[i:i+2]:
            row.append(InlineKeyboardButton(lang_label, callback_data=f"sublang_{lang_code}_{sub_index}"))
        rows.append(row)
    return InlineKeyboardMarkup(rows)


async def _show_waiting_for_subtitle(client, chat_id, user_id, state):
    """Show the 'send subtitle file' prompt with current queue"""
    subtitles = state.get('subtitles', [])
    summary = _build_subtitle_summary(subtitles)
    
    count_text = f"({len(subtitles)} added)" if subtitles else ""

    text = (
        f"<blockquote><b>📝 Sᴇɴᴅ Sᴜʙᴛɪᴛʟᴇ Fɪʟᴇ {count_text}</b>\n\n"
    )
    
    if subtitles:
        text += f"<b>📋 Queued Subtitles:</b>\n{summary}\n\n"
    
    text += (
        "Send me your next subtitle file.\n\n"
        "<b>Supported formats:</b>\n"
        "• <code>.srt</code> — SubRip (most common)\n"
        "• <code>.ass</code> — Advanced SubStation Alpha\n"
        "• <code>.ssa</code> — SubStation Alpha\n"
        "• <code>.vtt</code> — WebVTT\n"
        "• <code>.sub</code> — MicroDVD\n\n"
    )
    
    if subtitles:
        text += "Type /done when finished adding subtitles.</blockquote>"
    else:
        text += "Or press Cancel to skip.</blockquote>"

    buttons = []
    if subtitles:
        buttons.append([InlineKeyboardButton("✅ Dᴏɴᴇ — Proceed", callback_data="sub_done")])
    buttons.append([InlineKeyboardButton("❌ Cᴀɴᴄᴇʟ", callback_data=f"sub_skip_{state.get('media_type', 'upload_document')}")])

    # Try to edit existing status message, or send new one
    status_msg = state.get('status_msg')
    try:
        if status_msg:
            await status_msg.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
            return status_msg
    except:
        pass
    
    msg = await client.send_message(
        chat_id, text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    state['status_msg'] = msg
    pending_subtitle_state[user_id] = state
    return msg


# ===== CALLBACK HANDLERS =====

@Client.on_callback_query(filters.regex(r'^sub_add_upload_(video|document|audio)$'))
async def sub_add_callback(client, callback_query):
    """User wants to add subtitle(s) - put them in file-waiting mode"""
    user_id = callback_query.from_user.id
    media_type = callback_query.data.replace("sub_add_", "")  # e.g. upload_video

    # State was already set by show_subtitle_option; just make sure waiting is on
    state = pending_subtitle_state.get(user_id, {})
    state['waiting'] = True
    state['waiting_lang'] = False
    state['waiting_custom_lang'] = False
    pending_subtitle_state[user_id] = state

    try:
        await callback_query.message.delete()
    except:
        pass

    await _show_waiting_for_subtitle(client, callback_query.message.chat.id, user_id, state)
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r'^sub_skip_upload_(video|document|audio)$'))
async def sub_skip_callback(client, callback_query):
    """User wants to skip subtitle - proceed to upload with correct filename"""
    user_id = callback_query.from_user.id
    media_type = callback_query.data.replace("sub_skip_", "")

    # Pop state before anything else
    state = pending_subtitle_state.pop(user_id, {})

    # Clean up any downloaded subtitle files
    for sub in state.get('subtitles', []):
        if sub.get('path') and os.path.exists(sub['path']):
            try:
                os.remove(sub['path'])
            except:
                pass
    pending_path = state.get('pending_sub_path')
    if pending_path and os.path.exists(pending_path):
        try:
            os.remove(pending_path)
        except:
            pass

    file_msg = state.get('file_msg') or callback_query.message.reply_to_message
    if not file_msg:

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

        await callback_query.message.edit_text(
            "<blockquote>❌ Could not find the original file. Please send the file again.</blockquote>"
        )
        return await callback_query.answer()

    await callback_query.answer("⏭️ Skipping subtitle...")

    try:
        await callback_query.message.delete()
    except:
        pass

    from plugins.file_rename import upload_doc

    # Use stored custom_name
    custom_name = state.get('custom_name')
    if not custom_name:
        roxy_file = getattr(file_msg, file_msg.media.value)
        custom_name = roxy_file.file_name or "video.mp4"
        autorename_template = await roxy_bot.get_autorename(user_id)
        if autorename_template:
            from helper.utils import apply_autorename_template
            custom_name = await apply_autorename_template(custom_name, autorename_template)

    print(f"[SubtitleSkip] user={user_id} | uploading with name: {custom_name}")

    reply_msg = await client.send_message(
        callback_query.message.chat.id,
        text=f"<blockquote>📤 Uᴘʟᴏᴀᴅɪɴɢ...\n• Fɪʟᴇ Nᴀᴍᴇ :-`{custom_name}`</blockquote>",
        reply_to_message_id=file_msg.id
    )

    mock_update = _build_mock_update(reply_msg, file_msg, media_type, callback_query.from_user, custom_name)
    await upload_doc(client, mock_update)


@Client.on_callback_query(filters.regex(r'^sublang_'))
async def subtitle_language_callback(client, callback_query):
    """User selected a language for the last uploaded subtitle"""
    user_id = callback_query.from_user.id
    state = pending_subtitle_state.get(user_id, {})

    if not state.get('waiting_lang'):
        await callback_query.answer("❌ Not waiting for language selection.")
        return

    # Parse: sublang_{lang_code}_{sub_index}
    parts = callback_query.data.split('_')
    lang_code = parts[1]
    
    if lang_code == 'custom':
        # Ask user to type custom language name
        state['waiting_lang'] = False
        state['waiting_custom_lang'] = True
        pending_subtitle_state[user_id] = state

        await callback_query.message.edit_text(
            "<blockquote><b>✏️ Custom Language</b>\n\n"
            "Type the language name (e.g. <code>French</code>, <code>Spanish</code>, <code>Bengali</code>):\n\n"
            "This will be shown as the subtitle track name in your video player.</blockquote>"
        )
        await callback_query.answer()
        return

    # Map lang code to title
    lang_title = LANGUAGE_TITLES.get(lang_code, lang_code.capitalize())
    
    # Assign language to pending subtitle
    pending_path = state.get('pending_sub_path')
    pending_format = state.get('pending_sub_format', '.srt')
    pending_filename = state.get('pending_sub_filename', 'subtitle')
    
    if not pending_path or not os.path.exists(pending_path):
        await callback_query.answer("❌ Subtitle file not found!")
        state['waiting_lang'] = False
        state['waiting'] = True
        pending_subtitle_state[user_id] = state
        return

    # Add to subtitle list
    subtitle_entry = {
        'path': pending_path,
        'lang': lang_code,
        'title': lang_title,
        'format': pending_format,
        'filename': pending_filename,
    }
    state.setdefault('subtitles', []).append(subtitle_entry)

    # Clear pending
    state['pending_sub_path'] = None
    state['pending_sub_format'] = None
    state['pending_sub_filename'] = None
    state['waiting_lang'] = False
    state['waiting'] = True
    pending_subtitle_state[user_id] = state

    await callback_query.answer(f"✅ {lang_title} subtitle added!")
    
    # Show updated queue and prompt for next subtitle
    await _show_waiting_for_subtitle(client, callback_query.message.chat.id, user_id, state)

    try:
        await callback_query.message.delete()
    except:
        pass


@Client.on_callback_query(filters.regex(r'^sub_done$'))
async def subtitle_done_callback(client, callback_query):
    """User pressed Done button — proceed to upload with all subtitles"""
    user_id = callback_query.from_user.id
    state = pending_subtitle_state.get(user_id, {})

    subtitles = state.get('subtitles', [])
    if not subtitles:
        await callback_query.answer("❌ No subtitles added! Send a subtitle file first.")
        return

    await callback_query.answer("✅ Processing with subtitles...")
    await _proceed_to_upload(client, callback_query.message.chat.id, user_id, state)


# ===== /done COMMAND HANDLER =====

@Client.on_message(filters.private & filters.command("done"))
async def done_command(client, message):
    """Finalize subtitle queue and proceed to upload"""
    user_id = message.from_user.id
    await send_reaction(client, message)

    state = pending_subtitle_state.get(user_id, {})
    if not state:
        await message.reply_text("<blockquote>❌ No active subtitle session.</blockquote>")
        return

    subtitles = state.get('subtitles', [])
    if not subtitles:
        await message.reply_text(
            "<blockquote>❌ No subtitles added yet!\n\n"
            "Send subtitle files first, then type /done</blockquote>"
        )
        return

    # Stop any waiting state
    state['waiting'] = False
    state['waiting_lang'] = False
    state['waiting_custom_lang'] = False
    pending_subtitle_state[user_id] = state

    # Delete the /done message
    try:
        await message.delete()
    except:
        pass

    await _proceed_to_upload(client, message.chat.id, user_id, state)


async def _proceed_to_upload(client, chat_id, user_id, state):
    """Common function to proceed to upload after subtitles are finalized"""
    subtitles = state.get('subtitles', [])
    file_msg = state.get('file_msg')
    media_type = state.get('media_type', 'upload_document')
    custom_name = state.get('custom_name')

    if not file_msg:
        await client.send_message(
            chat_id,
            "<blockquote>❌ Session expired. Please send the video file again.</blockquote>"
        )
        clear_pending_subtitle(user_id)
        return

    # Delete the status message
    status_msg = state.get('status_msg')
    if status_msg:
        try:
            await status_msg.delete()
        except:
            pass

    # Resolve custom_name
    if not custom_name:
        try:
            roxy_file = getattr(file_msg, file_msg.media.value)
            custom_name = roxy_file.file_name or "video.mp4"
            autorename_template = await roxy_bot.get_autorename(user_id)
            if autorename_template:
                from helper.utils import apply_autorename_template
                custom_name = await apply_autorename_template(custom_name, autorename_template)
        except:
            custom_name = "video.mkv"

    summary = _build_subtitle_summary(subtitles)
    sub_count = len(subtitles)
    print(f"[SubtitleDone] user={user_id} | {sub_count} subtitle(s) | uploading with name: {custom_name}")

    from plugins.file_rename import upload_doc

    reply_msg = await client.send_message(
        chat_id,
        text=f"<blockquote>📤 Uᴘʟᴏᴀᴅɪɴɢ ᴡɪᴛʜ {sub_count} Sᴜʙᴛɪᴛʟᴇ(s)...\n\n{summary}\n\n• Fɪʟᴇ Nᴀᴍᴇ :-`{custom_name}`</blockquote>",
        reply_to_message_id=file_msg.id
    )

    mock_update = _build_mock_update(reply_msg, file_msg, media_type, 
                                      type('User', (), {'id': user_id})(), custom_name)
    await upload_doc(client, mock_update)


# ===== MESSAGE HANDLER: Catch subtitle file uploads =====

@Client.on_message(filters.private & filters.document, group=-2)
async def catch_subtitle_file(client, message):
    """
    Catch subtitle file when user is in subtitle-waiting mode.
    Runs at group=-2 (BEFORE rename_start at group=0).
    Downloads the subtitle and prompts for language selection.
    """
    user_id = message.from_user.id
    state = pending_subtitle_state.get(user_id, {})

    # If waiting for custom language text, handle that instead
    # (text messages handled by catch_custom_language below)

    if not state.get('waiting', False):
        return

    if not message.document or not message.document.file_name:
        return

    filename = message.document.file_name

    if not is_subtitle_file(filename):
        await message.reply_text(
            "<blockquote>❌ <b>Not a subtitle file!</b>\n\n"
            f"You sent: <code>{filename}</code>\n\n"
            "Please send a subtitle file with one of these extensions:\n"
            "<code>.srt</code>, <code>.ass</code>, <code>.ssa</code>, "
            "<code>.vtt</code>, <code>.sub</code></blockquote>"
        )
        message.stop_propagation()
        return

    file_msg = state.get('file_msg')
    if not file_msg:
        await message.reply_text(
            "<blockquote>❌ Session expired. Please send the video file again.</blockquote>"
        )
        pending_subtitle_state.pop(user_id, None)
        message.stop_propagation()
        return

    sub_format = get_subtitle_format(filename) or '.srt'

    # Stop waiting for file (will wait for language next)
    state['waiting'] = False
    pending_subtitle_state[user_id] = state

    download_msg = await message.reply_text(
        f"<blockquote>⏳ <b>Downloading subtitle...</b>\n\n📄 {filename}</blockquote>"
    )

    try:
        os.makedirs("downloads", exist_ok=True)
        sub_idx = len(state.get('subtitles', []))
        sub_path = await message.download(
            file_name=f"downloads/{user_id}_{int(time.time())}_sub{sub_idx}{sub_format}"
        )

        if not sub_path or not os.path.exists(sub_path):
            await download_msg.edit_text("<blockquote>❌ Subtitle download failed!</blockquote>")
            state['waiting'] = True
            pending_subtitle_state[user_id] = state
            message.stop_propagation()
            return

        # Store pending subtitle and ask for language
        state['pending_sub_path'] = sub_path
        state['pending_sub_format'] = sub_format
        state['pending_sub_filename'] = filename
        state['waiting_lang'] = True
        pending_subtitle_state[user_id] = state

        await download_msg.edit_text(
            f"<blockquote>✅ <b>Subtitle downloaded!</b>\n\n"
            f"📄 <code>{filename}</code>\n\n"
            f"<b>Select the language for this subtitle:</b></blockquote>",
            reply_markup=_build_language_buttons(sub_idx)
        )

    except Exception as e:
        print(f"[SubtitleAdd] Download error for user {user_id}: {e}")
        import traceback
        traceback.print_exc()
        try:
            await download_msg.edit_text(
                f"<blockquote>❌ <b>Subtitle Error:</b> {str(e)[:200]}</blockquote>"
            )
        except:
            pass
        state['waiting'] = True
        pending_subtitle_state[user_id] = state

    message.stop_propagation()


# ===== MESSAGE HANDLER: Catch custom language text =====

@Client.on_message(filters.private & filters.text, group=-3)
async def catch_custom_language(client, message):
    """
    Catch text messages when user is typing a custom language name.
    Runs at group=-3 (BEFORE everything else).
    """
    user_id = message.from_user.id
    state = pending_subtitle_state.get(user_id, {})

    if not state.get('waiting_custom_lang', False):
        return  # Not waiting for custom language

    # Don't catch commands
    if message.text and message.text.startswith('/'):
        return

    lang_name = message.text.strip()
    if not lang_name or len(lang_name) > 50:
        await message.reply_text(
            "<blockquote>❌ Invalid language name. Please type a short language name (e.g. French, Spanish).</blockquote>"
        )
        message.stop_propagation()
        return

    # Use first 3 chars as lang code (lowercase)
    lang_code = lang_name[:3].lower()
    lang_title = lang_name.strip()

    # Assign to pending subtitle
    pending_path = state.get('pending_sub_path')
    pending_format = state.get('pending_sub_format', '.srt')
    pending_filename = state.get('pending_sub_filename', 'subtitle')

    if not pending_path or not os.path.exists(pending_path):
        await message.reply_text("<blockquote>❌ Subtitle file not found!</blockquote>")
        state['waiting_custom_lang'] = False
        state['waiting'] = True
        pending_subtitle_state[user_id] = state
        message.stop_propagation()
        return

    # Add to subtitle list
    subtitle_entry = {
        'path': pending_path,
        'lang': lang_code,
        'title': lang_title,
        'format': pending_format,
        'filename': pending_filename,
    }
    state.setdefault('subtitles', []).append(subtitle_entry)

    # Clear pending
    state['pending_sub_path'] = None
    state['pending_sub_format'] = None
    state['pending_sub_filename'] = None
    state['waiting_custom_lang'] = False
    state['waiting'] = True
    pending_subtitle_state[user_id] = state

    # Delete user's text message
    try:
        await message.delete()
    except:
        pass

    await _show_waiting_for_subtitle(client, message.chat.id, user_id, state)

    message.stop_propagation()

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
