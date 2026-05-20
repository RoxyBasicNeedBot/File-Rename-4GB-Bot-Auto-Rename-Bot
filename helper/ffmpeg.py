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

import os, time, asyncio, subprocess, json, re, math
from helper.utils import metadata_text, TimeFormatter


def clean_resolution_from_filename(filename):
    """
    Remove existing resolution tags from filename before adding new resolution suffix.
    Handles formats like: [1080p], [720p], 1080p, 720p, etc.
    
    Args:
        filename: Original filename (without extension)
    
    Returns:
        Cleaned filename without resolution tags
    """
    # Pattern to match resolution tags: [1080p], [720p], [480p], [360p], 1080p, 720p, 480p, 360p
    # Also handles variations like [1080P], 1080P (case insensitive)
    patterns = [
        r'\s*\[?\d{3,4}[pP]\]?\s*',  # Matches [1080p], 1080p, [720P], etc.
        r'\s*\[?4K\]?\s*',            # Matches [4K], 4K
        r'\s*\[?2160[pP]\]?\s*',      # Matches [2160p], 2160p
    ]
    
    result = filename
    for pattern in patterns:
        result = re.sub(pattern, ' ', result, flags=re.IGNORECASE)
    
    # Clean up multiple spaces and trim
    result = ' '.join(result.split())
    
    return result


async def change_metadata(input_file, output_file, metadata):
    author, title, video_title, audio_title, subtitle_title = await metadata_text(metadata)
    
    # Get the video metadata
    output = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-print_format', 'json', input_file])
    data = json.loads(output)
    streams = data['streams']

    # Create the FFmpeg command to change metadata
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-map', '0',  # Map all streams
        '-c:v', 'copy',  # Copy video stream
        '-c:a', 'copy',  # Copy audio stream
        '-c:s', 'copy',  # Copy subtitles stream
        '-metadata', f'title={title}',
        '-metadata', f'author={author}',
    ]

    # Add title to video stream
    for stream in streams:
        if stream['codec_type'] == 'video' and video_title:
            cmd.extend([f'-metadata:s:{stream["index"]}', f'title={video_title}'])
        elif stream['codec_type'] == 'audio' and audio_title:
            cmd.extend([f'-metadata:s:{stream["index"]}', f'title={audio_title}'])
        elif stream['codec_type'] == 'subtitle' and subtitle_title:
            cmd.extend([f'-metadata:s:{stream["index"]}', f'title={subtitle_title}'])

    cmd.extend(['-metadata', f'comment=Added by @roxybasicneedbot1'])
    cmd.extend(['-f', 'matroska']) # support all format 
    cmd.append(output_file)
    print(cmd)
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("FFmpeg Error:", e.stderr)
        return False


async def get_video_duration(input_file):
    """Get video duration in seconds using ffprobe"""
    try:
        if not input_file or not os.path.exists(input_file):
            return 0
            
        file_size = os.path.getsize(input_file)
        if file_size == 0:
            return 0

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


async def get_video_codec(input_file):
    """Get video codec name using ffprobe"""
    try:
        if not input_file or not os.path.exists(input_file):
            return None
            
        file_size = os.path.getsize(input_file)
        if file_size == 0:
            return None

        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return output.decode().strip().lower()
    except Exception as e:
        print(f"Error getting codec: {e}")
        return None


async def get_video_info(input_file):
    """Get video codec, resolution, and frame rate using ffprobe"""
    try:
        if not input_file or not os.path.exists(input_file):
             return {'codec': None, 'width': 0, 'height': 0, 'fps': '30/1'}
            
        file_size = os.path.getsize(input_file)
        if file_size == 0:
             return {'codec': None, 'width': 0, 'height': 0, 'fps': '30/1'}

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
        return {
            'codec': stream.get('codec_name', '').lower(),
            'width': stream.get('width', 0),
            'height': stream.get('height', 0),
            'fps': stream.get('r_frame_rate', '30/1')
        }
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {'codec': None, 'width': 0, 'height': 0, 'fps': '30/1'}


