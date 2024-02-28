import pyaudio
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                output=True)

def main():
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # 在这里可以添加对音频流的处理逻辑

        stream.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    main()