from settings.setting import librosa
from settings.setting import wave
from settings.setting import np
from settings.setting import scipy

class Spectrogram(str):
    """
    Spectrogram

    Note:
        Support only .wav, .pcm, .txt format

    Function:
        set_img_path(path): store path to save spectrogram image
        set_spec_path(path): stroe path to save spectrogram pickle
        get_spectrogram(path): return numpy format spectrogram
    """

    def __init__(self, path):
        self.folder_path = path
        self.spec_path = path
        self.img_path = path
        self.file_path = None # target file path
        self.file_data = None # data

        self.sample_rate = 16000
        self.n_fft=512
        hop_length=256
        power=2.0
        self.spectrogram = None

    def set_spec_path(self, path):
        self.spec_path = path

    def set_img_path(self, path):
        self.img_path = path

    def set_file(self, filename):
        self.file_path = self.folder_path + filename
        if filename.split(".")[-1] == 'pcm':
            with open(self.file_path, 'rb') as pcm_fp:
                self.file_data = pcm_fp.read()

        elif filename.split(".")[-1] == 'wav':
            with wave.open(self.file_path, 'rb') as wav_fp:
                self.file_data = wav_fp.readframes(wav_fp.getparams()[3])[44:]

        elif filename.split(".")[-1] == 'txt':
            with open(self.file_path, 'rb') as txt_fp:
                x_num, sample_rate = txt_fp.readline().split()
                x_num = int(x_num)
                sample_rate = 1/float(sample_rate)
                self.sample_rate = int(sample_rate)

                self.file_data = np.ndarray((x_num,))
                for i in range(x_num):
                    _, amplitude = txt_fp.readline().split()
                    self.file_data[i] = float(amplitude)

    def get_spectrogram(self):
        self.spectrogram = librosa.core.stft(self.file_data, self.n_fft)
        return self.spectrogram
