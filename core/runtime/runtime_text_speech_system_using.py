import pyttsx3

class RuntimeTextSpeechSystemUsing:
    def __init__(self, **kwargs):
        self.ready = True
        try:
            import pyttsx3
        except ImportError:
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def run(self, prompt: str) -> dict:
        if not self.is_available():
            return {"error": "pyttsx3 is not available"}
        
        engine = pyttsx3.init()
        try:
            engine.say(prompt)
            engine.runAndWait()
            return {"status": "success", "message": "Text spoken successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}