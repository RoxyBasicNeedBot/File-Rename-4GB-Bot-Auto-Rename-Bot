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

# Subtitle FFmpeg Helper — Dedicated subtitle muxing module
# Separated from ffmpeg.py for clarity and maintainability
# Uses MKV container for best subtitle compatibility (VLC, MX Player, mpv)
#
# PRIMARY:  mkvmerge (MKVToolNix) — industry standard, zero re-encoding
# FALLBACK: ffmpeg with -c:s copy  — if mkvmerge is not installed

import os
import asyncio
import shutil


# ISO 639-2 language codes for subtitle tracks
SUBTITLE_LANGUAGES = {
    'eng': 'English',
    'hin': 'Hindi',
    'tam': 'Tamil',
    'tel': 'Telugu',
    'jpn': 'Japanese',
    'kor': 'Korean',
    'ara': 'Arabic',
    'und': 'Undefined',
}

# Cache mkvmerge availability (checked once)
_mkvmerge_available = None


def is_mkvmerge_available():
    """Check if mkvmerge binary is available on the system (cached)."""
    global _mkvmerge_available
    if _mkvmerge_available is None:
        _mkvmerge_available = shutil.which('mkvmerge') is not None
        if _mkvmerge_available:
            print("[SubMux] ✅ mkvmerge found — using MKVToolNix (primary)")
        else:
            print("[SubMux] ⚠️ mkvmerge not found — falling back to FFmpeg")
    return _mkvmerge_available


async def mux_subtitles(video_path, subtitle_list, output_path):
    """
    Mux multiple subtitle files into a video as selectable tracks.
    Always outputs MKV for best subtitle compatibility.

    Strategy:
      1. Try mkvmerge (MKVToolNix) — most reliable for MKV operations
      2. Fall back to ffmpeg with -c:s copy if mkvmerge unavailable

    Args:
        video_path: Path to input video
        subtitle_list: List of dicts:
            [{'path': '/path/to/sub.srt', 'lang': 'eng', 'title': 'English'}, ...]
        output_path: Path for output file (will be forced to .mkv)

    Returns:
        (success: bool, actual_output_path: str)
    """
    if not subtitle_list:
        print("[SubMux] No subtitles to mux")
        return False, output_path

    # Force MKV output for best subtitle support
    base_no_ext = os.path.splitext(output_path)[0]
    mkv_output = base_no_ext + '.mkv'

    if is_mkvmerge_available():
        success, result_path = await _mux_with_mkvmerge(video_path, subtitle_list, mkv_output)
        if success:
            return True, result_path
        # If mkvmerge fails, try ffmpeg as fallback
        print("[SubMux] mkvmerge failed, trying FFmpeg fallback...")

    return await _mux_with_ffmpeg(video_path, subtitle_list, mkv_output)


