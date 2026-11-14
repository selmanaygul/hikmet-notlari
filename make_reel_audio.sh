#!/bin/bash
# Kullanım: ./make_reel_audio.sh 002  -> reels/002-sesli.mp4
# Ses: posts/<id>.json içinde "ambient_file" varsa o kayıt (ör. Freesound'dan indirilen) kullanılır;
# yoksa "ambient" alanındaki sentez ses (gece, gol, yagmur, dere, dalga, sabah, ates, ...) üretilir.
set -e
id=$1
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 reels/$id.mp4)
file=$(python3 -c "import json;print(json.load(open('posts/$id.json')).get('ambient_file',''))")
if [ -n "$file" ]; then
  snd=$file
  fo=$(python3 -c "print(max(0,$d-2))")
  ffmpeg -y -loglevel error -stream_loop -1 -i "$file" -t "$d" -af "afade=t=in:d=1.5,afade=t=out:st=$fo:d=2" -ar 48000 audio/$id.wav
else
  snd=$(python3 -c "import json;print(json.load(open('posts/$id.json')).get('ambient','gece'))")
  python3 audio/ambient.py "$snd" "$d" audio/$id.wav $((10#$id))
fi
ffmpeg -y -loglevel error -i reels/$id.mp4 -i audio/$id.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -ar 48000 \
  -af "loudnorm=I=-20:TP=-2" -shortest -movflags +faststart reels/$id-sesli.mp4
echo "reels/$id-sesli.mp4 ($snd)"
