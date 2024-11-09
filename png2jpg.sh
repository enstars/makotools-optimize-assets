#!/usr/bin/env bash

# directory containing images
input_dir="$1"

# jpg image quality
quality="$2"

if [[ -z "$input_dir" ]]; then
  echo "Please specify an input directory."
  exit 1
elif [[ -z "$quality" ]]; then
  echo "Please specify image quality."
  exit 1
fi

# for each png in the input directory
# card_full1 are transparent renders
for img in $( find $input_dir -type f -iname "*.png" -a ! -iname "card_full1*"  );
do
  magick $img -quality $quality% ${img%.*}.jpg
done
