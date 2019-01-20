#!/bin/bash
dir=${1:-output/frames}
gif=${2:-output.gif}
convert $dir/frame_*.png -loop 0 -delay 100 -layers Optimize $gif
