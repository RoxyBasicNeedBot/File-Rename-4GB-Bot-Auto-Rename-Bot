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

# Auto-Detection Matrix — Advanced filename parser
# Extracts: title, year, season, episode, quality, codec, audio, source, type
# Handles dots, underscores, brackets, and complex naming patterns

import re
import os


def analyze_filename(filename):
    """
    Advanced filename analysis — extracts structured metadata from media filenames.
    
    Handles patterns like:
        - Avengers.Endgame.2019.1080p.BluRay.x265-RELEASE.mkv
        - The.Office.S03E14.720p.WEB-DL.mp4
        - [SubGroup] One Piece - 1050 [1080p].mkv
        - Movie.Name.2024.HDTV.Hindi.Dual.Audio.mkv
        
    Returns:
        dict with detected metadata fields
    """
    if not filename:
        return _empty_result()
    
    # Remove extension
    name_part = os.path.splitext(filename)[0]
    
    # Normalize separators: dots, underscores → spaces (but preserve S01E05 patterns)
    normalized = _normalize_name(name_part)
    
    result = {
        "original_filename": filename,
        "title": "",
        "year": "",
        "season": "",
        "episode": "",
        "quality": "",
        "codec": "",
        "audio": "",
        "source": "",
        "hdr": "",
        "language": "",
        "release_group": "",
        "type": "movie",  # default, will be changed if season/episode found
        "is_subtitle": _is_subtitle(filename),
    }
    
    # Extract structured metadata with regex
    result["year"] = _extract_year(normalized)
    result["season"] = _extract_season(normalized)
    result["episode"] = _extract_episode(normalized)
    result["quality"] = _extract_quality(normalized)
    result["codec"] = _extract_codec(normalized)
    result["audio"] = _extract_audio(normalized)
    result["source"] = _extract_source(normalized)
    result["hdr"] = _extract_hdr(normalized)
    result["language"] = _extract_language(normalized)
    result["release_group"] = _extract_release_group(name_part)
    
    # Determine type: if season or episode found → series
    if result["season"] or result["episode"]:
        result["type"] = "series"
    
    # Extract clean title (everything before the first metadata tag)
    result["title"] = _extract_title(normalized, result)
    
    return result


def _empty_result():
    return {
        "original_filename": "",
        "title": "",
        "year": "",
        "season": "",
        "episode": "",
        "quality": "",
        "codec": "",
        "audio": "",
        "source": "",
        "hdr": "",
        "language": "",
        "release_group": "",
        "type": "movie",
        "is_subtitle": False,
    }


def _normalize_name(name):
    """Replace dots and underscores with spaces, but preserve S01E05 patterns."""
    # First protect season/episode patterns
    protected = re.sub(r'([Ss]\d{1,2})[.]?([Ee]\d{1,3})', r'\1\2', name)
    # Replace dots and underscores with spaces
    result = protected.replace('.', ' ').replace('_', ' ')
    # Remove content in square brackets at start (like [SubGroup])
    result = re.sub(r'^\[.*?\]\s*', '', result)
    # Clean up multiple spaces
    result = ' '.join(result.split())
    return result


def _extract_year(text):
    """Extract 4-digit year (1950-2030 range)."""
    # Look for year in parentheses first: (2024)
    match = re.search(r'\((\d{4})\)', text)
    if match and 1950 <= int(match.group(1)) <= 2030:
        return match.group(1)
    
    # Look for standalone year
    match = re.search(r'(?<!\d)((?:19|20)\d{2})(?!\d)', text)
    if match and 1950 <= int(match.group(1)) <= 2030:
        return match.group(1)
    
    return ""


def _extract_season(text):
    """Extract season number."""
    # S01, S1, Season 1, Season 01
    match = re.search(r'[Ss](\d{1,2})(?:[Ee]\d)', text)
    if match:
        return match.group(1).zfill(2)
    
    match = re.search(r'[Ss]eason\s*(\d{1,2})', text, re.IGNORECASE)
    if match:
        return match.group(1).zfill(2)
    
    # Standalone S01 without episode
    match = re.search(r'[Ss](\d{1,2})(?:\s|$)', text)
    if match:
        return match.group(1).zfill(2)
    
    return ""


