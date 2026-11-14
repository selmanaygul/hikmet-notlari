#!/bin/bash
# Kullanım: ./make_reel_audio.sh 001  -> reels/001-sesli.mp4 (gece ortam sesi eklenir)
set -e
id=$1; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 reels/$id.mp4)
python3 audio/ambient_night.py "$d" audio/$id.wav
ffmpeg -y -loglevel error -i reels/$id.mp4 -i audio/$id.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -ar 48000 \
  -af "loudnorm=I=-20:TP=-2" -shortest -movflags +faststart reels/$id-sesli.mp4
