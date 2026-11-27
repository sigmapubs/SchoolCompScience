#!/bin/bash
# preview_many.sh lesson ... : audio + low-quality preview for each (4 at a time); prints timing warnings/errors
S=/tmp/claude-0/-home-user/6c5f1df8-ef71-5a33-8dfc-4a8dac211f34/scratchpad
P=/mnt/project-files/cs-channel
cls(){ python3 -c "import re;print(re.search(r'^class (\w+)\(', open('$P/videos/$1/scene.py').read(), re.M).group(1))"; }
for l in "$@"; do KOKORO_DIR=/tmp/kokoro /tmp/venv/bin/python $P/pipeline/make_audio.py $P/videos/$l/script.json /tmp/audio_$l > /dev/null 2>&1; done
set -- "$@"
while [ $# -gt 0 ]; do
  for l in $1 $2 $3 $4; do (bash $S/preview.sh $l $(cls $l) 2>&1 | grep -E "WARNING seg|Traceback|Error:|NOVIDEO" | grep -v muxer | sed "s/^/$l: /") & done; wait
  shift 4 2>/dev/null || shift $#
done
echo PREVIEWS DONE
