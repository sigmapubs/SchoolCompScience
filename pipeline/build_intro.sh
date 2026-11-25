#!/bin/bash
# build_intro.sh <slug>: renders intros/<slug>/intro.mp4 (title slide + spoken intro)
set -e
P=/mnt/project-files/cs-channel; L=$P/intros/$1; A=/tmp/audio_intro_$1; M=/tmp/media_intro_$1
rm -rf $A $M; KOKORO_DIR=/tmp/kokoro /tmp/venv/bin/python $P/pipeline/make_audio.py $L/script.json $A >/dev/null
cp $A/captions.srt $L/captions.srt; cp $A/timings.json $L/timings.json
cd /tmp && PYTHONPATH=$P/pipeline TIMINGS=$A/timings.json INTRO=$L/intro.json /tmp/venv/bin/manim -qh --disable_caching --media_dir $M $P/pipeline/intro_scene.py Intro 2>&1 | grep -E "WARNING seg|Error" || true
cp $(find $M -name Intro.mp4 | head -1) $L/intro.mp4
echo "intro $1 $(ffprobe -v error -show_entries stream=codec_type,duration -of compact $L/intro.mp4 | tr '\n' ' ')"
