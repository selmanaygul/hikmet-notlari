#!/bin/bash
# Kullanım: ./make_reel.sh 001  -> reels/001.mp4 (1080x1920, kapak + metin, yavaş yakınlaşma)
set -e
id=$1; A=cards/$id-1.jpg; B=cards/$id-2.jpg; T1=${T1:-6}; T2=${T2:-13}; X=1
ffmpeg -y -loglevel error \
 -framerate 30 -loop 1 -t $T1 -i "$A" -framerate 30 -loop 1 -t $T2 -i "$B" -filter_complex "
 [0]scale=2160:-1,zoompan=z='1+0.06*on/($T1*30)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1350:fps=30,split[a1][a2];
 [1]scale=2160:-1,zoompan=z='1+0.04*on/($T2*30)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1350:fps=30,split[b1][b2];
 [a1]scale=1536:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.18[abg];[abg][a2]overlay=0:285[A];
 [b1]scale=1536:1920,crop=1080:1920,boxblur=30:3,eq=brightness=-0.18[bbg];[bbg][b2]overlay=0:285[B];
 [A][B]xfade=transition=fade:duration=$X:offset=$((T1-X)),format=yuv420p[v]" \
 -map "[v]" -c:v libx264 -preset slow -crf 20 -r 30 -movflags +faststart reels/$id.mp4
ffmpeg -y -loglevel error -ss 2 -i reels/$id.mp4 -frames:v 1 reels/$id-cover.jpg
ffprobe -v error -show_entries format=duration -of csv=p=0 reels/$id.mp4
