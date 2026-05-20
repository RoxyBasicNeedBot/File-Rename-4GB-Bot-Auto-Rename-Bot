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

# Special Thanks To (https://github.com/JayMahakal98)

# extra imports
import math, time, re, datetime, pytz, os, random
from config import Config, roxy 

# pyrogram imports
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:        
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        # Hexagon progress bar (⬢ filled, ⬡ empty)
        progress = "{0}{1}".format(
            ''.join(["⬢" for i in range(math.floor(percentage / 5))]),
            ''.join(["⬡" for i in range(20 - math.floor(percentage / 5))])
        )            
        tmp = roxy.ROXY_PROGRESS.format( 
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),            
            estimated_total_time if estimated_total_time != '' else "0 s",
            progress  # {5} - hexagon progress bar
        )
        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",               
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]])                                               
            )
        except:
            pass

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

async def send_log(b, u):
    if Config.LOG_CHANNEL:
        curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        log_message = (
            "**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\n"
            f"Uꜱᴇʀ: {u.mention}\n"
            f"Iᴅ: `{u.id}`\n"
            f"Uɴ: @{u.username}\n\n"
            f"Dᴀᴛᴇ: {curr.strftime('%d %B, %Y')}\n"
            f"Tɪᴍᴇ: {curr.strftime('%I:%M:%S %p')}\n\n"
            f"By: {b.mention}"
        )
        await b.send_message(Config.LOG_CHANNEL, log_message)

