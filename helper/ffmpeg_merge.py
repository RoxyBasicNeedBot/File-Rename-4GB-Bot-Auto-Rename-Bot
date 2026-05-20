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

# FFmpeg Merge Module - Dedicated video merging functions

import os
import time
import asyncio
import subprocess
import json


async def get_video_info(input_file):
    """
    Get video codec, resolution, frame rate, and audio info using ffprobe.
    
    Returns:
        dict with codec, width, height, fps, audio_codec, sample_rate
    """
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name,width,height,r_frame_rate',
            '-of', 'json',
            input_file
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        data = json.loads(output.decode())
        stream = data.get('streams', [{}])[0]
        
        # Get audio info
        audio_cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name,sample_rate,channels',
            '-of', 'json',
            input_file
        ]
        audio_output = subprocess.check_output(audio_cmd, stderr=subprocess.STDOUT)
        audio_data = json.loads(audio_output.decode())
        audio_stream = audio_data.get('streams', [{}])[0]
        
        return {
            'codec': stream.get('codec_name', '').lower(),
            'width': stream.get('width', 0),
            'height': stream.get('height', 0),
            'fps': stream.get('r_frame_rate', '30/1'),
            'audio_codec': audio_stream.get('codec_name', '').lower(),
            'sample_rate': audio_stream.get('sample_rate', '44100'),
            'channels': audio_stream.get('channels', 2)
        }
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None


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


def check_videos_compatible(video_infos):
    """
    Check if all videos have compatible formats for direct concat.
    
    Returns:
        True if all videos can be directly concatenated
    """
    if not video_infos or len(video_infos) < 2:
        return False
    
    first = video_infos[0]
    if not first:
        return False
    
    for info in video_infos[1:]:
        if not info:
            return False
        # Check codec match
        if info['codec'] != first['codec']:
            return False
        # Check resolution match
        if info['width'] != first['width'] or info['height'] != first['height']:
            return False
        # Check audio codec match
        if info['audio_codec'] != first['audio_codec']:
            return False
    
    return True


