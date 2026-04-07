#!/usr/bin/env python3
"""Compose slide images into a video using ffmpeg.

Usage:
    python3 compose_video.py --slides-dir <dir> --output <file.mp4> [options]
    python3 compose_video.py --help

Options:
    --slides-dir DIR         Directory containing slide_XX.png files (required)
    --output FILE            Output video path (required)
    --duration SECONDS       Total video duration, default 60
    --transition TYPE        Transition type: crossfade (default), none
    --transition-duration S  Transition duration in seconds, default 0.5
    --audio FILE             Optional audio track to overlay
    --fps N                  Frames per second, default 30
    --durations JSON         JSON array of per-slide durations (overrides --duration)
"""

import glob
import json
import math
import os
import subprocess
import sys


def get_slide_files(slides_dir: str) -> list[str]:
    """Find slide images sorted by name."""
    patterns = ["slide_*.png", "slide_*.jpg"]
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(slides_dir, pat)))
    files.sort()
    if not files:
        print(f"ERROR: No slide images found in {slides_dir}")
        sys.exit(1)
    return files


def compute_durations(n_slides: int, total_duration: float,
                      transition_dur: float, per_slide: list[float] | None) -> list[float]:
    """Compute how long each slide displays (excluding transition overlap)."""
    if per_slide and len(per_slide) == n_slides:
        return per_slide
    # Distribute evenly, accounting for transition overlap
    total_transitions = (n_slides - 1) * transition_dur
    available = total_duration - total_transitions
    if available < n_slides * 0.5:
        available = n_slides * 0.5
    each = available / n_slides
    return [each] * n_slides


def build_ffmpeg_crossfade(slide_files: list[str], durations: list[float],
                           transition_dur: float, output: str, fps: int,
                           audio: str | None):
    """Build and execute an ffmpeg command with crossfade transitions."""
    n = len(slide_files)

    if n == 1:
        # Single slide — just show it for the duration
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", slide_files[0],
               "-t", str(durations[0]),
               "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps={fps}",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", output]
        subprocess.run(cmd, check=True)
        return

    # Build complex filtergraph with xfade transitions
    inputs = []
    for i, f in enumerate(slide_files):
        inputs.extend(["-loop", "1", "-t", str(durations[i] + transition_dur), "-i", f])

    # Scale all inputs
    filter_parts = []
    for i in range(n):
        filter_parts.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
                            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,"
                            f"setsar=1,fps={fps}[v{i}];")

    # Chain xfade transitions
    offset = durations[0]
    prev = "v0"
    for i in range(1, n):
        out_label = f"xf{i}" if i < n - 1 else "vout"
        filter_parts.append(
            f"[{prev}][v{i}]xfade=transition=fade:duration={transition_dur}:offset={offset:.3f}[{out_label}];"
        )
        prev = out_label
        if i < n - 1:
            offset += durations[i]

    filtergraph = "".join(filter_parts).rstrip(";")

    cmd = ["ffmpeg", "-y"] + inputs
    cmd.extend(["-filter_complex", filtergraph, "-map", "[vout]"])
    cmd.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast"])

    if audio and os.path.isfile(audio):
        cmd.extend(["-i", audio, "-map", f"{n}:a", "-c:a", "aac", "-shortest"])

    cmd.append(output)

    print(f"Running ffmpeg ({n} slides, {sum(durations):.1f}s)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ffmpeg STDERR:", result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
        sys.exit(1)
    print(f"Video saved to {output}")


def build_ffmpeg_concat(slide_files: list[str], durations: list[float],
                        output: str, fps: int, audio: str | None):
    """Simple concatenation without transitions (faster)."""
    # Create a concat file
    concat_path = output + ".concat.txt"
    with open(concat_path, "w") as f:
        for slide, dur in zip(slide_files, durations):
            f.write(f"file '{os.path.abspath(slide)}'\n")
            f.write(f"duration {dur}\n")
        # Repeat last to avoid ffmpeg concat truncation
        f.write(f"file '{os.path.abspath(slide_files[-1])}'\n")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_path,
           "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,"
                  f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps={fps}",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast"]

    if audio and os.path.isfile(audio):
        cmd.extend(["-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-shortest"])

    cmd.append(output)

    print(f"Running ffmpeg concat ({len(slide_files)} slides)...")
    subprocess.run(cmd, check=True)
    os.remove(concat_path)
    print(f"Video saved to {output}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slides-dir", required=True, help="Directory with slide PNGs")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--duration", type=float, default=60, help="Total duration (seconds)")
    parser.add_argument("--transition", default="crossfade", choices=["crossfade", "none"])
    parser.add_argument("--transition-duration", type=float, default=0.5)
    parser.add_argument("--audio", help="Optional audio file path")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--durations", help="JSON array of per-slide durations")

    args = parser.parse_args()

    slides = get_slide_files(args.slides_dir)
    per_slide = json.loads(args.durations) if args.durations else None
    durations = compute_durations(len(slides), args.duration,
                                  args.transition_duration, per_slide)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)

    if args.transition == "crossfade":
        build_ffmpeg_crossfade(slides, durations, args.transition_duration,
                               args.output, args.fps, args.audio)
    else:
        build_ffmpeg_concat(slides, durations, args.output, args.fps, args.audio)


if __name__ == "__main__":
    main()
