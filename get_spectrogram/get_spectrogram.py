import sys
sys.path.append('..')
from settings.setting import argparse
from settings.setting import os
from classes.spectrogram import Spectrogram
from settings.setting import scipy
from settings.setting import lid
from settings.setting import librosa
from settings.setting import plt
from settings.setting import np

def _get_args():
    parser = argparse.ArgumentParser(description="Spectrogram")
    parser.add_argument("--folder_path", type=str)
    parser.add_argument("--image_path", type=str)

    args = parser.parse_args()

    return args

def draw_spectrogram(data, window_size=1024, step_size=256, eps=1e-10, sample_rate=100):
    n_per_seg = int(round(window_size * sample_rate / 1000))
    n_overlap = int(round(step_size * sample_rate / 1000))

    freqs, times, spec = scipy.signal.spectrogram(data,
                                                  fs=sample_rate,
                                                  window='hann',
                                                  nperseg=n_per_seg,
                                                  noverlap=n_overlap,
                                                  detrend=False)

    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111)
    ax.set_title('Spectrogram of ' + "Sample")
    ax.set_ylabel('Freqency (Hz)')
    ax.set_xlabel('Seconds (s)')
    ax.imshow(spec.T, aspect='auto', origin='lower',
              extent=[times.min(), times.max(), freqs.min(), freqs.max()])
    plt.show()

    return freqs, times, spec

def save_spectrogram(freqs, times, spec, filename):
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111)
    ax.set_title('Spectrogram of ' + filename)
    ax.set_ylabel('Freqency (Hz)')
    ax.set_xlabel('Seconds (s)')
    ax.imshow(spec.T, aspect='auto', origin='lower',
              extent=[times.min(), times.max(), freqs.min(), freqs.max()])
    # You can change
    root_path = './spectrogram_image/'

    plt.savefig(root_path+filename.split('.')[0]+'.png')

if __name__ == "__main__":
    args = _get_args()
    file_list = os.listdir(args.folder_path)

    for filename in file_list:
        spec = Spectrogram(args.folder_path)
        spec.set_file(filename)
        freqs, times, spec = draw_spectrogram(spec.file_data)
        save_spectrogram(freqs,times, spec, filename)



