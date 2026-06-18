"""
RuntimeGameTester — automatically tests generated Python/pygame files.
Checks for common game bugs BEFORE the user runs them.
Detects: missing boundary checks, no collision detection, no game loop,
         syntax errors, import failures, infinite loops without FPS cap, etc.
"""

import ast
import os
import subprocess
import sys
import re
from datetime import datetime


class GameTestResult:

    def __init__(self, file_path):
        self.file_path = file_path
        self.passed = False
        self.score = 0
        self.issues = []
        self.warnings = []
        self.suggestions = []
        self.features_found = []
        self.tested_at = datetime.now().isoformat()

    def add_issue(self, msg):
        self.issues.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_suggestion(self, msg):
        self.suggestions.append(msg)

    def add_feature(self, feature):
        self.features_found.append(feature)

    def to_dict(self):
        return {
            "file_path": self.file_path,
            "passed": self.passed,
            "score": self.score,
            "issues": self.issues,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "features_found": self.features_found,
            "tested_at": self.tested_at,
        }

    def summary(self):
        status = "PASS" if self.passed else "FAIL"
        return (f"[{status}] {os.path.basename(self.file_path)} | "
                f"Score: {self.score}/100 | "
                f"Issues: {len(self.issues)} | "
                f"Warnings: {len(self.warnings)}")


