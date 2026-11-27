"""gen_examples.py <data_module>  (module in pipeline/examples_data/, defines GROUP, EX list, optional CAP dict)
Writes videos/<id>/{script.json,scene.py} for each worked example and the capstone, registers them in
combine.py (NAMES + GROUPS order), seg_labels.json, and points each base lesson's last practice line at its example."""
import json, os, re, sys, importlib, ast
P = "/mnt/project-files/cs-channel"
sys.path.insert(0, P + "/pipeline/examples_data")
D = importlib.import_module(sys.argv[1])
SUB = ["If this helped, subscribe to School Computer Science, Explained, so you don't miss the next lesson.", "See you there."]
def cls(i): return "".join(w.capitalize() for w in i.split("_"))
def write(i, script, scene):
    d = f"{P}/videos/{i}"; os.makedirs(d, exist_ok=True)
    json.dump(script, open(f"{d}/script.json", "w"), indent=1)
    open(f"{d}/scene.py", "w").write(scene)

names, labels, order = {}, {}, {}
for e in D.EX:
    i = e["id"]
    segs = [e["hook"], e["problem"][0], e["work"][0], e["trace"][0], e["result"][0],
            [e["practice"]["q_say"], "Pause the video now.", e["practice"]["a_say"], e["practice"]["next_say"]], SUB]
    pr = e["practice"]
    sc = f'''from worked import *
class {cls(i)}(Worked):
    TITLE = {e["title"]!r}; SUB = {e["sub"]!r}; LANG = {e.get("lang","python")!r}
    PROBLEM = {e["problem"][1]!r}
    CODE = {e["work"][1]!r}
    HL_LINES = {e["work"][2]!r}
    HEAD = {e["trace"][1]!r}
    ROWS = {e["trace"][2]!r}
    RESULT = {e["result"][1]!r}
    TIP = {e["result"][2]!r}
    Q = {pr["q"]!r}; Q_IS_CODE = {pr.get("q_is_code", False)!r}
    A = {pr["a"]!r}; NEXT = {pr["next"]!r}; OUTRO = {e["outro"]!r}
'''
    write(i, {"title": e["title"], "voice": "am_puck", "speed": 1.0, "segments": segs}, sc)
    names[i] = "Worked example: " + e["chapter"]
    labels[i] = ["", "The problem", "The work", e.get("trace_label", "Step by step"), "Result and tips", "Your turn"]
    order[e["after"]] = i
    # base lesson: point its last practice line at the example
    bp = f"{P}/videos/{e['after']}/script.json"; b = json.load(open(bp))
    b["segments"][-2][-1] = "Next, let's work through a full example, step by step."
    json.dump(b, open(bp, "w"), indent=1)
    sp = f"{P}/videos/{e['after']}/scene.py"; s = open(sp).read()
    s = re.sub(r'(practice\(self, [^\n]*?)"((?:Next|End|That|The end)[^"]*)"', r'\1"Next: worked example"', s, count=1)
    open(sp, "w").write(s)

cap = getattr(D, "CAP", None)
if cap:
    i = cap["id"]
    segs = [cap["hook_say"], cap["plan_say"]] + [p["say"] for p in cap["parts"]]
    if cap.get("run"): segs.append(cap["run_say"])
    segs += [[cap["q_say"], "Pause the video now.", cap["a_say"], cap["next_say"]], SUB]
    parts = [{k: v for k, v in p.items() if k != "say"} for p in cap["parts"]]
    sc = f'''from capstone import *
class {cls(i)}(Capstone):
    TITLE = {cap["title"]!r}; SUB = {cap["sub"]!r}; FILE = {cap["file"]!r}; LANG = {cap.get("lang","python")!r}
    HOOK = {cap["hook"]!r}
    PLAN = {cap["plan"]!r}
    PARTS = {parts!r}
    RUN_LINES = {cap.get("run", [])!r}
    Q = {cap["q"]!r}; A = {cap["a"]!r}; NEXT = {cap["next"]!r}; OUTRO = {cap["outro"]!r}
'''
    write(i, {"title": cap["title"], "voice": "am_puck", "speed": 1.0, "segments": segs}, sc)
    names[i] = cap["chapter"]
    labels[i] = ["", "The plan"] + [p["tag"] for p in cap["parts"]] + (["Run it"] if cap.get("run") else []) + ["Your turn"]
    # the old last lesson's ending now leads into the capstone
    last = cap["after"]; key = order.get(last, last)
    bp = f"{P}/videos/{key}/script.json"; b = json.load(open(bp))
    b["segments"][-2][-1] = cap.get("lead_in", "Next, let's put the whole unit together.")
    json.dump(b, open(bp, "w"), indent=1)
    sp = f"{P}/videos/{key}/scene.py"; s = open(sp).read()
    s = re.sub(r'(NEXT = )"[^"]*"', r'\1"Next: putting it together"', s, count=1)
    s = re.sub(r'(practice\(self, [^\n]*?)"((?:Next|End|That|The end)[^"]*)"', r'\1"Next: putting it together"', s, count=1)
    open(sp, "w").write(s)
    order[key + "__cap"] = i

# combine.py
p = f"{P}/pipeline/combine.py"; s = open(p).read()
s = s.replace("NAMES = {", "NAMES = {" + "".join(f"{json.dumps(k)}: {json.dumps(v)}, " for k, v in names.items() if f'"{k}"' not in s) + "\n ", 1)
a = s.index("GROUPS = {") + 9; d = 0
for j in range(a, len(s)):
    if s[j] == "{": d += 1
    elif s[j] == "}":
        d -= 1
        if d == 0: break
G = ast.literal_eval(s[a:j + 1])
for grp in D.GROUPS:
    old = [x for x in G[grp] if not x.endswith(tuple(["b"])) or x not in order.values()]
    new = []
    for x in G[grp]:
        if x in order.values() or x == (cap or {}).get("id"): continue
        new.append(x)
        if x in order: new.append(order[x])
        if cap and x == cap["after"]:
            if x in order: pass
    if cap and cap.get("group") == grp:
        new.append(cap["id"])
    G[grp] = new
body = "{\n" + "".join(f" {json.dumps(k)}: {json.dumps(v)},\n" for k, v in G.items()) + "}"
s = s[:a] + body + s[j + 1:]
open(p, "w").write(s)
L = json.load(open(f"{P}/pipeline/seg_labels.json")); L.update(labels)
json.dump(L, open(f"{P}/pipeline/seg_labels.json", "w"), indent=0, ensure_ascii=False)
print("ok", list(names))
