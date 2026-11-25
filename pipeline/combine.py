"""combine.py: join lesson parts into ~10-minute videos with chapters and merged captions."""
import json, os, re, subprocess, sys
V = "/mnt/project-files/cs-channel/videos"; OUT = "/mnt/project-files/cs-channel/final"
I = "/mnt/project-files/cs-channel/intros"
def part(d):
    if d.startswith("intro:"):
        k = d[6:]; return dict(video=f"{I}/{k}/intro.mp4", srt=f"{I}/{k}/captions.srt", timings=f"{I}/{k}/timings.json", extra=0.0, name="Introduction", intro=True)
    if d == "ep01":
        return dict(video=f"{V}/ep01/ep01_counting_in_binary.mp4", srt=f"{V}/ep01/ep01_captions.srt", timings="/tmp/cs_ep01_audio/timings.json", extra=0.5, name="Counting in Binary")
    return dict(video=f"{V}/{d}/video.mp4", srt=f"{V}/{d}/captions.srt", timings=f"/tmp/audio_{d}/timings.json", extra=0.0, name=None)
NAMES = {"csp_b2_l01": "Binary numbers, bits and overflow", "csp_b2_l02": "Lossless vs lossy compression", "csp_b2_l03": "Extracting information from data", "csp_b2_l04": "Using programs with data", "csp_b2_l05": "Metadata",
 "csp_b1_l01": "Collaboration", "csp_b1_l02": "Program function and purpose", "csp_b1_l03": "Program design and development", "csp_b1_l04": "Identifying and correcting errors",
 "icu6_l01": "Passwords and authentication", "icu6_l02": "Encryption, the big idea", "icu6_l03": "Phishing, malware and staying safe", "icu6_l04": "Privacy, AI and bias",
 "icu5_l01": "What is a network?", "icu5_l02": "Packets and routing", "icu5_l03": "IP addresses and DNS", "icu5_l04": "How the web works: HTTP and browsers", "icu5_l05": "The cloud, explained",
 "icu4_l07": "if, elif, else", "icu4_l08": "while loops", "icu4_l09": "for loops and range", "icu4_l10": "Functions: define and call", "icu4_l11": "Parameters and return values", "icu4_l12": "Lists",
 "icu4_l01": "Your first Python program", "icu4_l02": "Variables and assignment", "icu4_l03": "Numbers and arithmetic", "icu4_l04": "Strings", "icu4_l05": "Input from the user", "icu4_l06": "Booleans and comparisons",
 "icu3_l01": "What is an algorithm?", "icu3_l02": "Flowcharts and pseudocode", "icu3_l03": "Linear search", "icu3_l04": "Binary search", "icu3_l05": "Selection sort", "icu3_l06": "Comparing algorithms",
 "csa_u2_l07": "2.7 while loops", "csa_u2_l08": "2.8 for loops", "csa_u2_l09": "2.9 Selection and iteration algorithms", "csa_u2_l10": "2.10 String algorithms", "csa_u2_l11": "2.11 Nested iteration", "csa_u2_l12": "2.12 Informal run-time analysis",
 "csa_u2_l01": "2.1 Algorithms with selection and repetition", "csa_u2_l02": "2.2 Boolean expressions", "csa_u2_l03": "2.3 if statements", "csa_u2_l04": "2.4 Nested if statements", "csa_u2_l05": "2.5 Compound Boolean expressions", "csa_u2_l06": "2.6 Equivalent expressions and De Morgan's laws",
 "icu1_l01": "What a computer does", "icu1_l02": "Inside the box: CPU, memory, storage", "icu1_l03": "How the CPU runs instructions", "icu1_l04": "Memory vs storage", "icu1_l05": "The operating system", "icu1_l06": "Software and how programs get made",
 "ep01": "Counting in binary", "ep02": "Hexadecimal", "ep03": "Text as numbers: ASCII and Unicode", "ep04": "Images as numbers: pixels and RGB",
 "ep05": "Sound as numbers: sampling", "ep06": "Compression: lossless and lossy",
 "csa_u1_l01": "1.1 Algorithms, programs and compilers", "csa_u1_l02": "1.2 Variables and data types", "csa_u1_l03": "1.3 Expressions and output",
 "csa_u1_l04": "1.4 Assignment and input", "csa_u1_l05": "1.5 Casting and ranges", "csa_u1_l06": "1.6 Compound assignment", "csa_u1_l07": "1.7 APIs and libraries",
 "csa_u1_l08": "1.8 Comments and documentation", "csa_u1_l09": "1.9 Method signatures", "csa_u1_l10": "1.10 Calling class methods", "csa_u1_l11": "1.11 The Math class",
 "csa_u1_l12": "1.12 Objects: instances of classes", "csa_u1_l13": "1.13 Creating objects", "csa_u1_l14": "1.14 Calling instance methods", "csa_u1_l15": "1.15 String methods"}
