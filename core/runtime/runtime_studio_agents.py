"""
RuntimeStudioAgents — integrated AI studio agents for Umbra.
These run INSIDE Umbra automatically when needed.
No separate windows. Umbra calls them based on the project type.
"""

import os
import json
import urllib.request
from datetime import datetime


class AgentResult:

    def __init__(self, success, output, files=None, error=None):
        self.success = success
        self.output = output
        self.files = files or []
        self.error = error
        self.timestamp = datetime.now().isoformat()


class RuntimeStudioAgents:
    """
    All studio agents in one place. Umbra calls these automatically.
    Agents: character_design, world_builder, game_mechanics, npc_behavior,
            quest_generator, content_writer, overlay_app, companion_personality,
            code_reviewer, orchestrator
    """

    AGENT_DESCRIPTIONS = {
        "character_design": "Designs characters with full stats, backstory, and personality",
        "world_builder": "Creates detailed world lore, geography, factions, and history",
        "game_mechanics": "Designs gameplay systems, progression, and combat",
        "npc_behavior": "Creates NPC AI behavior trees and dialogue systems",
        "quest_generator": "Generates quests, story arcs, and branching narratives",
        "content_writer": "Writes scripts, lore texts, item descriptions, and dialogue",
        "overlay_app": "Designs desktop overlay applications and UI systems",
        "companion_personality": "Creates AI companion personalities and conversation styles",
        "code_reviewer": "Reviews and fixes code bugs automatically",
        "asset_planner": "Plans all art, audio, and data assets needed for a project",
    }

    def __init__(self, llm_provider=None, direct_generator=None, output_dir=None):
        self.llm = llm_provider
        self.direct = direct_generator
        self.output_dir = output_dir or os.path.join(os.getcwd(), "workspaces", "studio")
        os.makedirs(self.output_dir, exist_ok=True)
        self.history = []

    def _call_llm(self, prompt, max_tokens=2000):
        """Call LLM and return text response."""
        if self.llm and self.llm.is_configured():
            try:
                resp = self.llm.complete(prompt, max_tokens=max_tokens)
                if resp.success:
                    return resp.content
            except Exception:
                pass
        return None

    def _save_output(self, project_name, filename, content):
        """Save agent output to project folder."""
        if project_name:
            out_dir = os.path.join(self.output_dir, project_name.lower().replace(" ", "_"))
        else:
            out_dir = self.output_dir
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    # ------------------------------------------------------------------ #
    #  CHARACTER DESIGN                                                     #
    # ------------------------------------------------------------------ #

    def design_character(self, description, project_name=None, existing_world=None):
        """Generate a complete character profile."""
        world_context = f"\nWorld context: {existing_world}" if existing_world else ""
        prompt = (
            f"You are a game character designer. Create a complete character profile "
            f"for this character: {description}.{world_context}\n\n"
            "Return ONLY valid JSON with these exact fields:\n"
            "{\n"
            '  "name": "character name",\n'
            '  "age": 25,\n'
            '  "race": "human",\n'
            '  "class": "warrior",\n'
            '  "appearance": "detailed physical description",\n'
            '  "personality": ["trait1", "trait2", "trait3"],\n'
            '  "backstory": "full backstory paragraph",\n'
            '  "abilities": ["ability1", "ability2"],\n'
            '  "weaknesses": ["weakness1"],\n'
            '  "starting_stats": {"hp": 100, "attack": 10, "defense": 8, "speed": 6},\n'
            '  "dialogue_style": "how they speak",\n'
            '  "role": "player/npc/enemy/boss"\n'
            "}\n"
            "Output ONLY the JSON, nothing else."
        )

        response = self._call_llm(prompt, max_tokens=1000)
        if not response:
            return AgentResult(False, {}, error="LLM unavailable")

        try:
            clean = response.strip()
            if "```" in clean:
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean)
        except Exception:
            data = {"raw_output": response, "name": "Unknown"}

        files = []
        if project_name:
            char_name = data.get("name", "character").lower().replace(" ", "_")
            path = self._save_output(project_name, f"character_{char_name}.json",
                                     json.dumps(data, indent=2))
            files.append(path)

        return AgentResult(True, data, files=files)

    # ------------------------------------------------------------------ #
    #  WORLD BUILDING                                                       #
    # ------------------------------------------------------------------ #

    def build_world(self, concept, project_name=None):
        """Generate complete world lore and structure."""
        prompt = (
            f"You are a world-building expert for games. Create a detailed world based on: {concept}\n\n"
            "Return ONLY valid JSON:\n"
            "{\n"
            '  "world_name": "name",\n'
            '  "premise": "one paragraph summary",\n'
            '  "geography": {"regions": [], "landmarks": [], "climate": ""},\n'
            '  "lore": {"creation_myth": "", "major_events": [], "ancient_history": ""},\n'
            '  "factions": [{"name": "", "description": "", "alignment": "", "goals": ""}],\n'
            '  "gods_or_powers": [{"name": "", "domain": "", "description": ""}],\n'
            '  "magic_or_technology": {"system_name": "", "rules": [], "limitations": []},\n'
            '  "economy": {"currency": "", "main_trades": []},\n'
            '  "towns": [{"name": "", "description": "", "population": "", "notable_npcs": []}],\n'
            '  "threats": [{"name": "", "description": "", "danger_level": ""}]\n'
            "}\n"
            "Output ONLY the JSON."
        )

        response = self._call_llm(prompt, max_tokens=2000)
        if not response:
            return AgentResult(False, {}, error="LLM unavailable")

        try:
            clean = response.strip()
            if "```" in clean:
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean)
        except Exception:
            data = {"raw_output": response}

        files = []
        if project_name:
            path = self._save_output(project_name, "world_lore.json",
                                     json.dumps(data, indent=2))
            md_content = self._world_to_markdown(data)
            md_path = self._save_output(project_name, "world_lore.md", md_content)
            files.extend([path, md_path])

        return AgentResult(True, data, files=files)

    def _world_to_markdown(self, world):
        name = world.get("world_name", "World")
        lines = [f"# {name} — World Lore\n"]
        if "premise" in world:
            lines.append(f"## Overview\n{world['premise']}\n")
        if "lore" in world:
            lore = world["lore"]
            lines.append(f"## Creation\n{lore.get('creation_myth', '')}\n")
        if "factions" in world:
            lines.append("## Factions\n")
            for f in world["factions"]:
                lines.append(f"### {f.get('name', 'Unknown')}\n{f.get('description', '')}\n")
        if "gods_or_powers" in world:
            lines.append("## Gods & Powers\n")
            for g in world["gods_or_powers"]:
                lines.append(f"### {g.get('name', 'Unknown')} — {g.get('domain', '')}\n{g.get('description', '')}\n")
        if "towns" in world:
            lines.append("## Towns\n")
            for t in world["towns"]:
                lines.append(f"### {t.get('name', 'Unknown')}\n{t.get('description', '')}\n")
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    #  GAME MECHANICS                                                       #
    # ------------------------------------------------------------------ #

    def design_mechanics(self, concept, project_name=None):
        prompt = (
            f"You are a game designer. Design complete game mechanics for: {concept}\n\n"
            "Return ONLY valid JSON:\n"
            "{\n"
            '  "core_loop": "what the player does every session",\n'
            '  "player_stats": {"hp": 100, "mana": 50, "attack": 10, "defense": 8, "speed": 6, "level": 1, "exp": 0},\n'
            '  "combat_system": {"type": "real-time/turn-based", "actions": [], "rules": []},\n'
            '  "progression": {"level_cap": 50, "exp_curve": "linear", "stat_increases": {}},\n'
            '  "inventory": {"max_slots": 20, "item_categories": [], "equipment_slots": []},\n'
            '  "starting_options": [{"name": "", "description": "", "stats": {}}],\n'
            '  "enemies": [{"name": "", "hp": 0, "attack": 0, "behavior": "", "drops": []}],\n'
            '  "difficulty_scaling": "how enemies scale with player level"\n'
            "}\n"
            "Output ONLY the JSON."
        )

        response = self._call_llm(prompt, max_tokens=1500)
        if not response:
            return AgentResult(False, {}, error="LLM unavailable")

        try:
            clean = response.strip()
            if "```" in clean:
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean)
        except Exception:
            data = {"raw_output": response}

        files = []
        if project_name:
            path = self._save_output(project_name, "game_mechanics.json",
                                     json.dumps(data, indent=2))
            files.append(path)

        return AgentResult(True, data, files=files)

    # ------------------------------------------------------------------ #
    #  NPC BEHAVIOR                                                         #
    # ------------------------------------------------------------------ #

    def create_npc(self, npc_description, project_name=None, world_context=None):
        prompt = (
            f"Create a complete NPC behavior profile for: {npc_description}.\n"
            f"{('World context: ' + world_context) if world_context else ''}\n\n"
            "Return ONLY valid JSON:\n"
            "{\n"
            '  "name": "npc name",\n'
            '  "role": "shopkeeper/guard/quest_giver/enemy",\n'
            '  "schedule": [{"time": "morning", "activity": "", "location": ""}],\n'
            '  "dialogue": {\n'
            '    "greeting": ["line1", "line2"],\n'
            '    "quest_offer": ["line1"],\n'
            '    "trade": ["line1"],\n'
            '    "farewell": ["line1"]\n'
            '  },\n'
            '  "states": ["idle", "patrol", "hostile", "friendly"],\n'
            '  "memory": {"remembers_player": true, "tracks_reputation": true},\n'
            '  "inventory": [],\n'
            '  "faction": ""\n'
            "}\n"
            "Output ONLY the JSON."
        )

        response = self._call_llm(prompt, max_tokens=1000)
        if not response:
            return AgentResult(False, {}, error="LLM unavailable")

        try:
            clean = response.strip()
            if "```" in clean:
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean)
        except Exception:
            data = {"raw_output": response}

        files = []
        if project_name:
            npc_name = data.get("name", "npc").lower().replace(" ", "_")
            path = self._save_output(project_name, f"npc_{npc_name}.json",
                                     json.dumps(data, indent=2))
            files.append(path)

        return AgentResult(True, data, files=files)

    # ------------------------------------------------------------------ #
    #  QUEST GENERATOR                                                      #
    # ------------------------------------------------------------------ #

    def generate_quests(self, setting, project_name=None, world_context=None):
        prompt = (
            f"Create a complete quest system for a game set in: {setting}.\n"
            f"{('World context: ' + world_context) if world_context else ''}\n\n"
            "Return ONLY valid JSON:\n"
            "{\n"
            '  "main_quest": {\n'
            '    "title": "",\n'
            '    "description": "",\n'
            '    "stages": [{"stage": 1, "objective": "", "reward": ""}]\n'
            '  },\n'
            '  "side_quests": [\n'
            '    {"title": "", "giver": "", "description": "", "objective": "", "reward": ""}\n'
            '  ],\n'
            '  "world_events": [{"name": "", "trigger": "", "effect": ""}]\n'
            "}\n"
            "Output ONLY the JSON."
        )

        response = self._call_llm(prompt, max_tokens=1500)
        if not response:
            return AgentResult(False, {}, error="LLM unavailable")

        try:
            clean = response.strip()
            if "```" in clean:
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean)
        except Exception:
            data = {"raw_output": response}

        files = []
        if project_name:
            path = self._save_output(project_name, "quests.json",
                                     json.dumps(data, indent=2))
            files.append(path)

        return AgentResult(True, data, files=files)

    # ------------------------------------------------------------------ #
    #  CODE REVIEWER                                                        #
    # ------------------------------------------------------------------ #

    def review_code(self, file_path, project_name=None):
        if not os.path.exists(file_path):
            return AgentResult(False, {}, error=f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        prompt = (
            f"Review this Python code for bugs and issues:\n\n{code[:3000]}\n\n"
            "Return ONLY valid JSON:\n"
            "{\n"
            '  "overall_score": 85,\n'
            '  "bugs": [{"line": 0, "severity": "high/medium/low", "description": "", "fix": ""}],\n'
            '  "suggestions": [],\n'
            '  "fixed_code": "complete fixed Python code here"\n'
            "}\n"
            "Output ONLY the JSON."
        )

        response = self._call_llm(prompt, max_tokens=3000)
        if not response:
            return AgentResult(False, {}, error="LLM unavailable")

        try:
            clean = response.strip()
            if "```" in clean:
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean)
        except Exception:
            data = {"raw_output": response}

        files = []
        if "fixed_code" in data and data["fixed_code"]:
            fixed_path = file_path.replace(".py", "_fixed.py")
            with open(fixed_path, "w", encoding="utf-8") as f:
                f.write(data["fixed_code"])
            files.append(fixed_path)

        return AgentResult(True, data, files=files)

    # ------------------------------------------------------------------ #
    #  ORCHESTRATOR — decides which agents to run                          #
    # ------------------------------------------------------------------ #

    def orchestrate_project(self, project_description, project_name):
        """
        Given a project description, decide which agents to run and run them.
        Returns a summary of everything generated.
        """
        prompt = (
            f"A user wants to build: {project_description}\n\n"
            "Which of these agents should be run to prepare for building this project?\n"
            "Available agents: world_builder, character_design, game_mechanics, "
            "npc_behavior, quest_generator\n\n"
            "Return ONLY valid JSON:\n"
            "{\n"
            '  "project_type": "rpg/platformer/overlay/app/game/other",\n'
            '  "needs_world": true,\n'
            '  "needs_characters": true,\n'
            '  "needs_mechanics": true,\n'
            '  "needs_npcs": true,\n'
            '  "needs_quests": true,\n'
            '  "clarifying_questions": ["question1", "question2"]\n'
            "}\n"
            "Output ONLY the JSON."
        )

        response = self._call_llm(prompt, max_tokens=500)
        if not response:
            return {
                "project_type": "game",
                "needs_world": True,
                "needs_characters": True,
                "needs_mechanics": True,
                "needs_npcs": False,
                "needs_quests": False,
                "clarifying_questions": [],
            }

        try:
            clean = response.strip()
            if "```" in clean:
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean)
        except Exception:
            return {"project_type": "game", "needs_world": True,
                    "needs_characters": True, "needs_mechanics": True,
                    "needs_npcs": False, "needs_quests": False,
                    "clarifying_questions": []}

    def list_agents(self):
        return list(self.AGENT_DESCRIPTIONS.items())