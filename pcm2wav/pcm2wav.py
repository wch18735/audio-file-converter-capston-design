from classes.pcm import PCM
from settings.setting import os

# PATH SETTING
SAMPLE_PCM_PATH = '../data/pcm_16000_mono/'
SAMPLE_WAV_PATH = '../data/wav_16000_mono/'

# GET FILE LIST
PCM_LIST = os.listdir(SAMPLE_PCM_PATH)
WAV_LIST = os.listdir(SAMPLE_WAV_PATH)

# main
if __name__ == "__main__":
    pcm = PCM()

    for pcm_name in PCM_LIST:
        # get pcm
        pcm.get_pcm(SAMPLE_PCM_PATH+pcm_name)

        # make wav file with default setting
        pcm.make_wav(SAMPLE_WAV_PATH)
