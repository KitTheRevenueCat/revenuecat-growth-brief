#!/usr/bin/env python3
"""
Produce a ~90-second demo video for RevenueCat Growth Brief.
Uses ElevenLabs v3 with audio tags for voiceover, static screenshots for visuals, ffmpeg for assembly.
"""

import os, subprocess, json, requests
from pathlib import Path

ASSETS = Path(__file__).parent
FULL_IMG = ASSETS / "full-page.jpg"
OUTPUT = ASSETS.parent / "VIDEO_DEMO.mp4"

ELEVENLABS_API_KEY = "sk_667a7591c7e0b6abfec1e4ee9736851785ce5a7405f7604c"
VOICE_ID = "UgBBYS2sOqTuMpoF3BR0"
MODEL_ID = "eleven_v3"

# v3 audio tags for natural delivery
SCENES = [
    {
        "id": "scene1",
        "text": (
            "[confident, measured] Revenue up fourteen point seven percent. "
            "Trials up fourteen point seven percent. "
            "MRR... down three percent. "
            "[slightly concerned] That's exactly the kind of subscription contradiction "
            "dashboards make too easy to miss."
        ),
        "scroll_pct": 0,
    },
    {
        "id": "scene2",
        "text": (
            "[enthusiastic] This is RevenueCat Growth Brief — a brief-first monetization operator "
            "built on top of the Charts API. Instead of rebuilding RevenueCat's dashboard, "
            "it wraps a thin command-center shell around a weekly investigation brief. "
            "It answers three questions: what changed, why it matters, and what to investigate next."
        ),
        "scroll_pct": 5,
    },
    {
        "id": "scene3",
        "text": (
            "[clear, explanatory] Here's the investigation queue — ranked priorities "
            "with evidence and next steps. Priority one: acquisition quality check. "
            "Trial volume grew but conversion fell. "
            "Priority two: revenue momentum improved, but recurring revenue didn't follow. "
            "Each finding links to the exact evidence and tells you where to dig next."
        ),
        "scroll_pct": 20,
    },
    {
        "id": "scene4",
        "text": (
            "[steady] KPI cards give you headline context: MRR, revenue, new customers, "
            "active subscriptions, active trials. "
            "Below the brief, supporting charts back every finding — "
            "revenue, MRR, conversion rate, and churn. "
            "The charts are evidence, not the product. "
            "They exist to validate the brief, not to replace it."
        ),
        "scroll_pct": 40,
    },
    {
        "id": "scene5",
        "text": (
            "[thoughtful] I intentionally kept this deterministic and high-trust. "
            "No fake AI causality. No forecasting theater. "
            "The brief engine is about a hundred and fifty lines of TypeScript "
            "with transparent rules anyone can audit. "
            "The product thesis: build the insight layer on top of "
            "RevenueCat's existing charts."
        ),
        "scroll_pct": 75,
    },
    {
        "id": "scene6",
        "text": (
            "[warm, inviting] Clone the repo, connect your RevenueCat project, "
            "and turn chart data into a weekly growth brief "
            "your team can actually use. Link in the description."
        ),
        "scroll_pct": 0,
    },
]


def generate_voiceover(scene):
    """Generate TTS audio using ElevenLabs v3."""
    mp3_path = ASSETS / f"{scene['id']}_v2.mp3"
    if mp3_path.exists():
        print(f"  [skip] {mp3_path.name} already exists")
        return mp3_path

    print(f"  [tts] Generating {scene['id']} via ElevenLabs v3...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": scene["text"],
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.4,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)
    if response.status_code != 200:
        print(f"  [error] ElevenLabs API returned {response.status_code}: {response.text[:500]}")
        return None

    with open(mp3_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return mp3_path


def get_audio_duration(path):
    """Get duration in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        capture_output=True, text=True,
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def crop_scene_image(full_img, scroll_pct, out_path, viewport_h=720):
    """Crop a viewport-sized region from the full-page screenshot."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(full_img)],
        capture_output=True, text=True,
    )
    info = json.loads(result.stdout)
    total_h = int(info["streams"][0]["height"])
    total_w = int(info["streams"][0]["width"])

    max_y = max(total_h - viewport_h, 0)
    y = int(max_y * scroll_pct / 100)

    subprocess.run([
        "ffmpeg", "-y", "-i", str(full_img),
        "-vf", f"crop={total_w}:{viewport_h}:0:{y},scale=1280:720",
        str(out_path),
    ], capture_output=True, check=True)
    return out_path


def main():
    print("=== RevenueCat Growth Brief Video Builder (ElevenLabs v3) ===\n")

    # Step 1: Generate all voiceover segments
    print("[1/4] Generating voiceover audio via ElevenLabs v3...")
    audio_files = []
    for scene in SCENES:
        audio_path = generate_voiceover(scene)
        if audio_path is None:
            print("  [fatal] TTS generation failed, aborting.")
            return
        audio_files.append(audio_path)

    # Step 2: Get durations
    print("\n[2/4] Computing durations...")
    durations = []
    for af in audio_files:
        dur = get_audio_duration(af)
        durations.append(dur)
        print(f"  {af.name}: {dur:.1f}s")
    total = sum(durations)
    print(f"  Total: {total:.1f}s")

    # Step 3: Crop scene images
    print("\n[3/4] Preparing scene images...")
    scene_images = []
    for scene in SCENES:
        img_out = ASSETS / f"{scene['id']}_v2.jpg"
        crop_scene_image(FULL_IMG, scene["scroll_pct"], img_out)
        scene_images.append(img_out)
        print(f"  {img_out.name} (scroll {scene['scroll_pct']}%)")

    # Step 4: Build final video with ffmpeg
    print("\n[4/4] Assembling final video...")

    # Concatenate audio
    audio_list = ASSETS / "audio_list_v2.txt"
    with open(audio_list, "w") as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")

    concat_audio = ASSETS / "voiceover_v2.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(audio_list), "-c", "copy", str(concat_audio),
    ], capture_output=True, check=True)

    # Build video
    inputs = []
    filter_parts = []
    for i, (img, dur) in enumerate(zip(scene_images, durations)):
        inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", str(img)])
        filter_parts.append(
            f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{i}]"
        )

    concat_inputs = "".join(f"[v{i}]" for i in range(len(SCENES)))
    filter_parts.append(f"{concat_inputs}concat=n={len(SCENES)}:v=1:a=0[vout]")
    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-i", str(concat_audio),
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", f"{len(SCENES)}:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-movflags", "+faststart",
        str(OUTPUT),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [error] ffmpeg failed:\n{result.stderr[-2000:]}")
        return

    final_dur = get_audio_duration(OUTPUT)
    fsize = OUTPUT.stat().st_size / 1024 / 1024
    print(f"\n✅ Video complete: {OUTPUT}")
    print(f"   Duration: {final_dur:.1f}s")
    print(f"   Size: {fsize:.1f} MB")


if __name__ == "__main__":
    main()
