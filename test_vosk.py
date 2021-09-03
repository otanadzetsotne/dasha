import os
import json

import pyaudio
from vosk import Model
from vosk import KaldiRecognizer

from conf import *


def make_command(command):
    print(command)


def process_speech(speech):
    words = speech.split()

    if BOT_STOP in words:
        exit(1)

    if any(name_alias in words for name_alias in BOT_NAME_ALIASES):
        make_command(speech)


def set_listener():
    model = Model("model")
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    while True:
        data = stream.read(4000, exception_on_overflow=False)

        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            speech = json.loads(rec.Result())
            speech = speech['text']
            process_speech(speech)
        else:
            # rec.PartialResult()
            pass


if __name__ == '__main__':
    set_listener()
