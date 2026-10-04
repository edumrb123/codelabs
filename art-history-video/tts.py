"""Generate narration audio with Kokoro (free, local, Apache-2.0).

Writes build/audio/<chapter>/<beat>.wav and build/audio/durations.json.
Only beats whose text changed are regenerated.

Usage: python tts.py [--voice am_michael] [--speed 1.0] [chapter ...]
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

from narration import CHAPTERS

HERE = Path(__file__).parent
OUT = HERE / "build" / "audio"
MODEL_DIR = Path(os.environ.get("KOKORO_DIR", HERE / "models"))
TAIL_SILENCE = 0.35  # seconds of breathing room after each beat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapters", nargs="*")
    ap.add_argument("--voice", default="am_michael")
    ap.add_argument("--speed", type=float, default=1.0)
    args = ap.parse_args()

    kokoro = Kokoro(str(MODEL_DIR / "kokoro-v1.0.onnx"), str(MODEL_DIR / "voices-v1.0.bin"))
    OUT.mkdir(parents=True, exist_ok=True)
    dur_path = OUT / "durations.json"
    meta = json.loads(dur_path.read_text()) if dur_path.exists() else {}

    for ch_id, title, beats in CHAPTERS:
        if args.chapters and ch_id not in args.chapters:
            continue
        (OUT / ch_id).mkdir(exist_ok=True)
        for beat_id, text in beats:
            key = f"{ch_id}/{beat_id}"
            digest = hashlib.sha1(f"{text}|{args.voice}|{args.speed}".encode()).hexdigest()
            wav = OUT / ch_id / f"{beat_id}.wav"
            if wav.exists() and meta.get(key, {}).get("hash") == digest:
                continue
            samples, sr = kokoro.create(text, voice=args.voice, speed=args.speed, lang="en-us")
            samples = np.concatenate([samples, np.zeros(int(sr * TAIL_SILENCE), dtype=samples.dtype)])
            sf.write(wav, samples, sr)
            meta[key] = {"hash": digest, "duration": round(len(samples) / sr, 3)}
            print(f"{key}: {meta[key]['duration']:.1f}s")
            dur_path.write_text(json.dumps(meta, indent=1))

    total = sum(v["duration"] for v in meta.values())
    print(f"Total narration: {total / 60:.1f} min")


if __name__ == "__main__":
    main()
