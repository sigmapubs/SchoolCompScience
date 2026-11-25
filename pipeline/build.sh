#!/bin/bash
# build.sh <lesson_dir> <SceneClass>   lesson_dir holds script.json + scene.py; outputs video.mp4 + captions.srt
set -e
L=$1; S=$2; A=/tmp/audio_$(basename $L)
rm -rf $A; KOKORO_DIR=/tmp/kokoro /tmp/venv/bin/python /mnt/project-files/cs-channel/pipeline/make_audio.py $L/script.json $A
cp $A/captions.srt $L/captions.srt
rm -rf /tmp/media_$(basename $L); cd /tmp && PYTHONPATH=/mnt/project-files/cs-channel/pipeline TIMINGS=$A/timings.json /tmp/venv/bin/manim -qh --disable_caching --media_dir /tmp/media_$(basename $L) $L/scene.py $S 2>&1 | grep -E "WARNING seg|Traceback|Error" || true
V=$(find /tmp/media_$(basename $L) -name "$S.mp4" | head -1)
ffmpeg -v error -y -i $V -i $L/captions.srt -c:v copy -c:a aac -b:a 192k -c:s mov_text -metadata:s:s:0 language=eng -movflags +faststart $L/video.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $L/video.mp4
