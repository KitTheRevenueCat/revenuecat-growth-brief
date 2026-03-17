#!/usr/bin/env python3
"""
Produce a ~90-second demo video for RevenueCat Growth Brief.
Uses ElevenLabs v3 for voiceover + pre-captured viewport screenshots + ffmpeg.
Expects scene screenshots to already exist as scene1_v3.jpg .. scene6_v3.jpg (1280x720).
"""

import subprocess, json, requests
from pathlib import Path

ASSETS = Path(__file__).parent
OUTPUT = ASSETS.parent / "VIDEO_DEMO.mp4"

ELEVENLABS_API_KEY = "sk_667a7591c7e0b6abfec1e4ee9736851785ce5a7405f7604c"
VOICE_ID = "UgBBYS2sOqTuMpoF3BR0"
MODEL_ID = "eleven_v3"

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
    },
    {
        "id": "scene2",
        "text": (
            "[enthusiastic] This is RevenueCat Growth Brief — a brief-first monetization operator "
            "built on top of the Charts API. Instead of rebuilding RevenueCat's dashboard, "
            "it wraps a thin command-center shell around a weekly investigation brief. "
            "It answers three questions: what changed, why it matters, and what to investigate next."
        ),
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
    },
    {
        "id": "scene6",
        "text": (
            "[warm, inviting] Clone the repo, connect your RevenueCat project, "
            "and turn chart data into a weekly growth brief "
            "your team can actually use. Link in the description."
        ),
    },
]


def generate_voiceover(scene):
    mp3_path = ASSETS / f"{scene['id']}_v3.mp3"
    if mp3_path.exists():
        print(f"  [skip] {mp3_path.name} exists")
        return mp3_path

    print(f"  [tts] {scene['id']}...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, json={
        "text": scene["text"],
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
    print("=== Video Builder v3 (proper 16:9) ===\n")

    # Check screenshots exist
    for s in SCENES:
        img = ASSETS / f"{s['id']}_v3.jpg"
        if not img.exists():
            print(f"  [error] Missing {img}. Capture screenshots first.")
            return

    # Generate voiceover
    print("[1/3] Generating voiceover...")
    audio_files = []
    for scene in SCENES:
        af = generate_voiceover(scene)
        if not af:
            return
        audio_files.append(af)

    # Durations
    print("\n[2/3] Durations...")
    durations = []
    for af in audio_files:
        d = get_duration(af)
        durations.append(d)
        print(f"  {af.name}: {d:.1f}s")
    print(f"  Total: {sum(durations):.1f}s")

    # Concat audio
    audio_list = ASSETS / "audio_list_v3.txt"
    with open(audio_list, "w") as f:
        for af in audio_files:
            f.write(f"file '{af}'\n")
    concat_audio = ASSETS / "voiceover_v3.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(audio_list), "-c", "copy", str(concat_audio)], capture_output=True, check=True)

    # Build video
    print("\n[3/3] Assembling video...")
    inputs = []
    filter_parts = []
    for i, scene in enumerate(SCENES):
        img = ASSETS / f"{scene['id']}_v3.jpg"
        dur = durations[i]
        inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", str(img)])
        # Scale to exactly 1280x720, padding if needed
        filter_parts.append(
            f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x09090b,setsar=1,format=yuv420p[v{i}]"
        )

    # Add 2.5s hold on the last frame for breathing room + fade out
    TAIL_HOLD = 2.5
    FADE_DUR = 1.5

    concat_inputs = "".join(f"[v{i}]" for i in range(len(SCENES)))
    total_video_dur = sum(durations) + TAIL_HOLD
    fade_start = total_video_dur - FADE_DUR
    filter_parts.append(
        f"{concat_inputs}concat=n={len(SCENES)}:v=1:a=0,"
        f"tpad=stop_mode=clone:stop_duration={TAIL_HOLD},"
        f"fade=t=out:st={fade_start}:d={FADE_DUR}[vout]"
    )

    # Also fade the audio out at the end
    audio_fade_start = sum(durations) + TAIL_HOLD - FADE_DUR
    audio_idx = len(SCENES)

    cmd = [
        "ffmpeg", "-y", *inputs, "-i", str(concat_audio),
        "-filter_complex", ";".join(filter_parts) + f";[{audio_idx}:a]apad=pad_dur={TAIL_HOLD},afade=t=out:st={audio_fade_start}:d={FADE_DUR}[aout]",
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
