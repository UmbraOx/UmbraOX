"""
RuntimeVoiceInput — speech to text for Umbra.
Uses SpeechRecognition + pyaudio (already installed).
Runs in a background thread, posts transcribed text to a callback.
"""

import threading
import queue
import time


class VoiceInputResult:

    def __init__(self, text, success, error=None, source="microphone"):
        self.text = text
        self.success = success
        self.error = error
        self.source = source

    def to_dict(self):
        return {
            "text": self.text,
            "success": self.success,
            "error": self.error,
            "source": self.source,
        }


class RuntimeVoiceInput:
    """
    Listens to microphone and transcribes speech to text.
    Uses Google Speech Recognition (free, no API key needed).
    Falls back to Sphinx (offline) if no internet.
    """

    def __init__(self, language="en-US", energy_threshold=300, pause_threshold=0.8):
        self.language = language
        self.energy_threshold = energy_threshold
        self.pause_threshold = pause_threshold
        self._listening = False
        self._thread = None
        self._result_queue = queue.Queue()
        self._callbacks = []
        self._sr = None
        self._available = False
        self._init_sr()

    def _init_sr(self):
        try:
            import speech_recognition as sr
            self._sr = sr
            self._available = True
        except ImportError:
            self._available = False

    def is_available(self):
        return self._available

    def listen_once(self, timeout=5, phrase_limit=15):
        """Listen for one phrase and return the result."""
        if not self._available:
            return VoiceInputResult("", False, "SpeechRecognition not installed. Run: pip install SpeechRecognition pyaudio")

        sr = self._sr
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = self.energy_threshold
        recognizer.pause_threshold = self.pause_threshold

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

            # Try Google first
            try:
                text = recognizer.recognize_google(audio, language=self.language)
                return VoiceInputResult(text, True, source="google")
            except sr.UnknownValueError:
                return VoiceInputResult("", False, "Could not understand audio")
            except sr.RequestError:
                # Offline fallback — try Sphinx
                try:
                    text = recognizer.recognize_sphinx(audio)
                    return VoiceInputResult(text, True, source="sphinx_offline")
                except Exception:
                    return VoiceInputResult("", False, "Speech recognition unavailable (no internet and Sphinx not installed)")

        except sr.WaitTimeoutError:
            return VoiceInputResult("", False, "No speech detected within timeout")
        except Exception as e:
            return VoiceInputResult("", False, str(e))

    def start_continuous(self, callback, stop_phrase="umbra stop listening"):
        """Start continuous listening in background thread."""
        if not self._available:
            return False
        self._listening = True
        self._callbacks.append(callback)

        def listen_loop():
            while self._listening:
                result = self.listen_once(timeout=5, phrase_limit=20)
                if result.success and result.text.strip():
                    if stop_phrase.lower() in result.text.lower():
                        self._listening = False
                        for cb in self._callbacks:
                            cb(VoiceInputResult("__stop__", True, source="system"))
                        break
                    for cb in self._callbacks:
                        try:
                            cb(result)
                        except Exception:
                            pass
                time.sleep(0.1)

        self._thread = threading.Thread(target=listen_loop, daemon=True)
        self._thread.start()
        return True

    def stop_continuous(self):
        self._listening = False

    def get_result(self, timeout=0.1):
        try:
            return self._result_queue.get(timeout=timeout)
        except queue.Empty:
            return None