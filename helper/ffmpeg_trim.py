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

# FFmpeg Trim Module - Dedicated video trimming functions

import os
import time
import asyncio
import subprocess


def parse_time_string(time_str):
    """
    Convert time string to seconds.
    Supports formats: "MM:SS" or "HH:MM:SS"
    
    Args:
        time_str: Time string like "01:30" or "00:01:30"
    
    Returns:
        Total seconds as integer
    """
    parts = time_str.strip().split(":")
    
    if len(parts) == 2:
        # MM:SS format
        minutes, seconds = int(parts[0]), int(parts[1])
        return minutes * 60 + seconds
    elif len(parts) == 3:
        # HH:MM:SS format
        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")


async def get_video_duration(input_file):
    """Get video duration in seconds using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            input_file
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return float(output.decode().strip())
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0


async def trim_video(input_file, output_file, duration=None, start_time=None, end_time=None, progress_callback=None):
    """
    Trim video to specified duration or from start to end time.
    
    Args:
        input_file: Input video path
        output_file: Output video path
        duration: Duration in seconds (for auto trim from start)
        start_time: Start time string "HH:MM:SS" or "MM:SS" (for manual trim)
        end_time: End time string "HH:MM:SS" or "MM:SS" (for manual trim)
        progress_callback: Async progress function(percent, status)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Build FFmpeg command
        cmd = ['ffmpeg', '-y', '-i', input_file]
        
        if start_time and end_time:
            # Manual trim: start to end
            cmd.extend(['-ss', start_time, '-to', end_time])
            print(f"Manual trim: {start_time} to {end_time}")
        elif duration:
            # Auto trim: from start for duration seconds
            cmd.extend(['-t', str(duration)])
            print(f"Auto trim: {duration} seconds from start")
        else:
            print("No trim parameters specified")
            return False
        
        # Use stream copy for fast trimming
        cmd.extend([
            '-c', 'copy',
            '-avoid_negative_ts', 'make_zero',
            '-progress', 'pipe:1',
            output_file
        ])
        
        print(f"Trim command: {' '.join(cmd)}")
        
        if progress_callback:
            await progress_callback(0, "Starting trim...")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
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

        
        # Monitor progress
        total_duration = await get_video_duration(input_file)
        target_duration = duration if duration else total_duration
        last_update = 0
        
        while True:
            try:
                line = await asyncio.wait_for(process.stdout.readline(), timeout=120)
            except asyncio.TimeoutError:
                if process.returncode is not None:
                    break
                continue
            
            if not line:
                break
            
            line_str = line.decode('utf-8', errors='ignore').strip()
            
            if line_str == 'progress=end':
                if progress_callback:
                    await progress_callback(100, "Trim complete!")
                break
            
            if line_str.startswith('out_time_ms=') and target_duration > 0:
                try:
                    out_time_ms = int(line_str.split('=')[1])
                    out_time_sec = out_time_ms / 1000000
                    percentage = min((out_time_sec / target_duration) * 100, 99)
                    
                    now = time.time()
                    if now - last_update >= 2 and progress_callback:
                        await progress_callback(percentage, f"Trimming: {percentage:.0f}%")
                        last_update = now
                except:
                    pass
        
        await asyncio.wait_for(process.wait(), timeout=300)
        
        if process.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Trim successful: {output_file} ({file_size} bytes)")
            return True
        else:
            stderr = await process.stderr.read()
            print(f"Trim failed: {stderr.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"Trim error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def generate_trim_thumbnail(video_file, output_path, timestamp=1):
    """
    Generate a thumbnail from video at specified timestamp.
    
    Args:
        video_file: Path to video file
        output_path: Path to save thumbnail
        timestamp: Time in seconds to capture thumbnail (default: 1)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(timestamp),
            '-i', video_file,
            '-vframes', '1',
            '-vf', 'scale=320:-1',
            output_path
        ]
        
        print(f"Generating thumbnail at {timestamp}s...")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await asyncio.wait_for(process.wait(), timeout=30)
        
        if process.returncode == 0 and os.path.exists(output_path):
            print(f"Thumbnail generated: {output_path}")
            return True
        else:
            print("Thumbnail generation failed")
            return False
            
    except Exception as e:
        print(f"Thumbnail error: {e}")
        return False

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
