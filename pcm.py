from setting import wave

class PCM():
    '''
        PCM class
        NumChannels: Channels that pcm recorded. Default is mono channel.
        Sample Rate: Sample rate of sound. In this case, default case is 16000
        Bits per Sample: Quantization resolution. Default is generally 2byte
        Btye Rate: (Bit per samplee)/2 * Sample Rate * NumChannels

        get_pcm: get pcm data from path
        make_wav: make header concatenated file into path
        set_parameter: set private parameters
    '''

    def __init__(self, numchannels = 1, sample_rate = 16000, bits_per_sample = 16):
        self.__numchannels = numchannels
        self.__sample_rate = sample_rate
        self.__bits_per_sample = bits_per_sample
        self.__byte_rate = int(self.__numchannels * self.__sample_rate * (self.__bits_per_sample / 8))
        self.__pcmdata = None
        self.__wav_header = None
        self.__wav_path = None
        self.__pcm_path = None

    def get_pcm(self, pcm_path):
        self.__pcm_path = pcm_path
        with open(pcm_path, 'rb') as pcm_fp:
            self.__pcmdata = pcm_fp.read()

    def get_header(self, header):
        self.__wav_header = header

    def make_wav(self, wav_path):
        if wav_path.split('.')[-1] != 'pcm' or 'PCM':
            wav_path = wav_path + self.__pcm_path.split('/')[-1].split('.')[0] + '.wav'
            with wave.open(wav_path, 'wb') as wavdata:
                wavdata.setnchannels(self.__numchannels)
                wavdata.setframerate(self.__sample_rate)
                wavdata.setsampwidth(int(self.__bits_per_sample / 8))
                wavdata.writeframes(self.__pcmdata)
        else:
            with wave.open(wav_path, 'wb') as wavdata:
                wavdata.setnchannels(self.__numchannels)
                wavdata.setframerate(self.__sample_rate)
                wavdata.setsampwidth(int(self.__bits_per_sample / 8))
                wavdata.writeframes(self.__pcmdata)

    def set_numchannels(self, numchannels):
        self.__numchannels = numchannels
        self.__byte_rate = int(self.__numchannels * self.__sample_rate * (self.__bits_per_sample / 8))

    def set_sample_rate(self, sample_rate):
        self.__sample_rate = sample_rate
        self.__byte_rate = int(self.__numchannels * self.__sample_rate * (self.__bits_per_sample / 8))

    def set_bits_per_sample(self, bits_per_sample):
        self.__bits_per_sample = bits_per_sample
        self.__byte_rate = int(self.__numchannels * self.__sample_rate * (self.__bits_per_sample / 8))



