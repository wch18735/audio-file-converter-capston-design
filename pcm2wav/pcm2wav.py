import sys
sys.path.append('..')
from settings.setting import os
from settings.setting import argparse
from classes.pcm import PCM


def _get_path():
    """ get pcm, wav path """
    SAMPLE_PCM_PATH = '../data/pcm_16000_mono/'
    SAMPLE_WAV_PATH = '../data/wav_16000_mono/'

    return SAMPLE_PCM_PATH, SAMPLE_WAV_PATH

def _get_file_list(SAMPLE_PCM_PATH, SAMPLE_WAV_PATH):
    """ get sub-file list """
    PCM_LIST = os.listdir(SAMPLE_PCM_PATH)
    WAV_LIST = os.listdir(SAMPLE_WAV_PATH)

    return PCM_LIST, WAV_LIST

def _get_args():
    """ Get Arguments parser"""
    parser = argparse.ArgumentParser(description="pcm2wav")
    parser.add_argument('--sample_rate', type=int, required=False, default=16000)
    parser.add_argument('--bits_per_sample', type=int, required=False, default=16)
    parser.add_argument('--numchannels', type=int, required=False, default=1)
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    sample_pcm_path, sample_wav_path = _get_path()
    pcm_list, wav_list = _get_file_list(sample_pcm_path, sample_wav_path)
    args = _get_args()

    pcm = PCM(numchannels=args.numchannels, sample_rate=args.sample_rate, bits_per_sample=args.bits_per_sample)

    for pcm_name in pcm_list:
        # get pcm
        pcm.get_pcm(sample_pcm_path + pcm_name)

        # make wav file with default setting
        pcm.make_wav(sample_wav_path)