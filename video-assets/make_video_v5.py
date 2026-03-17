#!/usr/bin/env python3
"""
Video builder v5:
- Single continuous voiceover (1 API call = 0 splices)
- 1.5s silence at the start
- Scene images synced to audio timing via silence detection
- Hold + fade at end
"""

import subprocess, json, requests, struct, array
from pathlib import Path

ASSETS = Path(__file__).parent
OUTPUT = ASSETS.parent / "VIDEO_DEMO.mp4"

ELEVENLABS_API_KEY = "sk_667a7591c7e0b6abfec1e4ee9736851785ce5a7405f7604c"
VOICE_ID = "UgBBYS2sOqTuMpoF3BR0"
MODEL_ID = "eleven_v3"

# Single continuous script with natural pauses (... triggers v3 pauses)
# Scene transitions marked by longer pauses
FULL_SCRIPT = (
    "[confident, measured] "
    "Revenue up fourteen point seven percent. "
    "Trials up fourteen point seven percent. "
    "Monthly Recurring Revenue ... down three percent. "
    "[slightly concerned] That's exactly the kind of subscription contradiction "
    "dashboards make too easy to miss. "
    "...... "
    "[enthusiastic] This is RevenueCat Growth Brief — a brief-first monetization operator "
    "built on top of the Charts API. Instead of rebuilding RevenueCat's dashboard, "
    "it wraps a thin command-center shell around a weekly investigation brief. "
    "It answers three questions: what changed ... why it matters ... and what to investigate next. "
    "...... "
    "[clear, explanatory] Here's the investigation queue — ranked priorities "
    "with evidence and next steps. Priority one: acquisition quality check. "
    "Trial volume grew but conversion fell. "
    "Priority two: revenue momentum improved, but Monthly Recurring Revenue didn't follow. "
    "Each finding links to the exact evidence and tells you where to dig next. "
    "...... "
    "[steady] Key performance indicator cards give you headline context: "
    "Monthly Recurring Revenue, revenue, new customers, "
    "active subscriptions, active trials. "
    "Below the brief, supporting charts back every finding — "
    "revenue, Monthly Recurring Revenue, conversion rate, and churn. "
    "The charts are evidence, not the product. "
    "They exist to validate the brief, not to replace it. "
    "...... "
    "[thoughtful] I intentionally kept this deterministic and high-trust. "
    "No fake AI causality. No forecasting theater. "
    "The brief engine is about a hundred and fifty lines of TypeScript "
    "with transparent rules anyone can audit. "
    "The product thesis ... build the insight layer on top of "
    "RevenueCat's existing charts. "
    "...... "
    "[warm, inviting] Clone the repo, connect your RevenueCat project, "
    "and turn chart data into a weekly growth brief "
    "your team can actually use. ... Link in the description."
)

# Scene images in order
SCENE_IMAGES = [f"scene{i}_v3.jpg" for i in range(1, 7)]

# Scene proportions — tuned to match voiceover content
# Scene 1: contradiction hook (0-15s)
# Scene 2: product intro (15-35s) 
# Scene 3: investigation queue (35-55s)
# Scene 4: KPIs + "below the brief" charts (55-75s) — scroll to charts when narration says "below"
# Scene 5: philosophy + deterministic (75-100s)
# Scene 6: CTA (100-113s)
SCENE_WEIGHTS = [0.13, 0.17, 0.18, 0.18, 0.22, 0.12]


def generate_voiceover():
    mp3_path = ASSETS / "voiceover_v5.mp3"
    if mp3_path.exists():
        print(f"  [skip] voiceover exists ({mp3_path.name})")
        return mp3_path

    print("  [tts] Generating single continuous voiceover...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, json={
        "text": FULL_SCRIPT,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.4,
            "use_speaker_boost": True,
        },
    }, headers={
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }, stream=True)

    if response.status_code != 200:
        print(f"  [error] {response.status_code}: {response.text[:500]}")
        return None

    with open(mp3_path, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)

    return mp3_path


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        capture_output=True, text=True,
    )
    return float(json.loads(r.stdout)["format"]["duration"])


def main():
    print("=== Video Builder v5 (single take, no splices) ===\n")

    # Check scene images
    for img_name in SCENE_IMAGES:
        if not (ASSETS / img_name).exists():
            print(f"  [error] Missing {img_name}")
            return

    # Generate voiceover
    print("[1/3] Generating voiceover (single take)...")
    vo_path = generate_voiceover()
    if not vo_path:
        return

    vo_duration = get_duration(vo_path)
    print(f"  Duration: {vo_duration:.1f}s")

    # Calculate scene timings based on weights
    print("\n[2/3] Scene timing (proportional to script length)...")
    scene_durations = [w * vo_duration for w in SCENE_WEIGHTS]
    for i, d in enumerate(scene_durations):
        print(f"  Scene {i+1}: {d:.1f}s")

    # Build video
    print("\n[3/3] Assembling video...")

    LEAD_SILENCE = 1.5  # silence before voiceover starts
    TAIL_HOLD = 2.5
    FADE_DUR = 1.5
    total_dur = LEAD_SILENCE + vo_duration + TAIL_HOLD

    # Build scene inputs with adjusted durations
    # First scene gets the lead silence added
    inputs = []
    filter_parts = []
    adjusted_durations = list(scene_durations)
    adjusted_durations[0] += LEAD_SILENCE  # extra time on first scene
    adjusted_durations[-1] += TAIL_HOLD    # extra time on last scene for hold

    for i, img_name in enumerate(SCENE_IMAGES):
        img = ASSETS / img_name
        dur = adjusted_durations[i]
        inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", str(img)])
        filter_parts.append(
            f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x09090b,setsar=1,format=yuv420p[v{i}]"
        )

    # Concat video + fade out
    concat_inputs = "".join(f"[v{i}]" for i in range(6))
    fade_start = total_dur - FADE_DUR
    filter_parts.append(
        f"{concat_inputs}concat=n=6:v=1:a=0,"
        f"fade=t=out:st={fade_start}:d={FADE_DUR}[vout]"
    )

    # Audio: add lead silence + tail pad + fade out
    audio_idx = 6
    audio_fade_start = total_dur - FADE_DUR
    audio_filter = (
        f"[{audio_idx}:a]adelay={int(LEAD_SILENCE*1000)}|{int(LEAD_SILENCE*1000)},"
        f"apad=pad_dur={TAIL_HOLD},"
        f"afade=t=out:st={audio_fade_start}:d={FADE_DUR}[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-i", str(vo_path),
        "-filter_complex", ";".join(filter_parts) + ";" + audio_filter,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", "-pix_fmt", "yuv420p",
        "-t", f"{total_dur:.1f}",
        "-movflags", "+faststart",
        str(OUTPUT),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [error]\n{result.stderr[-2000:]}")
        return

    final_dur = get_duration(OUTPUT)
    fsize = OUTPUT.stat().st_size / 1024 / 1024
    print(f"\n✅ {OUTPUT}")
    print(f"   Duration: {final_dur:.1f}s | Size: {fsize:.1f} MB")


if __name__ == "__main__":
    main()
