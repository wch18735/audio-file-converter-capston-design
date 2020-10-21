#!/bin/bash
# @github{
#   title = {Audio_File_Conversion},
#   author = {Cheolhwang Won}
#   link = {https://github.com/wch18735/Audio_File_Conversion},
#   year = {2020}
# }

SAMPLE_RATE=16000
NUMCHANNEL=1
BITS_PER_SAMPLE=16

cd pcm2wav

python ./pcm2wav.py --sample_rate=$SAMPLE_RATE --numchannels=$NUMCHANNEL --bits_per_sample=$BITS_PER_SAMPLE

