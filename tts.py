# Usage example:
#
# > import tts
# > mytts = tts.TTS()
# > mytts.say('Hello, World')

import pyttsx3
import os
import simpleaudio
import tempfile

HAS_GOOGLE = False
try:
    from google.auth import exceptions
    from google.cloud import texttospeech

    HAS_GOOGLE = True
except ImportError:
    pass


class TTS:
    def __init__(self):
        self._engine = pyttsx3.init()
        self._voices = {
            voice.id: voice.name for voice in self._engine.getProperty("voices")
        }

        if HAS_GOOGLE:
            # Only add Google TTS if environment variable for authentication is set.
            try:
                self._google_tts_client = texttospeech.TextToSpeechClient()
                self._play_buffer = None
                self._voices["google-english"] = "Google Englisch"
                self._voices["google-german"] = "Google Deutsch"
            except exceptions.DefaultCredentialsError:
                pass

        self._rate_modifier = 1.0

        # Reading properties on SAPI doesn't reflect actual value after a change, store values in local variable
        self._volume = self._engine.getProperty("volume")
        self._base_rate = self._engine.getProperty("rate")
        self._voice_id = self._engine.getProperty("voice")
        self._playing = False

    def googleTtsIsActive(self):
        return self._voice_id.startswith("google")

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
        assert 0.0 <= volume <= 1.0, "Volume must be between 0.0 and 1.0"
        self._volume = volume
        self._engine.setProperty("volume", volume)

    def rate(self):
        return self._rate_modifier

    def setRate(self, rate):
        assert 0.25 <= rate <= 4.0, "Rate must be between 0.25 and 4.0"
        self._rate_modifier = rate
        self._engine.setProperty("rate", rate * self._base_rate)

    def say(self, text):
        # Refuse playback while there's an active playback.
        if self._playing:
            return
        self._playing = True
        if self.googleTtsIsActive():
            synthesis_input = texttospeech.SynthesisInput(text=text)
            language = {
                "google-english": "en-GB",
                "google-german": "de-DE",
            }.get(self._voice_id, "de-DE")
            voice = texttospeech.VoiceSelectionParams(
                language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate=self._rate_modifier,
                volume_gain_db=(1.0 - self._volume) * -96,
            )
            response = self._google_tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            self._play_buffer = simpleaudio.play_buffer(
                response.audio_content, 1, 2, 24000
            ).wait_done()
            self._play_buffer = None
        else:
            with tempfile.TemporaryDirectory() as tmpdirname:
                ttsfile = os.path.join(tmpdirname, "tts.wav")
                self._engine.save_to_file(text, ttsfile)
                self._engine.runAndWait()
                simpleaudio.WaveObject.from_wave_file(ttsfile).play().wait_done()
        self._playing = False

    def cancel(self):
        if self.googleTtsIsActive():
            if self._play_buffer is not None:
                self._play_buffer.stop()
                self._play_buffer = None
        else:
            self._engine.stop()
        self._playing = False