def _extract_episode(text):
    """Extract episode number."""
    # E05, E005, EP05, Episode 05
    match = re.search(r'[Ee][Pp]?(\d{1,4})', text)
    if match:
        return match.group(1).zfill(2)
    
    match = re.search(r'[Ee]pisode\s*(\d{1,4})', text, re.IGNORECASE)
    if match:
        return match.group(1).zfill(2)
    
    # Anime style: " - 1050 " or " - 05 "

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

    match = re.search(r'\s-\s(\d{1,4})(?:\s|$|\[)', text)
    if match:
        return match.group(1).zfill(2)
    
    # Chapter style: C05, Ch05, Chapter 05
    match = re.search(r'[Cc](?:h|hapter)?\s*(\d{1,4})', text)
    if match:
        return match.group(1).zfill(2)
    
    return ""


def _extract_quality(text):
    """Extract video quality/resolution."""
    patterns = [
        (r'2160[pP]|4[kK]|UHD', '2160p'),
        (r'1080[pP]|FHD', '1080p'),
        (r'720[pP]|HD(?!TV|Rip)', '720p'),
        (r'480[pP]|SD', '480p'),
        (r'360[pP]', '360p'),
    ]
    for pattern, quality in patterns:
        if re.search(pattern, text):
            return quality
    return ""


def _extract_codec(text):
    """Extract video codec."""
    patterns = [
        (r'[xX]265|[Hh]\.?265|HEVC', 'x265'),
        (r'[xX]264|[Hh]\.?264|AVC', 'x264'),
        (r'AV1', 'AV1'),
        (r'VP9', 'VP9'),
        (r'MPEG-?4', 'MPEG4'),
    ]
    for pattern, codec in patterns:
        if re.search(pattern, text):
            return codec
    return ""


def _extract_audio(text):
    """Extract audio format/codec."""
    patterns = [
        (r'DTS-?HD(?:\s*MA)?', 'DTS-HD MA'),
        (r'DTS', 'DTS'),
        (r'DD[P+]?\s*5\.?1|Dolby\s*Digital\s*Plus', 'DD+ 5.1'),
        (r'DD\s*5\.?1|AC-?3\s*5\.?1', 'DD 5.1'),
        (r'AC-?3|Dolby\s*Digital', 'AC3'),
        (r'AAC\s*5\.?1', 'AAC 5.1'),
        (r'AAC\s*2\.?0|AAC', 'AAC'),
        (r'FLAC', 'FLAC'),
        (r'Atmos', 'Atmos'),
        (r'TrueHD', 'TrueHD'),
    ]
    for pattern, audio in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return audio
    return ""


def _extract_source(text):
    """Extract media source."""
    patterns = [
        (r'BluRay|Blu-Ray|BDRip|BRRip', 'BluRay'),
        (r'WEB-?DL|WEBRip|AMZN|NF|DSNP|ATVP|HMAX', 'WEB-DL'),
        (r'HDTV', 'HDTV'),
        (r'DVDRip|DVD', 'DVDRip'),
        (r'HDRip', 'HDRip'),
        (r'CAMRip|CAM|HDCAM|HDTS|TS', 'CAM'),
        (r'REMUX', 'REMUX'),
    ]
    for pattern, source in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return source
    return ""


def _extract_hdr(text):
    """Extract HDR format."""
    patterns = [
        (r'Dolby\s*Vision|DV|DoVi', 'Dolby Vision'),
        (r'HDR10\+|HDR10Plus', 'HDR10+'),
        (r'HDR10|HDR', 'HDR10'),
        (r'HLG', 'HLG'),
    ]
    for pattern, hdr in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return hdr
    return ""


def _extract_language(text):
    """Extract audio/subtitle language."""
    patterns = [
        (r'\b(?:Dual\s*Audio|Dual)\b', 'Dual Audio'),
        (r'\bMulti\s*Audio\b|\bMulti\b', 'Multi'),
        (r'\bHindi\b|\bHINDI\b|\bHin\b', 'Hindi'),
        (r'\bEnglish\b|\bENG\b|\bEn\b', 'English'),
        (r'\bJapanese\b|\bJAP\b|\bJPN\b', 'Japanese'),
        (r'\bKorean\b|\bKOR\b', 'Korean'),
        (r'\bTamil\b|\bTAM\b', 'Tamil'),
        (r'\bTelugu\b|\bTEL\b', 'Telugu'),
        (r'\bBengali\b|\bBEN\b', 'Bengali'),
        (r'\bArabic\b|\bARA\b', 'Arabic'),
        (r'\bFrench\b|\bFR\b', 'French'),
        (r'\bSpanish\b|\bESP\b', 'Spanish'),
        (r'\bGerman\b|\bDEU\b', 'German'),
    ]
    for pattern, lang in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return lang
    return ""


