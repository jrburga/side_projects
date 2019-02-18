"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

dtype = np.dtype('int')
dt = dtype.newbyteorder('>')

data = stream.read(CHUNK)
array = np.frombuffer(data, dtype=np.uint8)
array = [x / 255. for x in array]
print array

stream.stop_stream()
stream.close()
p.terminate()
