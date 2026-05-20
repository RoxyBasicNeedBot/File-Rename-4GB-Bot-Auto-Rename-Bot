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

import re, os, time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

id_pattern = re.compile(r'^.\d+$') 
class Config(object):
    # roxy_bot client config
    # API credentials from Telegram (get from my.telegram.org)
    API_ID = os.environ.get("API_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    # Bot token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
    BOT = None

    # premium account string session required 😢 
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    
    # database config
    DB_NAME = os.environ.get("DB_NAME", "Roxy_Rename_Bot")     
    DB_URL = os.environ.get("DB_URL", "")
 
    # Wallhaven API - can add multiple keys separated by space for rotation
    ROXY_PIC_API = os.environ.get("ROXY_PIC_API", "")
    ROXY_PIC_API_KEYS = ROXY_PIC_API.split()  # Split by space to get list of API keys
    WALLHAVEN_API_URL = "https://wallhaven.cc/api/v1/search"
    
    # Split admin IDs; default to empty string if not set
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()]
    
    # Log channel for bot tracking events
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # free upload limit 
    FREE_UPLOAD_LIMIT = 2147483648 # calculation 2*1024*1024*1024=results

    # premium mode feature ✅
    UPLOAD_LIMIT_MODE = True 
    PREMIUM_MODE = True 
    
    # TMDb API Key (free: https://www.themoviedb.org/settings/api)
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
    
    # TMDb Supported Languages
    TMDB_LANGUAGES = [
        ("en-US", "English 🇬🇧"),
        ("hi-IN", "Hindi 🇮🇳"),
        ("ta-IN", "Tamil 🇮🇳"),
        ("te-IN", "Telugu 🇮🇳"),
        ("ja-JP", "Japanese 🇯🇵"),
        ("ko-KR", "Korean 🇰🇷"),
        ("de-DE", "Deutsch 🇩🇪"),
        ("es-ES", "Español 🇪🇸"),
        ("fr-FR", "Français 🇫🇷"),
        ("ar-SA", "Arabic 🇸🇦"),
        ("zh-CN", "Chinese 🇨🇳"),
        ("ru-RU", "Russian 🇷🇺"),
    ]
    
    # Premium Plan Tiers — features list controls what each plan can access
    # features: rename, autorename, subtitle, tmdb_auto, tmdb_thumb, compress, watermark, trim, screenshot, mkv_to_mp4, auto_delete
    PREMIUM_PLANS = {
        "Free":     {"limit": 2 * 1024**3,   "features": ["rename", "autorename", "tmdb_auto"]},
        "Trial":    {"limit": 32 * 1024**3,  "features": ["rename", "autorename", "subtitle", "tmdb_auto", "tmdb_thumb", "compress", "trim"]},
        "Bronze":   {"limit": 10 * 1024**3,  "features": ["rename", "autorename", "subtitle", "tmdb_auto", "tmdb_thumb"]},
        "Silver":   {"limit": 25 * 1024**3,  "features": ["rename", "autorename", "subtitle", "tmdb_auto", "tmdb_thumb", "compress"]},
        "Gold":     {"limit": 50 * 1024**3,  "features": ["rename", "autorename", "subtitle", "tmdb_auto", "tmdb_thumb", "compress", "watermark", "trim"]},
        "Platinum": {"limit": 100* 1024**3,  "features": ["all"]},
        "Diamond":  {"limit": -1,            "features": ["all"]},
    }
    
    # NSFW Content Scanning
    # ✅ Set True to ENABLE NSFW scanning, False to DISABLE it
    NSFW_SCAN_ENABLED = True  # Change to True to turn ON nsfw filter
    NSFW_API_URL = os.environ.get("NSFW_API_URL", "https://nsfw-api-blocker.onrender.com/detect/image")
    NSFW_API_KEY = os.environ.get("NSFW_API_KEY", "")
    NSFW_VIDEO_SIZE_LIMIT = int(os.environ.get("NSFW_VIDEO_SIZE_LIMIT", str(200 * 1024 * 1024)))  # 200MB
    NSFW_FRAME_COUNT = int(os.environ.get("NSFW_FRAME_COUNT", "10"))  # Extract 10 frames
    
    # Auto-delete output files (hours)
    AUTO_DELETE_HOURS = int(os.environ.get("AUTO_DELETE_HOURS", "4"))  # 4 hours
    
    # Contact bot for ban appeals  
    CONTACT_BOT = os.environ.get("CONTACT_BOT", "@roxycontactbot")
    
    #force subs
    try:
        FORCE_SUB = int(os.environ.get("FORCE_SUB", "0")) 
    except:
        FORCE_SUB = os.environ.get("FORCE_SUB", "")

    try:
        FORCE_SUB2 = int(os.environ.get("FORCE_SUB2", "0")) 
    except:
        FORCE_SUB2 = os.environ.get("FORCE_SUB2", "")
        
    # force sub image
    FORCE_SUB_IMAGE = os.environ.get("FORCE_SUB_IMAGE", "")
        
    # wes response configuration     
    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()

