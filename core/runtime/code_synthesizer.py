class CodeSynthesizer:
    """
    Generates starter implementation code
    for approved upgrade plans.
    """

    def synthesize(self, plan):

        generated = {}

        title = plan.get("title", "")

        if "Speech" in title:

            generated[
                "core/runtime/speech/recognizer.py"
            ] = self._speech_recognizer()

            generated[
                "core/runtime/speech/audio_input.py"
            ] = self._audio_input()

            generated[
                "core/runtime/speech/__init__.py"
            ] = "# speech runtime\n"

        elif "Conversation" in title:

            generated[
                "core/runtime/conversation/session.py"
            ] = self._conversation_session()

            generated[
                "core/runtime/conversation/router.py"
            ] = self._conversation_router()

        return generated

    def _speech_recognizer(self):

        return '''
class SpeechRecognizer:

    def transcribe(self, audio):

        return "transcribed text"
'''

    def _audio_input(self):

        return '''
class AudioInput:

    def capture(self):

        return b""
'''

    def _conversation_session(self):

        return '''
class ConversationSession:

    def start(self):

        return True
'''

    def _conversation_router(self):

        return '''
class ConversationRouter:

    def route(self, message):

        return message
'''