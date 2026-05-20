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

import os
import re
import logging
from typing import Tuple, Dict
from urllib.parse import unquote
import aiohttp

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of adult content related keywords
ADULT_KEYWORDS = [
    # Common indicators
    'porn', 'xxx', 'adult', 'nsfw', 'hentai', '18+', 'sex', 'sexy', 'hot',
    
    # Video platforms
    'pornhub', 'xvideos', 'xnxx', 'brazzers', 'onlyfans', 'xhamster', 'redtube',
    'youporn', 'javhd', 'pornhd', 'tube8', 'spankbang', 'worldsex', 'porntrex',
    'pornhd', 'javfor', 'javfinder', 'r18', 'dmm',
    
    # Common terms
    'nude', 'nudes', 'nudity', 'naked', 'leaked', 'uncensored', 'explicit',
    'erotic', 'erotica', 'strip', 'striptease', 'stripclub', 'stripper',
    'escort', 'escorts', 'hooker', 'adult_content', 'adult_video', 'adult_film',
    'nsfw_content', 'adult_only', 'x_rated', 'xrated', 'rated_x', 'explicit_content',
    
    # File indicators
    'porn_video', 'adult_video', 'xxx_video', 'nsfw_video', 'adult_film',
    'porn_movie', 'adult_movie', 'xxx_movie', 'nsfw_movie', 'erotic_video',
    'porn_clip', 'adult_clip', 'xxx_clip', 'nsfw_clip', 'erotic_clip',
    
    # Japanese terms
    'jav', 'idol_video', 'gravure', 'oppai', 'ecchi', 'doujin',
    'doujinshi', 'javlib', 'jav_lib', 'r18_video',
    
    # Website indicators
    'adult_site', 'porn_site', 'xxx_site', 'nsfw_site', 'adult_website',
    'porn_website', 'xxx_website', 'nsfw_website', 'adult_forum', 'porn_forum',
    
    # Common prefixes/suffixes
    '_xxx_', '_porn_', '_adult_', '_nsfw_', '_18plus_', '_r18_',
    'xxx_', 'porn_', 'adult_', 'nsfw_', '18plus_', 'r18_',
    '_xxx', '_porn', '_adult', '_nsfw', '_18plus', '_r18',
    
    # Misc indicators
    'onlyfanz', 'fanz', 'fanclub', 'premiumcontent', 'private_content',
    'exclusive_content', 'premium_snap', 'premium_kik', 'premium_telegram',
    
    # Archive related
    'adult_zip', 'porn_zip', 'xxx_zip', 'nsfw_zip', 'adult_rar', 'porn_rar',
    'xxx_rar', 'nsfw_rar', 'adult_7z', 'porn_7z', 'xxx_7z', 'nsfw_7z',
    
    # Common misspellings
    'pronhub', 'prn', 'pr0n', 'p0rn', 'pornn', 'porrn', 'poorn', 'p0rno',
    'pr0no', 'n_s_f_w', 'n_s_f_w_', 'n.s.f.w', 'n.s.f.w.',
    
    # Common concatenations
    'pornvideo', 'xxxvideo', 'adultvideo', 'nsfwvideo', 'pornclip', 'xxxclip',
    'adultclip', 'nsfwclip', 'pornfilm', 'xxxfilm', 'adultfilm', 'nsfwfilm',
    
    # Additional variations
    'onlyf', 'onlyfn', 'onlyfns', 'of_leak', 'of_leaked', 'of_content',
    'privatecontent', 'private_show', 'premium_content', 'vip_content',
    
    # Content descriptions
    'uncensored', 'uncut', 'leaked', 'private', 'exclusive', 'forbidden',
    'banned', 'hidden', 'secret', 'underground', 'restricted', 'explicit',
    
    # File types with adult content
    'adult_archive', 'xxx_archive', 'nsfw_archive', 'porn_archive',
    'adult_folder', 'xxx_folder', 'nsfw_folder', 'porn_folder',
    'adult_collection', 'xxx_collection', 'nsfw_collection', 'porn_collection',
    
    # Common combinations
    'adult_pack', 'xxx_pack', 'nsfw_pack', 'porn_pack',
    'adult_set', 'xxx_set', 'nsfw_set', 'porn_set',
    'adult_dump', 'xxx_dump', 'nsfw_dump', 'porn_dump',
    
    # Additional indicators
    'naughty', 'dirty', 'filthy', 'lewd', 'perverted', 'kinky',
    'obscene', 'indecent', 'inappropriate', 'mature_content',
    
    # URL patterns
    'adult_link', 'xxx_link', 'nsfw_link', 'porn_link',
    'adult_url', 'xxx_url', 'nsfw_url', 'porn_url',
    'adult_download', 'xxx_download', 'nsfw_download', 'porn_download'
]

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


def contains_adult_keywords(text: str) -> bool:
    """Check if text contains any adult content related keywords"""
    text = text.lower()
    return any(keyword in text for keyword in ADULT_KEYWORDS)

async def download_file_head(url: str) -> str:
    """Get filename from URL without downloading entire file"""
    async with aiohttp.ClientSession() as session:
        async with session.head(url, allow_redirects=True) as response:
            if 'Content-Disposition' in response.headers:
                cd = response.headers['Content-Disposition']
                filename = re.findall("filename=(.+)", cd)
                if filename:
                    return unquote(filename[0].strip('"'))
            return os.path.basename(unquote(url))

async def check_file_safety(file_path: str, file_name: str = None) -> Tuple[bool, str]:
    """
    Check if file is safe by checking filename for adult keywords.
    Returns: (is_safe, message)
    """
    if file_name:
        file_name_lower = file_name.lower()
        if contains_adult_keywords(file_name_lower):
            return False, "File name contains adult content keywords"
    
    if file_path:
        file_path_lower = os.path.basename(file_path).lower()
        if contains_adult_keywords(file_path_lower):
            return False, "File name contains adult content keywords"
    
    return True, "File is safe"

async def validate_url_file(url: str) -> Tuple[bool, str]:
    """Validate a URL's filename for adult content"""
    try:
        if contains_adult_keywords(url.lower()):
            return False, "URL contains adult content keywords"

        try:
            filename = await download_file_head(url)
            if contains_adult_keywords(filename.lower()):
                return False, "URL filename contains adult content keywords"
        except:
            pass

        return True, "URL is safe"
    except Exception as e:
        logger.error(f"URL validation error: {e}")
        return False, "URL could not be validated - blocked for safety"

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
