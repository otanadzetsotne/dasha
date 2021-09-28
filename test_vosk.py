import os
import json

import pyaudio
from vosk import Model
from vosk import KaldiRecognizer
from pymorphy2 import MorphAnalyzer

from configs import *


class Recognizer:
    def __init__(self):
        self.model = Model('model')
        self.kaldi = KaldiRecognizer(self.model, 16_000)

    def accept_wave(self, wave):
        return self.kaldi.AcceptWaveform(wave)

    def result(self):
        return self.kaldi.Result()


class Listener:
    def __init__(self):
        self.steam = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16_000,
            input=True,
            frames_per_buffer=8000,
        )

    def start(self, *args, **kwargs):
        self.steam.start_stream(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.steam.read(*args, **kwargs)


class Morph:
    def __init__(self):
        self.morph = MorphAnalyzer()

    def normalize(self, word: str):
        return self.morph.parse(word)[0].normal_form


class Tokenizer:
    def __init__(self):
        self.morph = Morph()

    def tokenize(self, speech: str):
        tokens = speech.split()
        # Delete call
        tokens = [token for token in tokens if token not in BOT_NAME_ALIASES]
        # Morph analyze
        tokens = [self.morph.normalize(token) for token in tokens]
        # Delete stop words
        tokens = [token for token in tokens if token not in STOP_WORDS]
        # Sort tokens
        tokens.sort()

        return tokens


class Dasha:
    def __init__(self):
        self.recognizer = Recognizer()
        self.tokenizer = Tokenizer()
        self.listener = Listener()

    def awake(self):
        """
        Wake up Dasha so she can listen
        :return:
        """

        # Start listening microphone
        self.listener.start()

        while True:
            # Listen audio batch
            wave = self.listener.read(4000, exception_on_overflow=False)

            # Nothing received
            if len(wave) <= 0:
                self.sleep()

            # Speech audio received
            if self.recognizer.accept_wave(wave):
                # Speech as text
                speech = self.recognizer.result()
                speech = json.loads(speech)
                speech = speech['text']
                # Process speech
                self.listen(speech)

    def listen(self, speech):
        """
        Process request
        :param speech:
        :return:
        """

        if self.is_command_sleep(speech):
            self.sleep()

        if self.is_call(speech):
            self.command(speech)

    def command(self, speech):
        """
        Make request command
        :param speech:
        :return:
        """

        tokens = self.tokenizer.tokenize(speech)

        print(tokens)

    @staticmethod
    def sleep():
        """
        Lull Dasha
        :return:
        """

        exit(1)

    @staticmethod
    def is_call(speech):
        """
        Was Dasha called
        :param speech:
        :return: bool
        """

        # TODO: delete 'or True'
        return any(name_alias in speech.split() for name_alias in BOT_NAME_ALIASES) or True

    @staticmethod
    def is_command_sleep(speech):
        """
        Was command to sleep
        :param speech:
        :return: bool
        """

        return BOT_STOP in speech.split()


if __name__ == '__main__':
    Dasha().awake()
