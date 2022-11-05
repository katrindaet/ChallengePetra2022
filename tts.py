# Usage example:
#
# > import tts
# > mytts = tts.TTS()
# > mytts.say('Hello, World')

import pyttsx3


class TTS:
    def __init__(self):
        self._engine = pyttsx3.init()
        self._voices = {
            voice.id: voice.name for voice in self._engine.getProperty("voices")
        }
        # Reading properties on SAPI doesn't reflect actual value after a change, store values in local variable
        self._volume = self._engine.getProperty("volume")
        self._rate = self._engine.getProperty("rate")
        self._voice_id = self._engine.getProperty("voice")

    def voiceId(self):
        return self._voice_id

    def voices(self):
        return self._voices

    def setVoice(self, voice_id):
        assert voice_id in self._voices
        self._voice_id = voice_id
        self._engine.setProperty("voice", voice_id)

    def volume(self):
        return self._volume

    def setVolume(self, volume):
        assert 0.0 <= volume <= 1.0
        self._volume = volume
        self._engine.setProperty("volume", volume)

    def rate(self):
        return self._rate

    def setRate(self, rate):
        assert rate > 0
        self._rate = rate
        self._engine.setProperty("rate", rate)

    def say(self, text):
        self._engine.say(text)
        self._engine.runAndWait()

    def cancel(self):
        self._engine.stop()
