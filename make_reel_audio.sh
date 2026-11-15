#!/bin/bash
# Kullanım: ./make_reel_audio.sh 002  -> reels/002-sesli.mp4
# posts/<id>.json içinde "music" varsa o parça kullanılır (audio/muzik/ altından, bkz. audio/muzik/KAYNAKLAR.md);
# yoksa "ambient" alanındaki sentez ortam sesi (gece, gol, yagmur, dere, dalga, sabah, ates, ...).
set -e
id=$1
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 reels/$id.mp4)
read -r music start credit < <(python3 -c "
import json; p=json.load(open('posts/$id.json')); m=p.get('music')
print(m['file'], m.get('start', 0), m['credit'].replace(' ', '_')) if m else print('-', 0, '-')")
if [ "$music" != "-" ]; then
  fo=$(python3 -c "print(max(0, $d - 2.5))")
  ffmpeg -y -loglevel error -i reels/$id.mp4 -ss "$start" -t "$d" -i "audio/muzik/$music" -map 0:v -map 1:a -c:v copy \
    -c:a aac -b:a 160k -ar 48000 -af "afade=t=in:d=1,afade=t=out:st=$fo:d=2.5,loudnorm=I=-20:TP=-2" \
    -shortest -movflags +faststart reels/$id-sesli.mp4
  echo "reels/$id-sesli.mp4 (müzik: $music)"
  echo "Açıklamaya ekle: ${credit//_/ }"
else
  snd=$(python3 -c "import json;print(json.load(open('posts/$id.json')).get('ambient','gece'))")
  python3 audio/ambient.py "$snd" "$d" audio/$id.wav $((10#$id))
  ffmpeg -y -loglevel error -i reels/$id.mp4 -i audio/$id.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -ar 48000 \
    -af "loudnorm=I=-20:TP=-2" -shortest -movflags +faststart reels/$id-sesli.mp4
  echo "reels/$id-sesli.mp4 ($snd)"
fi
