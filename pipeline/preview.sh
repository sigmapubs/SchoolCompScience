#!/bin/bash
# preview.sh <lesson_id> <Class>
L=/mnt/project-files/cs-channel/videos/$1; A=/tmp/audio_$1; M=/tmp/pmedia_$1; S=/tmp/claude-0/-home-user/6c5f1df8-ef71-5a33-8dfc-4a8dac211f34/scratchpad
rm -rf $M; cd /tmp && PYTHONPATH=/mnt/project-files/cs-channel/pipeline TIMINGS=$A/timings.json /tmp/venv/bin/manim -ql --disable_caching --media_dir $M $L/scene.py $2 2>&1 | grep -E "WARNING seg|Traceback|Error|line [0-9]" | head -20
V=$(find $M -name "$2.mp4" | head -1); [ -z "$V" ] && { echo NOVIDEO; exit 1; }
TS=$(python3 -c "
import json;T=json.load(open('$A/timings.json'));t=0;o=[]
for x in T: t+=x['duration']; o.append(max(0,t-0.8))
print(' '.join('%.2f'%v for v in o))")
i=0; for t in $TS; do ffmpeg -v error -y -ss $t -i $V -frames:v 1 $M/f$i.png; i=$((i+1)); done
ffmpeg -v error -y -i $M/f%d.png -vf "tile=4x2" $S/$1_sheet.png 2>/dev/null || ffmpeg -v error -y -pattern_type glob -i "$M/f*.png" -vf tile=4x2 $S/$1_sheet.png
echo done $1
