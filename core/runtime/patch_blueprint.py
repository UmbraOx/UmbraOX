class PatchBlueprint:
    """
    Defines safe execution blueprints
    before live patching occurs.
    """

    def create(self, plan):

        files = []

        target = plan.get("target", "")

        if "speech" in target:

            files.extend([
                "core/runtime/speech/__init__.py",
                "core/runtime/speech/recognizer.py",
                "core/runtime/speech/audio_input.py",
            ])

        elif "conversation" in target:

            files.extend([
                "core/runtime/conversation/session.py",
                "core/runtime/conversation/router.py",
            ])

        elif "audio" in target:

            files.extend([
                "core/audio/device_manager.py",
                "core/audio/audio_stream.py",
            ])

        return {
            "target": target,
            "files": files,
            "safe_mode": True,
            "rollback_enabled": True,
        }