async def normalize_video_to_codec(input_file, output_file, target_codec='h264', progress_callback=None):
    """
    Re-encode a video with CONSISTENT format for merge compatibility.
    Forces: H.264, 720p max, 30fps, AAC audio at 44100Hz.
    This guarantees all videos can be concatenated.
    """
    try:
        duration = await get_video_duration(input_file)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # FFmpeg command with CONSISTENT parameters for all videos
        cmd = [
            'ffmpeg', '-y',
            '-i', input_file,
            # Video: H.264, scale to max 720p maintaining aspect ratio, 30fps
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', '23',
            '-vf', 'scale=-2:720,fps=30',  # Scale to 720p height, 30fps
            '-pix_fmt', 'yuv420p',  # Standard pixel format
            # Audio: AAC, stereo, 44100Hz
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',  # Same sample rate for all
            '-ac', '2',  # Stereo
            # Output settings
            '-movflags', '+faststart',
            '-progress', 'pipe:1',
            output_file
        ]
        
        print(f"Converting: {os.path.basename(input_file)} -> H.264/720p/30fps")
        
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
                    await progress_callback(100, "Complete!")
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
            print(f"Conversion successful: {output_file} ({file_size} bytes)")
            return True
        else:
            stderr = await process.stderr.read()
            print(f"Conversion failed: {stderr.decode()[:1000]}")
            return False
            
    except Exception as e:
        print(f"Conversion error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def trim_video(input_file, output_file, duration=None, start_time=None, end_time=None, progress_callback=None, thumbnail_path=None):
    """
    Trim video to specified duration or from start to end time.
    
    Args:
        input_file: Input video path
        output_file: Output video path
        duration: Duration in seconds (for auto trim from start)
        start_time: Start time string "HH:MM:SS" (for manual trim)
        end_time: End time string "HH:MM:SS" (for manual trim)
        progress_callback: Async progress function
        thumbnail_path: Optional path to save thumbnail
    
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
            await progress_callback(0, "Trimming video...")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
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
            
            # Generate thumbnail if path provided
            if thumbnail_path:
                await generate_trim_thumbnail(output_file, thumbnail_path)
            
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


async def generate_screenshots(input_file, output_dir="Screenshots", interval=5):
    """
    Generate screenshots from video at regular intervals.
    
    Args:
        input_file: Path to the video file
        output_dir: Directory to save screenshots
        interval: Interval in seconds between screenshots (default 5)
    
    Returns:
        List of screenshot file paths
    """
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get video duration
    duration = await get_video_duration(input_file)
    if duration <= 0:
        print("Could not get video duration")
        return []
    
    # Generate base filename from input
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    timestamp = int(time.time())
    
    screenshot_paths = []
    current_time = 0
    screenshot_num = 1
    
    while current_time < duration:
        # Output filename for this screenshot
        output_file = os.path.join(output_dir, f"{base_name}_{timestamp}_ss{screenshot_num:03d}.jpg")
        
        # FFmpeg command to extract single frame
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(current_time),
            '-i', input_file,
            '-vframes', '1',
            '-q:v', '2',  # High quality JPEG
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if os.path.exists(output_file):
                screenshot_paths.append(output_file)
                screenshot_num += 1
        except subprocess.CalledProcessError as e:
            print(f"Error generating screenshot at {current_time}s: {e}")
        
        current_time += interval
    
    return screenshot_paths


async def cleanup_screenshots(screenshot_paths):
    """Remove screenshot files"""
    for path in screenshot_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error removing screenshot {path}: {e}")


async def convert_mkv_to_mp4(input_file, output_file):
    """
    Convert MKV to MP4 using FFmpeg remux (stream copy).
    This just changes the container without re-encoding, so it's very fast.
    
    Args:
        input_file: Path to the input MKV file
        output_file: Path for the output MP4 file
    
    Returns:
        True if conversion successful, False otherwise
    """
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-c', 'copy',  # Copy all streams without re-encoding
        '-movflags', '+faststart',  # Optimize for web playback
        output_file
    ]
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0 and os.path.exists(output_file):
            print(f"MKV to MP4 conversion successful: {output_file}")
            return True
        else:
            print(f"FFmpeg conversion error: {stderr.decode()}")
            return False
    except Exception as e:
        print(f"Error converting MKV to MP4: {e}")
        return False


async def compress_video_single(input_file, output_file, height, duration=0, progress_callback=None, target_percentage=None):
    """
    Compress video to a single resolution with real-time progress tracking.
    Uses ultrafast preset and copies audio for maximum speed.
    
    Args:
        input_file: Path to input video
        output_file: Path for output video
        height: Target height (720, 480, 360)
        duration: Video duration in seconds (for progress calculation)
        progress_callback: Async function(percentage, eta_str) for progress updates
        target_percentage: Target file size as percentage of original (optional)
    
    Returns:
        True if successful, False otherwise
    """
    # Get original file size for bitrate calculation
    original_size = os.path.getsize(input_file)
    
    # Calculate target bitrate if percentage is specified
    target_bitrate = None
    if target_percentage and duration > 0:
        # target_size in bits = original_size * percentage / 100 * 8
        target_size_bits = (original_size * target_percentage / 100) * 8
        # bitrate = total_bits / duration (in kbps)
        target_bitrate = int(target_size_bits / duration / 1000)
        # Ensure minimum bitrate for decent quality
        target_bitrate = max(target_bitrate, 200)  # At least 200kbps
        print(f"Target bitrate calculated: {target_bitrate}kbps for {target_percentage}% compression")
    
    # Optimized FFmpeg command - prioritizing speed with ultrafast preset
    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-vf', f'scale=-2:{height}',
        '-c:v', 'libx264',           # H.264 codec
        '-preset', 'ultrafast',      # Fastest encoding speed
        '-c:a', 'copy',              # Copy audio without re-encoding (saves time & quality)
        '-movflags', '+faststart',
        '-threads', '0',             # Use all available CPU cores
        '-progress', 'pipe:1',       # Output progress to stdout
    ]
    
    # Add bitrate or CRF based on whether target percentage is specified
    if target_bitrate:
        cmd.extend(['-b:v', f'{target_bitrate}k'])
    else:
        cmd.extend(['-crf', '28'])   # Default CRF for reasonable compression
    
    cmd.append(output_file)
    
    process = None
    try:
        print(f"Starting compression to {height}p: {output_file}")
        print(f"FFmpeg command: {' '.join(cmd)}")

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

        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        start_time = time.time()
        last_update = 0
        compression_complete = False
        
        # Read progress from stdout with timeout protection
        try:
            while True:
                try:
                    # Add timeout to readline to prevent hanging
                    line = await asyncio.wait_for(
                        process.stdout.readline(),
                        timeout=120  # Increased timeout to 120 seconds
                    )
                except asyncio.TimeoutError:
                    print(f"Compression readline timeout for {height}p, checking if process is still running")
                    if process.returncode is not None:
                        # Process has ended
                        break
                    continue
                
                if not line:
                    break
                
                line_str = line.decode('utf-8', errors='ignore').strip()
                
                # Detect completion signal from FFmpeg
                if line_str == 'progress=end':
                    compression_complete = True
                    # Send 100% progress
                    if progress_callback:
                        try:
                            await progress_callback(100, "Complete!")
                        except Exception as cb_err:
                            print(f"Progress callback error: {cb_err}")
                    break
                
                # Parse out_time from FFmpeg progress output
                if line_str.startswith('out_time_ms='):
                    try:
                        out_time_ms = int(line_str.split('=')[1])
                        out_time_sec = out_time_ms / 1000000  # Convert microseconds to seconds
                        
                        if duration > 0 and progress_callback:
                            percentage = min((out_time_sec / duration) * 100, 99)
                            
                            # Calculate ETA
                            elapsed = time.time() - start_time
                            if percentage > 0:
                                total_est = elapsed * 100 / percentage
                                eta_ms = int((total_est - elapsed) * 1000)
                                eta_str = TimeFormatter(eta_ms) if eta_ms > 0 else "0s"
                            else:
                                eta_str = "Calculating..."
                            
                            # Update every 3 seconds to avoid flooding
                            now = time.time()
                            if now - last_update >= 3:
                                try:
                                    await progress_callback(percentage, eta_str)
                                except Exception as cb_err:
                                    print(f"Progress callback error: {cb_err}")
                                last_update = now
                    except Exception as parse_err:
                        pass  # Ignore parsing errors
                        
        except Exception as read_err:
            print(f"Error reading FFmpeg output: {read_err}")
        
        # Wait for process to complete with longer timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=60)  # Increased timeout
        except asyncio.TimeoutError:
            print(f"Compression wait timeout for {height}p, killing process")
            try:
                process.kill()
                await process.wait()
            except:
                pass
            return False
        
        # Check result
        if process.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Compression to {height}p successful! Size: {file_size} bytes")
            
            # Final progress update if not already sent
            if progress_callback and not compression_complete:
                try:
                    await progress_callback(100, "Complete!")
                except:
                    pass
            return True
        else:
            # Read stderr for error info
            try:
                stderr_data = await asyncio.wait_for(
                    process.stderr.read(),
                    timeout=5
                )
                print(f"FFmpeg error for {height}p: {stderr_data.decode('utf-8', errors='ignore')[:500]}")
            except:
                print(f"FFmpeg failed for {height}p with return code: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"Exception during compression to {height}p: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup process if it's still running
        if process:
            try:
                process.kill()
                await process.wait()
            except:
                pass
        return False


async def compress_video_multi_resolution(input_file, base_filename, output_dir="Compressed", progress_callback=None):
    """
    Compress video into 720p, 480p, 360p versions with progress tracking.
    Uses CRF 23 (high quality) for best quality-to-size ratio.
    
    Args:
        input_file: Path to the input video file
        base_filename: Base filename for output (without extension)
        output_dir: Directory to save compressed files
        progress_callback: Async function(res_name, status) for progress updates
    
    Returns:
        dict of {resolution: file_path} for successful compressions
    """
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    resolutions = [
        ('720p', 720),
        ('480p', 480),
        ('360p', 360)
    ]
    
    results = {}
    
    for res_name, height in resolutions:
        # Output filename with resolution suffix
        output_file = os.path.join(output_dir, f"{base_filename}_{res_name}.mp4")
        
        if progress_callback:
            await progress_callback(res_name, "compressing")
        
        success = await compress_video_single(input_file, output_file, height)
        
        if success:
            results[res_name] = output_file
            if progress_callback:
                await progress_callback(res_name, "done")
        else:
            if progress_callback:
                await progress_callback(res_name, "failed")
    
    return results


async def cleanup_compressed_files(file_paths):
    """Remove compressed video files"""
    if not file_paths:
        return
    for path in file_paths.values() if isinstance(file_paths, dict) else file_paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error removing compressed file {path}: {e}")


async def merge_videos(input_files, output_file, progress_callback=None):
    """
    Merge multiple video files by converting ALL to same format first.
    Converts every video to H.264/AAC/MP4 for guaranteed compatibility.
    
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
    
    normalized_files = []  # Track converted files for cleanup
    
    try:
        total_files = len(input_files)
        
        if progress_callback:
            await progress_callback(0, f"Converting {total_files} videos...")
        
        # Step 1: Convert ALL videos to H.264/AAC format
        for i, orig_file in enumerate(input_files):
            base_name = os.path.splitext(os.path.basename(orig_file))[0]
            normalized_path = f"MergeFiles/normalized_{int(time.time())}_{i}_{base_name}.mp4"
            
            # Calculate progress for this file (0-70% for conversion phase)
            file_base_pct = (i / total_files) * 70
            
            if progress_callback:
                await progress_callback(file_base_pct, f"Converting {i+1}/{total_files}...")
            
            # Convert to H.264/AAC
            success = await normalize_video_to_codec(orig_file, normalized_path, 'h264', None)
            
            if success and os.path.exists(normalized_path):
                normalized_files.append(normalized_path)
                print(f"Converted {i+1}/{total_files}: {os.path.basename(orig_file)}")
            else:
                print(f"Failed to convert: {orig_file}")
                # Cleanup and fail
                for nf in normalized_files:
                    try:
                        if os.path.exists(nf):
                            os.remove(nf)
                    except:
                        pass
                return False
        
        if progress_callback:
            await progress_callback(70, "Merging videos...")
        
        # Step 2: Merge all converted files
        input_list_file = f"merge_input_{int(time.time())}.txt"
        
        # Calculate total duration
        total_duration = 0
        for f in normalized_files:
            duration = await get_video_duration(f)
            total_duration += duration
        
        # Write concat input file
        with open(input_list_file, 'w', encoding='utf-8') as f:
            for video_file in normalized_files:
                abs_path = os.path.abspath(video_file)
                ffmpeg_path = abs_path.replace(os.sep, '/')
                escaped_path = ffmpeg_path.replace("'", "'\\''")
                f.write(f"file '{escaped_path}'\n")
        
        print(f"Created input list with {len(normalized_files)} converted files")
        
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
        
        print(f"FFmpeg merge: {' '.join(cmd)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        start_time = time.time()
        last_update = 0
        
        # Read progress
        try:
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
                        overall_pct = 70 + (merge_pct * 0.3)  # 70-100% range
                        overall_pct = min(overall_pct, 99)
                        
                        now = time.time()
                        if now - last_update >= 3 and progress_callback:
                            await progress_callback(overall_pct, f"Merging: {merge_pct:.0f}%")
                            last_update = now
                    except:
                        pass
                        
        except Exception as e:
            print(f"Progress read error: {e}")
        
        # Cleanup input list
        try:
            if os.path.exists(input_list_file):
                os.remove(input_list_file)
        except:
            pass
        
        # Wait for completion
        try:
            await asyncio.wait_for(process.wait(), timeout=120)
        except asyncio.TimeoutError:
            print("Merge timeout")
            process.kill()
            await process.wait()
            return False
        
        # Check result
        if process.returncode == 0 and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Merge successful! Size: {file_size} bytes")
            return True
        else:
            stderr_data = await process.stderr.read()
            print(f"Merge failed: {stderr_data.decode('utf-8', errors='ignore')[:500]}")
            return False
            
    except Exception as e:
        print(f"Merge error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup converted temp files
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


async def add_text_watermark(input_file, output_file, text, position="bottom_right",
                              font_size=24, opacity=0.7, progress_callback=None):
    """
    Adds text watermark using FFmpeg drawtext filter.
    
    Position mapping (FFmpeg x:y coordinates):
      top_left      → x=10:y=10
      top_right     → x=w-tw-10:y=10
      center        → x=(w-tw)/2:y=(h-th)/2
      center_left   → x=10:y=(h-th)/2
      center_right  → x=w-tw-10:y=(h-th)/2
      bottom_left   → x=10:y=h-th-10
      bottom_right  → x=w-tw-10:y=h-th-10
    """
    position_map = {
        'top_left': 'x=10:y=10',
        'top_right': 'x=w-tw-10:y=10',
        'center': 'x=(w-tw)/2:y=(h-th)/2',
        'center_left': 'x=10:y=(h-th)/2',
        'center_right': 'x=w-tw-10:y=(h-th)/2',
        'bottom_left': 'x=10:y=h-th-10',
        'bottom_right': 'x=w-tw-10:y=h-th-10',
    }
    
    pos_coords = position_map.get(position, position_map['bottom_right'])
    
    # Escape special characters in text for FFmpeg
    escaped_text = text.replace("'", "\\'").replace(":", "\\:").replace("\\", "\\\\")
    
    # Build drawtext filter
    drawtext = (
        f"drawtext=text='{escaped_text}':"
        f"fontsize={font_size}:"
        f"fontcolor=white@{opacity}:"
        f"{pos_coords}:"
        f"borderw=2:bordercolor=black@0.5"
    )
    
    try:
        duration = await get_video_duration(input_file)
        
        cmd = [
            'ffmpeg', '-y',
            '-i', input_file,
            '-vf', drawtext,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', '23',
            '-c:a', 'copy',
            '-movflags', '+faststart',
            '-progress', 'pipe:1',
            output_file
        ]
        
        print(f"Adding watermark '{text}' at {position}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        start_time_val = time.time()
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
                    await progress_callback(100, "Complete!")
                break
            
            if line_str.startswith('out_time_ms=') and duration > 0 and progress_callback:
                try:
                    out_time_ms = int(line_str.split('=')[1])
                    out_time_sec = out_time_ms / 1000000
                    percentage = min((out_time_sec / duration) * 100, 99)
                    
                    now = time.time()
                    if now - last_update >= 3:
                        await progress_callback(percentage, "Adding watermark...")
                        last_update = now
                except:
                    pass
        
        await asyncio.wait_for(process.wait(), timeout=600)
        
        if process.returncode == 0 and os.path.exists(output_file):
            print(f"Watermark added successfully: {output_file}")
            return True
        else:
            stderr = await process.stderr.read()
            print(f"Watermark failed: {stderr.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"Watermark error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def extract_audio_from_video(input_file, output_file, audio_format="mp3",
                                    bitrate="192k", progress_callback=None):
    """
    Extract audio track from video using FFmpeg.
    
    Args:
        input_file: Path to input video
        output_file: Path for output audio file
        audio_format: Output format (mp3, aac, flac, etc.)
        bitrate: Audio bitrate (128k, 192k, 320k)
        progress_callback: Async function(percentage, status)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        duration = await get_video_duration(input_file)
        
        cmd = [
            'ffmpeg', '-y',
            '-i', input_file,
            '-vn',  # No video
            '-c:a', 'libmp3lame' if audio_format == 'mp3' else 'aac',
            '-b:a', bitrate,
            '-progress', 'pipe:1',
            output_file
        ]
        
        print(f"Extracting audio to {audio_format} at {bitrate}")
        
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
            
            if line_str.startswith('out_time_ms=') and duration > 0 and progress_callback:
                try:
                    out_time_ms = int(line_str.split('=')[1])
                    out_time_sec = out_time_ms / 1000000
                    percentage = min((out_time_sec / duration) * 100, 99)
                    
                    now = time.time()
                    if now - last_update >= 2:
                        await progress_callback(percentage, "Extracting audio...")
                        last_update = now
                except:
                    pass
        
        await asyncio.wait_for(process.wait(), timeout=300)
        
        if process.returncode == 0 and os.path.exists(output_file):
            print(f"Audio extraction successful: {output_file}")
            return True
        else:
            stderr = await process.stderr.read()
            print(f"Audio extraction failed: {stderr.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return False



# Subtitle muxing functions have been moved to helper/subtitle_ffmpeg.py

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
