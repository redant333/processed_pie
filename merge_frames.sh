#!/bin/bash

frames_folder=$1
video_name=$2

ffmpeg -framerate 24 -i "${frames_folder}/frame_%d.png" \
  -c:v libx264 -pix_fmt yuv420p -r 24 "$video_name"
