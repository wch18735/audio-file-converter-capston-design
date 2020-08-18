#!/bin/bash
# @github{
#   title = {Audio_File_Conversion},
#   author = {Soohwan Kim, Seyoung Bae, Cheolhwang Won},
#   link = {https://github.com/wch18735/Audio_File_Conversion},
#   year = {2020}
# }

SAMPLE_PCM_PATH='../data/pcm_16000_mono/'
SAMPLE_WAV_PATH='../data/wav_16000_mono/'

cd wav2pcm

python ./wav2pcm.py --sample_pcm_path="$SAMPLE_PCM_PATH" --sample_wav_path="$SAMPLE_WAV_PATH"

