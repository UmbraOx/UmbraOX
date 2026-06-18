class ImplementationPlanner:
    """
    Converts approved proposals into
    executable implementation plans.
    """

    def build_plan(self, proposal):

        title = proposal.get("title", "")
        target = proposal.get("target", "")

        steps = []

        if "Speech" in title:

            steps = [
                "Create speech runtime package",
                "Add microphone input manager",
                "Add speech recognition engine",
                "Add realtime transcription pipeline",
                "Connect speech output to boss agent",
            ]

        elif "Audio" in title:

            steps = [
                "Create audio subsystem",
                "Add audio device manager",
                "Add streaming audio pipeline",
                "Add runtime audio validation",
            ]

        elif "Conversation" in title:

            steps = [
                "Create conversation runtime",
                "Add realtime session manager",
                "Add interruption handling",
                "Add multi-agent message routing",
            ]

        else:

            steps = [
                "Analyze subsystem",
                "Create implementation files",
                "Validate architecture",
                "Prepare runtime integration",
            ]

        return {
            "title": title,
            "target": target,
            "steps": steps,
        }