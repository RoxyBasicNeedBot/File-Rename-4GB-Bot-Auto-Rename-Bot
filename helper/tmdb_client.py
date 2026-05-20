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

# TMDb API Client — Movie/Series metadata fetching
# Uses TMDb API v3 (free, unlimited for bots)
# Get your API key: https://www.themoviedb.org/settings/api

import os
import aiohttp
import asyncio

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p"

# In-memory cache to avoid duplicate API calls
_cache = {}


def _get_api_key():
    """Get TMDb API key from config."""
    from config import Config
    return getattr(Config, 'TMDB_API_KEY', '') or ''


def is_tmdb_available():
    """Check if TMDb API key is configured."""
    key = _get_api_key()
    return bool(key and len(key) > 10)


async def search_movie(title, year=None, language="en-US"):
    """
    Search TMDb for a movie by title.
    
    Args:
        title: Movie title to search
        year: Optional release year to narrow results
        language: TMDb language code (default en-US)
    
    Returns:
        dict with movie data or None if not found
    """
    api_key = _get_api_key()
    if not api_key:
        return None
    
    cache_key = f"movie:{title}:{year}:{language}"
    if cache_key in _cache:
        return _cache[cache_key]
    
    params = {
        "api_key": api_key,
        "query": title,
        "language": language,
        "include_adult": "false",
    }
    if year:
        params["year"] = str(year)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{TMDB_BASE_URL}/search/movie",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    print(f"[TMDb] Movie search failed: HTTP {resp.status}")
                    return None
                
                data = await resp.json()
                results = data.get("results", [])
                
                if not results:
                    return None
                
                # Take the first (most relevant) result
                movie = results[0]
                
                result = {
                    "tmdb_id": movie.get("id"),
                    "title": movie.get("title", title),
                    "original_title": movie.get("original_title", ""),
                    "year": movie.get("release_date", "")[:4],
                    "overview": movie.get("overview", ""),
                    "poster_path": movie.get("poster_path"),
                    "poster_url": f"{TMDB_IMAGE_BASE}/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                    "poster_thumb_url": f"{TMDB_IMAGE_BASE}/w200{movie['poster_path']}" if movie.get("poster_path") else None,
                    "vote_average": movie.get("vote_average", 0),
                    "genre_ids": movie.get("genre_ids", []),
                    "type": "movie",
                    "release_date": movie.get("release_date", ""),
                }
                
                _cache[cache_key] = result
                return result
                
    except asyncio.TimeoutError:
        print("[TMDb] Movie search timeout")
        return None
    except Exception as e:
        print(f"[TMDb] Movie search error: {e}")
        return None


async def search_series(title, year=None, language="en-US"):
    """
    Search TMDb for a TV series by title.
    
    Args:
        title: Series title to search
        year: Optional first air date year
        language: TMDb language code
    
    Returns:
        dict with series data or None
    """
    api_key = _get_api_key()
    if not api_key:
        return None
    
    cache_key = f"series:{title}:{year}:{language}"
    if cache_key in _cache:
        return _cache[cache_key]
    
    params = {
        "api_key": api_key,
        "query": title,
        "language": language,
        "include_adult": "false",
    }
    if year:
        params["first_air_date_year"] = str(year)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{TMDB_BASE_URL}/search/tv",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    print(f"[TMDb] Series search failed: HTTP {resp.status}")
                    return None
                
                data = await resp.json()
                results = data.get("results", [])
                
                if not results:
                    return None
                
                series = results[0]
                
                result = {
                    "tmdb_id": series.get("id"),
                    "title": series.get("name", title),
                    "original_title": series.get("original_name", ""),
                    "year": series.get("first_air_date", "")[:4],
                    "overview": series.get("overview", ""),
                    "poster_path": series.get("poster_path"),
                    "poster_url": f"{TMDB_IMAGE_BASE}/w500{series['poster_path']}" if series.get("poster_path") else None,
                    "poster_thumb_url": f"{TMDB_IMAGE_BASE}/w200{series['poster_path']}" if series.get("poster_path") else None,
                    "vote_average": series.get("vote_average", 0),
                    "genre_ids": series.get("genre_ids", []),
                    "type": "series",
                    "release_date": series.get("first_air_date", ""),
                }
                
                _cache[cache_key] = result
                return result
                
    except asyncio.TimeoutError:
        print("[TMDb] Series search timeout")
        return None
    except Exception as e:
        print(f"[TMDb] Series search error: {e}")
        return None


