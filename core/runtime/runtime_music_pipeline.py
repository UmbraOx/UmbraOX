import os
import subprocess
from threading import Thread

try:
    import pygame
except ImportError:
    pygame = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

class RuntimeMusicPipeline:
    def __init__(self, **kwargs):
        self.ready = True
        if pygame is None or pyttsx3 is None:
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def run(self, prompt: str) -> dict:
        if not self.is_available():
            return {"status": "error", "message": "Required libraries are not available"}

        # Initialize pygame mixer
        pygame.mixer.init()

        # Initialize text-to-speech engine
        tts_engine = pyttsx3.init()
        
        # Convert prompt to speech and save as a temporary file
        temp_audio_file = "temp_prompt.mp3"
        tts_engine.save_to_file(prompt, temp_audio_file)
        tts_engine.runAndWait()

        # Play the audio in a separate thread
        def play_audio():
            pygame.mixer.music.load(temp_audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
            os.remove(temp_audio_file)

        Thread(target=play_audio).start()

        return {"status": "success", "message": "Prompt processed and audio playing"}