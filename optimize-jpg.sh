#!/usr/bin/env bash

# directory containing images
input_dir="$1"

# target image quality
quality="$2"

if [[ -z "$input_dir" ]]; then
  echo "Please specify an input directory."
  exit 1
elif [[ -z "$quality" ]]; then
  echo "Please specify image quality."
  exit 1
fi

# for each jpg or jpeg in the input directory
for img in $( find $input_dir -type f -iname "*.jpg" -o -iname "*.jpeg" );
do
#   cp $img ${img%.*}-copy.jpg
  jpegoptim -m $quality ${img%.*}.jpg
  magick ${img%.*}.jpg    -resize 10x10  ${img%.*}-placeholder.jpg
done
