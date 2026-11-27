"""split_group.py OLD NEW1=l1,l2,.. NEW2=l3,..  -- split a video group into parts.
Updates combine.py GROUPS, thumbs.py, final_meta.py V (title/part/also/prev/next), intros/<slug>/."""
import sys, re, json, os, shutil
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(P)
old = sys.argv[1]; parts = [a.split("=") for a in sys.argv[2:]]; n = len(parts)
# combine.py
s = open(f"{P}/combine.py").read()
m = re.search(r'^ "%s": \[[^\]]*\],\n' % re.escape(old), s, re.M)
assert m, "group not found"
new = "".join(' "%s": [%s],\n' % (k, ", ".join('"%s"' % x for x in v.split(","))) for k, v in parts)
s = s[:m.start()] + new + s[m.end():]; open(f"{P}/combine.py", "w").write(s)
# thumbs.py
t = open(f"{P}/thumbs.py").read()
m = re.search(r'^ \("\.\./final/%s", "([^"]*)",(.*)\),\n' % re.escape(old), t, re.M)
if m:
    rows = "".join(' ("../final/%s", "%s  ·  PART %d",%s),\n' % (k, m.group(1), i + 1, m.group(2)) for i, (k, v) in enumerate(parts))
    t = t[:m.start()] + rows + t[m.end():]; open(f"{P}/thumbs.py", "w").write(t)
# final_meta.py: duplicate the dict entry per part
f = open(f"{P}/final_meta.py").read()
m = re.search(r'^ "%s": dict\(\n(.*?)\n   tagsh=[^\n]*\),\n' % re.escape(old), f, re.M | re.S)
assert m, "meta not found"
body = m.group(0)
out = ""
for i, (k, v) in enumerate(parts):
    b = body.replace('"%s": dict(' % old, '"%s": dict(' % k, 1)
    b = re.sub(r'(title="[^"|]*)', lambda mm: mm.group(1).rstrip() + " (Part %d of %d) " % (i + 1, n), b, 1)
    b = re.sub(r'part="([^"·]*)·[^"]*"', lambda mm: 'part="%s· Part %d of %d"' % (mm.group(1), i + 1, n), b, 1)
    b = re.sub(r'also="[^"]*"', 'also="This unit is split into %d videos."' % n, b, 1)
    if i > 0: b = re.sub(r'prev="[^"]*"', 'prev="Part %d of this unit"' % i, b, 1)
    if i < n - 1: b = re.sub(r'next="[^"]*"', 'next="Part %d of this unit"' % (i + 2), b, 1)
    out += b
f = f[:m.start()] + out + f[m.end():]; open(f"{P}/final_meta.py", "w").write(f)
# intros
oi = json.load(open(f"{R}/intros/{old}/intro.json")); osc = json.load(open(f"{R}/intros/{old}/script.json"))
names = json.load(open(f"{P}/seg_labels.json")) if False else None
start = 0
for i, (k, v) in enumerate(parts):
    ls = v.split(","); d = f"{R}/intros/{k}"; os.makedirs(d, exist_ok=True)
    ii = dict(oi); ii["part"] = "Part %d of %d" % (i + 1, n); ii["topics"] = oi["topics"][start:start + len(ls)]; start += len(ls)
    json.dump(ii, open(f"{d}/intro.json", "w"), indent=1)
    sc = json.loads(json.dumps(osc)); sc["title"] = osc["title"] + " Part %d" % (i + 1)
    sc["segments"][0][0] = sc["segments"][0][0].replace("Unit 3:", "Unit 3, part %d:" % (i + 1)) if "Unit 3:" in sc["segments"][0][0] else sc["segments"][0][0] + " This is part %d of %d." % (i + 1, n)
    json.dump(sc, open(f"{d}/script.json", "w"), indent=1)
print("split", old, "->", [k for k, _ in parts])
