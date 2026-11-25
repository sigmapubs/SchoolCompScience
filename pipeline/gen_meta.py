"""gen_meta.py <lesson_dir>: reads <lesson_dir>/meta_in.json + /tmp/audio_<name>/timings.json -> metadata.md"""
import json, sys, os
L = sys.argv[1].rstrip("/"); M = json.load(open(f"{L}/meta_in.json"))
t = json.load(open(f"/tmp/audio_{os.path.basename(L)}/timings.json")); s, st = 0, []
for x in t: st.append(s); s += x["duration"]
chap = "\n".join(f"{int(v//60)}:{int(v%60):02d} {n}" for v, n in zip(st, M["chapters"]))
open(f"{L}/metadata.md", "w").write(f"""Title: {M['title']}

Description:
{M['description']}

Course: {M['course']}

{chap}

{M['nav']}

{M['hashtags']}

Playlists: {'; '.join(M['playlists'])}
Audience: Not made for kids
Tags: {M['tags']}
Captions: captions.srt (English)
""")
print(chap)
