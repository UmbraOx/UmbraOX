class FeatureSynthesizer:
    """
    Converts natural language requests into structured feature blueprints.
    This is the bridge between human intent and system evolution.
    """

    def synthesize(self, prompt: str) -> list:
        prompt_lower = prompt.lower()

        features = []

        # -------------------------------------------------
        # VOICE SYSTEMS
        # -------------------------------------------------
        if "voice" in prompt_lower or "speech" in prompt_lower:
            features.append({
                "feature": "voice_system",
                "components": [
                    "speech_to_text_module",
                    "text_to_speech_module",
                    "audio_stream_handler"
                ],
                "files_to_create": [
                    "core/voice/stt_engine.py",
                    "core/voice/tts_engine.py",
                    "core/voice/audio_router.py"
                ],
                "files_to_modify": [
                    "core/boss_agent.py",
                    "core/control_center/server.py"
                ],
                "risk": "high",
                "explanation": "Adds bidirectional audio interface for natural interaction."
            })

        # -------------------------------------------------
        # UI / CONTROL CENTER EXTENSIONS
        # -------------------------------------------------
        if "ui" in prompt_lower or "dashboard" in prompt_lower:
            features.append({
                "feature": "ui_extension",
                "components": [
                    "state_panel",
                    "event_stream_ui",
                    "approval_console"
                ],
                "files_to_create": [
                    "core/control_center/widgets.py"
                ],
                "files_to_modify": [
                    "core/control_center/static_dashboard.py"
                ],
                "risk": "medium",
                "explanation": "Expands control center visibility and interaction layers."
            })

        # -------------------------------------------------
        # AGENT EXPANSION
        # -------------------------------------------------
        if "agent" in prompt_lower or "multi agent" in prompt_lower:
            features.append({
                "feature": "agent_expansion",
                "components": [
                    "specialist_agent_registry",
                    "agent_router",
                    "task_dispatch_layer"
                ],
                "files_to_create": [
                    "core/agents/agent_registry.py",
                    "core/agents/task_dispatcher.py"
                ],
                "files_to_modify": [
                    "core/boss_agent.py"
                ],
                "risk": "high",
                "explanation": "Enables modular specialist agents under Boss control."
            })

        # -------------------------------------------------
        # FALLBACK
        # -------------------------------------------------
        if not features:
            features.append({
                "feature": "generic_feature",
                "components": ["analysis_required"],
                "files_to_create": [],
                "files_to_modify": [],
                "risk": "unknown",
                "explanation": "Feature not recognized — requires architectural planning phase."
            })

        return features