#!/usr/bin/env bash

# directory containing images
input_dir="$1"

for img in $( find $input_dir -type f -iname "*.png" -a -iname "card_full1*"  );
do
   echo $img
   convert $img \( -clone 0 -channel a -fx 0 \) \( -clone 0  -alpha extract -channel RGB -black-threshold 5% +channel  \) -swap 0,1 -composite  $img
   # testing command to check:
   # convert a/$img  -alpha extract -channel RGB -threshold 0% +channel  a/$img
done
