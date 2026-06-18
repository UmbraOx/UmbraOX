class UmbraUnifiedGenerationRouter:
    """
    Single entry point for ALL generation requests:

    - images
    - sprites
    - games
    - audio
    - video
    - UI apps
    - assets

    This ensures Umbra does NOT drift into fragmented pipelines.
    """

    def __init__(self, agent_mesh, llm_orchestrator, logger=None):

        self.agent_mesh = agent_mesh
        self.llm = llm_orchestrator
        self.logger = logger

    # -----------------------------
    # ROUTE REQUEST
    # -----------------------------

    def route(self, request: dict):

        task_type = request.get("type")

        if task_type == "image":
            return self._route_image(request)

        if task_type == "sprite":
            return self._route_sprite(request)

        if task_type == "game":
            return self._route_game(request)

        if task_type == "audio":
            return self._route_audio(request)

        if task_type == "video":
            return self._route_video(request)

        return self._route_generic(request)

    # -----------------------------
    # IMAGE PIPELINE
    # -----------------------------

    def _route_image(self, req):
        return self.agent_mesh.dispatch({
            "domain": "vision",
            "task": req,
            "constraints": [
                "no anatomical artifacts",
                "high coherence",
                "stable diffusion style safety filters"
            ]
        })

    # -----------------------------
    # SPRITE PIPELINE (GAME READY)
    # -----------------------------

    def _route_sprite(self, req):
        return self.agent_mesh.dispatch({
            "domain": "sprite_generation",
            "task": req,
            "constraints": [
                "pixel consistency",
                "fixed palette",
                "no distortion across frames"
            ]
        })

    # -----------------------------
    # GAME PIPELINE
    # -----------------------------

    def _route_game(self, req):
        return self.agent_mesh.dispatch({
            "domain": "game_engine",
            "task": req,
            "constraints": [
                "playable loop required",
                "no placeholder geometry",
                "must include input + physics + UI layer"
            ]
        })

    # -----------------------------
    # AUDIO PIPELINE
    # -----------------------------

    def _route_audio(self, req):
        return self.agent_mesh.dispatch({
            "domain": "audio",
            "task": req,
            "constraints": [
                "clean waveform",
                "no clipping",
                "consistent tempo if music"
            ]
        })

    # -----------------------------
    # VIDEO PIPELINE
    # -----------------------------

    def _route_video(self, req):
        return self.agent_mesh.dispatch({
            "domain": "video",
            "task": req,
            "constraints": [
                "frame continuity required",
                "no flicker",
                "stable scene identity"
            ]
        })

    # -----------------------------
    # FALLBACK
    # -----------------------------

    def _route_generic(self, req):
        return self.agent_mesh.dispatch({
            "domain": "general",
            "task": req
        })