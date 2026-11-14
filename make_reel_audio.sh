#!/bin/bash
# Kullanım: ./make_reel_audio.sh 002  -> reels/002-sesli.mp4
# Ses türü posts/<id>.json içindeki "ambient" alanından alınır (gece, gol, yagmur, dere, dalga, sabah, ates).
set -e
id=$1
snd=$(python3 -c "import json;print(json.load(open('posts/$id.json')).get('ambient','gece'))")
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 reels/$id.mp4)
python3 audio/ambient.py "$snd" "$d" audio/$id.wav $((10#$id))
ffmpeg -y -loglevel error -i reels/$id.mp4 -i audio/$id.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -ar 48000 \
  -af "loudnorm=I=-20:TP=-2" -shortest -movflags +faststart reels/$id-sesli.mp4
echo "reels/$id-sesli.mp4 ($snd)"