async def get_movie_details(tmdb_id, language="en-US"):

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
    Get full movie details including genres, tagline, runtime.
    
    Args:
        tmdb_id: TMDb movie ID
        language: TMDb language code
    
    Returns:
        dict with full movie details or None
    """
    api_key = _get_api_key()
    if not api_key:
        return None
    
    cache_key = f"movie_detail:{tmdb_id}:{language}"
    if cache_key in _cache:
        return _cache[cache_key]
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{TMDB_BASE_URL}/movie/{tmdb_id}",
                params={"api_key": api_key, "language": language},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    return None
                
                movie = await resp.json()
                
                genres = [g.get("name", "") for g in movie.get("genres", [])]
                
                result = {
                    "tmdb_id": movie.get("id"),
                    "title": movie.get("title", ""),
                    "original_title": movie.get("original_title", ""),
                    "year": movie.get("release_date", "")[:4],
                    "overview": movie.get("overview", ""),
                    "tagline": movie.get("tagline", ""),
                    "genres": ", ".join(genres),
                    "genre_list": genres,
                    "runtime": movie.get("runtime", 0),
                    "vote_average": movie.get("vote_average", 0),
                    "poster_url": f"{TMDB_IMAGE_BASE}/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                    "poster_thumb_url": f"{TMDB_IMAGE_BASE}/w200{movie['poster_path']}" if movie.get("poster_path") else None,
                    "release_date": movie.get("release_date", ""),
                    "type": "movie",
                }
                
                _cache[cache_key] = result
                return result
                
    except Exception as e:
        print(f"[TMDb] Movie details error: {e}")
        return None


async def get_series_details(tmdb_id, language="en-US"):
    """
    Get full TV series details.
    """
    api_key = _get_api_key()
    if not api_key:
        return None
    
    cache_key = f"series_detail:{tmdb_id}:{language}"
    if cache_key in _cache:
        return _cache[cache_key]
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{TMDB_BASE_URL}/tv/{tmdb_id}",
                params={"api_key": api_key, "language": language},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    return None
                
                series = await resp.json()
                
                genres = [g.get("name", "") for g in series.get("genres", [])]
                networks = [n.get("name", "") for n in series.get("networks", [])]
                
                result = {
                    "tmdb_id": series.get("id"),
                    "title": series.get("name", ""),
                    "original_title": series.get("original_name", ""),
                    "year": series.get("first_air_date", "")[:4],
                    "overview": series.get("overview", ""),
                    "tagline": series.get("tagline", ""),
                    "genres": ", ".join(genres),
                    "genre_list": genres,
                    "networks": ", ".join(networks),
                    "seasons": series.get("number_of_seasons", 0),
                    "episodes": series.get("number_of_episodes", 0),
                    "vote_average": series.get("vote_average", 0),
                    "poster_url": f"{TMDB_IMAGE_BASE}/w500{series['poster_path']}" if series.get("poster_path") else None,
                    "poster_thumb_url": f"{TMDB_IMAGE_BASE}/w200{series['poster_path']}" if series.get("poster_path") else None,
                    "release_date": series.get("first_air_date", ""),
                    "type": "series",
                }
                
                _cache[cache_key] = result
                return result
                
    except Exception as e:
        print(f"[TMDb] Series details error: {e}")
        return None


async def download_poster(poster_url, save_dir="downloads"):
    """
    Download a TMDb poster image for use as video thumbnail.
    
    Args:
        poster_url: Full URL to poster image
        save_dir: Directory to save the downloaded poster
    
    Returns:
        Path to downloaded poster file or None
    """
    if not poster_url:
        return None
    
    try:
        os.makedirs(save_dir, exist_ok=True)
        
        # Generate unique filename
        import time
        poster_path = os.path.join(save_dir, f"tmdb_poster_{int(time.time())}.jpg")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                poster_url,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                if resp.status != 200:
                    print(f"[TMDb] Poster download failed: HTTP {resp.status}")
                    return None
                
                content = await resp.read()
                
                with open(poster_path, 'wb') as f:
                    f.write(content)
                
                if os.path.exists(poster_path) and os.path.getsize(poster_path) > 0:
                    print(f"[TMDb] ✅ Poster downloaded: {poster_path} ({os.path.getsize(poster_path)} bytes)")
                    return poster_path
                
                return None
                
    except Exception as e:
        print(f"[TMDb] Poster download error: {e}")
        return None


# Genre ID to name mapping (TMDb standard)
GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
    53: "Thriller", 10752: "War", 37: "Western",
    # TV genres
    10759: "Action & Adventure", 10762: "Kids", 10763: "News",
    10764: "Reality", 10765: "Sci-Fi & Fantasy", 10766: "Soap",
    10767: "Talk", 10768: "War & Politics",
}


def get_genre_names(genre_ids):
    """Convert genre IDs to human-readable names."""
    return [GENRE_MAP.get(gid, "Unknown") for gid in genre_ids if gid in GENRE_MAP]


def clear_cache():
    """Clear the in-memory TMDb cache."""
    global _cache
    _cache = {}

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
