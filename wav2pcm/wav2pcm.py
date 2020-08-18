import sys
sys.path.append('..')
from settings.setting import os
from settings.setting import argparse
from classes.wav import WAV

def _get_file_list(SAMPLE_PCM_PATH, SAMPLE_WAV_PATH):
    """ get sub-file list """
    PCM_LIST = os.listdir(SAMPLE_PCM_PATH)
    WAV_LIST = os.listdir(SAMPLE_WAV_PATH)

    return PCM_LIST, WAV_LIST

def _get_args():
    """ Get Arguments parser"""
    parser = argparse.ArgumentParser(description="wav2pcm")
    parser.add_argument('--sample_pcm_path', type=str, required=False)
    parser.add_argument('--sample_wav_path', type=str, required=False)
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = _get_args()  # get args
    sample_pcm_path = args.sample_pcm_path
    sample_wav_path = args.sample_wav_path
    pcm_list, wav_list = _get_file_list(sample_pcm_path, sample_wav_path)

    wav = WAV()
    wav(sample_wav_path, sample_pcm_path)

    for wav_name in wav_list:
        # get wav
        wav.get_wav(sample_wav_path + wav_name)

        # make pcm file with default setting
        pcm_name = wav_name.split('.')[0]+'.pcm'
        wav.make_pcm(sample_pcm_path + pcm_name)