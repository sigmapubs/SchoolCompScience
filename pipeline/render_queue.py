"""render_queue.py : render+push every group listed in pipeline/queue.txt ("<group> <repo_path>") that is not yet in
pipeline/queue_done.txt. Safe to re-run after a container restart (resumes)."""
import subprocess, re, ast, os, time, sys
MAXG = int(sys.argv[1]) if len(sys.argv) > 1 else 10**9   # stop after this many groups (keeps a run under the 2 h task limit)
N = 0
P = "/mnt/project-files/cs-channel"
def groups():
    s = open(f"{P}/pipeline/combine.py").read(); a = s.index("GROUPS = {") + 9; d = 0
    for j in range(a, len(s)):
        if s[j] == "{": d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0: break
    return ast.literal_eval(s[a:j + 1])
while True:
    q = [l.split() for l in open(f"{P}/pipeline/queue.txt") if l.strip() and not l.startswith("#")]
    done = set(x.replace("_FAILED", "") for x in open(f"{P}/pipeline/queue_done.txt").read().split()) if os.path.exists(f"{P}/pipeline/queue_done.txt") else set()
    todo = [x for x in q if x[0] not in done]
    if not todo: print("queue empty", flush=True); break
    if N >= MAXG: print(f"stopping after {N} groups; {len(todo)} left", flush=True); break
    N += 1
    g, repo = todo[0]; G = groups()
    args = [f"{l}:" + re.search(r"^class (\w+)\(", open(f"{P}/videos/{l}/scene.py").read(), re.M).group(1) for l in G[g]]
    t0 = time.time()
    subprocess.run(["bash", f"{P}/pipeline/do_group.sh", g, repo] + args, cwd=P, stdout=open(f"/tmp/g_{g}.log", "w"), stderr=subprocess.STDOUT)
    st = open(f"/tmp/status_{g}.txt").read()
    warn = sum(int(m) for m in re.findall(r"(\d+) warn", st))
    ok = "ALLDONE" in st
    if ok:
        r = subprocess.run(["flock", "/tmp/push.lock", "bash", f"{P}/pipeline/push_repo.sh", f"Regenerate {g} with worked examples"], cwd=P, capture_output=True, text=True)
        ok = r.returncode == 0
    print(f"{g}: {'pushed' if ok else 'FAILED'} warn={warn} {int(time.time()-t0)}s", flush=True)
    with open(f"{P}/pipeline/queue_done.txt", "a") as f: f.write(g + ("\n" if ok else "_FAILED\n"))
