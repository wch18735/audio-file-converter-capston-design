from setting import wave
from setting import os
from setting import ipd
from wav import WAV
from pcm import PCM

from setting import SAMPLE_WAV_PATH
from setting import SAMPLE_PCM_PATH
from setting import PCM_LIST
from setting import WAV_LIST

# main
if __name__ == "__main__":
    test_pcm = PCM()

    # get pcm from path
    file_idx = 0 # from PCM_LIST, you can choose idx

    # get pcm
    test_pcm.get_pcm(os.path.join(SAMPLE_PCM_PATH, PCM_LIST[file_idx]))

    # make wav file with default setting
    test_pcm.make_wav(SAMPLE_WAV_PATH)
