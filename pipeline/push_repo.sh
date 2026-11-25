#!/bin/bash
# push_repo.sh "<message>": refresh metadata of every video already in the repo, copy pipeline, commit, push
G=/home/user/schoolcompscience; F=/mnt/project-files/cs-channel/final; cd $G
declare -A M=([introcs_u1_what_is_a_computer]=intro-cs/unit-1/full [introcs_u2_data_and_binary]=intro-cs/unit-2/full [introcs_u3_algorithms]=intro-cs/unit-3/full
 [apcsa_u1_part1]=ap-csa/unit-1/part-1 [apcsa_u1_part2]=ap-csa/unit-1/part-2 [apcsa_u1_part3]=ap-csa/unit-1/part-3 [apcsa_u2_part1]=ap-csa/unit-2/part-1 [apcsa_u2_part2]=ap-csa/unit-2/part-2
 [introcs_u4_part1]=intro-cs/unit-4/part-1 [introcs_u4_part2]=intro-cs/unit-4/part-2 [introcs_u5_networks]=intro-cs/unit-5/full [introcs_u6_security]=intro-cs/unit-6/full)
for s in "${!M[@]}"; do r=${M[$s]}; [ -f $G/$r/video.mp4 ] && [ -f $F/$s/metadata.json ] && cp $F/$s/metadata.json $F/$s/description.txt $F/$s/thumbnail.png $G/$r/; done
cp /mnt/project-files/cs-channel/pipeline/*.py /mnt/project-files/cs-channel/pipeline/*.sh /mnt/project-files/cs-channel/pipeline/*.json pipeline/
/usr/bin/python3 - <<'PY'
import os,json
G="/home/user/schoolcompscience"; rows=[]
for root,ds,fs in sorted(os.walk(G)):
    if "metadata.json" in fs and "video.mp4" in fs:
        rows.append((os.path.relpath(root,G), json.load(open(root+"/metadata.json"))["title"]))
t=open(G+"/README.md").read().split("| Folder | Video |")[0]
t+="| Folder | Video |\n|---|---|\n"+"".join(f"| {a} | {b.replace('|','·')} |\n" for a,b in sorted(rows))+"\n`pipeline/` has the Manim + Kokoro TTS scripts that render the lessons.\n"
open(G+"/README.md","w").write(t)
PY
git add -A && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01TgNzgdMDDn4dCTXptsbsoV" && git -c push.negotiate=true push 2>&1 | tail -1
