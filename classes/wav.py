
from settings.setting import wave

class WAV():
    '''
        WAV class

        NumChannels: Channels that pcm recorded. Default is mono channel.
        Sample Rate: Sample rate of sound. In this case, default case is 16000
        Byte per Sample: Quantization resolution. Default is generally 2byte
        Btye Rate: (Bit per samplee)/2 * Sample Rate * NumChannels
        PCM path: PCM path with filename
        WAV path: WAV path with filename

        get header: get wav file header
        print header: print wav file header
        get_wav: get wav file from path
        get_pcm: get pcm file from wav
        make_pcm: seperate header and pcm data
    '''

    def __init__(self):
        self.__numchannels = None
        self.__sample_rate = None
        self.__byte_per_sample = None
        self.__byte_rate = None
        self.__nframes = None
        self.__pcm_data = None
        self.__wav_data = None
        self.__wav_header = None
        self.__wav_path = None
        self.__pcm_path = None

    def __call__(self, wav_path, pcm_path):
        self.__wav_path = wav_path
        self.__pcm_path = pcm_path

    def get_wav(self, wav_path):
        with wave.open(wav_path, 'rb') as wav_fp:
            # getparams: (nchannels, sampwidth, framerate, nframes, comptype, compname)
            wav_params = wav_fp.getparams()

            # update params
            self.__numchannels = wav_params[0]  # nchannels
            self.__byte_per_sample = wav_params[1]  # sampwidth
            self.__sample_rate = wav_params[2]  # framerate
            self.__nframes = wav_params[3]  # nframes

            # update wav data
            self.__wav_data = wav_fp.readframes(nframes=self.__nframes)

            # update wav header
            # fixed header 44 bytes
            self.__wav_header = self.__wav_data[0:44]

            # update pcm data
            self.__pcm_data = self.__wav_data[44:]

        return self.__wav_data

    def get_header(self, wav_path = None):
        if wav_path is None:
            with wave.open(self.__wav_path, 'rb') as wav_fp:
                return wav_fp.readframes(nframes=44)
        else:
            with wave.open(wav_path, 'rb') as wav_fp:
                return wav_fp.readframes(nframes=44)

    def get_pcm(self, wav_path = None):
        if wav_path is None:
            with wave.open(self.__wav_path, 'rb') as wav_fp:
                # getparams: (nchannels, sampwidth, framerate, nframes, comptype, compname)
                wav_params = wav_fp.getparams(wav_path)
            # get nframes
            nframes = wav_params[3]

            # update wav data
            return wav_fp.readframes(nframes=nframes)[44:]
        else:
            with wave.open(wav_path, 'rb') as wav_fp:
                # getparams: (nchannels, sampwidth, framerate, nframes, comptype, compname)
                wav_params = wav_fp.getparams(wav_path)
            # get nframes
            nframes = wav_params[3]

            # update wav data
            return wav_fp.readframes(nframes=nframes)[44:]

    def make_pcm(self, pcm_path = None):
        if pcm_path is None:
            with open(self.__pcm_path, 'wb') as pcm_fp:
                pcm_fp.write(self.__pcm_data)
        else:
            with open(pcm_path, 'wb') as pcm_fp:
                pcm_fp.write(self.__pcm_data)

