#!/usr/bin/env python3
"""
Video builder v6: single take voiceover, 7 scene images with precise timing,
charts appear when "below the brief" is spoken (~68s).
"""

import subprocess, json
from pathlib import Path

ASSETS = Path(__file__).parent
OUTPUT = ASSETS.parent / "VIDEO_DEMO.mp4"

# Reuse the v5 voiceover (single continuous take, no splices)
VOICEOVER = ASSETS / "voiceover_v5.mp3"

# 7 scenes with manual timing (based on listening to the voiceover)
# Total voiceover: ~113s
SCENES = [
    ("scene1_v3.jpg",  14.5),   # Hero — contradiction hook (0-14.5s)
    ("scene2_v3.jpg",  19.0),   # Brief intro (14.5-33.5s)
    ("scene3_v3.jpg",  20.5),   # Investigation queue (33.5-54s)
    ("scene4a_v5.jpg", 14.0),   # KPI cards (54-68s)
    ("scene4b_v5.jpg", 14.0),   # Charts — "below the brief" (68-82s)
    ("scene5_v3.jpg",  20.0),   # Philosophy/deterministic (82-102s)
    ("scene6_v3.jpg",  11.0),   # CTA (102-113s)
]

LEAD_SILENCE = 1.5
TAIL_HOLD = 2.5
FADE_DUR = 1.5


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        capture_output=True, text=True,
    )
    return float(json.loads(r.stdout)["format"]["duration"])


def main():
    print("=== Video Builder v6 (7 scenes, precise timing) ===\n")

    if not VOICEOVER.exists():
        print(f"[error] Missing voiceover: {VOICEOVER}")
        return

    vo_dur = get_duration(VOICEOVER)
    scene_total = sum(d for _, d in SCENES)
    print(f"Voiceover: {vo_dur:.1f}s")
    print(f"Scene total: {scene_total:.1f}s")

    # Adjust last scene to match voiceover exactly
    diff = vo_dur - scene_total
    name, dur = SCENES[-1]
    SCENES[-1] = (name, dur + diff)

    total_dur = LEAD_SILENCE + vo_dur + TAIL_HOLD

    print(f"\nScene timing:")
    t = LEAD_SILENCE
    for i, (name, dur) in enumerate(SCENES):
        extra = " (+lead silence)" if i == 0 else ""
        actual = dur + (LEAD_SILENCE if i == 0 else 0)
        print(f"  {i+1}. {name}: {actual:.1f}s ({t:.1f}s - {t+actual:.1f}s){extra}")
        t += actual

    # Build ffmpeg command
    inputs = []
    filter_parts = []
    n = len(SCENES)

    for i, (img_name, dur) in enumerate(SCENES):
        img = ASSETS / img_name
        actual_dur = dur + (LEAD_SILENCE if i == 0 else 0)
        if i == n - 1:
            actual_dur += TAIL_HOLD  # Last scene holds
        inputs.extend(["-loop", "1", "-t", f"{actual_dur:.3f}", "-i", str(img)])
        filter_parts.append(
            f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x09090b,setsar=1,format=yuv420p[v{i}]"
        )

    concat_inputs = "".join(f"[v{i}]" for i in range(n))
    fade_start = total_dur - FADE_DUR
    filter_parts.append(
        f"{concat_inputs}concat=n={n}:v=1:a=0,"
        f"fade=t=out:st={fade_start}:d={FADE_DUR}[vout]"
    )

    audio_idx = n
    audio_fade_start = total_dur - FADE_DUR
    audio_filter = (
        f"[{audio_idx}:a]adelay={int(LEAD_SILENCE*1000)}|{int(LEAD_SILENCE*1000)},"
        f"apad=pad_dur={TAIL_HOLD},"
        f"afade=t=out:st={audio_fade_start}:d={FADE_DUR}[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-i", str(VOICEOVER),
        "-filter_complex", ";".join(filter_parts) + ";" + audio_filter,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p",
        "-t", f"{total_dur:.1f}",
        "-movflags", "+faststart",
        str(OUTPUT),
    ]

    print("\nAssembling...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[error]\n{result.stderr[-1500:]}")
        return

    final_dur = get_duration(OUTPUT)
    fsize = OUTPUT.stat().st_size / 1024 / 1024
    print(f"\n✅ {OUTPUT}")
    print(f"   Duration: {final_dur:.1f}s | Size: {fsize:.1f} MB")


if __name__ == "__main__":
    main()
