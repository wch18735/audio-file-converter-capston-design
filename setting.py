import os
import sys
import wave
import librosa
import numpy as np
import librosa.display
import IPython.display as ipd

# PATH
SAMPLE_PCM_PATH = './data_sample/pcm_16000_mono/'
SAMPLE_WAV_PATH = './data_sample/wav_16000_mono/'

# FILE LIST
PCM_LIST = os.listdir(SAMPLE_PCM_PATH)
WAV_LIST = os.listdir(SAMPLE_WAV_PATH)