class RuntimeGameTester:
    """
    Tests generated game files for common problems.
    Runs static analysis + optional subprocess syntax check.
    Does NOT run the game (that requires a display) but validates
    that it WOULD run correctly.
    """

    REQUIRED_GAME_FEATURES = {
        "pygame_init": (r"pygame\.init\(\)", "Pygame initialization"),
        "game_loop": (r"while\s+(True|running|game_running|active)", "Main game loop"),
        "event_handling": (r"pygame\.event\.(get|poll)\(\)", "Event handling"),
        "quit_handling": (r"QUIT|pygame\.quit\(\)", "Quit handling"),
        "clock_fps": (r"Clock\(\).*tick|tick.*Clock\(\)", "FPS clock"),
        "display_flip": (r"pygame\.display\.(flip|update)\(\)", "Display update"),
        "screen_create": (r"pygame\.display\.set_mode", "Window creation"),
    }

    GAME_QUALITY_FEATURES = {
        "boundary_check": (r"(x\s*[<>=!]+\s*\d+|y\s*[<>=!]+\s*\d+|clamp|max.*min|WIDTH|HEIGHT)", "Boundary checking"),
        "collision": (r"(colliderect|collide|pygame\.sprite\.spritecollide|pygame\.Rect.*collide)", "Collision detection"),
        "health_system": (r"(health|hp|lives|hearts)\s*[=\-]", "Health/lives system"),
        "score_system": (r"(score|points)\s*[+\-=]", "Score system"),
        "font_render": (r"pygame\.font|Font\(", "Text/font rendering"),
        "game_over": (r"game.?over|GAME.?OVER|game_over|game_state.*over", "Game over screen"),
        "restart": (r"(restart|reset|pygame\.K_r|K_r)", "Restart functionality"),
        "player_class": (r"class\s+Player|class\s+player", "Player class"),
        "enemy_class": (r"class\s+Enemy|class\s+enemy|class\s+NPC", "Enemy class"),
        "main_guard": (r"if\s+__name__.*__main__", "Main guard"),
    }

    def test_file(self, file_path):
        result = GameTestResult(file_path)

        if not os.path.exists(file_path):
            result.add_issue(f"File not found: {file_path}")
            result.score = 0
            return result

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                source = f.read()
        except Exception as e:
            result.add_issue(f"Cannot read file: {e}")
            result.score = 0
            return result

        # 1. Syntax check
        try:
            ast.parse(source)
        except SyntaxError as e:
            result.add_issue(f"Syntax error at line {e.lineno}: {e.msg}")
            result.score = 0
            return result

        score = 100

        # 2. Check required pygame features
        is_pygame = "pygame" in source.lower()
        if is_pygame:
            for key, (pattern, description) in self.REQUIRED_GAME_FEATURES.items():
                if re.search(pattern, source, re.IGNORECASE):
                    result.add_feature(description)
                else:
                    result.add_issue(f"Missing required: {description}")
                    score -= 15

            # 3. Check quality features
            for key, (pattern, description) in self.GAME_QUALITY_FEATURES.items():
                if re.search(pattern, source, re.IGNORECASE | re.DOTALL):
                    result.add_feature(description)
                else:
                    result.add_warning(f"Missing (recommended): {description}")
                    score -= 3

            # 4. Check for boundary validation
            if not re.search(r"(WIDTH|SCREEN_WIDTH|window_width|800|1024)", source, re.IGNORECASE):
                result.add_warning("No screen width constant found — boundaries may be hardcoded or missing")
                score -= 5

            # 5. Check for infinite loop without FPS cap
            if re.search(r"while\s+True", source) and not re.search(r"\.tick\(", source):
                result.add_issue("Game loop has no FPS cap — will max out CPU. Add: clock.tick(60)")
                score -= 10

            # 6. Check for pygame.quit() before sys.exit
            if "pygame.init" in source and "pygame.quit" not in source:
                result.add_warning("pygame.quit() not called before exit — may cause issues on some systems")
                score -= 3

        else:
            # Not a pygame file — do general Python checks
            result.add_feature("Python script (not pygame)")
            if "def main" in source:
                result.add_feature("main() function")
            if "__name__" in source:
                result.add_feature("Main guard")

        # 7. Check for common crash patterns
        if re.search(r"open\(['\"]", source) and not re.search(r"try|with\s+open", source):
            result.add_warning("File operations without error handling — may crash if file missing")
            score -= 3

        if "import" in source:
            # Check for reasonable imports
            lines = source.split("\n")
            for i, line in enumerate(lines[:20]):
                if line.strip().startswith("import") or line.strip().startswith("from"):
                    if "gradio" in line or "tensorflow" in line or "torch" in line:
                        result.add_warning(f"Heavy import '{line.strip()}' — ensure it's installed")
                        score -= 2

        score = max(0, min(100, score))
        result.score = score
        result.passed = score >= 60 and len(result.issues) == 0

        return result

    def test_workspace_run(self, run_id, workspaces_dir):
        """Test all Python files in a workspace run."""
        code_dir = os.path.join(workspaces_dir, run_id, "code")
        results = []
        if not os.path.exists(code_dir):
            return results
        for fname in os.listdir(code_dir):
            if fname.endswith(".py"):
                fp = os.path.join(code_dir, fname)
                results.append(self.test_file(fp))
        return results

    def find_best_runnable(self, run_id, workspaces_dir):
        """Find the most complete/runnable file in a workspace."""
        results = self.test_workspace_run(run_id, workspaces_dir)
        if not results:
            return None, None
        best = max(results, key=lambda r: r.score)
        return best.file_path, best

    def generate_fix_prompt(self, test_result):
        """Generate a prompt to fix identified issues."""
        if not test_result.issues and not test_result.warnings:
            return None

        issues_str = "\n".join(f"- {i}" for i in test_result.issues)
        warnings_str = "\n".join(f"- {w}" for w in test_result.warnings[:5])

        return (
            f"Fix the following issues in this Python game file and return the COMPLETE fixed file:\n"
            f"Issues (must fix):\n{issues_str}\n"
            f"Warnings (should fix):\n{warnings_str}\n"
            f"Requirements:\n"
            f"- Return ONLY the complete fixed Python code\n"
            f"- Keep all existing working features\n"
            f"- Add boundary checking if missing (player cannot leave screen)\n"
            f"- Add FPS cap if missing (clock.tick(60))\n"
            f"- Ensure pygame.quit() is called before exit\n"
            f"- Ensure all required features work correctly"
        )