async def get_seconds_first(time_string):
    conversion_factors = {
        's': 1,
        'min': 60,
        'hour': 3600,
        'day': 86400,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    parts = time_string.split()
    total_seconds = 0

    for i in range(0, len(parts), 2):
        value = int(parts[i])
        unit = parts[i+1].rstrip('s')  # Remove 's' from unit
        total_seconds += value * conversion_factors.get(unit, 0)

    return total_seconds

async def get_seconds(time_string):
    conversion_factors = {
        's': 1,
        'min': 60,
        'hour': 3600,
        'day': 86400,
        'month': 86400 * 30,
        'year': 86400 * 365
    }

    total_seconds = 0
    pattern = r'(\d+)\s*(\w+)'
    matches = re.findall(pattern, time_string)

    for value, unit in matches:
        total_seconds += int(value) * conversion_factors.get(unit, 0)

    return total_seconds

async def add_prefix_suffix(input_string, prefix='', suffix=''):
    pattern = r'(?P<filename>.*?)(\.\w+)?$'
    match = re.search(pattern, input_string)
    
    if match:
        filename = match.group('filename')
        extension = match.group(2) or ''
        
        prefix_str = f"{prefix} " if prefix else ""
        suffix_str = f" {suffix}" if suffix else ""
        
        return f"{prefix_str}{filename}{suffix_str}{extension}"
    else:
        return input_string

async def remove_path(*paths):
    for path in paths:
        if path and os.path.lexists(path):
            os.remove(path)

async def metadata_text(metadata_text):
    author = None
    title = None
    video_title = None
    audio_title = None
    subtitle_title = None

    flags = [i.strip() for i in metadata_text.split('--')]
    for f in flags:
        if "change-author" in f:

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

            author = f[len("change-author"):].strip()
        if "change-title" in f:
            title = f[len("change-title"):].strip()
        if "change-video-title" in f:
            video_title = f[len("change-video-title"):].strip()
        if "change-audio-title" in f:
            audio_title = f[len("change-audio-title"):].strip()
        if "change-subtitle-title" in f:
            subtitle_title = f[len("change-subtitle-title"):].strip()

    return author, title, video_title, audio_title, subtitle_title

reactions = [
    "👍", "👎", "❤️", "🔥", 
    "🥰", "👏", "😁", "🤔",    
    "🎉", "🤩", "🍾", "😈",
    "🙏", "👌", "🕊", "🤡",
    "🥱", "😍", "🐳", "🤮",
    "🔥", "🌚", "🌭", "💯",
    "🤣", "⚡️", "🍌", "🏆",
    "💔", "🤨", "😐", "🍓",        
    "😴", "🤓", "👻", "🤪",
    "👨‍💻", "👀", "🎃", "🙈",
    "😇", "🤝", "✍️", "🗿",
    "🤗", "🫡", "🎅", "🎄",          
    "🆒", "💘", "🙉", "🦄",
    "😘", "💊", "🙊", "😎",
    "👾", "🤷‍♂️", "🤷", "🤷‍♀️",
    "💩", "🖕", "🤬", "😡",
    "😱"
]

async def send_reaction(client, message):
    try:
        random_emoji = random.choice(reactions)
        await client.send_reaction(
            chat_id=message.chat.id,
            message_id=message.id,
            emoji=random_emoji,
            big=True
        )
    except Exception as e:
        print(f"Error sending reaction: {e}")

def extract_metadata_from_filename(filename):
    """
    Extract metadata values from filename for caption formatting.
    Returns a dict with: episode, season, chapter, quality, audio
    """
    patterns = {
        'episode': r'(?:E|EP|Episode)[.\s-]*(\d+)',
        'season': r'(?:S|Season)[.\s-]*(\d+)',
        'chapter': r'(?:C|Ch|Chapter)[.\s-]*(\d+)',
        'quality': r'(480p|720p|1080p|2160p|4K|HDRip|WEBRip|BluRay|HDTV|DVDRip)',
        'audio': r'(Hindi|English|Dual|Multi|Japanese|Korean|Tamil|Telugu|HINDI|ENG|JAP)',
    }
    
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            result[key] = match.group(1)
        else:
            result[key] = ''
    
    return result


async def apply_autorename_template(original_filename, template):
    """
    Extract metadata from original filename and apply to template.
    Supports: {episode}, {season}, {chapter}, {quality}, {audio}
    Enhanced: {title}, {year}, {genres}, {source}, {codec}, {language}, {hdr}, {release}
    """
    # Extract extension from original filename
    name_part, ext = os.path.splitext(original_filename)
    
    # Use advanced detection engine if available
    try:
        from helper.tmdb_detect import analyze_filename
        detected = analyze_filename(original_filename)
    except ImportError:
        detected = {}
    
    # Basic patterns (original) + advanced detection (new)
    patterns = {
        'episode': r'(?:E|EP|Episode)[.\s-]*(\d+)',
        'season': r'(?:S|Season)[.\s-]*(\d+)',
        'chapter': r'(?:C|Ch|Chapter)[.\s-]*(\d+)',
        'quality': r'(480p|720p|1080p|2160p|4K|HDRip|WEBRip|BluRay|HDTV|DVDRip)',
        'audio': r'(Hindi|English|Dual|Multi|Japanese|Korean|Tamil|Telugu|HINDI|ENG|JAP)',
    }
    
    result = template
    for key, pattern in patterns.items():
        match = re.search(pattern, original_filename, re.IGNORECASE)
        if match:
            value = match.group(1)
            result = result.replace('{' + key + '}', value)
        else:
            # Use advanced detection as fallback
            adv_value = detected.get(key, '')
            result = result.replace('{' + key + '}', adv_value)
    
    # New advanced placeholders from detection engine
    advanced_keys = {
        'title': detected.get('title', ''),
        'year': detected.get('year', ''),
        'source': detected.get('source', ''),
        'codec': detected.get('codec', ''),
        'language': detected.get('language', ''),
        'hdr': detected.get('hdr', ''),
        'release': detected.get('release_group', ''),
    }
    for key, value in advanced_keys.items():
        result = result.replace('{' + key + '}', value)
    
    # Clean up any double spaces
    result = ' '.join(result.split())
    
    # Add extension if not present in template
    if ext and not result.lower().endswith(ext.lower()):
        result = result + ext
    
    return result


def sanitize_filename(filename, max_length=200):
    """
    Sanitize and truncate filename to safe length.
    Removes problematic characters and limits filename to max_length bytes.
    
    Args:
        filename: Original filename
        max_length: Maximum length for filename (default 200 to be safe for most filesystems)
    
    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed_file"
    
    # Replace problematic characters with underscores
    invalid_chars = [':', '<', '>', '|', '?', '*', '"', '─', '‣', '/', '\\', '\n', '\r', '\t']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Replace multiple spaces with single space
    filename = ' '.join(filename.split())
    
    # Remove multiple consecutive underscores
    while '__' in filename:
        filename = filename.replace('__', '_')
    
    # Get extension and base name
    if '.' in filename:
        parts = filename.rsplit('.', 1)
        base = parts[0]
        ext = '.' + parts[1]
    else:
        base = filename
        ext = ''
    
    # Truncate if too long (preserve extension)
    # Account for UTF-8 encoding where chars can be multiple bytes
    if len(filename.encode('utf-8')) > max_length:
        # Leave room for extension plus some safety margin
        max_base_bytes = max_length - len(ext.encode('utf-8')) - 10
        
        # Truncate base name byte by byte
        encoded_base = base.encode('utf-8')
        if len(encoded_base) > max_base_bytes:
            # Decode back to handle multi-byte chars properly
            truncated = encoded_base[:max_base_bytes].decode('utf-8', errors='ignore')
            base = truncated.rstrip('_').rstrip()
        
        filename = base + ext
    
    return filename.strip() if filename.strip() else "unnamed_file"



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
