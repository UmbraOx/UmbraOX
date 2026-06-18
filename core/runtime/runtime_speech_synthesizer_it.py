import os

class RuntimeSpeechSynthesizerIt:
    def __init__(self, **kwargs):
        self.ready = True
        try:
            import gtts  # gTTS (Google Text-to-Speech)
        except ImportError:
            print("gtts is not installed. You can install it using 'pip install gtts'.")
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def synthesize_speech(self, text: str, output_file: str) -> dict:
        if not self.is_available():
            return {'status': 'error', 'message': 'gtts is not installed'}

        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en')
            tts.save(output_file)
            return {'status': 'ok', 'output_file': output_file}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Example usage:
# synthesizer = RuntimeSpeechSynthesizerIt()
# result = synthesizer.synthesize_speech("Hello, world!", "hello.mp3")
# print(result)