#!/usr/bin/env python3
"""
Produce a ~90-second demo video for RevenueCat Growth Brief.
Uses macOS `say` for voiceover, static screenshots for visuals, ffmpeg for assembly.
"""

import os, subprocess, json
from pathlib import Path

ASSETS = Path(__file__).parent
FULL_IMG = ASSETS / "full-page.jpg"
OUTPUT = ASSETS.parent / "VIDEO_DEMO.mp4"

# macOS voice — Samantha is clear and professional
VOICE = "Samantha"
RATE = 175  # words per minute

SCENES = [
    {
        "id": "scene1",
        "text": (
            "RevenueCat's Charts API gives developers direct access to subscription metrics "
            "like revenue, MRR, churn, trial conversion, and customer growth. "
            "But most teams don't struggle because they can't see charts. "
            "They struggle because charts don't automatically turn into operating decisions."
        ),
        "scroll_pct": 0,
    },
    {
        "id": "scene2",
        "text": (
            "This is RevenueCat Growth Brief. A brief-first monetization operator "
            "built on top of the Charts API. Instead of rebuilding RevenueCat's dashboard, "
            "it wraps a thin command-center shell around a weekly investigation brief."
        ),
        "scroll_pct": 5,
    },
    {
        "id": "scene3",
        "text": (
            "The core idea: compare recent performance against the previous window, "
            "detect meaningful changes, and produce a ranked operator brief. "
            "Here you can see the investigation queue. Ranked priorities "
            "with evidence and next steps. Acquisition quality check, "
            "trial conversion weakening, churn pressure, "
            "and top of funnel outpacing conversion."
        ),
        "scroll_pct": 20,
    },
    {
        "id": "scene4",
        "text": (
            "On the right, KPI cards show MRR, revenue, new customers, "
            "active subscriptions, and active trials at a glance. "
            "These provide the headline context. "
            "The brief is the primary object. The KPIs support it."
        ),
        "scroll_pct": 30,
    },
    {
        "id": "scene5",
        "text": (
            "Below the brief, supporting charts back every finding. "
            "Revenue, MRR, conversion rate, and churn. "
            "Each with sparklines and summary totals. "
            "The charts are evidence, not the product."
        ),
        "scroll_pct": 75,
    },
    {
        "id": "scene6",
        "text": (
            "I intentionally kept this deterministic and high-trust. "
            "No fake AI causality, no forecasting theater. "
            "The product thesis: build the insight layer on top of "
            "RevenueCat's existing charts. "
            "Clone the repo, connect your RevenueCat project, "
            "and turn chart data into a weekly growth brief "
            "your team can actually use."
        ),
        "scroll_pct": 0,
    },
]


def generate_voiceover(scene):
    """Generate TTS audio for a scene using macOS say."""
    aiff_path = ASSETS / f"{scene['id']}.aiff"
    mp3_path = ASSETS / f"{scene['id']}.mp3"
    if mp3_path.exists():
        print(f"  [skip] {mp3_path.name} already exists")
        return mp3_path
    print(f"  [tts] Generating {scene['id']}...")
    subprocess.run([
        "say", "-v", VOICE, "-r", str(RATE),
        "-o", str(aiff_path), scene["text"],
    ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(aiff_path),
        "-ar", "44100", "-ab", "128k",
        str(mp3_path),
    ], capture_output=True, check=True)
    aiff_path.unlink()
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

    # Crop and scale to 1280x720
    subprocess.run([
        "ffmpeg", "-y", "-i", str(full_img),
        "-vf", f"crop={total_w}:{viewport_h}:0:{y},scale=1280:720",
        str(out_path),
    ], capture_output=True, check=True)
    return out_path


def main():
    print("=== RevenueCat Growth Brief Video Builder ===\n")

    # Step 1: Generate all voiceover segments
    print("[1/4] Generating voiceover audio...")
    audio_files = []
    for scene in SCENES:
        audio_path = generate_voiceover(scene)
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
        img_out = ASSETS / f"{scene['id']}.jpg"
        crop_scene_image(FULL_IMG, scene["scroll_pct"], img_out)
        scene_images.append(img_out)
        print(f"  {img_out.name} (scroll {scene['scroll_pct']}%)")

    # Step 4: Build final video with ffmpeg
    print("\n[4/4] Assembling final video...")

    # Concatenate audio
    audio_list = ASSETS / "audio_list.txt"
    with open(audio_list, "w") as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")

    concat_audio = ASSETS / "voiceover.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(audio_list), "-c", "copy", str(concat_audio),
    ], capture_output=True, check=True)

    # Build video: each image shown for the duration of its audio
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
