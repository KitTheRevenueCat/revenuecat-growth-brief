#!/usr/bin/env python3
"""
Video builder v4: generates voiceover in 2 large chunks to minimize splice artifacts,
adds audio crossfades, proper 16:9 screenshots, hold + fade ending.
"""

import subprocess, json, requests
from pathlib import Path

ASSETS = Path(__file__).parent
OUTPUT = ASSETS.parent / "VIDEO_DEMO.mp4"

ELEVENLABS_API_KEY = "sk_667a7591c7e0b6abfec1e4ee9736851785ce5a7405f7604c"
VOICE_ID = "UgBBYS2sOqTuMpoF3BR0"
MODEL_ID = "eleven_v3"

# Generate voiceover in 2 chunks to minimize splicing artifacts
# Chunk 1: scenes 1-3 (intro + investigation queue)
# Chunk 2: scenes 4-6 (KPIs + philosophy + CTA)

CHUNK1_TEXT = (
    "[confident, measured] Revenue up fourteen point seven percent. "
    "Trials up fourteen point seven percent. "
    "Monthly Recurring Revenue ... down three percent. "
    "[slightly concerned] That's exactly the kind of subscription contradiction "
    "dashboards make too easy to miss. "
    "... "
    "[enthusiastic] This is RevenueCat Growth Brief — a brief-first monetization operator "
    "built on top of the Charts API. Instead of rebuilding RevenueCat's dashboard, "
    "it wraps a thin command-center shell around a weekly investigation brief. "
    "It answers three questions: what changed, why it matters, and what to investigate next. "
    "... "
    "[clear, explanatory] Here's the investigation queue — ranked priorities "
    "with evidence and next steps. Priority one: acquisition quality check. "
    "Trial volume grew but conversion fell. "
    "Priority two: revenue momentum improved, but Monthly Recurring Revenue didn't follow. "
    "Each finding links to the exact evidence and tells you where to dig next."
)

CHUNK2_TEXT = (
    "[steady] Key performance indicator cards give you headline context: "
    "Monthly Recurring Revenue, revenue, new customers, "
    "active subscriptions, active trials. "
    "Below the brief, supporting charts back every finding — "
    "revenue, Monthly Recurring Revenue, conversion rate, and churn. "
    "The charts are evidence, not the product. "
    "They exist to validate the brief, not to replace it. "
    "... "
    "[thoughtful] I intentionally kept this deterministic and high-trust. "
    "No fake AI causality. No forecasting theater. "
    "The brief engine is about a hundred and fifty lines of TypeScript "
    "with transparent rules anyone can audit. "
    "The product thesis: build the insight layer on top of "
    "RevenueCat's existing charts. "
    "... "
    "[warm, inviting] Clone the repo, connect your RevenueCat project, "
    "and turn chart data into a weekly growth brief "
    "your team can actually use. ... Link in the description."
)

# Scene-to-image mapping (still 6 scenes visually, but only 2 audio chunks)
SCENE_IMAGES = ["scene1_v3.jpg", "scene2_v3.jpg", "scene3_v3.jpg", "scene4_v3.jpg", "scene5_v3.jpg", "scene6_v3.jpg"]


def generate_chunk(chunk_id, text):
    mp3_path = ASSETS / f"chunk{chunk_id}_v4.mp3"
    if mp3_path.exists():
        print(f"  [skip] {mp3_path.name} exists")
        return mp3_path

    print(f"  [tts] chunk {chunk_id}...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, json={
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "use_speaker_boost": True},
    }, headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}, stream=True)

    if response.status_code != 200:
        print(f"  [error] {response.status_code}: {response.text[:300]}")
        return None

    with open(mp3_path, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)
    return mp3_path


def get_duration(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)], capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def main():
    print("=== Video Builder v4 (2-chunk voiceover, crossfades) ===\n")

    # Check scene images
    for img_name in SCENE_IMAGES:
        if not (ASSETS / img_name).exists():
            print(f"  [error] Missing {img_name}")
            return

    # Generate 2 audio chunks
    print("[1/3] Generating voiceover (2 chunks)...")
    chunk1 = generate_chunk(1, CHUNK1_TEXT)
    chunk2 = generate_chunk(2, CHUNK2_TEXT)
    if not chunk1 or not chunk2:
        return

    dur1 = get_duration(chunk1)
    dur2 = get_duration(chunk2)
    print(f"  Chunk 1: {dur1:.1f}s")
    print(f"  Chunk 2: {dur2:.1f}s")

    # Crossfade the 2 chunks with a 0.5s overlap
    XFADE = 0.5
    concat_audio = ASSETS / "voiceover_v4.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(chunk1), "-i", str(chunk2),
        "-filter_complex",
        f"[0:a][1:a]acrossfade=d={XFADE}:c1=tri:c2=tri[aout]",
        "-map", "[aout]", "-c:a", "libmp3lame", "-b:a", "128k",
        str(concat_audio),
    ], capture_output=True, check=True)

    total_audio = get_duration(concat_audio)
    print(f"  Combined: {total_audio:.1f}s (with {XFADE}s crossfade)")

    # Split audio duration roughly across 6 scenes
    # Chunk 1 covers scenes 1-3, chunk 2 covers scenes 4-6
    chunk1_per_scene = (dur1 - XFADE/2) / 3
    chunk2_per_scene = (dur2 - XFADE/2) / 3
    scene_durations = [chunk1_per_scene]*3 + [chunk2_per_scene]*3

    # Adjust last scene to eat any rounding
    TAIL_HOLD = 2.5
    FADE_DUR = 1.5

    print("\n[2/3] Scene timing:")
    for i, d in enumerate(scene_durations):
        print(f"  Scene {i+1}: {d:.1f}s")

    # Build video
    print("\n[3/3] Assembling video...")
    inputs = []
    filter_parts = []
    for i, img_name in enumerate(SCENE_IMAGES):
        img = ASSETS / img_name
        dur = scene_durations[i]
        inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", str(img)])
        filter_parts.append(
            f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x09090b,setsar=1,format=yuv420p[v{i}]"
        )

    concat_inputs = "".join(f"[v{i}]" for i in range(6))
    total_video_dur = sum(scene_durations) + TAIL_HOLD
    fade_start = total_video_dur - FADE_DUR
    filter_parts.append(
        f"{concat_inputs}concat=n=6:v=1:a=0,"
        f"tpad=stop_mode=clone:stop_duration={TAIL_HOLD},"
        f"fade=t=out:st={fade_start}:d={FADE_DUR}[vout]"
    )

    audio_idx = 6
    audio_fade_start = total_video_dur - FADE_DUR
    audio_filter = f"[{audio_idx}:a]apad=pad_dur={TAIL_HOLD},afade=t=out:st={audio_fade_start}:d={FADE_DUR}[aout]"

    cmd = [
        "ffmpeg", "-y", *inputs, "-i", str(concat_audio),
        "-filter_complex", ";".join(filter_parts) + ";" + audio_filter,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p",
        "-t", f"{total_video_dur:.1f}",
        "-movflags", "+faststart", str(OUTPUT),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [error]\n{result.stderr[-1500:]}")
        return

    print(f"\n✅ {OUTPUT}")
    print(f"   Duration: {get_duration(OUTPUT):.1f}s | Size: {OUTPUT.stat().st_size/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
