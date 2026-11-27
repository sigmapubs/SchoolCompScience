#!/bin/bash
# do_group.sh <slug> <repo_path> dir:Class ...   (serialized via flock)
exec 9>/tmp/render.lock; flock 9
P=/mnt/project-files/cs-channel; S=$1; R=$2; shift 2; ST=/tmp/status_$S.txt; : > $ST
for dc in "$@"; do n=${dc%%:*}; c=${dc##*:}
  if [ -n "$ONLY" ] && ! echo " $ONLY " | grep -q " $n " && [ -f $P/videos/$n/video.mp4 ]; then :; else
  bash $P/pipeline/build.sh $P/videos/$n $c > /tmp/rb_$n.log 2>&1; fi
  echo "$n $(ffprobe -v error -show_entries stream=codec_type,duration -of compact $P/videos/$n/video.mp4 | tr '\n' ' ') $(grep -c 'WARNING seg' /tmp/rb_$n.log) warn" >> $ST
done
bash $P/pipeline/build_intro.sh $S >> $ST 2>&1
cd $P/pipeline && /tmp/venv/bin/python combine.py $S >> $ST 2>&1 && /tmp/venv/bin/python thumbs.py groups >> $ST 2>&1 && /tmp/venv/bin/python final_meta.py >> $ST 2>&1
for d in $P/final/*/; do /tmp/venv/bin/python -c "
import json,sys;d=sys.argv[1];m=json.load(open(d+'/metadata.json'));open(d+'/description.txt','w').write(m['title']+'\n\n'+m['description']+'\n')" $d; done
F=$P/final/$S/video.mp4
echo "final $(ffprobe -v error -show_entries stream=codec_type,duration -of compact $F | tr '\n' ' ')" >> $ST
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); for fr in 0.01 0.2 0.4 0.6 0.8 0.95; do t=$(echo "$D*$fr" | bc); echo "vol $t $(ffmpeg -nostats -ss $t -t 4 -i $F -vn -af volumedetect -f null - 2>&1 | grep mean_volume | sed 's/.*mean_volume//')" >> $ST; done
# copy into repo
G=/home/user/schoolcompscience; mkdir -p $G/$R
for f in video.mp4 captions.srt thumbnail.png metadata.json description.txt; do cp $P/final/$S/$f $G/$R/; done
echo ALLDONE >> $ST
