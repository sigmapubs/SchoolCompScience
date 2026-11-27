"""Script JSON -> per-segment WAV narration, timings JSON and SRT captions (Kokoro TTS)."""
import json, sys, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
MODEL = os.environ.get("KOKORO_DIR", "/tmp/kokoro")
script_path, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
S = json.load(open(script_path))
k = Kokoro(f"{MODEL}/kokoro-v1.0.onnx", f"{MODEL}/voices-v1.0.bin")
GAP, TAIL = 0.45, 0.7   # pause between sentences, pause after a segment
timings, cues, rel, t0 = [], [], [], 0.0
for i, seg in enumerate(S["segments"]):
    parts, t = [], 0.0
    for sent in seg:
        a, sr = k.create(sent, voice=S.get("voice", "am_puck"), speed=S.get("speed", 1.0), lang="en-us")
        cues.append((t0 + t, t0 + t + len(a) / sr, sent)); rel.append([i, t, t + len(a) / sr, sent])
        parts += [a, np.zeros(int(GAP * sr), dtype=a.dtype)]
        t += len(a) / sr + GAP
    parts.append(np.zeros(int(TAIL * sr), dtype=a.dtype))
    audio = np.concatenate(parts)
    path = os.path.join(out_dir, f"seg{i:02d}.wav")
    sf.write(path, audio, sr)
    d = len(audio) / sr
    timings.append({"file": os.path.abspath(path), "duration": d})
    t0 += d
json.dump(timings, open(os.path.join(out_dir, "timings.json"), "w"), indent=1)
json.dump(rel, open(os.path.join(out_dir, "cues.json"), "w"), indent=1)
def ts(x):
    h, m = divmod(int(x), 3600); m, s = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{int(round((x - int(x)) * 1000)):03d}"
def chunks(text, n=42):  # wrap to two short lines
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur); return lines
with open(os.path.join(out_dir, "captions.srt"), "w") as f:
    n = 1
    for a, b, text in cues:
        lines = chunks(text)
        groups = [lines[j:j+2] for j in range(0, len(lines), 2)]
        total = sum(len(" ".join(g)) for g in groups)
        s = a
        for g in groups:
            e = s + (b - a) * len(" ".join(g)) / total
            f.write(f"{n}\n{ts(s)} --> {ts(e)}\n" + "\n".join(g) + "\n\n"); n += 1; s = e
print("total", round(t0, 1), "s")