def _extract_release_group(text):
    """Extract release group (usually after a dash at the end)."""
    match = re.search(r'-([A-Za-z0-9]+)$', text)
    if match:
        group = match.group(1)
        # Filter out common false positives
        false_positives = {'mkv', 'mp4', 'avi', 'srt', 'ass', 'sub', 'vtt'}
        if group.lower() not in false_positives:
            return group
    return ""


def _extract_title(text, metadata):
    """
    Extract the clean title by removing all detected metadata from the string.
    The title is usually everything before the first metadata marker.
    """
    title = text
    
    # Strategy: find the earliest position where metadata starts
    # and take everything before it as the title
    
    # All metadata patterns to strip (order matters)
    cut_patterns = [
        r'(?:19|20)\d{2}',                          # Year
        r'[Ss]\d{1,2}[Ee]\d{1,4}',                  # S01E05
        r'[Ss]eason\s*\d{1,2}',                     # Season 1
        r'[Ee]pisode\s*\d{1,4}',                    # Episode 5
        r'(?:480|720|1080|2160)[pP]',                # Quality
        r'4[kK]|UHD|FHD',                           # Quality alt
        r'[xXhH]\.?26[45]|HEVC|AVC|AV1',           # Codec
        r'BluRay|Blu-Ray|BDRip|WEB-?DL|WEBRip',    # Source
        r'HDTV|DVDRip|HDRip|REMUX|CAM',            # Source alt
        r'DTS|DD[P+]?\s*5|AC-?3|AAC|FLAC|Atmos',   # Audio
        r'HDR\d*\+?|Dolby\s*Vision|DV|DoVi|HLG',   # HDR
        r'\b(?:Hindi|English|Japanese|Korean|Tamil|Telugu|Dual\s*Audio|Multi)\b',  # Language
    ]
    
    earliest_pos = len(title)
    for pattern in cut_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match and match.start() < earliest_pos:
            earliest_pos = match.start()
    
    # Also check for anime-style episode marker " - 1050 "
    anime_match = re.search(r'\s-\s\d{1,4}(?:\s|$)', title)
    if anime_match and anime_match.start() < earliest_pos:
        earliest_pos = anime_match.start()
    
    title = title[:earliest_pos].strip()
    
    # Clean up trailing dashes, dots, underscores
    title = re.sub(r'[\s\-_.]+$', '', title)
    
    # Remove leading/trailing brackets content
    title = re.sub(r'^\[.*?\]\s*', '', title)
    title = re.sub(r'\s*\[.*?\]$', '', title)
    
    # Remove parentheses that are empty or contain just whitespace
    title = re.sub(r'\(\s*\)', '', title)
    
    return title.strip() if title.strip() else os.path.splitext(metadata.get("original_filename", ""))[0]


def _is_subtitle(filename):
    """Check if file is a subtitle based on extension."""
    sub_exts = ['.srt', '.ass', '.ssa', '.vtt', '.sub', '.idx']
    return any(filename.lower().endswith(ext) for ext in sub_exts)


async def auto_match_tmdb(metadata, language="en-US"):
    """
    Take detection output and search TMDb for a match.
    
    Args:
        metadata: dict from analyze_filename()
        language: TMDb language preference
    
    Returns:
        Enriched metadata dict with TMDb data, or None
    """
    from helper.tmdb_client import search_movie, search_series, get_movie_details, get_series_details, get_genre_names, is_tmdb_available
    
    if not is_tmdb_available():
        return None
    
    title = metadata.get("title", "")
    year = metadata.get("year", "")
    media_type = metadata.get("type", "movie")
    
    if not title:
        return None
    
    # Search based on detected type
    if media_type == "series":
        tmdb_data = await search_series(title, year if year else None, language)
    else:
        tmdb_data = await search_movie(title, year if year else None, language)
    
    # If no result, try the other type as fallback
    if not tmdb_data:
        if media_type == "series":
            tmdb_data = await search_movie(title, year if year else None, language)
        else:
            tmdb_data = await search_series(title, year if year else None, language)
    
    if not tmdb_data:
        return None
    
    # Get full details for genre names
    tmdb_id = tmdb_data.get("tmdb_id")
    if tmdb_id:
        if tmdb_data.get("type") == "movie":
            details = await get_movie_details(tmdb_id, language)
        else:
            details = await get_series_details(tmdb_id, language)
        
        if details:
            tmdb_data.update(details)
    
    # If we only have genre_ids, convert to names
    if "genres" not in tmdb_data and "genre_ids" in tmdb_data:
        tmdb_data["genres"] = ", ".join(get_genre_names(tmdb_data["genre_ids"]))
    
    return tmdb_data

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