class roxy(object):
    START_TXT = """<blockquote><b>ʜᴇʏ, {} ⚡️

🌺 GULMHOR ʀᴇɴᴀᴍᴇ ʙᴏᴛ

⚡️ ꜰᴀꜱᴛ ꜱᴇʀᴠᴇʀꜱ | ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ | TMDb | ᴍᴇᴛᴀᴅᴀᴛᴀ ⚡️

⚙️ ʙʏ: 𝕽𝕺𝕏𝕐•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️</b></blockquote>
"""

    ABOUT_TXT = """<blockquote><b>📖 Aʙᴏᴜᴛ Tʜɪꜱ Bᴏᴛ

✘ Bᴏᴛ: {}
✘ Dᴇᴠᴇʟᴏᴘᴇʀ: {}
✘ Pʀᴏɢʀᴀᴍᴇʀ: {}
✘ Lɪʙʀᴀʀʏ: {}
✘ Lᴀɴɢᴜᴀɢᴇ: {}
✘ Dᴀᴛᴀʙᴀsᴇ: {}
✘ Nᴇᴡ: Sᴜʙᴛɪᴛʟᴇ Mᴜx, Wᴀᴛᴇʀᴍᴀʀᴋ, Cᴏᴍᴘʀᴇss, Tʀɪᴍ
✘ Vᴇʀsɪᴏɴ: <a href=https://github.com/RoxyBasicNeedBot>{}</a>

⚙️ ʙʏ: @roxybasicneedbot1</b></blockquote>"""

    HELP_TXT = """<blockquote>
 <b>•></b> /start Tʜᴇ Bᴏᴛ.
 
 ✏️ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
 <b>•></b> Sᴇɴᴅ Aɴy Fɪʟᴇ Aɴᴅ Tyᴩᴇ Nᴇᴡ Fɪʟᴇ Nɴᴀᴍᴇ \nAɴᴅ Aᴇʟᴇᴄᴛ Tʜᴇ Fᴏʀᴍᴀᴛ [ document, video, audio ].           
 ℹ️ 𝗔𝗻y 𝗢𝘁𝗵𝗲𝗿 𝗛𝗲𝗹𝗽 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 :- <a href=https://t.me/roxybasicneed1>ROXY CHAT ⚡️</a>
 </blockquote>"""

    UPGRADE_PREMIUM= """<blockquote>
     •⪼ ★𝘗𝘭𝘢𝘯𝘴    -  ⏳𝘋𝘢𝘵𝘦 - 💸𝘗𝘳𝘪𝘤𝘦 
     •⪼ 🥉𝘉𝘳𝘰𝘯𝘻𝘦  -   3𝘥𝘢𝘺𝘴 -   19
     •⪼ 🥈𝘚𝘪𝘭𝘷𝘦𝘳   -   7𝘥𝘢𝘺𝘴 -   39
     •⪼ 🥇𝘎𝘰𝘭𝘥    -  15𝘥𝘢𝘺𝘴 -   89
     •⪼ 🏆𝘗𝘭𝘢𝘵𝘪𝘯𝘶𝘮 -  1𝘮𝘰𝘯𝘵𝘩 -  179
     •⪼ 💎𝘋𝘪𝘢𝘮𝘰𝘯𝘥 -  2𝘮𝘰𝘯𝘵𝘩 -  239
     
     - ⚡ 𝘋𝘢𝘪𝘭𝘺 𝘜𝘱𝘭𝘰𝘢𝘥 𝘓𝘪𝘮𝘪𝘵 𝘜𝘯𝘭𝘪𝘮𝘪𝘵𝘦𝘥
     - 🎨 𝘈𝘥𝘥 𝘊𝘶𝘴𝘵𝘰𝘮 𝘞𝘢𝘵𝘦𝘳𝘮𝘢𝘳𝘬 𝘵𝘰 𝘝𝘪𝘥𝘦𝘰𝘴
     - ✂️ 𝘝𝘪𝘥𝘦𝘰 𝘛𝘳𝘪𝘮𝘮𝘪𝘯𝘨 & 𝘊𝘰𝘮𝘱𝘳𝘦𝘴𝘴𝘪𝘰𝘯
     - 🎵 𝘌𝘹𝘵𝘳𝘢𝘤𝘵 𝘈𝘶𝘥𝘪𝘰 & 𝘈𝘥𝘥 𝘚𝘶𝘣𝘵𝘪𝘵𝘭𝘦𝘴
     - 🎊 𝘋𝘪𝘴𝘤𝘰𝘶𝘯𝘵 𝘈𝘭𝘭 𝘗𝘭𝘢𝘯 ₹9
     
     ⚠️ <b>Only Google Play Redeem Code Accepted</b>
     </blockquote>"""

    UPGRADE_PLAN= """<blockquote>
     •⪼ ★𝘗𝘭𝘢𝘯𝘴    -  ⏳𝘋𝘢𝘵𝘦 - 💸𝘗𝘳𝘪𝘤𝘦 
     •⪼ 🥉𝘉𝘳𝘰𝘯𝘻𝘦  -   3𝘥𝘢𝘺𝘴 -   19
     •⪼ 🥈𝘚𝘪𝘭𝘷𝘦𝘳   -   7𝘥𝘢𝘺𝘴 -   39
     •⪼ 🥇𝘎𝘰𝘭𝘥    -  15𝘥𝘢𝘺𝘴 -   89
     •⪼ 🏆𝘗𝘭𝘢𝘵𝘪𝘯𝘶𝘮 -  1𝘮𝘰𝘯𝘵𝘩 -  179
     •⪼ 💎𝘋𝘪𝘢𝘮𝘰𝘯𝘥 -  2𝘮𝘰𝘯𝘵𝘩 -  239
     
     - ⚡ 𝘋𝘢𝘪𝘭𝘺 𝘜𝘱𝘭𝘰𝘢𝘥 𝘓𝘪𝘮𝘪𝘵 𝘜𝘯𝘭𝘪𝘮𝘪𝘵𝘦𝘥
     - 🎨 𝘈𝘥𝘥 𝘊𝘶𝘴𝘵𝘰𝘮 𝘞𝘢𝘵𝘦𝘳𝘮𝘢𝘳𝘬 𝘵𝘰 𝘝𝘪𝘥𝘦𝘰𝘴
     - ✂️ 𝘝𝘪𝘥𝘦𝘰 𝘛𝘳𝘪𝘮𝘮𝘪𝘯𝘨 & 𝘊𝘰𝘮𝘱𝘳𝘦𝘴𝘴𝘪𝘰𝘯
     - 🎵 𝘌𝘹𝘵𝘳𝘢𝘤𝘵 𝘈𝘶𝘥𝘪𝘰 & 𝘈𝘥𝘥 𝘚𝘶𝘣𝘵𝘪𝘵𝘭𝘦𝘴
     - 🎊 𝘋𝘪𝘴𝘤𝘰𝘶𝘯𝘵 𝘈𝘭𝘭 𝘗𝘭𝘢𝘯 ₹9
     
     ⚠️ <b>Only Google Play Redeem Code Accepted</b>
     </blockquote>"""

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

    THUMBNAIL = """<blockquote>
 🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>
 
 <b>•></b> Sᴇɴᴅ Aɴy Pʜᴏᴛᴏ Tᴏ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟy Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ.
 <b>•></b> /del_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Oʟᴅ Tʜᴜᴍʙɴɪʟᴇ.
 <b>•></b> /view_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴɪʟᴇ.
 </blockquote>"""
    CAPTION= """<blockquote><b>📑 Cᴜsᴛᴏᴍ Cᴀᴘᴛɪᴏɴ

✘ /set_caption - Sᴇᴛ ᴀ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ
✘ /see_caption - Vɪᴇᴡ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ
✘ /del_caption - Dᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ

📝 Exᴀᴍᴘʟᴇ:</b>
<code>/set_caption 📕 {filename}
💾 Size: {filesize}
⏰ Duration: {duration}
@roxybasicneedbot1</code>
</blockquote>"""
    BOT_STATUS = """<blockquote>
 ⚡️ ʙᴏᴛ sᴛᴀᴛᴜs ⚡️
 
 ⌚️ ʙᴏᴛ ᴜᴩᴛɪᴍᴇ: `{}`
 👭 ᴛᴏᴛᴀʟ ᴜsᴇʀꜱ: `{}`
 💸 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs: `{}`
 ֍ ᴜᴘʟᴏᴀᴅ: `{}`
 ⊙ ᴅᴏᴡɴʟᴏᴀᴅ: `{}`
 </blockquote>"""
    LIVE_STATUS = """<blockquote>
 ⚡ ʟɪᴠᴇ sᴇʀᴠᴇʀ sᴛᴀᴛᴜs ⚡
 
 ᴜᴘᴛɪᴍᴇ: `{}`
 ᴄᴘᴜ: `{}%`
 ʀᴀᴍ: `{}%` 
 ᴛᴏᴛᴀʟ ᴅɪsᴋ: `{}`
 ᴜsᴇᴅ sᴘᴀᴄᴇ: `{} {}%`
 ғʀᴇᴇ sᴘᴀᴄᴇ: `{}`
 ᴜᴘʟᴏᴀᴅ: `{}`
 ᴅᴏᴡɴʟᴏᴀᴅ: `{}`
 V𝟹.𝟶.𝟶 [STABLE]
 </blockquote>"""
    ROXY_METADATA = """<blockquote>
 ❪ SET CUSTOM METADATA ❫
 
 - /metadata - Tᴏ Sᴇᴛ & Cʜᴀɴɢᴇ ʏᴏᴜʀ ᴍᴇᴛᴀᴅᴀᴛᴀ ᴄᴏᴅᴇ
 
 ☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-
 
 `--change-title @roxybasicneedbot1
 --change-video-title @roxybasicneedbot1
 --change-audio-title @roxybasicneedbot1
 --change-subtitle-title @roxybasicneedbot1
 --change-author @roxybasicneedbot1`
 
 📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛ. @roxybasicneedbot1
 </blockquote>"""
    
    CUSTOM_FILE_NAME = """<blockquote>
 <u>🖋️ Custom File Name</u>
 
 you can pre-add a prefix and suffix along with your new filename
 
 ➢ /set_prefix - To add a prefix along with your _filename.
 ➢ /see_prefix - Tᴏ Sᴇᴇ Yᴏᴜʀ Pʀᴇғɪx !!
 ➢ /del_prefix - Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Pʀᴇғɪx !!
 ➢ /set_suffix - To add a suffix along with your filename_.
 ➢ /see_suffix - Tᴏ Sᴇᴇ Yᴏᴜʀ Sᴜғғɪx !!
 ➢ /del_suffix - Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Sᴜғғɪx !!
 
 Exᴀᴍᴩʟᴇ:- `/set_suffix @roxybasicneedbot1`
 Exᴀᴍᴩʟᴇ:- `/set_prefix @roxybasicneedbot1`
 </blockquote>"""
    
    AUTORENAME_TXT = """<blockquote>
 📝 <b><u>Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Tᴇᴍᴘʟᴀᴛᴇ</u></b>
 
 Sᴇᴛ ᴀ ᴛᴇᴍᴘʟᴀᴛᴇ ᴛᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ꜰɪʟᴇs.
 
 ➢ /autorename - Sᴇᴛ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ
 ➢ /see_autorename - Vɪᴇᴡ ʏᴏᴜʀ ᴛᴇᴍᴘʟᴀᴛᴇ
 ➢ /del_autorename - Dᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴛᴇᴍᴘʟᴀᴛᴇ
 
 <b>Bᴀsɪᴄ Pʟᴀᴄᴇʜᴏʟᴅᴇʀs:</b>
 • {episode} - Ep number
 • {season} - S0 number  
 • {chapter} - Chapter number
 • {quality} - Video quality (480p, 720p, etc.)
 • {audio} - Audio language
 
 <b>Aᴅᴠᴀɴᴄᴇᴅ Pʟᴀᴄᴇʜᴏʟᴅᴇʀs (TMDb):</b>
 • {title} - Detected title
 • {year} - Release year
 • {source} - Source (BluRay, WEB-DL)
 • {codec} - Codec (x264, x265)
 • {language} - Language (Hindi, English)
 • {hdr} - HDR format
 • {release} - Release group
 
 <b>Exᴀᴍᴩʟᴇs:</b>
 ➥ Exᴀᴍᴘʟᴇ1: <code>/autorename [WF] [C{chapter}] One Pie @roxybasicneedbot1</code>

 ➤ Exᴀᴍᴘʟᴇ2: <code>/autorename [S{season} E{episode}] One Pie [{quality}] [{audio}]</code>

 ➤ Exᴀᴍᴘʟᴇ3: <code>/autorename {title} ({year}) [{quality}] [{source}] [{codec}]</code>
 
 Note: Don't put .mkv or .mp4 at the end.
 Tʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴜsᴇ ᴛʜɪs ᴛᴇᴍᴘʟᴀᴛᴇ ᴛᴏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ғɪʟᴇs ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.
 </blockquote>"""
    
    #⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
    # ᴡʜᴏᴇᴠᴇʀ ɪs ᴅᴇᴘʟᴏʏɪɴɢ ᴛʜɪs ʀᴇᴘᴏ ɪs ᴡᴀʀɴᴇᴅ ⚠️ ᴅᴏ ɴᴏᴛ ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛs ɢɪᴠᴇɴ ɪɴ ᴛʜɪs ʀᴇᴘᴏ #ғɪʀsᴛ ᴀɴᴅ ʟᴀsᴛ ᴡᴀʀɴɪɴɢ ⚠️
    DEV_TXT = """<blockquote><b><u>Sᴩᴇᴄɪᴀʟ Tʜᴀɴᴋꜱ & Dᴇᴠᴇʟᴏᴩᴇʀꜱ</b></u>
     
 » 𝗦𝗢𝗨𝗥𝗖𝗘 𝗖𝗢𝗗𝗘 : <a href=https://github.com/RoxyBasicNeedBot>RoxyBasicNeedBot</a> </blockquote>"""
    # ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

    SEND_METADATA = """<blockquote>
 ❪ SET CUSTOM METADATA ❫
 
 ☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-
 
 `--change-title @roxybasicneedbot1
 --change-video-title @roxybasicneedbot1
 --change-audio-title @roxybasicneedbot1
 --change-subtitle-title @roxybasicneedbot1
 --change-author @roxybasicneedbot1`
 
 📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛ. @roxybasicneedbot1
 </blockquote>"""
    
    BANNED_TXT = """<blockquote><b>Sorry Sir, 😔 You are Banned!..</b>

📝 <b>Reason:</b> {}

📞 <b>Please Contact - @roxycontactbot</b></blockquote>

<blockquote><b><u>⚠️ 18+ Content Strictly Prohibited ⚠️</u></b></blockquote>"""

    AUTO_DELETE_TXT = """<blockquote>⏳ <b>Auto-Delete Notice</b>

This file will be <b>automatically deleted in {} hours</b>.

📥 <b>Please forward this file to save it!</b>

💡 Forward to "Saved Messages" or any chat to keep it permanently.</blockquote>"""

    ROXY_PROGRESS = """<blockquote><b>📤 Rᴏxʏ Pʀᴏᴄᴇssɪɴɢ...

{5}

✘ Sɪᴢᴇ: {1} | {2}
✘ Dᴏɴᴇ: {0}%
✘ Sᴘᴇᴇᴅ: {3}/s
✘ ETA: {4}</b></blockquote>"""

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
