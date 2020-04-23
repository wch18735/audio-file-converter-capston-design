import collections
import contextlib
import sys
import wave
import webrtcvad
import os
import errno

def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def write_wave(path, audio, sample_rate):
    """Writes a .wav file.

    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)


class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.

    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.

    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(sample_rate, frame_duration_ms,
                  padding_duration_ms, vad, frames):
    """Filters out non-voiced audio frames.

    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.

    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.

    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.

    Arguments:

    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).

    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False

    voiced_frames = []
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        sys.stdout.write('1' if is_speech else '0')
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                sys.stdout.write('+(%s)' % (ring_buffer[0][0].timestamp,))
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []
    if triggered:
        sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
    sys.stdout.write('\n')
    # If we have any leftover voiced audio when we run out of input,
    # yield it.
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])

def get_wav_list(path):
    path = os.getcwd()
    target_foler = '\\sample_wav\\'
    file_list = os.listdir(path+target_foler)               # sample_wav == target folder
    file_list_wav = [file for file in file_list if file.startswith("Kai")]

    return file_list_wav

def mkdir(target_path, foldername):    # make folder if there is no folder in target_path
    try:
        if not (os.path.isdir(target_path + foldername)):
            os.makedirs(os.path.join(target_path + foldername))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!")
            raise

def save_chunk(segments, tested_sample_path, filename):
    # make folder named after filename
    mkdir(tested_sample_path, filename)

    # save chunk files in tested file path in folder_#
    for i, segment in enumerate(segments):
        chunk_name = 'chunk-%002d.wav' % (i,)
        print(' Writing %s' % (chunk_name,))
        write_wave(tested_sample_path + filename + '\\' + chunk_name, segment, sample_rate)

def wav_concatenate(target_path, filename):
    # target_path = target_path+'\\'

    file_list = os.listdir(target_path)
    file_list_wav = [file for file in file_list if file.startswith("chunk")]
    print("file_list: {}".format(file_list_wav))
    # outfile = target_path+"concatenated_all\\"+filename
    outfile = "C:\\Users\\EC\\Desktop\\CH\\Voice_Activity_Detection\\Google_VAD\\Tested_Sample\\concatenated_all\\" + filename
    data = []

    for infile in file_list_wav:
        w = wave.open(target_path + infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])

    for audio_chunk_index in range(len(file_list_wav)):
        output.writeframes(data[audio_chunk_index][1])

    print('context concatenate success')

    output.close()

if __name__ == '__main__':

    # initializing setting
    base_path = os.getcwd()
    filepath = base_path + '\\sample_wav\\'                 # sample_wav folder has wav auido data
    tested_sample_path = base_path + '\\Tested_Sample\\'           # chunked wave folder is going to save in this folder
    Kai_list = get_wav_list(base_path + '\\sample_wav\\')   # to get sample audio.wav in "sample_wav" folder in 'list'
    # filename = 'KaiSpeech_000020.wav'
    aggressiveness = 3                                      # choose 1, 2, 3 for agressiveness

    for filename in Kai_list:

        # read_wave file
        audio, sample_rate = read_wave(filepath + filename)
        vad = webrtcvad.Vad(aggressiveness)

        # generate samples in one audio
        frames = frame_generator(30, audio, sample_rate)
        frames = list(frames)

        # segments : segmented files in one audio
        segments = vad_collector(sample_rate, 30, 300, vad, frames)

        # save_file
        save_chunk(segments, tested_sample_path, filename)

        # concatenate
        wav_concatenate(tested_sample_path+'\\'+filename+'\\', filename)
        print(filename)


