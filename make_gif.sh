#!/bin/bash
gif=${1:-output.gif}
convert output/frames/frame_*.png -loop 0 -delay 100 -layers Optimize $gif