async def _mux_with_mkvmerge(video_path, subtitle_list, mkv_output):
    """
    Mux subtitles using mkvmerge (MKVToolNix).

    mkvmerge is the industry standard for MKV operations:
      - Zero re-encoding of any stream
      - Native support for SRT, ASS, SSA, VTT, SUB
      - Correct Matroska timestamp handling
      - Properly handles image-based subs in source
    """
    try:
        # Build mkvmerge command
        # --no-subtitles on the video input: strip existing subs from source
        # (we only want the new user-provided subtitle tracks)
        cmd = [
            'mkvmerge',
            '-o', mkv_output,
            '--no-subtitles',   # Don't carry existing subtitle tracks from source
            video_path,
        ]

        # Add each subtitle file with language and track name metadata
        for i, sub_info in enumerate(subtitle_list):
            lang = sub_info.get('lang', 'und')
            title = sub_info.get('title', SUBTITLE_LANGUAGES.get(lang, lang))

            cmd.extend([
                '--language', f'0:{lang}',
                '--track-name', f'0:{title}',
            ])

            # First subtitle track is the default (auto-shown in players)
            if i == 0:
                cmd.extend(['--default-track-flag', '0:1'])
            else:
                cmd.extend(['--default-track-flag', '0:0'])

            cmd.append(sub_info['path'])

        # Log
        sub_count = len(subtitle_list)
        lang_info = ', '.join(
            [f"{s.get('title', '?')} ({s.get('lang', '?')})" for s in subtitle_list]
        )
        print(f"[SubMux/mkvmerge] Muxing {sub_count} subtitle(s): {lang_info}")
        print(f"[SubMux/mkvmerge] Command: {' '.join(cmd)}")

        # Execute
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=300
        )

        if process.returncode == 0 and os.path.exists(mkv_output) and os.path.getsize(mkv_output) > 0:
            print(f"[SubMux/mkvmerge] ✅ Success: {mkv_output} ({os.path.getsize(mkv_output)} bytes)")
            return True, mkv_output
        else:
            # mkvmerge returns 1 for warnings (still success), 2 for errors

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

            output_text = stdout.decode(errors='replace')[:500]
            stderr_text = stderr.decode(errors='replace')[:500]

            if process.returncode == 1 and os.path.exists(mkv_output) and os.path.getsize(mkv_output) > 0:
                # Return code 1 = warnings, output is still valid
                print(f"[SubMux/mkvmerge] ⚠️ Warnings but output OK: {output_text}")
                return True, mkv_output

            print(f"[SubMux/mkvmerge] ❌ Failed (exit {process.returncode})")
            print(f"[SubMux/mkvmerge] stdout: {output_text}")
            print(f"[SubMux/mkvmerge] stderr: {stderr_text}")
            return False, mkv_output

    except asyncio.TimeoutError:
        print("[SubMux/mkvmerge] ❌ Timeout (>300s)")
        return False, mkv_output
    except Exception as e:
        print(f"[SubMux/mkvmerge] ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, mkv_output


async def _mux_with_ffmpeg(video_path, subtitle_list, mkv_output):
    """
    Fallback: mux subtitles using FFmpeg.

    CRITICAL FIXES (vs previous broken version):
      1. Uses '-c:s copy' — copies subtitle bytes verbatim, NO re-encoding
         (previously used 'subrip' encoder which corrupted non-UTF8 files)
      2. REMOVED '-max_interleave_delta 0' — was corrupting video timestamps
      3. Maps only video+audio from source (no existing subs that might be
         image-based and incompatible)
    """
    try:
        # Build ffmpeg command
        cmd = ['ffmpeg', '-y', '-i', video_path]

        # Add each subtitle file as a separate input
        for sub_info in subtitle_list:
            cmd.extend(['-i', sub_info['path']])

        # Stream mapping: ONLY video + audio from source
        # DO NOT use '-map 0' — it copies existing subtitle tracks
        # which may be image-based (hdmv_pgs) and cause crashes
        cmd.extend([
            '-map', '0:v',      # video streams only
            '-map', '0:a?',     # audio streams (? = optional)
        ])

        # Map each new subtitle input (inputs 1, 2, 3, …)
        for i in range(len(subtitle_list)):
            cmd.extend(['-map', str(i + 1)])

        # Codec settings — copy everything, NO re-encoding
        cmd.extend([
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-c:s', 'copy',     # KEY FIX: copy subtitles verbatim (was 'subrip')
        ])

        # Metadata for each subtitle track
        for i, sub_info in enumerate(subtitle_list):
            lang = sub_info.get('lang', 'und')
            title = sub_info.get('title', SUBTITLE_LANGUAGES.get(lang, lang))
            cmd.extend([
                f'-metadata:s:s:{i}', f'language={lang}',
                f'-metadata:s:s:{i}', f'title={title}',
            ])

        # Mark first subtitle as default (auto-shown in players)
        if len(subtitle_list) > 0:
            cmd.extend(['-disposition:s:0', 'default'])

        # NOTE: '-max_interleave_delta 0' was REMOVED
        # It was corrupting video timestamps on certain files

        cmd.append(mkv_output)

        # Log
        sub_count = len(subtitle_list)
        lang_info = ', '.join(
            [f"{s.get('title', '?')} ({s.get('lang', '?')})" for s in subtitle_list]
        )
        print(f"[SubMux/ffmpeg] Muxing {sub_count} subtitle(s): {lang_info}")
        print(f"[SubMux/ffmpeg] Command: {' '.join(cmd)}")

        # Execute
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=300
        )

        if process.returncode == 0 and os.path.exists(mkv_output) and os.path.getsize(mkv_output) > 0:
            print(f"[SubMux/ffmpeg] ✅ Success: {mkv_output} ({os.path.getsize(mkv_output)} bytes)")
            return True, mkv_output
        else:
            stderr_text = stderr.decode(errors='replace')[:800]
            print(f"[SubMux/ffmpeg] ❌ Failed (exit {process.returncode}): {stderr_text}")
            return False, mkv_output

    except asyncio.TimeoutError:
        print("[SubMux/ffmpeg] ❌ Timeout (>300s)")
        return False, mkv_output
    except Exception as e:
        print(f"[SubMux/ffmpeg] ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, mkv_output


async def mux_soft_subtitle(video_path, sub_path, output_path):
    """
    Backward-compatible wrapper: adds a single subtitle track.
    Always outputs MKV.
    """
    subtitle_list = [{
        'path': sub_path,
        'lang': 'eng',
        'title': 'English',
    }]
    success, actual_path = await mux_subtitles(video_path, subtitle_list, output_path)

    # Rename to expected path for backward compat if needed
    if success and actual_path != output_path:
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(actual_path, output_path)
        except Exception as e:
            print(f"[SubMux] Rename failed: {e}, using {actual_path}")
            output_path = actual_path

    return success

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
