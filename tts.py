# TTS Abstraction library.
#
# Usage example:
#
# > import tts
# > mytts = tts.TTS()
# > mytts.say('Hello, World')
#
# This file presents a public interface (`TTS`) and internal driver
# implementations.
#
# The pyttsx3 library is used for SAPI on Windows and espeak on Linux.
# A vendored copy which fixes Umlauts on cp1252 Windows setups is used.
#
# For Mac OS, there's a custom implementation using the Mac OS `say` utility.
# Pyttsx3's Mac OS support failed during testing and the developer has no Mac
# to investigate, so this alternate implementation is used.

import os
import subprocess
import sys
import tempfile

import simpleaudio


class TTSDriver:
    """Driver interface for TTS engine implementations."""

    def __init__(self):
        self._volume = 1.0
        self._rate = 1.0
        self._voice_id = ""

    def tryInit(self):
        """Initialise TTS engine and return supported voices.

        Voices are returned as a dictionary from opaque voice Id (str) to human
        readable name (str).
        """
        return {}

    def setVoice(self, voice_id):
        self._voice_id = voice_id

    def setVolume(self, volume):
        self._volume = volume

    def setRate(self, rate):
        self._rate = rate

    def voiceIdMatches(self, voice_id):
        """Check if voice Id is support by the driver."""
        return False

    def textToWav(self, text, ttsfile):
        """Convert text to audio and save it as wav file in `ttsfile`."""
        return NotImplemented


class GoogleTTS(TTSDriver):
    """TTS driver using Google Cloud TTS.

    This is optional: If the required libraries are not installed or the
    credentials file does not exist, the driver will not be used.

    Please see https://cloud.google.com/text-to-speech/docs/before-you-begin
    for how to enable TTS, create a service account, download a JSON
    authentication file and set the `GOOGLE_APPLICATION_CREDENTIALS`
    environment variable.

    voice Ids are prefixed with `google-`.
    """

    def __init__(self):
        super().__init__()
        self._google_tts_client = None
        self._texttospeech = None

    def try_init(self):
        voices = {}
        if "texttospeech" not in sys.modules:
            try:
                from google.auth import exceptions
                from google.cloud import texttospeech

                # Get reference to name, otherwise texttospeech is unknown in textToWav
                self._texttospeech = texttospeech
            except ImportError:
                return {}
        # Only add Google TTS if environment variable for authentication is set.
        try:
            self._google_tts_client = texttospeech.TextToSpeechClient()
            voices["google-english"] = "Google Englisch"
            voices["google-german"] = "Google Deutsch"
        except exceptions.DefaultCredentialsError:
            return {}

        return voices

    def voiceIdMatches(self, voice_id):
        return voice_id.startswith("google-")

    def textToWav(self, text, ttsfile):
        synthesis_input = self._texttospeech.SynthesisInput(text=text)
        language = {
            "google-english": "en-GB",
            "google-german": "de-DE",
        }.get(self._voice_id, "de-DE")
        voice = self._texttospeech.VoiceSelectionParams(
            language_code=language,
            ssml_gender=self._texttospeech.SsmlVoiceGender.FEMALE,
        )
        audio_config = self._texttospeech.AudioConfig(
            audio_encoding=self._texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=self._rate,
            volume_gain_db=(1.0 - self._volume) * -96,
        )
        response = self._google_tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(ttsfile, "wb") as outfile:
            outfile.write(response.audio_content)


class MacSayTTS(TTSDriver):
    """TTS driver using the Mac OS `say` utility.

    This is only available on the Mac OS platform.

    voice Ids are prefixed with `mac-`.
    """

    def try_init(self):
        if sys.platform != "darwin":
            return {}
        if "subprocess" not in sys.modules:
            import subprocess
        languages = ["de_", "en_"]
        proc = subprocess.run(["say", "-v", "?"], capture_output=True)
        voices = {}
        for line in proc.stdout.decode("utf-8", errors="ignore").splitlines():
            try:
                name, language, comment = line.split(maxsplit=2)
                if any(language.startswith(l) for l in languages):
                    voices[name] = language
            except ValueError:
                continue
        return {
            f"mac-{voice.lower()}": f"{voice} ({language})"
            for voice, language in voices.items()
        }

    def voiceIdMatches(self, voice_id):
        return voice_id.startswith("mac-")

    def textToWav(self, text, ttsfile):
        subprocess.run(["say", "-v", self._voice_id[4:], "-o", ttsfile, text])


