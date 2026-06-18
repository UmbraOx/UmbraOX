import speech_recognition as sr

class RuntimeContinuousMicListener:
    def __init__(self, **kwargs):
        self.ready = True
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        except Exception as e:
            print(f"Error initializing microphone listener: {e}")
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def run(self, prompt: str) -> dict:
        if not self.ready:
            return {"error": "Microphone listener is not available"}

        with self.microphone as source:
            print(f"Listening for {prompt}...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            return {"transcript": text}
        except sr.UnknownValueError:
            return {"error": "Google Speech Recognition could not understand audio"}
        except sr.RequestError as e:
            return {"error": f"Could not request results from Google Speech Recognition service; {e}"}