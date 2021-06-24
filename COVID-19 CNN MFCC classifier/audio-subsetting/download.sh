#!/bin/bash

SAMPLE_RATE=22050

# fetch_clip(videoID, startTime, endTime)
echo "Fetching $1 ($2 to $3)..."
outname="$1_$2_$3"
if [ -f "../non_covid/${outname}.wav" ]; then
  echo "Already have it."
  #return
fi

youtube-dl https://youtube.com/watch?v=$1 \
  --quiet --extract-audio --audio-format wav \
  --output "../non_covid/$outname.%(ext)s"
if [ $? -eq 0 ]; then
  # If we don't pipe `yes`, ffmpeg seems to steal a
  # character from stdin. I have no idea why.
  yes | ffmpeg -loglevel quiet -i "../non_covid/$outname.wav" -ar $SAMPLE_RATE \
    -ss "$2" -to "$3" "../non_covid/${outname}_out.wav"
  mv "../non_covid/${outname}_out.wav" "../non_covid/$outname.wav"
  #gzip "./audio-locations/$outname.wav"
else
  # Give the user a chance to Ctrl+C.
  #sleep 1
  echo "..."
fi