async def normalize_video_for_merge(input_file, output_file, target_height=None, progress_callback=None):
    """
    Re-encode video to H.264/AAC for merge compatibility.
    Uses veryfast preset for good speed/quality balance.
    Keeps original resolution unless target_height specified.
    
    Args:
        input_file: Input video path
        output_file: Output video path
        target_height: Optional target height (e.g., 720)
        progress_callback: Async progress function
    
    Returns:
        True if successful, False otherwise
    """
    try:
        duration = await get_video_duration(input_file)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Build FFmpeg command
        cmd = [
            'ffmpeg', '-y',
            '-i', input_file,
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
        ]
        
        # Add scaling only if target_height specified
        if target_height:
            cmd.extend(['-vf', f'scale=-2:{target_height}'])
        
        # Audio settings - consistent for all videos
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-ac', '2',
            '-movflags', '+faststart',
            '-progress', 'pipe:1',
            output_file
        ])
        
        print(f"Normalizing: {os.path.basename(input_file)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        start_time = time.time()
        last_update = 0
        
        while True:
            try:
                line = await asyncio.wait_for(process.stdout.readline(), timeout=300)
            except asyncio.TimeoutError:
                if process.returncode is not None:
                    break
                continue
            
            if not line:
                break
            
            line_str = line.decode('utf-8', errors='ignore').strip()
            
            if line_str == 'progress=end':
                if progress_callback:
                    await progress_callback(100, "Done!")
                break
            
            if line_str.startswith('out_time_ms=') and duration > 0:
                try:
                    out_time_ms = int(line_str.split('=')[1])
                    out_time_sec = out_time_ms / 1000000
                    percentage = min((out_time_sec / duration) * 100, 99)
                    
                    now = time.time()
                    if now - last_update >= 3 and progress_callback:
                        await progress_callback(percentage, "Converting...")
                        last_update = now
                except:
                    pass
        
        await asyncio.wait_for(process.wait(), timeout=600)
        
        if process.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Normalized: {output_file} ({file_size} bytes)")
            return True
        else:
            stderr = await process.stderr.read()
            print(f"Normalization failed: {stderr.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"Normalization error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def try_direct_concat(input_files, output_file, progress_callback=None):
    """
    Try to concatenate videos using stream copy (no re-encoding).
    This is fast but only works if all videos have same codec/resolution.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create concat input file
        input_list_file = f"concat_list_{int(time.time())}.txt"
        
        with open(input_list_file, 'w', encoding='utf-8') as f:
            for video_file in input_files:
                # Handle Windows paths properly
                abs_path = os.path.abspath(video_file)
                # FFmpeg requires forward slashes
                ffmpeg_path = abs_path.replace('\\', '/')
                # Escape single quotes
                escaped_path = ffmpeg_path.replace("'", "'\\''")
                f.write(f"file '{escaped_path}'\n")
        
        if progress_callback:
            await progress_callback(10, "Trying direct concat...")
        
        # FFmpeg concat command with stream copy

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

        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', input_list_file,
            '-c', 'copy',
            '-movflags', '+faststart',
            output_file
        ]
        
        print(f"Direct concat: {' '.join(cmd)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)
        
        # Cleanup input list
        try:
            os.remove(input_list_file)
        except:
            pass
        
        if process.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            if file_size > 0:
                print(f"Direct concat successful! Size: {file_size} bytes")
                if progress_callback:
                    await progress_callback(100, "Complete!")
                return True
        
        print(f"Direct concat failed: {stderr.decode()[:300]}")
        return False
        
    except Exception as e:
        print(f"Direct concat error: {e}")
        return False


async def merge_videos(input_files, output_file, progress_callback=None):
    """
    Merge multiple video files into one.
    
    Strategy:
    1. Check if all videos are compatible (same codec/resolution)
    2. If yes, try direct concat (fast!)
    3. If no or direct fails, re-encode all to common format
    
    Args:
        input_files: List of input file paths to merge
        output_file: Path for the merged output file
        progress_callback: Async function(percentage, status) for progress updates
    
    Returns:
        True if successful, False otherwise
    """
    if not input_files or len(input_files) < 2:
        print("Need at least 2 files to merge")
        return False
    
    normalized_files = []
    
    try:
        total_files = len(input_files)
        
        if progress_callback:
            await progress_callback(0, f"Analyzing {total_files} videos...")
        
        # Step 1: Get info for all videos
        video_infos = []
        for f in input_files:
            info = await get_video_info(f)
            video_infos.append(info)
            print(f"Video: {os.path.basename(f)} - {info}")
        
        # Step 2: Check compatibility
        compatible = check_videos_compatible(video_infos)
        
        if compatible:
            if progress_callback:
                await progress_callback(5, "Videos compatible, trying fast merge...")
            
            # Try direct concat first
            success = await try_direct_concat(input_files, output_file, progress_callback)
            if success:
                return True
            
            print("Direct concat failed, falling back to re-encode...")
        else:
            print("Videos not compatible, need to normalize...")
        
        # Step 3: Re-encode all videos to common format
        if progress_callback:
            await progress_callback(10, f"Converting {total_files} videos...")
        
        for i, orig_file in enumerate(input_files):
            base_name = os.path.splitext(os.path.basename(orig_file))[0]
            normalized_path = f"MergeFiles/norm_{int(time.time())}_{i}_{base_name}.mp4"
            
            # Progress: 10-70% for conversion phase
            file_pct = 10 + ((i / total_files) * 60)
            
            if progress_callback:
                await progress_callback(file_pct, f"Converting {i+1}/{total_files}...")
            
            success = await normalize_video_for_merge(orig_file, normalized_path)
            
            if success and os.path.exists(normalized_path):
                normalized_files.append(normalized_path)
                print(f"Converted {i+1}/{total_files}: {os.path.basename(orig_file)}")
            else:
                print(f"Failed to convert: {orig_file}")
                # Continue with remaining files instead of failing completely
                continue
        
        if len(normalized_files) < 2:
            print("Not enough files converted successfully")
            return False
        
        # Step 4: Concat the normalized files
        if progress_callback:
            await progress_callback(75, "Merging videos...")
        
        # Create concat input file
        input_list_file = f"merge_input_{int(time.time())}.txt"
        
        # Calculate total duration for progress
        total_duration = 0
        for f in normalized_files:
            dur = await get_video_duration(f)
            total_duration += dur
        
        with open(input_list_file, 'w', encoding='utf-8') as f:
            for video_file in normalized_files:
                abs_path = os.path.abspath(video_file)
                ffmpeg_path = abs_path.replace('\\', '/')
                escaped_path = ffmpeg_path.replace("'", "'\\''")
                f.write(f"file '{escaped_path}'\n")
        
        # FFmpeg merge command
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', input_list_file,
            '-c', 'copy',
            '-movflags', '+faststart',
            '-progress', 'pipe:1',
            output_file
        ]
        
        print(f"Merge command: {' '.join(cmd)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
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
                    await progress_callback(100, "Complete!")
                break
            
            if line_str.startswith('out_time_ms=') and total_duration > 0:
                try:
                    out_time_ms = int(line_str.split('=')[1])
                    out_time_sec = out_time_ms / 1000000
                    merge_pct = (out_time_sec / total_duration) * 100
                    overall_pct = 75 + (merge_pct * 0.25)  # 75-100% range
                    overall_pct = min(overall_pct, 99)
                    
                    now = time.time()
                    if now - last_update >= 3 and progress_callback:
                        await progress_callback(overall_pct, f"Merging: {merge_pct:.0f}%")
                        last_update = now
                except:
                    pass
        
        # Cleanup input list
        try:
            os.remove(input_list_file)
        except:
            pass
        
        await asyncio.wait_for(process.wait(), timeout=120)
        
        if process.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Merge successful! Size: {file_size} bytes")
            return True
        else:
            stderr = await process.stderr.read()
            print(f"Merge failed: {stderr.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"Merge error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup normalized temp files
        for nf in normalized_files:
            try:
                if os.path.exists(nf):
                    os.remove(nf)
                    print(f"Cleaned up: {nf}")
            except:
                pass


async def cleanup_merge_files(file_paths):
    """Remove downloaded files used for merging"""
    if not file_paths:
        return
    for path in file_paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
                print(f"Cleaned up merge file: {path}")
        except Exception as e:
            print(f"Error removing merge file {path}: {e}")

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
