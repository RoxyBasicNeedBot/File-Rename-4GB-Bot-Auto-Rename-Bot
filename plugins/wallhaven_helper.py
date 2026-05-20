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

from config import Config
import random, aiohttp, asyncio

# Comprehensive search queries - SFW content only
# Categories: Hollywood, Bollywood, Chinese, Korean, Russian actresses, Anime, Cars, Nature, etc.

SEARCH_QUERIES = [
    # Hollywood Actresses
    "scarlett johansson",
    "emma watson",
    "jennifer lawrence",
    "margot robbie",
    "gal gadot",
    "anne hathaway",
    "natalie portman",
    "emma stone",
    "zendaya",
    "florence pugh",
    "ana de armas",
    "sydney sweeney",
    "hailee steinfeld",
    "alexandra daddario",
    "elizabeth olsen",
    "brie larson",
    "blake lively",
    "kate beckinsale",
    "kate winslet",
    "angelina jolie",
    "megan fox",
    "jessica alba",
    "jennifer aniston",
    "cameron diaz",
    "charlize theron",
    "kristen stewart",
    "dakota johnson",
    "vanessa hudgens",
    "selena gomez",
    "dua lipa",
    "taylor swift",
    "ariana grande",
    "billie eilish",
    "rihanna",
    "beyonce",
    
    # Korean Actresses & K-pop
    "kim ji won",
    "song hye kyo",
    "jun ji hyun",
    "park min young",
    "iu singer",
    "blackpink jennie",
    "blackpink lisa",
    "blackpink rose",
    "blackpink jisoo",
    "twice tzuyu",
    "red velvet irene",
    "suzy bae",
    "han so hee",
    "kim tae ri",
    "shin min ah",
    
    # Chinese Actresses
    "yang mi actress",
    "fan bingbing",
    "liu yifei",
    "zhao liying",
    "angelababy",
    "dilraba dilmurat",
    "zhou dongyu",
    "ni ni actress",
    "gao yuanyuan",
    "tang yan actress",
    
    # Japanese Actresses
    "satomi ishihara",
    "haruka ayase",
    "keiko kitagawa",
    "masami nagasawa",
    "yui aragaki",
    "nanao model",
    
    # Russian & European Models
    "irina shayk",
    "natalia vodianova",
    "daria strokous",
    "sasha luss",
    "valentina sampaio",
    "barbara palvin",
    "emily ratajkowski",
    "cara delevingne",
    "kendall jenner",
    "gigi hadid",
    "bella hadid",
    
    # Indian Actresses & Bollywood
    "deepika padukone",
    "priyanka chopra",
    "alia bhatt",
    "kiara advani",
    "kriti sanon",
    "shraddha kapoor",
    "disha patani",
    "janhvi kapoor",
    "ananya panday",
    "katrina kaif",
    "kareena kapoor",
    "aishwarya rai",
    
    # Anime & Animation
    "anime girl wallpaper",
    "anime aesthetic",
    "anime landscape",
    "solo leveling wallpaper",
    "jujutsu kaisen",
    "demon slayer wallpaper",
    "one piece wallpaper",
    "naruto wallpaper",
    "attack on titan",
    "my hero academia",
    "spy x family",
    "chainsaw man",
    "genshin impact",
    "honkai star rail",
    "fate series",
    "violet evergarden",
    "your name anime",
    "studio ghibli",
    "cyberpunk edgerunners",
    "bocchi the rock",
    "frieren anime",
    "oshi no ko",
    
    # Cars & Vehicles
    "lamborghini wallpaper",
    "ferrari wallpaper",
    "porsche 911",
    "bmw m series",
    "mercedes amg",
    "audi r8",
    "mclaren supercar",
    "bugatti chiron",
    "mustang gt",
    "nissan gtr",
    "toyota supra",
    "dodge challenger",
    "corvette",
    "aston martin",
    "rolls royce",
    "bentley luxury",
    "tesla cybertruck",
    "ford raptor",
    "jeep wrangler",
    "land rover",
    "motorcycle wallpaper",
    "superbike",
    "f1 racing",
    "rally car",
    
    # Nature & Landscapes
    "mountain landscape",
    "sunset wallpaper",
    "ocean waves",
    "forest wallpaper",
    "aurora borealis",
    "starry night sky",
    "milky way galaxy",
    "waterfall nature",
    "cherry blossom japan",
    "autumn leaves",
    "snow mountains",
    "tropical beach",
    "desert landscape",
    "rainbow nature",
    "thunderstorm lightning",
    
    # Cities & Architecture
    "tokyo night",
    "new york skyline",
    "dubai city",
    "paris eiffel tower",
    "london city",
    "singapore skyline",
    "hong kong night",
    "neon city",
    "cyberpunk city",
    "futuristic city",
    
    # Space & Sci-Fi
    "space galaxy",
    "nebula wallpaper",
    "planet earth",
    "mars landscape",
    "astronaut wallpaper",
    "spaceship",
    "sci fi wallpaper",
    "futuristic",
    
    # Gaming
    "valorant wallpaper",
    "fortnite",
    "apex legends",
    "call of duty",
    "overwatch",
    "league of legends",
    "elden ring",
    "god of war",
    "the witcher",
    "cyberpunk 2077",
    "red dead redemption",
    "minecraft",
    
    # Abstract & Art
    "abstract art",
    "minimalist wallpaper",
    "gradient wallpaper",
    "geometric art",
    "digital art",
    "3d render",
    "neon lights",
    "aesthetic wallpaper",
    "dark aesthetic",
    "vaporwave"
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


# Fallback queries - guaranteed to have results
FALLBACK_QUERIES = [
    "anime wallpaper",
    "nature landscape",
    "city night",
    "space galaxy",
    "abstract art",
    "car wallpaper",
    "sunset"
]

# Static fallback images if API completely fails
STATIC_FALLBACK_IMAGES = [
    "https://i.ibb.co/27SZFvzv/file-29500.jpg",
    "https://i.ibb.co/G3NDht97/file-29498.jpg",
    "https://i.ibb.co/Rph1Bs8q/file-29680.jpg"
]

# API Configuration
API_TIMEOUT = 10  # seconds
MAX_RETRIES = 3


async def fetch_from_wallhaven(session, query, api_key, categories="111", purity="100"):
    """
    Fetch images from Wallhaven API with specific parameters.
    
    Args:
        session: aiohttp ClientSession
        query: Search query string
        api_key: Wallhaven API key to use
        categories: "xyz" where x=General, y=Anime, z=People (1=on, 0=off)
        purity: "100" = SFW only (NO sketchy, NO NSFW)
    
    Returns:
        Image URL or None if failed
    """
    try:
        params = {
            "apikey": api_key,
            "q": query,
            "categories": categories,
            "purity": purity,
            "sorting": "random",
            "seed": str(random.randint(1000, 999999))
        }
        
        async with session.get(
            Config.WALLHAVEN_API_URL, 
            params=params,
            timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                if "data" in data and len(data["data"]) > 0:
                    # Get random image from results
                    random_image = random.choice(data["data"])
                    image_url = random_image.get("path")
                    if image_url:
                        return image_url
            elif resp.status == 401:
                print(f"Wallhaven API: Invalid API key")
            elif resp.status == 429:
                print(f"Wallhaven API: Rate limited for key, trying next...")
            else:
                print(f"Wallhaven API error {resp.status} for query: {query}")
                
    except asyncio.TimeoutError:
        print(f"Wallhaven API timeout for query: {query}")
    except aiohttp.ClientError as e:
        print(f"Wallhaven API connection error: {e}")
    except Exception as e:
        print(f"Wallhaven API unexpected error: {e}")
    
    return None


async def try_query_with_variations(session, query):
    """
    Try a single query with different category combinations.
    Also rotates through all available API keys.
    SFW ONLY - purity is always "100" (no sketchy, no NSFW)
    """
    # Different category combinations to try - ALL SFW ONLY (purity="100")
    variations = [
        {"categories": "111", "purity": "100"},  # All categories + SFW only
        {"categories": "100", "purity": "100"},  # General only + SFW only
        {"categories": "010", "purity": "100"},  # Anime only + SFW only
        {"categories": "001", "purity": "100"},  # People only + SFW only
    ]
    
    # Get list of API keys
    api_keys = Config.ROXY_PIC_API_KEYS if hasattr(Config, 'ROXY_PIC_API_KEYS') else [Config.ROXY_PIC_API]
    
    # Shuffle API keys for load balancing
    shuffled_keys = api_keys.copy()
    random.shuffle(shuffled_keys)
    
    for api_key in shuffled_keys:
        for variation in variations:
            result = await fetch_from_wallhaven(
                session, 
                query,
                api_key,
                variation["categories"], 
                variation["purity"]
            )
            if result:
                return result
    
    return None


async def get_random_pic():
    """
    Main function to get a random picture from Wallhaven.
    
    Strategy:
    1. Try random query from SEARCH_QUERIES with different variations
    2. If fails, try shuffled queries from SEARCH_QUERIES
    3. If still fails, try FALLBACK_QUERIES
    4. If all API calls fail, return a static fallback image
    
    Returns:
        Image URL (string)
    """
    try:
        # Create session with headers for better compatibility
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            
            # STEP 1: Try primary random query with variations
            primary_query = random.choice(SEARCH_QUERIES)
            result = await try_query_with_variations(session, primary_query)
            if result:
                print(f"Wallhaven: Found image for '{primary_query}'")
                return result
            
            # STEP 2: Try other random queries from main list
            shuffled_queries = SEARCH_QUERIES.copy()
            random.shuffle(shuffled_queries)
            
            for query in shuffled_queries[:5]:  # Try up to 5 more
                if query == primary_query:
                    continue
                result = await try_query_with_variations(session, query)
                if result:
                    print(f"Wallhaven: Found image for '{query}'")
                    return result
            
            # STEP 3: Try fallback queries
            for fallback_query in FALLBACK_QUERIES:
                result = await try_query_with_variations(session, fallback_query)
                if result:
                    print(f"Wallhaven: Found image using fallback '{fallback_query}'")
                    return result
            
            print("Wallhaven: All queries failed, using static fallback")
    
    except Exception as e:
        print(f"Wallhaven: Critical error in get_random_pic: {e}")
    
    # STEP 4: Return static fallback image
    return random.choice(STATIC_FALLBACK_IMAGES)


async def validate_image_url(url):
    """
    Validate if an image URL is accessible.
    
    Args:
        url: Image URL to validate
    
    Returns:
        True if accessible, False otherwise
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                return resp.status == 200
    except:
        return False


# Enhanced version with comprehensive search queries and robust error handling
# SFW ONLY - No adult content

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
