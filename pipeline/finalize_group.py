"""finalize_group.py <group> : after gen_examples, update the intro topics/narration and the description intro
to mention the worked examples and the 'putting it together' example (idempotent)."""
import json, re, sys, ast
P = "/mnt/project-files/cs-channel"; g = sys.argv[1]
s = open(f"{P}/pipeline/combine.py").read()
a = s.index("GROUPS = {") + 9; d = 0
for j in range(a, len(s)):
    if s[j] == "{": d += 1
    elif s[j] == "}":
        d -= 1
        if d == 0: break
G = ast.literal_eval(s[a:j + 1])
lessons = G[g]
cap = [x for x in lessons if x.endswith("_cap") or x.endswith("_prog")]
ij = f"{P}/intros/{g}/intro.json"; it = json.load(open(ij))
if cap and not any("together" in t.lower() or "program" in t.lower() for t in it["topics"]):
    it["topics"].append("Putting it together")
json.dump(it, open(ij, "w"), indent=1, ensure_ascii=False)
sj = f"{P}/intros/{g}/script.json"; sc = json.load(open(sj))
add = " After every lesson, we'll work through a full example step by step" + (", and we'll finish by putting the whole unit together." if cap else ".")
if "work through a full example" not in sc["segments"][0][-1] and "worked example" not in sc["segments"][0][-1]:
    sc["segments"][0][-1] = sc["segments"][0][-1].rstrip() + add
sc["speed"] = 1.0
json.dump(sc, open(sj, "w"), indent=1)
fm = f"{P}/pipeline/final_meta.py"; m = open(fm).read()
k = m.index(f'"{g}": dict(')
e = m.index('intro="', k) + 7; f = m.index('",', e)
intro = m[e:f]
extra = " Every lesson is followed by a step-by-step worked example" + (", and the unit ends with a 'putting it together' example that uses everything at once." if cap else ".")
if "step-by-step worked example" not in intro:
    intro = intro.replace(" Each lesson ends with a practice problem.", "").replace(" Each topic ends with an AP-style practice problem.", "") + extra + ("" if re.search(r"ends with (a|an) [^.]*practice", intro) else " Each part ends with a practice problem.")
    m = m[:e] + intro + m[f:]
    open(fm, "w").write(m)
print(g, len(lessons), "lessons; cap:", cap)
