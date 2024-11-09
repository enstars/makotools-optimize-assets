#!/usr/bin/env bash

## array of ids to go through
declare -a arr=("2050" "2051" "2052" "2053" "2054" "2055" "2056" "2057" "2058" "2059" "2061" "2062" "2063" "2064" "2065" "2066" "2067" "2068" "2069" "2070" "2073" "2074" "2075" "2076" "2077" "2078" "2079" "2080" "2081" "2082" "2460" "2461" "2083" "2071" "2084" "2060" "2072" "2085" "2086" "2088" "2090" "2087" "2089" "2091" "2092" "2093" "2094" "2095" "2097" "2096" "2098")

for i in "${arr[@]}"
do
   echo "card_full1_${i}_evolution.png"
   # change paths according to wherever the images are
   convert "assets/card_full1_${i}_evolution.png" "assets/card_full1_${i}_normal.png" \( -clone 0 -clone 1 -compose difference -composite -threshold 0 \) -delete 1 -alpha off -compose copy_opacity -composite "assets/card_full1_${i}_subtracted.png"
done
