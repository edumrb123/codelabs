#!/usr/bin/env bash
# Build the full video: narration audio -> Manim scenes -> one MP4.
#   ./build.sh            720p30 (default)
#   QUALITY=h ./build.sh  1080p60
#   QUALITY=l ./build.sh  480p15 quick preview
#   ./build.sh Ch03 Ch05  render only these chapters, then re-join everything
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python}
Q=${QUALITY:-m}
JOBS=${JOBS:-4}
case $Q in l) RES=480p15 ;; m) RES=720p30 ;; h) RES=1080p60 ;; k) RES=2160p60 ;; esac

$PY tts.py

SCENES=("$@")
[ ${#SCENES[@]} -eq 0 ] && SCENES=(Ch00 Ch01 Ch02 Ch03 Ch04 Ch05 Ch06 Ch07 Ch08 Ch09 Ch10 Ch11 Ch12)

printf '%s\n' "${SCENES[@]}" | xargs -P "$JOBS" -I{} sh -c \
  "$PY -m manim -q$Q --disable_caching --progress_bar none --media_dir build/media_{} scenes.py {} > build/{}.log 2>&1 && echo 'rendered {}' || { echo 'FAILED {} (see build/{}.log)'; exit 255; }"

LIST=build/concat.txt
: > "$LIST"
for s in Ch00 Ch01 Ch02 Ch03 Ch04 Ch05 Ch06 Ch07 Ch08 Ch09 Ch10 Ch11 Ch12; do
  echo "file 'media_$s/videos/scenes/$RES/$s.mp4'" >> "$LIST"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -c:v copy -c:a aac -b:a 160k art_history_$RES.mp4
echo "Done: $(pwd)/art_history_$RES.mp4"
