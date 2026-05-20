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
import asyncio
import aiohttp
import logging
from typing import Union, Dict
from PIL import Image
from io import BytesIO
from urllib.parse import unquote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from config import Config

# Hugging Face NSFW API Configuration
HF_TOKEN = Config.NSFW_API_KEY
API_URL = Config.NSFW_API_URL

class ContentScanner:
    def __init__(self):
        self.temp_dir = "temp_scan"
        os.makedirs(self.temp_dir, exist_ok=True)
        
    async def scan_url(self, url: str) -> Dict[str, Union[bool, str]]:
        """Scan a URL for adult content before downloading"""
        try:
            decoded_url = unquote(url.lower())
            from helper.adult_filter import ADULT_KEYWORDS
            
            for keyword in ADULT_KEYWORDS:
                if keyword in decoded_url:
                    return {
                        "safe": False,
                        "reason": f"URL contains suspicious keyword: {keyword}"
                    }
            
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True) as response:
                    content_type = response.headers.get('Content-Type', '')
                    if 'image' in content_type or 'video' in content_type:
                        return await self.scan_media_url(url)
                        
            return {"safe": True, "reason": "URL appears safe"}
            
        except Exception as e:
            logger.error(f"Error scanning URL: {e}")
            return {"safe": False, "reason": f"Error scanning URL: {str(e)}"}

    async def scan_media_url(self, url: str) -> Dict[str, Union[bool, str]]:
        """Scan media URL by downloading and checking content"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if 'image' in response.headers.get('Content-Type', ''):
                        data = await response.read()
                        return await self.scan_image_bytes(data)
            return {"safe": True, "reason": "Media content appears safe"}
        except Exception as e:
            logger.error(f"Error scanning media URL: {e}")
            return {"safe": False, "reason": f"Error scanning media: {str(e)}"}

    async def scan_image_bytes(self, image_bytes: bytes) -> Dict[str, Union[bool, str]]:
        """Scan image bytes for NSFW content using Hugging Face API"""
        try:
            headers = {
                "Authorization": f"Bearer {HF_TOKEN}"
            }
            
            form_data = aiohttp.FormData()
            form_data.add_field('file', image_bytes, filename='image.jpg', content_type='image/jpeg')
            
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, data=form_data, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    response_text = await response.text()
                    logger.info(f"📡 NSFW API Response Status: {response.status}")
                    logger.info(f"📡 NSFW API Response: {response_text[:300]}")
                    
                    if response.status == 200:
                        try:
                            result = await response.json()
                            
                            is_nsfw_content = False
                            confidence = 0.0
                            
                            # Format 1: {"is_nsfw": true, "confidence": 0.95}
                            if isinstance(result, dict):
                                if 'is_nsfw' in result:
                                    is_nsfw_content = result.get('is_nsfw', False)

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

                                    confidence = result.get('confidence', 0)
                                elif 'nsfw' in result:
                                    is_nsfw_content = result.get('nsfw', False)
                                    confidence = result.get('score', result.get('confidence', 0))
                                elif 'safe' in result:
                                    is_nsfw_content = not result.get('safe', True)
                                    confidence = 0.95 if is_nsfw_content else 0.0
                                elif 'label' in result:
                                    label = result.get('label', '').lower()
                                    is_nsfw_content = label in ['nsfw', 'porn', 'sexy', 'hentai', 'explicit']
                                    confidence = result.get('score', 0)
                            
                            # Format 5: List of classifications
                            elif isinstance(result, list) and len(result) > 0:
                                for item in result:
                                    if isinstance(item, dict):
                                        label = item.get('label', '').lower()
                                        score = item.get('score', 0)
                                        if label in ['nsfw', 'porn', 'sexy', 'hentai', 'explicit'] and score > confidence:
                                            is_nsfw_content = True
                                            confidence = score
                            
                            logger.info(f"📡 NSFW Result: is_nsfw={is_nsfw_content}, confidence={confidence}")
                            
                            if is_nsfw_content and confidence > 85.0:
                                return {
                                    "safe": False,
                                    "reason": f"Detected NSFW content with confidence: {confidence:.2f}%"
                                }
                            
                            return {"safe": True, "reason": "Image appears safe"}
                        except Exception as e:
                            logger.error(f"Failed to parse NSFW response: {e}")
                            return {"safe": True, "reason": "Parse error - content allowed"}
                    else:
                        logger.warning(f"NSFW API error: {response.status}")
                        return {"safe": True, "reason": "API unavailable - content allowed"}

        except asyncio.TimeoutError:
            logger.warning("NSFW API request timed out - allowing content through")
            return {"safe": True, "reason": "API timeout - content allowed"}
        except Exception as e:
            logger.warning(f"NSFW scan error: {e} - allowing content through")
            return {"safe": True, "reason": "Scan error - content allowed"}

    async def scan_file_name(self, file_name: str) -> Dict[str, Union[bool, str]]:
        """Check if file name contains adult content indicators"""
        try:
            from helper.adult_filter import ADULT_KEYWORDS
            
            file_name = file_name.lower()
            for keyword in ADULT_KEYWORDS:
                if keyword in file_name:
                    return {
                        "safe": False,
                        "reason": f"File name contains suspicious keyword: {keyword}"
                    }
            
            return {"safe": True, "reason": "File name appears safe"}
        except Exception as e:
            logger.error(f"Error scanning file name: {e}")
            return {"safe": False, "reason": f"Error scanning file name: {str(e)}"}

    async def scan_document(self, file_path: str) -> Dict[str, Union[bool, str]]:
        """Scan a document file for adult content"""
        try:
            file_name = os.path.basename(file_path)
            name_check = await self.scan_file_name(file_name)
            if not name_check["safe"]:
                return name_check

            try:
                with open(file_path, 'rb') as f:
                    img = Image.open(f)
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format=img.format)
                    img_byte_arr = img_byte_arr.getvalue()
                    return await self.scan_image_bytes(img_byte_arr)
            except:
                pass

            return {"safe": True, "reason": "Document appears safe"}

        except Exception as e:
            logger.error(f"Error scanning document: {e}")
            return {"safe": False, "reason": f"Error scanning document: {str(e)}"}

# Create singleton instance
content_scanner = ContentScanner()

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