class PyTTSX3TTS(TTSDriver):
    """TTS driver based on the pyttsx3 library.

    This is not used on the Mac OS platform.

    voice Ids are used as returned by the library.
    """

    def __init__(self):
        super().__init__()
        self._engine = None
        self._base_rate = 0
        self._voices = {}

    def try_init(self):
        if sys.platform == "darwin":
            return {}

        if "pyttsx3" not in sys.modules:
            import pyttsx3

        self._engine = pyttsx3.init()
        self._voices.update(
            {voice.id: voice.name for voice in self._engine.getProperty("voices")}
        )
        # Properties are set correctly, but reading after changing them doesn't
        # return updated values.
        self._volume = self._engine.getProperty("volume")
        # Rate is 0.25 - 4.0 in the TTS library, but has a start value of 200
        # here. Store the base rate to allow for scaling by TTS library rate.
        self._base_rate = self._engine.getProperty("rate")
        self._voice_id = self._engine.getProperty("voice")
        return self._voices

    def setVoice(self, voice_id):
        super().setVoice(voice_id)
        self._engine.setProperty("voice", voice_id)

    def setVolume(self, volume):
        super().setVolume(volume)
        self._engine.setProperty("volume", volume)

    def setRate(self, rate):
        super().setRate(rate)
        self._engine.setProperty("rate", rate * self._base_rate)

    def voiceIdMatches(self, voice_id):
        return voice_id in self._voices

    def textToWav(self, text, ttsfile):
        self._engine.save_to_file(text, ttsfile)
        self._engine.runAndWait()


DRIVERS = [GoogleTTS, MacSayTTS, PyTTSX3TTS]


class TTS:
    def __init__(self):
        self._drivers = []
        self._voices = {}

        # Try to initialise all potential drivers. If `try_init` returns no
        # voices, initialisation failed.
        for driver_class in DRIVERS:
            driver = driver_class()
            voices = driver.try_init()
            if voices:
                self._drivers.append(driver)
                self._voices.update(voices)

        assert self._voices, "No voices available"

        self._rate_modifier = 1.0
        self._volume = 1.0
        self._voice_id = list(self._voices.keys())[0]
        self._playing = False

    def voiceId(self):
        return self._voice_id

    def voices(self):
        return self._voices

    def setVoice(self, voice_id):
        if voice_id not in self._voices:
            print(f"Not setting unknown voice: {voice_id}. Available: {self._voices}")
            return
        self._voice_id = voice_id
        for driver in self._drivers:
            driver.setVoice(voice_id)

    def volume(self):
        return self._volume

    def setVolume(self, volume):
        if not (0.0 <= volume <= 1.0):
            print(f"Volume {volume} must be between 0.0 and 1.0, not updating.")
            return
        self._volume = volume
        for driver in self._drivers:
            driver.setVolume(volume)

    def rate(self):
        return self._rate_modifier

    def setRate(self, rate):
        if not (0.25 <= rate <= 4.0):
            print(f"Rate {rate} must be between 0.25 and 4.0, not updating.")
            return
        self._rate_modifier = rate

    def say(self, text):
        # Refuse playback while there's an active playback.
        if self._playing:
            return
        self._playing = True
        with tempfile.TemporaryDirectory() as tmpdirname:
            ttsfile = os.path.join(tmpdirname, "tts.wav")
            for driver in self._drivers:
                if driver.voiceIdMatches(self._voice_id):
                    driver.textToWav(text, ttsfile)
                    break
            simpleaudio.WaveObject.from_wave_file(ttsfile).play().wait_done()
        self._playing = False