LABELS = json.load(open("/mnt/project-files/cs-channel/pipeline/seg_labels.json"))
def ts2s(h, m, s, ms): return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
def s2ts(v): return f"{int(v//3600):02d}:{int(v%3600//60):02d}:{int(v%60):02d},{int(round((v-int(v))*1000))%1000:03d}"
def build(slug, parts):
    os.makedirs(f"{OUT}/{slug}", exist_ok=True)
    inputs, filt, cues, chapters, full, t0 = [], [], [], [], [], 0.0
    for i, d in enumerate(parts):
        p = part(d); T = json.load(open(p["timings"]))
        last = i == len(parts) - 1
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p["video"]]).decode())
        cut = dur if (last or p.get("intro")) else sum(x["duration"] for x in T[:-1]) + p["extra"]
        inputs += ["-i", p["video"]]
        filt.append(f"[{i}:v]trim=0:{cut:.3f},setpts=PTS-STARTPTS[v{i}];[{i}:a]atrim=0:{cut:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[a{i}]")
        chapters.append((t0, "Introduction" if p.get("intro") else NAMES[d]))
        if not p.get("intro"):
            st, starts = 0.0, []
            for k, x in enumerate(T):
                starts.append(st + (p["extra"] if k >= 4 else 0)); st += x["duration"]
            full.append((t0, NAMES[d]))
            for k, lab in enumerate(LABELS[d][1:], 1):
                if k < len(T) - 1 and starts[k] < cut: full.append((t0 + starts[k], lab))
        else: full.append((t0, "Introduction"))
        for m in re.finditer(r"\d+\n(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)\n(.*?)\n\n", open(p["srt"]).read() + "\n", re.S):
            a, b = ts2s(*m.groups()[0:4]), ts2s(*m.groups()[4:8])
            if a < cut - 0.05: cues.append((t0 + a, t0 + min(b, cut), m.group(9)))
        t0 += cut
    n = len(parts)
    fc = ";".join(filt) + ";" + "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    srt = f"{OUT}/{slug}/captions.srt"
    open(srt, "w").write("".join(f"{k+1}\n{s2ts(a)} --> {s2ts(b)}\n{t}\n\n" for k, (a, b, t) in enumerate(cues)))
    tmp = f"/tmp/{slug}_nosub.mp4"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "60", "-c:a", "aac", "-b:a", "192k", tmp])
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", srt, "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", f"{OUT}/{slug}/video.mp4"])
    os.remove(tmp)
    ch = "\n".join(f"{int(a//60)}:{int(a%60):02d} {nm}" for a, nm in chapters)
    kept = []
    for a, nm in full:
        if kept and a - kept[-1][0] < 10:  # YouTube needs >=10 s per chapter; lesson headings win
            if nm in NAMES.values() and len(kept) > 1: kept[-1] = (a, nm)
            continue
        kept.append((a, nm))
    chf = "\n".join(f"{int(a//60)}:{int(a%60):02d} {nm}" for a, nm in kept)
    json.dump({"chapters": ch, "chapters_full": chf, "duration": t0}, open(f"{OUT}/{slug}/build.json", "w"), indent=1)
    print(slug, round(t0/60, 1), "min\n" + ch)
GROUPS = {
 "apcsp_bi2": ["csp_b2_l01", "csp_b2_l02", "csp_b2_l03", "csp_b2_l04", "csp_b2_l05"],
 "apcsp_bi1": ["csp_b1_l01", "csp_b1_l02", "csp_b1_l03", "csp_b1_l04"],
 "introcs_u6_security": ["icu6_l01", "icu6_l02", "icu6_l03", "icu6_l04"],
 "introcs_u5_networks": ["icu5_l01", "icu5_l02", "icu5_l03", "icu5_l04", "icu5_l05"],
 "introcs_u4_part2": ["icu4_l07", "icu4_l08", "icu4_l09", "icu4_l10", "icu4_l11", "icu4_l12"],
 "introcs_u4_part1": ["icu4_l01", "icu4_l02", "icu4_l03", "icu4_l04", "icu4_l05", "icu4_l06"],
 "introcs_u3_algorithms": ["icu3_l01", "icu3_l02", "icu3_l03", "icu3_l04", "icu3_l05", "icu3_l06"],
 "apcsa_u2_part2": ["csa_u2_l07", "csa_u2_l08", "csa_u2_l09", "csa_u2_l10", "csa_u2_l11", "csa_u2_l12"],
 "apcsa_u2_part1": ["csa_u2_l01", "csa_u2_l02", "csa_u2_l03", "csa_u2_l04", "csa_u2_l05", "csa_u2_l06"],
 "introcs_u1_what_is_a_computer": ["icu1_l01", "icu1_l02", "icu1_l03", "icu1_l04", "icu1_l05", "icu1_l06"],
 "introcs_u2_data_and_binary": ["ep01", "ep02", "ep03", "ep04", "ep05", "ep06"],
 "apcsa_u1_part1": ["csa_u1_l01", "csa_u1_l02", "csa_u1_l03", "csa_u1_l04", "csa_u1_l05"],
 "apcsa_u1_part2": ["csa_u1_l06", "csa_u1_l07", "csa_u1_l08", "csa_u1_l09", "csa_u1_l10"],
 "apcsa_u1_part3": ["csa_u1_l11", "csa_u1_l12", "csa_u1_l13", "csa_u1_l14", "csa_u1_l15"]}
if __name__ == "__main__":
    for s in (sys.argv[1:] or GROUPS): build(s, ["intro:" + s] + GROUPS[s])
