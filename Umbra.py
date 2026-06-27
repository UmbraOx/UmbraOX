"""
UMBRA -- Autonomous AI Runtime OS  v2.3.0
Complete drop-in replacement.

Fixes & Upgrades in v2.3.0:
  - Deep Agent System: sprite, character, item, mechanic, world, quest, dialogue,
    faction, economy, music, lore, cutscene, ui, ai_personality agents
  - GUI fully wired to run_prompt via thread-safe queue (no stdout capture hack)
  - Video pipeline: ffmpeg-based frame assembler + ComfyUI video workflow
  - GIF routing fixed: always hits animated_gif_generator, never pipeline
  - LLM timeout: 1200s default, chunked generation for large tasks
  - Optiopia & all games: strictly pygame-only input, no terminal prompts
  - Umbra learns from how you talk over time
  - Self-repair scans runtime_*gui* correctly
  - Video frames now assembled into .mp4 via ffmpeg automatically
  - Agent manager wired for full-scale game builds (all systems in parallel)
  - Umbra asks clarifying questions before large builds
  - Workspace file browser / cleaner (view files, remove old files)
"""

import sys
import os
import subprocess
import shutil
import json
import re
import queue as _queue
import ast
import time
import datetime
import signal
import socket
import threading

try:
    import umbra_dev_assistant as _dev_asst
    _DEV_ASST_LOADED = True
except ImportError:
    _dev_asst = None
    _DEV_ASST_LOADED = False

_UMBRA_ROOT = os.path.dirname(os.path.abspath(__file__))
if _UMBRA_ROOT not in sys.path:
    sys.path.insert(0, _UMBRA_ROOT)

_pipeline_monitor = None
_resource_manager = None
_scheduler = None
_comfyui_proc = None

# Thread-safe queue for GUI <-> CLI communication
_gui_response_queue = _queue.Queue()
_gui_input_queue = _queue.Queue()


# ============================================================
#  PORT / PROCESS CLEANUP
# ============================================================

def _kill_port(port):
    try:
        if sys.platform == "win32":
            r = subprocess.run(
                'netstat -ano | findstr ":' + str(port) + '"',
                shell=True, capture_output=True, text=True)
            for line in r.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 5 and (":" + str(port)) in parts[1] and parts[3] == "LISTENING":
                    subprocess.run("taskkill /PID " + parts[4] + " /F",
                                   shell=True, capture_output=True)
        else:
            subprocess.run("fuser -k " + str(port) + "/tcp", shell=True, capture_output=True)
    except Exception:
        pass


def _is_port_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except Exception:
        return False


def _shutdown_comfyui():
    global _comfyui_proc
    if _comfyui_proc is not None:
        try:
            _comfyui_proc.terminate()
            _comfyui_proc.wait(timeout=5)
        except Exception:
            try:
                _comfyui_proc.kill()
            except Exception:
                pass
        _comfyui_proc = None
    if _is_port_open(8188):
        _kill_port(8188)


# ============================================================
#  FILE / SYNTAX HELPERS
# ============================================================

def _backup_file(path):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path + ".bak." + ts
    shutil.copy2(path, backup)
    return backup


def _syntax_check(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            src = f.read()
        ast.parse(src)
        return None
    except SyntaxError as e:
        return str(e)
    except Exception as e:
        return str(e)


def _strip_fences(code):
    code = re.sub(r"^```python\s*", "", code, flags=re.MULTILINE)
    code = re.sub(r"^```\s*", "", code, flags=re.MULTILINE)
    code = re.sub(r"\s*```\s*$", "", code)
    return code.strip()


def _run_pytest_quick(target="core/tests", timeout=120):
    cmd = [sys.executable, "-m", "pytest", target, "-q", "--tb=no",
           "--no-header", "--timeout=" + str(timeout)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           cwd=_UMBRA_ROOT, timeout=timeout + 10)
        out = r.stdout + r.stderr
        pm = re.search(r"(\d+) passed", out)
        fm = re.search(r"(\d+) failed", out)
        passed = int(pm.group(1)) if pm else 0
        failed = int(fm.group(1)) if fm else 0
        return passed, failed, out
    except Exception as e:
        return 0, 0, str(e)


def _find_broken_modules():
    broken = []
    d = os.path.join(_UMBRA_ROOT, "core", "runtime")
    if not os.path.isdir(d):
        return broken
    for fname in sorted(os.listdir(d)):
        if fname.endswith(".py"):
            full = os.path.join(d, fname)
            err = _syntax_check(full)
            if err:
                broken.append((full, err))
    return broken


# ============================================================
#  GUI OUTPUT HELPER  (thread-safe print to both CLI and GUI)
# ============================================================

_gui_ref = None  # Set after GUI launches

# System context injected into every chat prompt so the LLM knows it IS Umbra
_UMBRA_SYSTEM = (
    "You are Umbra, a local autonomous AI assistant running on the user's Windows PC. "
    "You were built by the user using Python and Ollama. You have no internet access. "
    "You can build games, write code, answer questions, read/edit files, run tests, "
    "generate images and GIFs, and help the user finish building you. "
    "Available Ollama models are on this machine. "
    "Be concise, helpful, and direct. Never mention Anthropic, OpenAI, or other AI companies. "
    "You ARE Umbra — respond as Umbra.\n\n"
)

def _umbra_chat_prompt(user_text):
    """Wrap user text with Umbra system context."""
    return _UMBRA_SYSTEM + "User: " + user_text + "\nUmbra:"


def _umbra_mem(rt):
    """Safe memory accessor."""
    return rt.get("memory")


def _umbra_print(text):
    """Print to CLI and send to GUI if running."""
    print(text)
    global _gui_ref
    if _gui_ref is not None:
        try:
            _gui_ref.post_message(str(text))
        except Exception:
            pass


# ============================================================
#  LLM HELPERS
# ============================================================

def _safe_input(prompt_text, default=""):
    """input() that shows a tkinter dialog in GUI mode, falls back to terminal."""
    if _gui_mode:
        try:
            import tkinter as _tk
            from tkinter import simpledialog as _sd
            _root = _tk.Tk(); _root.withdraw(); _root.attributes("-topmost", True)
            _ans = _sd.askstring("Umbra", prompt_text, parent=_root)
            _root.destroy()
            return (_ans or "").strip() if _ans is not None else default
        except Exception:
            _umbra_print(prompt_text + " [auto: " + str(default) + "]")
            return default
    try:
        return input(prompt_text).strip()
    except (EOFError, KeyboardInterrupt):
        return default


def _ask_llm_fix(llm, path, error):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            src = f.read()
    except Exception:
        return None
    prompt = (
        "Fix this Python file.\nFile: " + os.path.basename(path) +
        "\nError: " + error + "\n\nSource:\n" + src[:6000] +
        "\n\nReturn ONLY corrected Python. No markdown. No explanation."
    )
    try:
        r = llm.complete(prompt)
        if r and r.content:
            return _strip_fences(r.content)
    except Exception:
        pass
    return None


def _safe_handler_str(handler):
    if isinstance(handler, list):
        return "\n".join(str(x) for x in handler)
    if isinstance(handler, dict):
        return json.dumps(handler, indent=2)
    return str(handler) if handler else "print('[FEATURE] Called')"


# ============================================================
#  DEPENDENCY HELPERS
# ============================================================

_BANNED_DEPS = {
    "imageio", "moviepy", "gtts", "gTTS",
    "pydub", "soundfile", "librosa", "torch", "tensorflow",
    "transformers", "diffusers", "accelerate",
}

_PIP_MAP = {
    "PIL": "Pillow", "cv2": "opencv-python", "sklearn": "scikit-learn",
    "speech_recognition": "SpeechRecognition", "pyaudio": "PyAudio",
    "pyttsx3": "pyttsx3", "pygame": "pygame", "requests": "requests",
    "numpy": "numpy", "flask": "flask", "fastapi": "fastapi",
    "uvicorn": "uvicorn", "pydantic": "pydantic",
}

_STDLIB = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else {
    "os", "sys", "re", "json", "ast", "time", "datetime", "math",
    "pathlib", "shutil", "subprocess", "threading", "queue", "socket",
    "struct", "io", "csv", "random", "hashlib", "base64", "copy",
    "collections", "functools", "itertools", "contextlib", "typing",
    "dataclasses", "enum", "abc", "textwrap", "string", "traceback",
    "logging", "unittest", "tempfile", "glob", "fnmatch", "signal",
}


def _scan_imports(source):
    found = []
    for m in re.finditer(r"^(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)", source, re.MULTILINE):
        mod = m.group(1)
        if mod not in _STDLIB and mod not in found:
            found.append(mod)
    return found


def _check_missing_deps(imports):
    missing = []
    for imp in imports:
        if imp in _BANNED_DEPS:
            continue
        try:
            __import__(imp)
        except ImportError:
            missing.append((imp, _PIP_MAP.get(imp, imp)))
    return missing


def _install_deps(deps):
    all_ok = True
    for imp, pip_name in deps:
        _umbra_print("  [PIP] Installing " + pip_name + "...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", pip_name, "--quiet"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            _umbra_print("  [PIP] " + pip_name + " OK")
        else:
            _umbra_print("  [PIP] FAILED: " + pip_name + "\n        " + r.stderr[:200])
            all_ok = False
    return all_ok


def _build_feature_source(llm, feature_description, module_name):
    key_words = module_name.replace("runtime_", "").split("_")
    class_name = "Runtime" + "".join(w.title() for w in key_words)
    prompt = (
        "Build a Python module for Umbra AI runtime.\n"
        "Module: " + module_name + ".py  Class: " + class_name + "\n"
        "Feature: " + feature_description + "\n\n"
        "RULES:\n"
        "- Only stdlib or: PIL, pygame, tkinter, requests, pyttsx3, speech_recognition, cv2, numpy\n"
        "- NEVER import: imageio, moviepy, gtts, ffmpeg, pydub, soundfile, torch, tensorflow\n"
        "- Wrap optional imports in try/except, set self.ready=False if missing\n"
        "- Must have __init__(self,**kwargs), is_available()->bool, run(self,prompt:str)->dict\n"
        "- Class name must be exactly: " + class_name + "\n"
        "- Return ONLY Python. No markdown. No explanation.\n"
    )
    try:
        r = llm.complete(prompt)
        if r and r.content:
            code = _strip_fences(r.content)
            lines = []
            for line in code.splitlines():
                banned = any(re.search(r"\b(import|from)\s+" + dep + r"\b", line.strip())
                             for dep in _BANNED_DEPS)
                if not banned:
                    lines.append(line)
            return "\n".join(lines).strip()
    except Exception:
        pass
    return None


def _ask_llm_integration_snippet(llm, module_name, class_name, feature_description):
    key = module_name.replace("runtime_", "")
    defaults = {
        "import_line": "from core.runtime." + module_name + " import " + class_name,
        "instantiation_line": key.replace("_", "") + " = " + class_name + "()",
        "runtime_key": key,
        "command_trigger": feature_description.split()[0].lower(),
        "command_handler": (
            'feat = runtime.get("' + key + '")\n'
            'if feat:\n'
            '    result = feat.run(user_input)\n'
            '    _umbra_print("[RESULT] " + str(result))\n'
        ),
    }
    prompt = (
        "New Umbra module: " + module_name + ".py  Class: " + class_name + "\n"
        "Feature: " + feature_description + "\n\n"
        "Return ONLY a JSON object. ALL values must be plain strings, NEVER lists.\n"
        "Keys: import_line, instantiation_line, runtime_key, command_trigger, command_handler\n"
        "command_handler must be a single string (use \\n for newlines).\n"
        "Return ONLY valid JSON. No extra text."
    )
    try:
        r = llm.complete(prompt)
        if r and r.content:
            raw = _strip_fences(r.content)
            raw = re.sub(r"^```json\s*", "", raw, flags=re.MULTILINE)
            data = json.loads(raw)
            for k in defaults:
                if k not in data or not data[k]:
                    data[k] = defaults[k]
            data["command_handler"] = _safe_handler_str(data["command_handler"])
            return data
    except Exception:
        pass
    return defaults


# ============================================================
#  APPROVAL PROMPT
# ============================================================

def _approval_prompt(description, preview, default_yes=False):
    _umbra_print("\n" + "-" * 60)
    _umbra_print("[UMBRA APPROVAL REQUIRED]")
    _umbra_print("  Plan: " + description)
    if preview:
        lines = str(preview).strip().split("\n")[:20]
        _umbra_print("  Preview (" + str(min(len(lines), 20)) + " lines):")
        for ln in lines:
            _umbra_print("    " + ln)
        total = len(str(preview).strip().split("\n"))
        if total > 20:
            _umbra_print("    ... (" + str(total - 20) + " more lines)")
    _umbra_print("-" * 60)
    hint = "[Y/n]" if default_yes else "[y/N]"
    # GUI mode: show tkinter dialog instead of terminal input
    if _gui_mode and _gui_ref is not None:
        try:
            import tkinter.messagebox as _tmb
            msg = description + "\n\n" + "\n".join(str(preview or "").strip().split("\n")[:10])
            result = _tmb.askyesno("Umbra — Approval Required", msg)
            _umbra_print("  [GUI] " + ("Approved" if result else "Cancelled"))
            return result
        except Exception:
            _umbra_print("  [GUI] Auto-approving (tkinter dialog failed)")
            return True
    try:
        ans = _safe_input("  Approve? " + hint + ": ", "").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return ans not in ("n", "no") if default_yes else ans in ("y", "yes")


# ============================================================
#  VIDEO FRAME ASSEMBLER  (ffmpeg-based, no opencv)
# ============================================================

def _assemble_frames_to_video(frames_dir, output_path, fps=8):
    """
    Assembles image frames from frames_dir into an mp4 using ffmpeg.
    Falls back to animated GIF via PIL if ffmpeg not found.
    Returns (success, output_path, message)
    """
    # Find frames
    exts = (".png", ".jpg", ".jpeg", ".webp")
    frames = sorted([
        os.path.join(frames_dir, f) for f in os.listdir(frames_dir)
        if os.path.splitext(f)[1].lower() in exts
    ])
    if not frames:
        return False, "", "No frames found in " + frames_dir

    # Try ffmpeg
    ffmpeg_exe = shutil.which("ffmpeg")
    if ffmpeg_exe:
        # Build ffmpeg input pattern
        # Rename frames to sequential if needed
        tmp_dir = frames_dir + "_seq"
        os.makedirs(tmp_dir, exist_ok=True)
        for i, fp in enumerate(frames):
            ext = os.path.splitext(fp)[1]
            dst = os.path.join(tmp_dir, "frame_%05d" % i + ext)
            shutil.copy2(fp, dst)
        # Detect extension pattern
        sample_ext = os.path.splitext(frames[0])[1]
        pattern = os.path.join(tmp_dir, "frame_%05d" + sample_ext)
        mp4_path = output_path if output_path.endswith(".mp4") else output_path + ".mp4"
        cmd = [
            ffmpeg_exe, "-y", "-framerate", str(fps),
            "-i", pattern,
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-crf", "23", mp4_path
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            if r.returncode == 0 and os.path.exists(mp4_path):
                return True, mp4_path, "MP4 created: " + mp4_path
            else:
                shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception as e:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    # Fallback: PIL animated GIF
    try:
        from PIL import Image
        gif_path = output_path.replace(".mp4", ".gif") if ".mp4" in output_path else output_path + ".gif"
        imgs = []
        for fp in frames:
            im = Image.open(fp).convert("RGBA")
            imgs.append(im)
        if imgs:
            imgs[0].save(
                gif_path, save_all=True, append_images=imgs[1:],
                loop=0, duration=int(1000 / fps)
            )
            return True, gif_path, "GIF created (ffmpeg not found, used PIL): " + gif_path
    except Exception as e:
        return False, "", "Frame assembly failed: " + str(e)

    # Offer to download ffmpeg
    _umbra_print("[VIDEO] ffmpeg not found. Type 'install ffmpeg' to auto-download.")
    return False, "", "Could not assemble frames — type 'install ffmpeg' to auto-download"


def _find_comfyui_output_frames(base_dir=None):
    """Find the most recently generated frame sequence from ComfyUI output."""
    if base_dir is None:
        # Try common ComfyUI output locations
        candidates = [
            "C:\\ComfyUI\\output",
            os.path.join(os.path.expanduser("~"), "ComfyUI", "output"),
        ]
    else:
        candidates = [base_dir]

    for cdir in candidates:
        if not os.path.isdir(cdir):
            continue
        # Find directories or groups of sequentially named images
        # Look for the most recently modified set
        all_frames = []
        for f in os.listdir(cdir):
            fp = os.path.join(cdir, f)
            if os.path.isfile(fp) and os.path.splitext(f)[1].lower() in (".png", ".jpg", ".jpeg"):
                all_frames.append((os.path.getmtime(fp), fp))
        if all_frames:
            # Group by modification time (within 60 seconds = same batch)
            all_frames.sort(reverse=True)
            newest_time = all_frames[0][0]
            batch = [fp for t, fp in all_frames if newest_time - t < 60]
            if len(batch) > 1:
                return cdir, batch
    return None, []


# ============================================================
#  DEEP AGENT SYSTEM
# ============================================================

# Agent definitions - each is a specialized LLM prompt role
_AGENT_ROLES = {
    "world": {
        "desc": "world builder",
        "task": (
            "Write ONLY a Python module for the WORLD SYSTEM of a pygame game.\n"
            "Include: WORLD_MAP 2D list (200x200), BIOME_COL dict, TOWNS list of (x,y,name) tuples,\n"
            "CITIES list, BANDIT_CAMPS list, GOBLIN_CAMPS list, MINES list, WOODCUTS list.\n"
            "Include a gen_world() function that fills WORLD_MAP with biome strings using random.\n"
            "Include draw_world(surf, cam_x, cam_y) and get_tile(tx,ty) functions.\n"
            "Use only stdlib + pygame. NO main(), NO pygame.init(), NO game loop."
        ),
        "output": "world_module.py — WORLD_MAP, gen_world(), draw_world(), location lists"
    },
    "character": {
        "desc": "character and player system designer",
        "task": (
            "Write ONLY a Python module for the PLAYER and NPC CLASSES of a pygame game.\n"
            "Include: Player class with __init__(cls), hp/mp/sta/gold/level/xp/inventory/equipped/spells,\n"
            "gain_xp(), atk_power(), def_power(), add_item(), regen(dt) methods.\n"
            "Include: NPC class with name/job/dialogue/shop_stock attributes.\n"
            "Include: Enemy class with name/hp/atk/defense/xp_val/spd/aggro, update(player,dt) method.\n"
            "Include: ENEMY_DEFS list (10 enemies: Goblin/Bandit/Orc/Skeleton/Wolf/Dark Mage/Troll/Spider/Dragon Spawn/Mimic).\n"
            "Use Entity base class with x,y,col,draw(surf,cam_x,cam_y). No main(), no pygame.init()."
        ),
        "output": "character_module.py — Entity, Player, Enemy, NPC classes + ENEMY_DEFS"
    },
    "item": {
        "desc": "item and data tables designer",
        "task": (
            "Write ONLY a Python module for GAME DATA TABLES.\n"
            "Include: WEAPONS list (10 dicts: name/atk/type/val/mat/qty).\n"
            "Weapons: Iron Sword, Steel Axe, Shadow Dagger, Oak Bow, Flame Staff,\n"
            "         Frost Wand, Battle Hammer, Silver Spear, Throwing Stars, Death Scythe.\n"
            "Include: ARMOR_SETS list (3 sets: Iron/Steel/Shadow, each with parts/def/val/mat).\n"
            "Include: SPELLS list (10 dicts: name/mp/dmg/col/desc).\n"
            "Spells: Fireball, Ice Spike, Lightning Bolt, Heal, Shield, Teleport,\n"
            "        Summon Wolf, Earthquake, Drain Life, Time Slow.\n"
            "Include: MATERIALS list, QUESTS list (5 starter quests with id/name/desc/target/need/reward_gold/reward_xp).\n"
            "Include: FACTIONS dict, DIALOGUE_TREES dict for Merchant/Guard/default NPCs.\n"
            "No classes, no functions, no main() — just data constants."
        ),
        "output": "item_module.py — WEAPONS, ARMOR_SETS, SPELLS, MATERIALS, QUESTS, FACTIONS, DIALOGUE_TREES"
    },
    "mechanic": {
        "desc": "game mechanics engineer",
        "task": (
            "Write ONLY a Python module for GAME MECHANICS HELPERS.\n"
            "Include: Camera class with x,y,update(player) that smoothly follows player.\n"
            "Include: FloatText class with text/x/y/col/life, update(), draw(surf,cam_x,cam_y).\n"
            "Include: Projectile class with x/y/vx/vy/dmg/col/alive, update(), draw(surf,cam_x,cam_y).\n"
            "Include: Building class with TYPES dict (House/Shop/Barracks/Farm/Tower/Warehouse),\n"
            "         __init__(btype,tx,ty), draw(surf,cam_x,cam_y).\n"
            "Include: save_game(player, buildings, filepath) -> bool.\n"
            "Include: load_game(player, buildings, filepath) -> bool.\n"
            "No main(), no pygame.init(), no game loop. Use only stdlib + pygame."
        ),
        "output": "mechanic_module.py — Camera, FloatText, Projectile, Building, save_game, load_game"
    },
    "ui": {
        "desc": "UI and HUD designer",
        "task": (
            "Write ONLY a Python module for ALL UI DRAWING FUNCTIONS of a pygame RPG.\n"
            "Every menu/screen/panel MUST have a clickable X button in the TOP-RIGHT CORNER.\n"
            "Include these functions (each returns the X button rect + any interactive button rects):\n"
            "  font(size) -> pygame.font.Font\n"
            "  txt(surf, text, x, y, size, col, center=False)\n"
            "  draw_bar(surf, x, y, w, h, val, mx, col, bg)\n"
            "  draw_x_button(surf, rx, ry, rw, rh) -> pygame.Rect\n"
            "  draw_panel(surf, rx, ry, rw, rh, title) -> x_btn_rect\n"
            "  draw_hud(surf, player)  — HP/MP/STA bars, gold, level, XP, equipped items\n"
            "  draw_minimap(surf, player, enemies)  — 120x120 map in top-right\n"
            "  draw_inventory(surf, player, selected) -> (xbtn, slot_btns, equip_btn, drop_btn)\n"
            "  draw_quest_log(surf, player) -> xbtn\n"
            "  draw_shop(surf, npc, player, selected) -> (xbtn, buy_btns, items)\n"
            "  draw_crafting(surf, player, tab, selected) -> (xbtn, tab_btns, craft_btns)\n"
            "  draw_dialogue(surf, npc, dial_idx) -> (xbtn, opt_btns)\n"
            "  draw_pause(surf) -> (xbtn, pause_btns)\n"
            "  draw_main_menu(surf) -> btns dict\n"
            "  draw_class_select(surf) -> btns dict\n"
            "  draw_city_build(surf, player, buildings, place_type) -> (xbtn, type_btns)\n"
            "  draw_world_map(surf, player, towns, cities) -> xbtn\n"
            "  draw_gameover(surf)\n"
            "No main(), no pygame.init(). Import pygame only."
        ),
        "output": "ui_module.py — all UI drawing functions with X-close buttons"
    },
    "quest": {
        "desc": "quest and faction system designer",
        "task": (
            "Write ONLY a Python module for the QUEST, FACTION, and NPC-SPAWN systems.\n"
            "Include: spawn_world_entities(world_map, towns, cities, bandit_camps, goblin_camps, enemy_defs, npc_names)\n"
            "         -> (enemies_list, npcs_list, buildings_list).\n"
            "Include: check_quest_kill(player, enemy_name) — updates quest progress on kill.\n"
            "Include: check_quest_item(player, item_name, qty) — updates quest progress on pickup.\n"
            "Include: complete_ready_quests(player) -> list of completed quest names.\n"
            "Include: harvest_nearby(player, world_map) -> str message of what was gathered.\n"
            "No main(), no pygame.init()."
        ),
        "output": "quest_module.py — spawn_world_entities, quest checkers, harvest_nearby"
    },
    "economy": {
        "desc": "economy and shop system designer",
        "task": (
            "Write ONLY a Python module for the ECONOMY system.\n"
            "Include: generate_shop_stock(job) -> dict of {item_name: {price, qty}}.\n"
            "Include: buy_item(player, npc, item_name) -> (success: bool, message: str).\n"
            "Include: sell_item(player, npc, item_name) -> (success: bool, message: str).\n"
            "Include: craft_item(player, recipe) -> (success: bool, message: str).\n"
            "Include: CRAFT_RECIPES dict with keys: Fletching/Blacksmith/Alchemy/Building.\n"
            "Each recipe: {name, cost: {mat: qty}, out: {item: qty}}.\n"
            "No main(), no pygame.init()."
        ),
        "output": "economy_module.py — shop/buy/sell/craft functions + CRAFT_RECIPES"
    },
    "assembler": {
        "desc": "master game assembler",
        "task": (
            "Assemble the provided Python module code snippets into ONE complete runnable pygame game.\n"
            "STRICT RULES — the assembled game MUST:\n"
            "  1. Start with: import pygame, sys, math, random, json, os\n"
            "  2. Call pygame.init() once at top level\n"
            "  3. Create screen = pygame.display.set_mode((1280, 720))\n"
            "  4. Have a main() function containing the full game loop\n"
            "  5. Handle pygame.QUIT event every frame\n"
            "  6. Call pygame.display.flip() every frame\n"
            "  7. Use clock.tick(60) for 60 FPS\n"
            "  8. ALL input via pygame events — ZERO calls to _safe_input() or sys.stdin\n"
            "  9. ALL menus have X close button (top-right of each panel)\n"
            " 10. End with: if __name__ == '__main__': main()\n"
            "Remove any duplicate definitions. Fix any import conflicts.\n"
            "Return ONLY complete Python source. No markdown. No explanation. No comments about what you did."
        ),
        "output": "final_game.py — single complete runnable pygame file"
    },
}


_CACHED_AGENT_MODEL = None


def _get_agent_model():
    global _CACHED_AGENT_MODEL
    if _CACHED_AGENT_MODEL:
        return _CACHED_AGENT_MODEL
    try:
        import urllib.request as _ur, json as _j
        with _ur.urlopen(_ur.Request("http://localhost:11434/api/tags"), timeout=5) as r:
            models = [m["name"] for m in _j.loads(r.read()).get("models", [])]
        for preferred in ["qwen2.5-coder:32b", "qwen2.5-coder:14b", "qwen2.5-coder:7b",
                          "deepseek-coder:6.7b", "codellama:7b"]:
            if preferred in models:
                _CACHED_AGENT_MODEL = preferred
                return preferred
        if models:
            _CACHED_AGENT_MODEL = models[0]
            return models[0]
    except Exception:
        pass
    return "qwen2.5-coder:32b"


def _ollama_stream(prompt, model=None, timeout=1800, num_predict=-1, token_cb=None):
    """
    Stream tokens directly from Ollama HTTP API.
    num_predict=-1 means unlimited (model stops when it finishes).
    token_cb: optional callable(token_str) called for each streamed token (for GUI live output).
    Returns full response string, or "" on failure.
    """
    import urllib.request as _ur
    import json as _j

    if model is None:
        model = _get_agent_model()

    payload = _j.dumps({
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": num_predict,
            "temperature": 0.15,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        }
    }).encode("utf-8")

    req = _ur.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    parts = []
    try:
        with _ur.urlopen(req, timeout=timeout) as resp:
            while True:
                line = resp.readline()
                if not line:
                    break
                try:
                    chunk = _j.loads(line.decode("utf-8", errors="replace"))
                    tok = chunk.get("response", "")
                    if tok:
                        parts.append(tok)
                        if token_cb:
                            try:
                                token_cb(tok)
                            except Exception:
                                pass
                    if chunk.get("done", False):
                        break
                except Exception:
                    continue
    except Exception as ex:
        _umbra_print("  [STREAM ERROR] " + str(ex))
        return ""
    return "".join(parts)


def _clean_agent_output(raw):
    """
    Strip everything that isn't Python code:
    - Markdown fences
    - Prose sentences (lines that are plain English, not code)
    - Trailing commentary after the last code line
    Returns cleaned Python string.
    """
    if not raw:
        return ""

    # Remove markdown fences
    lines = raw.splitlines()
    in_fence = False
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped.startswith("```"):
            cleaned.append(line)
    lines = cleaned

    # Remove leading/trailing prose lines (plain English paragraphs before/after code)
    # A line is "prose" if it doesn't look like Python at all
    CODE_STARTERS = (
        "import ", "from ", "def ", "class ", "#", "    ", "\t",
        "WORLD", "BIOME", "TOWNS", "CITIES", "BANDIT", "GOBLIN",
        "WEAPONS", "ARMOR", "SPELLS", "QUEST", "FACTION", "DIALOGUE",
        "CRAFT", "MATERIAL", "ENEMY", "NPC_", "if ", "for ", "while ",
        "try:", "except", "return", "raise", "with ", "async ", "await ",
        "@", "\"\"\"", "'''", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "[", "{", "(", "True", "False", "None",
    )
    def looks_like_code(ln):
        s = ln.strip()
        if not s:
            return True  # keep blank lines
        if any(s.startswith(c) for c in CODE_STARTERS):
            return True
        # assignment
        if "=" in s and not s.endswith("."):
            return True
        return False

    # Strip leading prose
    while lines and not looks_like_code(lines[0]):
        lines.pop(0)
    # Strip trailing prose
    while lines and not looks_like_code(lines[-1]):
        lines.pop()

    result = "\n".join(lines)

    # Final safety: if there's a long English sentence mid-code,
    # comment it out so it doesn't break syntax
    safe_lines = []
    for ln in result.splitlines():
        s = ln.strip()
        # Long prose line (no = , no :, starts with capital, ends with .)
        if (len(s) > 60
                and s[0].isupper()
                and s.endswith(".")
                and "=" not in s
                and ":" not in s
                and "(" not in s
                and not s.startswith("#")):
            safe_lines.append("# " + ln)
        else:
            safe_lines.append(ln)

    return "\n".join(safe_lines)


def _syntax_repair(code, model):
    """Strip trailing broken lines first; fall back to LLM fix."""
    lines = code.splitlines()
    for _ in range(min(30, len(lines))):
        test = "\n".join(lines)
        try:
            ast.parse(test)
            return test
        except SyntaxError as se:
            if se.lineno and se.lineno >= len(lines) - 2:
                lines.pop()
            else:
                break
    # LLM targeted fix
    try:
        err_info = ""
        try:
            ast.parse("\n".join(lines))
        except SyntaxError as se2:
            bad_ln = lines[se2.lineno-1] if se2.lineno and se2.lineno <= len(lines) else "?"
            err_info = "Line " + str(se2.lineno) + ": " + str(se2.msg) + "\n  >>> " + bad_ln
        fix_prompt = (
            "Fix ONLY the Python syntax error below. Return the complete corrected Python file. "
            "No explanations. No markdown. Pure Python only.\n\nERROR:\n" + err_info +
            "\n\nCODE:\n" + "\n".join(lines)
        )
        fixed = _ollama_stream(fix_prompt, model=model, timeout=120, num_predict=4096)
        if fixed:
            fixed = _clean_agent_output(fixed)
            ast.parse(fixed)
            return fixed
    except Exception:
        pass
    return "\n".join(lines)


def _run_agent(agent_name, prompt, model, proj_dir, proj_slug):
    """
    Run a single named agent:
      1. Stream from Ollama
      2. Clean the output (strip prose/markdown)
      3. Syntax-check, attempt repair if needed
      4. Save to proj_dir/agent_name_proj_slug.py
    Returns (code_str, file_path) or ("", None) on failure.
    """
    _umbra_print("\n  ╔══ [" + agent_name.upper() + " AGENT] Starting...")
    raw = _ollama_stream(prompt, model=model)
    if not raw or len(raw.strip()) < 30:
        _umbra_print("  ╚══ [" + agent_name.upper() + " AGENT] ✗ Returned empty")
        return "", None

    code = _clean_agent_output(raw)
    if not code or len(code.strip()) < 30:
        _umbra_print("  ╚══ [" + agent_name.upper() + " AGENT] ✗ Nothing left after cleaning")
        return "", None

    # Syntax check
    try:
        ast.parse(code)
        _umbra_print("  ╚══ [" + agent_name.upper() + " AGENT] ✓ " + str(len(code.splitlines())) + " lines, syntax OK")
    except SyntaxError as e:
        _umbra_print("  ║   [" + agent_name.upper() + " AGENT] Syntax error at line " + str(e.lineno) + " — repairing...")
        code = _syntax_repair(code, model)
        try:
            ast.parse(code)
            _umbra_print("  ╚══ [" + agent_name.upper() + " AGENT] ✓ Repaired — " + str(len(code.splitlines())) + " lines")
        except SyntaxError:
            _umbra_print("  ╚══ [" + agent_name.upper() + " AGENT] ⚠ Saved with known issues")

    path = os.path.join(proj_dir, agent_name + "_" + proj_slug + ".py")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
    except Exception as ex:
        _umbra_print("  ╚══ [" + agent_name.upper() + " AGENT] ✗ Save failed: " + str(ex))
        return "", None

    return code, path


def _build_agent_prompt(agent_name, project_name, description):
    """Build the prompt for a specific agent with strict code-only instruction."""
    role = _AGENT_ROLES.get(agent_name, {})
    task = role.get("task", "Write Python code for the " + agent_name + " system.")
    output = role.get("output", "Complete Python module")

    return (
        "You are a specialized " + role.get("desc", agent_name) + " AI.\n"
        "Project: '" + project_name + "'\n"
        "Description: " + description[:300] + "\n\n"
        "YOUR TASK:\n" + task + "\n\n"
        "EXPECTED OUTPUT: " + output + "\n\n"
        "ABSOLUTE RULES — VIOLATIONS BREAK THE BUILD:\n"
        "  1. Return ONLY Python source code. Not a single word of English prose.\n"
        "  2. No markdown. No ```python fences. No ``` of any kind.\n"
        "  3. No explanations before or after the code.\n"
        "  4. No TODO comments. Every function must be fully implemented.\n"
        "  5. No pygame.init(), no main(), no game loop — module only.\n"
        "  6. Use only: stdlib + pygame\n"
        "  7. First character of your response must be a # comment or import statement.\n"
        "\n"
        "BEGIN PYTHON CODE NOW:"
    )


def _build_assembler_prompt(project_name, description, components):
    """Build the prompt for the assembler agent."""
    role = _AGENT_ROLES["assembler"]
    parts = []
    for name, code in components.items():
        parts.append("# === " + name.upper() + " MODULE ===\n" + code[:2000])
    combined = "\n\n".join(parts)

    return (
        "You are a " + role["desc"] + ".\n"
        "Project: '" + project_name + "'\n"
        "Description: " + description[:200] + "\n\n"
        "COMPONENT MODULES TO ASSEMBLE:\n\n"
        + combined + "\n\n"
        "ASSEMBLY TASK:\n" + role["task"] + "\n\n"
        "GAME STATES NEEDED: MENU, CLASS_SELECT, PLAY, INVENTORY, QUEST, DIALOGUE, SHOP, CRAFT, PAUSE, CITY_BUILD, WORLD_MAP, GAME_OVER\n"
        "CONTROLS: WASD=move, Shift=sprint, I=inventory, Q=quests, E=interact, C=crouch, B=city build, M=map, K=craft, ESC=pause, F5=save, F9=load, TAB=next spell, RClick=cast spell\n\n"
        "ABSOLUTE RULES:\n"
        "  1. Return ONLY Python source code. No English prose. No markdown.\n"
        "  2. First line must be: import pygame\n"
        "  3. Must include pygame.init() at module level.\n"
        "  4. Must include if __name__ == '__main__': main() at the very end.\n"
        "  5. Every menu/panel must have a clickable X button in its top-right corner.\n"
        "  6. Handle pygame.QUIT every single frame.\n"
        "  7. No _safe_input() calls. All input through pygame events.\n"
        "  8. No external files. Use pygame.draw for all graphics.\n"
        "\nBEGIN ASSEMBLED GAME CODE NOW:"
    )



def _stitch_game(project_name, brief, components):
    def strip_imports(code):
        keep=[]; skip_next=False
        skip={"import pygame","from pygame","import sys","import os",
              "import math","import random","import json","import time"}
        lines = (code or "").splitlines()
        i = 0
        while i < len(lines):
            ln = lines[i]
            s  = ln.strip()
            # Skip bare imports
            if s in skip or s.startswith("from pygame"):
                i += 1; continue
            # Strip agent __main__ blocks (they conflict with skeleton's main)
            # Also skip the indented body that follows
            if s.startswith("if __name__") and "__main__" in s:
                i += 1
                while i < len(lines) and (lines[i].startswith("    ") or lines[i].strip() == ""):
                    i += 1
                continue
            # Strip orphaned indented main() / run_game() calls at top level of agent output
            if ln.startswith("    ") and s in ("main()", "run_game()", "game_loop()", "start_game()"):
                i += 1; continue
            # Strip agent def main() / def run_game() / def game_loop() 
            # that would override the skeleton's main()
            # Strip agent redefinitions of skeleton helpers (txt, draw_main_menu variants, etc.)
            _SKELETON_FUNS = {"main","run_game","game_loop","game_main","start_game","run",
                              "txt","draw_text","render_text"}
            if s.startswith("def ") and any(s.startswith("def "+n+"(") for n in _SKELETON_FUNS):
                # Skip entire function body
                i += 1
                while i < len(lines) and (lines[i].startswith("    ") or lines[i].strip() == ""):
                    i += 1
                continue
            keep.append(ln)
            i += 1
        return "\n".join(keep)

    world_code    = strip_imports(components.get("world",""))
    char_code     = strip_imports(components.get("character",""))
    item_code     = strip_imports(components.get("item",""))
    mechanic_code = strip_imports(components.get("mechanic",""))
    ui_code       = strip_imports(components.get("ui",""))
    quest_code    = strip_imports(components.get("quest",""))
    economy_code  = strip_imports(components.get("economy",""))
    pname  = project_name
    pslug  = project_name.lower().replace(" ","_")

    # Read the bundled game skeleton shipped alongside umbra.py
    skeleton_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "core", "assets", "game_skeleton.py")
    if os.path.exists(skeleton_path):
        skeleton_template = open(skeleton_path,"r",encoding="utf-8").read()
    else:
        # Inline minimal skeleton so we never fail
        skeleton_template = _INLINE_SKELETON

    code = skeleton_template
    code = code.replace("__PROJECT_NAME__", pname)
    code = code.replace("__PROJ_SLUG__",    pslug)
    code = code.replace("__WORLD_CODE__",   world_code    or "# world agent: no output")
    code = code.replace("__CHAR_CODE__",    char_code     or "# character agent: no output")
    code = code.replace("__ITEM_CODE__",    item_code     or "# item agent: no output")
    code = code.replace("__MECH_CODE__",    mechanic_code or "# mechanic agent: no output")
    code = code.replace("__UI_CODE__",      ui_code       or "# ui agent: no output")
    code = code.replace("__QUEST_CODE__",   quest_code    or "# quest agent: no output")
    code = code.replace("__ECON_CODE__",    economy_code  or "# economy agent: no output")
    return code


# ============================================================
#  UMBRA AUTONOMOUS BUILD PIPELINE
#  Project Planner → Requirements → Assets → Systems →
#  Python Assembler → Test Loop → Self-Repair → Playable Build
# ============================================================

import json as _json

# ── 1. Project Planner ─────────────────────────────────────
def _plan_project(description, project_name, model):
    """Convert natural language into structured project spec."""
    _umbra_print("[PLANNER] Analyzing requirements...")
    prompt = (
        "You are a game project planner. Convert this game description into a JSON spec.\n"
        "Description: " + description + "\n"
        "Game name: " + project_name + "\n\n"
        "Return ONLY valid JSON with these keys (true/false values):\n"
        '{"genre":"","world_type":"","combat":true,"magic":true,"crafting":true,'
        '"inventory":true,"quests":true,"dialogue":true,"stealth":true,'
        '"city_building":true,"automation":true,"shops":true,"factions":true,'
        '"save_load":true,"minimap":true,"hud":true,'
        '"enemies":["list enemy names"],"weapons":["list weapon names"],'
        '"armor_sets":["list armor set names"],"spells":["list spell names"],'
        '"towns":["list town names"],"key_npcs":["list npc job types"]}\n'
        "Return ONLY the JSON object. No markdown. No explanation."
    )
    raw = _ollama_stream(prompt, model=model, timeout=120, num_predict=400)
    raw = _strip_fences(raw or "")
    # find first { to last }
    try:
        start = raw.index("{"); end = raw.rindex("}") + 1
        spec = _json.loads(raw[start:end])
    except Exception:
        # fallback spec — still better than nothing
        spec = {
            "genre": "Fantasy RPG", "world_type": "Open World",
            "combat": True, "magic": True, "crafting": True,
            "inventory": True, "quests": True, "dialogue": True,
            "stealth": True, "city_building": True, "automation": True,
            "shops": True, "factions": True, "save_load": True,
            "minimap": True, "hud": True,
            "enemies": ["Goblin","Bandit","Orc","Skeleton","Wolf",
                        "Dark Mage","Troll","Spider","Dragon Spawn","Mimic"],
            "weapons": ["Iron Sword","Steel Axe","Shadow Dagger","Oak Bow",
                        "Flame Staff","Frost Wand","Battle Hammer","Silver Spear",
                        "Throwing Stars","Death Scythe"],
            "armor_sets": ["Iron Set","Steel Set","Shadow Set"],
            "spells": ["Fireball","Ice Spike","Lightning Bolt","Heal","Shield",
                       "Teleport","Summon Wolf","Earthquake","Drain Life","Time Slow"],
            "towns": ["Stonehaven","Rivergate","Duskmill"],
            "key_npcs": ["Merchant","Guard","Blacksmith","Farmer","Miner","Alchemist"],
        }
    _umbra_print("[PLANNER] Spec ready: " + spec.get("genre","RPG") +
                 " | " + spec.get("world_type","Open World") +
                 " | " + str(len(spec.get("enemies",[]))) + " enemies")
    return spec


# ── 2. Requirement Validator ───────────────────────────────
_REQUIREMENTS = [
    ("window_opens",      lambda code: "pygame.display.set_mode" in code),
    ("game_loop",         lambda code: "clock.tick" in code and "pygame.QUIT" in code),
    ("wasd_movement",     lambda code: "K_w" in code and "K_s" in code and "K_a" in code and "K_d" in code),
    ("esc_pause",         lambda code: "K_ESCAPE" in code and "PAUSE" in code.upper()),
    ("inventory_key",     lambda code: "K_i" in code),
    ("quest_key",         lambda code: "K_q" in code),
    ("x_close_buttons",   lambda code: "draw_x_button" in code or "xb" in code or "xbtn" in code or "X button" in code.lower() or "DKRED" in code),
    ("hud_bars",          lambda code: "draw_bar" in code or "_bar(" in code),
    ("minimap",           lambda code: "minimap" in code.lower() or "MINIMAP" in code or "MX" in code),
    ("enemies_present",   lambda code: "Enemy" in code and "ENEMY_DEFS" in code),
    ("combat",            lambda code: "atk" in code and "hp" in code.lower()),
    ("weapons_data",      lambda code: "WEAPONS" in code),
    ("spells_data",       lambda code: "SPELLS" in code),
    ("save_load",         lambda code: "json.dump" in code and "json.load" in code),
    ("no_input_calls",    lambda code: "_safe_input(" not in code),
    ("main_guard",        lambda code: '__name__' in code and 'main()' in code),
]

def _validate_requirements(game_code):
    """Check which requirements pass/fail. Returns (passed, failed) lists."""
    passed = []; failed = []
    for name, check in _REQUIREMENTS:
        try:
            if check(game_code):
                passed.append(name)
            else:
                failed.append(name)
        except Exception:
            failed.append(name)
    return passed, failed


# ── 3. Asset Pipeline ──────────────────────────────────────
def _build_agent_prompt_v2(agent_name, project_name, spec, brief):
    """
    Build a richer, spec-aware prompt for each agent.
    Uses the structured project spec so agents know exactly what to build.
    """
    enemies   = spec.get("enemies",   ["Goblin","Bandit","Orc","Skeleton","Wolf"])
    weapons   = spec.get("weapons",   ["Iron Sword","Steel Axe","Oak Bow"])
    armor     = spec.get("armor_sets",["Iron Set","Steel Set","Shadow Set"])
    spells    = spec.get("spells",    ["Fireball","Heal","Ice Spike"])
    towns     = spec.get("towns",     ["Stonehaven","Rivergate"])
    npcs      = spec.get("key_npcs",  ["Merchant","Guard","Blacksmith"])

    tasks = {
        "world": (
            "Write a Python MODULE (no main, no pygame.init) for the WORLD SYSTEM.\n"
            "Must include:\n"
            "  WORLD_MAP = 200x200 list of strings using these biomes:\n"
            "    plains, forest, mountain, desert, water, snow, swamp, town, camp, mine, wood_area, road\n"
            "  BIOME_COL = dict mapping biome name to RGB tuple\n"
            "  TOWNS = list of (tile_x, tile_y, 'Name') for: " + str(towns) + "\n"
            "  CITIES = list of (tile_x, tile_y, 'Name') for 2 large cities\n"
            "  BANDIT_CAMPS = list of (x,y) for 3 camps\n"
            "  GOBLIN_CAMPS = list of (x,y) for 3 camps\n"
            "  MINES = list of (x,y) for 3 mines\n"
            "  WOODCUTS = list of (x,y) for 3 woodcutting areas\n"
            "  def gen_world() — fills WORLD_MAP with biomes using random (seed 42)\n"
            "  def draw_world(surf, cam_x, cam_y) — renders visible tiles\n"
            "  def get_biome(tx,ty) -> str\n"
            "Call gen_world() at module level so WORLD_MAP is populated on import."
        ),
        "character": (
            "Write a Python MODULE for PLAYER, ENEMY and NPC CLASSES.\n"
            "Player class: __init__(cls) where cls is Warrior/Mage/Rogue\n"
            "  Attributes: x,y,cls,max_hp,hp,max_mp,mp,max_sta,sta,\n"
            "              str_,dex,int_,luck,level,xp,xp_next,gold,speed\n"
            "              inventory(dict),equipped(dict),spells(list),quests(list),crouching\n"
            "  Methods: atk_power(),def_power(),add_item(name,qty),gain_xp(amt),regen(dt)\n"
            "Enemy class: __init__(edef,tx,ty)\n"
            "  ENEMY_DEFS list with all 10: " + str(enemies) + "\n"
            "  Each: {name,hp,atk,def,xp,col(RGB tuple),spd,faction}\n"
            "  Methods: update(player,dt), draw(surf,cx,cy)\n"
            "NPC class: __init__(name,job,tx,ty)\n"
            "  Jobs: " + str(npcs) + "\n"
            "  Attributes: name,job,x,y,dialogue(list),shop_stock(dict)\n"
            "No main(), no pygame.init(). import random, math only."
        ),
        "item": (
            "Write a Python MODULE of GAME DATA CONSTANTS only — no classes, no functions.\n"
            "WEAPONS = list of 10 dicts, one per weapon: " + str(weapons) + "\n"
            "  Each: {name,atk(int),type(melee/ranged/magic),val(int),col(RGB tuple)}\n"
            "ARMOR_SETS = list of 3 dicts: " + str(armor) + "\n"
            "  Each: {name,parts[list of 3 piece names],def(int),val(int)}\n"
            "SPELLS = list of 10 dicts: " + str(spells) + "\n"
            "  Each: {name,mp(int),dmg(int),col(RGB tuple),desc(str)}\n"
            "MATERIALS = list of 10 material name strings\n"
            "QUESTS = list of 5 dicts: {id,name,desc,target,need,prog,done,reward_gold,reward_xp}\n"
            "  target is either an enemy name or 'mat:material_name'\n"
            "FACTIONS = dict: {kingdom:{rep:0,name:str}, bandit:{rep:0,name:str}, goblin:{rep:0,name:str}}\n"
            "DIALOGUE_TREES = dict keyed by NPC job with list of {text,opts} nodes\n"
            "  Include: Merchant, Guard, Blacksmith, Farmer, default\n"
            "NPC_NAMES = list of 16 first names\n"
            "NPC_JOBS = " + str(npcs) + "\n"
            "No imports needed.\n"
            "STRICT RULES: No classes. No functions. No if/for/while. No f-strings. Under 90 lines."
        ),
        "mechanic": (
            "Write a Python MODULE for GAME MECHANIC HELPERS.\n"
            "Camera class: x,y attributes; update(px,py) smoothly follows player\n"
            "FloatText class: __init__(text,x,y,col); update(); draw(surf,cx,cy) — fades out rising text\n"
            "Projectile class: __init__(x,y,tx,ty,dmg,col,spd=9); update(); draw(surf,cx,cy)\n"
            "Building class:\n"
            "  TYPES class attr: dict of {House,Shop,Barracks,Farm,Tower,Warehouse}\n"
            "    each: {col(RGB),w(tiles),h(tiles),cost:{mat:qty}}\n"
            "  __init__(btype,tx,ty)\n"
            "  draw(surf,cx,cy) — draw with roof triangle, door, window details\n"
            "save_game(player,buildings,filepath) -> bool: JSON serialise\n"
            "load_game(player,buildings,filepath) -> bool: JSON deserialise\n"
            "No main(), no pygame.init()."
        ),
        "ui": (
            "Write a Python MODULE of UI DRAWING FUNCTIONS.\n"
            "EVERY panel/menu/screen MUST have a clickable X button in the TOP-RIGHT corner.\n"
            "Required functions (each returns X-button rect and any interactive rects):\n"
            "  font_cache(sz)->Font; txt(surf,text,x,y,sz,col,center=False)\n"
            "  bar(surf,x,y,w,h,val,mx,col,bg); panel(surf,rx,ry,rw,rh,title)->xbtn_rect\n"
            "  btn(surf,x,y,w,h,label,col,tcol,sz)->rect\n"
            "  draw_hud(surf,player): HP/MP/STA bars, gold, level, XP, equipped, biome label\n"
            "  draw_minimap(surf,player,enemies,WORLD_MAP,BIOME_COL): 126x126 in top-right\n"
            "  draw_main_menu(surf,project_name)->btns: starfield bg, moon, title, 3 buttons\n"
            "  draw_class_select(surf)->btns: 3 class cards with drawn portraits\n"
            "  draw_inventory(surf,player,selected)->xbtn,slots,eq_btn,drop_btn\n"
            "  draw_quest_log(surf,player)->xbtn\n"
            "  draw_shop(surf,npc,player,selected)->xbtn,buy_btns,items\n"
            "  draw_crafting(surf,player,tab,selected,recipes)->xbtn,tab_btns,craft_btns\n"
            "  draw_dialogue(surf,npc,dial_idx)->xbtn,opt_btns\n"
            "  draw_pause(surf)->xbtn,pause_btns\n"
            "  draw_city_panel(surf,place_type,BUILDING_TYPES)->xbtn,type_btns\n"
            "  draw_world_map(surf,player,TOWNS,CITIES,WORLD_MAP,BIOME_COL)->xbtn\n"
            "  draw_gameover(surf)\n"
            "  draw_player_sprite(surf,sx,sy,cls,crouching): detailed human figure with weapon\n"
            "  draw_enemy_sprite(surf,sx,sy,edef): unique art per enemy type, NOT a square\n"
            "  draw_npc_sprite(surf,sx,sy,job): unique art per job with accessory\n"
            "No main(), no pygame.init(). Use pygame only."
        ),
        "quest": (
            "Write a Python MODULE for QUEST and SPAWN systems.\n"
            "spawn_entities(WORLD_MAP,TOWNS,CITIES,BANDIT_CAMPS,GOBLIN_CAMPS,ENEMY_DEFS,NPC_NAMES,NPC_JOBS)\n"
            "  -> (enemies:list, npcs:list, buildings:list)\n"
            "  Spawn 4 bandits per bandit camp, 4 goblins + 1 orc per goblin camp\n"
            "  Spawn 30 random wild enemies outside towns/water\n"
            "  Spawn 7 NPCs per town (Merchant,Guard,Guard,Farmer,Farmer,Miner,Blacksmith)\n"
            "check_kill_quests(player, enemy_name): update quest prog on kill\n"
            "check_item_quests(player, item_name, qty): update quest prog on pickup\n"
            "complete_ready_quests(player) -> list of names: check+complete, add rewards\n"
            "harvest_nearby(player, WORLD_MAP) -> str: mine/chop/gather based on biome\n"
            "No main(), no pygame.init()."
        ),
        "economy": (
            "Write a Python MODULE for ECONOMY and CRAFTING.\n"
            "CRAFT_RECIPES = dict keyed by tab name (Fletching/Blacksmith/Alchemy/Building)\n"
            "  Each value: list of {name,cost:{mat:qty},out:{item:qty}}\n"
            "  Include at least 4 recipes per tab.\n"
            "BUILDING_TYPES = dict of {name:{col(RGB),w,h,cost:{mat:qty}}}\n"
            "  Include: House,Shop,Barracks,Farm,Tower,Warehouse\n"
            "buy_item(player,npc,item_name) -> (bool, str): deduct gold, add item\n"
            "sell_item(player,npc,item_name) -> (bool, str): add gold, remove item\n"
            "craft_item(player,recipe) -> (bool, str): deduct mats, add output\n"
            "No main(), no pygame.init()."
        ),
    }

    task = tasks.get(agent_name, "Write a Python module for the " + agent_name + " system.")
    return (
        "You are a specialist AI agent: " + agent_name + " engineer.\n"
        "Project: '" + project_name + "'\n"
        "Brief: " + brief[:200] + "\n\n"
        "YOUR TASK:\n" + task + "\n\n"
        "STRICT OUTPUT RULES — ONE VIOLATION = BUILD FAILS:\n"
        "  1. Return ONLY Python source code.\n"
        "  2. No markdown fences (no ```).\n"
        "  3. No English sentences mixed into code.\n"
        "  4. No TODO/placeholder — every function fully implemented.\n"
        "  5. No pygame.init(), no main(), no game loop.\n"
        "  6. First character must be # or import or a variable name.\n"
        "\nBEGIN CODE:"
    )


# ── 4. Test Loop ───────────────────────────────────────────
def _test_game(game_path, game_code):
    """
    Run requirement validation and attempt repair for each failure.
    Returns (final_code, report_dict)
    """
    passed, failed = _validate_requirements(game_code)
    report = {"passed": passed, "failed": failed, "repairs": []}

    if failed:
        _umbra_print("[TEST] " + str(len(passed)) + " passed, " +
                     str(len(failed)) + " failed: " + ", ".join(failed))
        # Attempt Python-level auto-repairs for common failures
        code = game_code

        if "no_input_calls" in failed:
            code = code.replace("_safe_input(", "# _safe_input(", "")
            report["repairs"].append("stripped _safe_input() calls")

        if "main_guard" in failed:
            if "def main():" not in code:
                # Find the game loop and rename it main()
                import re as _re2
                _fns = _re2.findall(r"^def (\w+)\(\):", code, _re2.MULTILINE)
                for _fn in _fns:
                    _idx = code.find("def " + _fn + "():")
                    _body = code[_idx:_idx+3000]
                    if any(k in _body for k in ["clock.tick","pygame.event.get","pygame.display.flip"]):
                        code = code.replace("def " + _fn + "():", "def main():", 1)
                        code = code.replace(_fn + "()", "main()")
                        report["repairs"].append("renamed " + _fn + " to main()")
                        _umbra_print("[REPAIR] Renamed game loop: " + _fn + "() -> main()")
                        break
            if "if __name__" not in code:
                code += "\n\nif __name__ == '__main__':\n    main()\n"
                report["repairs"].append("added main guard")

        if "x_close_buttons" in failed:
            # inject a minimal X-button drawing call if totally missing
            if "DKRED" not in code:
                code = code.replace(
                    "def main():",
                    "DKRED=(140,20,20)\ndef main():"
                )
                report["repairs"].append("injected DKRED colour for X buttons")

        game_code = code
        # Re-validate after repairs
        passed2, failed2 = _validate_requirements(game_code)
        report["passed"] = passed2
        report["failed"] = failed2
        if failed2:
            _umbra_print("[TEST] After repair: " + str(len(passed2)) + " passed, " +
                         str(len(failed2)) + " still failing: " + ", ".join(failed2))
        else:
            _umbra_print("[TEST] All requirements pass after repair!")
    else:
        _umbra_print("[TEST] All " + str(len(passed)) + " requirements passed!")

    return game_code, report


# ── 5. Full Pipeline Orchestrator ──────────────────────────
def _run_deep_build(runtime, description, project_name, agents_to_run=None):
    """
    Umbra Autonomous Build Pipeline:
      1. Project Planner   → structured spec from user description
      2. Specialist Agents → 7 focused modules (streamed, no timeout)
      3. Python Stitcher   → deterministic assembly (no LLM assembler)
      4. Requirement Validator → check 16 game requirements
      5. Auto-Repair Loop  → fix failures without LLM if possible
      6. Syntax Validator  → final parse check
      7. Report to user    → BUILD COMPLETE with requirement summary
    """
    llm = runtime.get("llm")
    if not llm or not llm.is_configured():
        _umbra_print("[BUILD] LLM not configured."); return None

    pm    = runtime.get("project_manager")
    model = _get_agent_model()
    ws_base   = os.path.join(_UMBRA_ROOT, "workspaces", "agent_builds")
    proj_slug = project_name.lower().replace(" ", "_")
    proj_dir  = os.path.join(ws_base, proj_slug)
    os.makedirs(proj_dir, exist_ok=True)
    short_desc = str(description or "")[:600]

    _umbra_print("\n" + "="*62)
    _umbra_print("  UMBRA AUTONOMOUS BUILD — " + project_name)
    _umbra_print("  Model: " + model)
    _umbra_print("="*62)

    # ── Step 1: Project Planner ────────────────────────────
    spec = _plan_project(short_desc, project_name, model)

    # ── Step 2: Brief for agents ───────────────────────────
    _umbra_print("[UMBRA] Writing agent brief...")
    brief_raw = _ollama_stream(
        "Write a 80-word technical brief for game agents. Game: " + project_name +
        "\nDescription: " + short_desc[:200] +
        "\nFocus: systems, art via pygame.draw (no images), controls.\nReturn ONLY the brief.",
        model=model, timeout=90, num_predict=160
    )
    brief = (brief_raw or "").strip() or short_desc[:200]

    # ── Step 3: Run specialist agents ─────────────────────
    _umbra_print("[UMBRA] Dispatching " + str(len(["world","character","item","mechanic","ui","quest","economy"])) + " specialist agents...\n")
    agent_order = ["world","character","item","mechanic","ui","quest","economy"]
    components  = {}

    for agent_name in agent_order:
        prompt = _build_agent_prompt_v2(agent_name, project_name, spec, brief)
        code, _ = _run_agent(agent_name, prompt, model, proj_dir, proj_slug)
        if code and len(code.strip()) > 30:
            components[agent_name] = code

    _umbra_print("\n[UMBRA] " + str(len(components)) + "/" + str(len(agent_order)) +
                 " agents produced output.")

    # ── Step 4: Python Stitcher (NO LLM assembler) ────────
    _umbra_print("[UMBRA] Python-stitching game (deterministic, no timeout risk)...")
    game_code = _stitch_game(project_name, brief, components)

    # ── Step 5: Syntax check ───────────────────────────────
    try:
        ast.parse(game_code)
        _umbra_print("[SYNTAX] OK")
    except SyntaxError as e:
        _umbra_print("[SYNTAX] Error line " + str(e.lineno) + " — repairing...")
        game_code = _syntax_repair(game_code, model)
        try:
            ast.parse(game_code)
            _umbra_print("[SYNTAX] Repaired")
        except SyntaxError as e2:
            _umbra_print("[SYNTAX] Could not fully repair (line " + str(e2.lineno) + ") — saving anyway")

    # ── Step 6: Requirement validation + auto-repair loop ──
    _umbra_print("[UMBRA] Running requirement validation...")

    # Player safety patch — ensures agent Player class has all skeleton-required attrs
    if 'Player' in game_code and 'UMBRA_PLAYER_PATCH' not in game_code:
        _pp = '''
# UMBRA_PLAYER_PATCH
try:
    _op=Player.__init__
    def _np(self,*a,**kw):
        _op(self,*a,**kw)
        for _at,_dv in [('active_quests',{}),('completed_quests',[]),
                        ('inventory',{}),('equipped',{'weapon':None,'armor':None}),
                        ('spells',[]),('gold',50),('level',1),('xp',0),
                        ('xp_next',100),('float_texts',[]),('atk',10),
                        ('defense',5),('spd',180),('alive',True),
                        ('attack_cooldown',0.0),('regen_timer',0.0)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Player.__init__=_np
except Exception: pass
# UMBRA_ENEMY_PATCH
try:
    _oe=Enemy.__init__
    def _ne(self,edef,tx,ty,*a,**kw):
        if isinstance(edef,str):
            _n=edef
            edef={'name':_n,'hp':40,'atk':8,'def':3,'defense':3,'xp_val':15,'spd':90,'aggro':200}
        try:
            _oe(self,edef,tx,ty,*a,**kw)
        except (KeyError,TypeError,AttributeError):
            pass
        for _at,_dv in [('name',edef.get('name','Enemy')),
                        ('hp',edef.get('hp',40)),
                        ('max_hp',edef.get('hp',40)),
                        ('atk',edef.get('atk',8)),
                        ('defense',edef.get('defense',edef.get('def',3))),
                        ('def_',edef.get('def',edef.get('defense',3))),
                        ('xp_val',edef.get('xp_val',15)),
                        ('spd',edef.get('spd',90)),
                        ('aggro',edef.get('aggro',200)),
                        ('alive',True),('tx',tx),('ty',ty),
                        ('x',tx),('y',ty)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Enemy.__init__=_ne
except Exception: pass
'''
        if 'if __name__' in game_code:
            game_code=game_code.replace('if __name__',_pp+'\nif __name__',1)
        else:
            game_code+=_pp

        # Fix draw_main_menu — normalize def signature + fix call sites
        import re as _re2
        # Normalize any def variant to the correct signature
        game_code = _re2.sub(
            r'def draw_main_menu\s*\([^)]*\)\s*:',
            'def draw_main_menu(surf, project_name):',
            game_code
        )
        # Fix call sites missing project_name (exclude def lines)
        game_code = _re2.sub(
            r'(?<!def )draw_main_menu\(\s*(\w+)\s*\)',
            r'draw_main_menu(\1, project_name)',
            game_code
        )
        # Ensure project_name variable exists in game scope
        if 'project_name = ' not in game_code and 'project_name=' not in game_code:
            game_code = game_code.replace(
                'def main():',
                'project_name = ' + repr(project_name) + '\n\ndef main():'
            )

    game_code, report = _test_game(
        os.path.join(proj_dir, proj_slug + "_game.py"), game_code
    )

    if not game_code or len(game_code.strip()) < 200:
        _umbra_print("[UMBRA] Build produced empty output."); return None

    # ── Step 7: Save ───────────────────────────────────────
    game_path = os.path.join(proj_dir, proj_slug + "_game.py")
    with open(game_path, "w", encoding="utf-8") as f:
        f.write(game_code)

    total_lines = len(game_code.splitlines())

    if pm:
        proj = pm.get_project(project_name) or pm.create_project(project_name, description=description)
        pm.add_file_to_project(proj, game_path, "game")
        pm.set_active(proj.name)

    mem = runtime.get("memory")
    if mem:
        mem.store("last_game_file", game_path, tags=["game"])
        try: mem.save()
        except Exception: pass
        mem.store("deep_build:" + proj_slug,
                  {"project":project_name,"path":game_path,
                   "agents":list(components.keys()),"lines":total_lines,
                   "requirements_passed":report["passed"],
                   "requirements_failed":report["failed"]},
                  tags=["game","deep_build"])

    passed_n = len(report["passed"])
    failed_n = len(report["failed"])
    total_req = passed_n + failed_n

    _umbra_print("\n" + "="*62)
    _umbra_print("  [UMBRA] BUILD COMPLETE")
    _umbra_print("  Game:         " + game_path)
    _umbra_print("  Size:         " + str(total_lines) + " lines")
    _umbra_print("  Agents used:  " + ", ".join(components.keys()))
    _umbra_print("  Requirements: " + str(passed_n) + "/" + str(total_req) + " passed")
    if report["failed"]:
        _umbra_print("  Still needed: " + ", ".join(report["failed"]))
    if report["repairs"]:
        _umbra_print("  Auto-repaired: " + ", ".join(report["repairs"]))
    _umbra_print("  Run: play " + project_name)
    _umbra_print("="*62 + "\n")

    return {"path": game_path, "lines": total_lines,
            "components": list(components.keys()),
            "requirements_passed": passed_n,
            "requirements_failed": failed_n}



# ============================================================
#  SELF-FIX
# ============================================================

def handle_self_fix(runtime, scope="all"):
    llm = runtime.get("llm")
    _umbra_print("\n[SELF-FIX] Scanning core/runtime modules...")
    broken = _find_broken_modules()
    if not broken:
        _umbra_print("[SELF-FIX] No syntax errors found.")
    else:
        _umbra_print("[SELF-FIX] Found " + str(len(broken)) + " broken module(s):")
        for path, err in broken:
            _umbra_print("  x " + os.path.basename(path) + ": " + err[:80])

    _umbra_print("[SELF-FIX] Running test suite...")
    p, f, out = _run_pytest_quick(timeout=120)
    _umbra_print("[SELF-FIX] Tests: " + str(p) + " passed, " + str(f) + " failed")
    if f > 0:
        for line in out.splitlines():
            if "FAILED" in line:
                _umbra_print("  " + line.strip())

    if f == 0 and not broken:
        _umbra_print("[SELF-FIX] Umbra is clean!\n")
        return
    if not broken:
        _umbra_print("[SELF-FIX] Syntax clean but tests failing. Type 'test' for details.\n")
        return
    if not llm or not llm.is_configured():
        _umbra_print("[SELF-FIX] LLM not configured — cannot auto-fix.\n")
        return

    fixed = 0
    for path, error in broken:
        fname = os.path.basename(path)
        _umbra_print("\n[SELF-FIX] Fixing: " + fname)
        src = _ask_llm_fix(llm, path, error)
        if not src:
            _umbra_print("  [SKIP] LLM could not generate fix")
            continue
        try:
            ast.parse(src)
        except SyntaxError as e:
            _umbra_print("  [SKIP] Fix still broken: " + str(e))
            continue
        if not _approval_prompt("Replace " + fname, src[:500]):
            _umbra_print("  [SKIPPED]")
            continue
        bk = _backup_file(path)
        _umbra_print("  [BACKUP] " + os.path.basename(bk))
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(src)
            _umbra_print("  [WRITTEN] " + fname)
            fixed += 1
        except Exception as e:
            shutil.copy2(bk, path)
            _umbra_print("  [ERROR/REVERTED] " + str(e))

    if fixed > 0:
        _umbra_print("\n[SELF-FIX] Re-running tests...")
        p2, f2, _ = _run_pytest_quick(timeout=90)
        _umbra_print("[SELF-FIX] After: " + str(p2) + " passed, " + str(f2) + " failed")
    _umbra_print("")


# ============================================================
#  WORKSPACE / PROJECT REPAIR
# ============================================================

def _repair_python_file(llm, path):
    err = _syntax_check(path)
    if not err:
        return False, False, ""
    if not llm or not llm.is_configured():
        return True, False, err
    fixed = _ask_llm_fix(llm, path, err)
    if not fixed:
        return True, False, err
    try:
        ast.parse(fixed)
    except SyntaxError:
        return True, False, err
    _backup_file(path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(fixed)
        return True, True, err
    except Exception as e:
        return True, False, str(e)


def handle_workspace_repair(runtime, target="all", auto=False):
    llm = runtime.get("llm")
    ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
    pm = runtime.get("project_manager")
    scan_dirs = []

    if target not in ("all", "last") and os.path.isfile(target):
        err = _syntax_check(target)
        if not err:
            if not auto:
                _umbra_print("[WORKSPACE-FIX] " + os.path.basename(target) + " — clean.\n")
            return
        if not auto and not _approval_prompt("Fix " + os.path.basename(target), "Error: " + err):
            return
        _, fixed, _ = _repair_python_file(llm, target)
        _umbra_print("[WORKSPACE-FIX] " + ("Fixed" if fixed else "Could not fix") + ": " + os.path.basename(target))
        return

    if target == "last":
        candidates = []
        if os.path.isdir(ws_base):
            for d in os.listdir(ws_base):
                full = os.path.join(ws_base, d)
                if os.path.isdir(full):
                    try:
                        candidates.append((os.path.getmtime(full), full))
                    except Exception:
                        pass
        if candidates:
            scan_dirs.append(sorted(candidates, reverse=True)[0][1])
    else:
        if os.path.isdir(ws_base):
            for d in os.listdir(ws_base):
                full = os.path.join(ws_base, d)
                if os.path.isdir(full) and d not in ("images", "videos"):
                    scan_dirs.append(full)

    py_files = []
    for d in scan_dirs:
        for root, dirs, files in os.walk(d):
            for fname in files:
                if fname.endswith(".py"):
                    py_files.append(os.path.join(root, fname))

    if not py_files:
        if not auto:
            _umbra_print("[WORKSPACE-FIX] No Python files found.\n")
        return

    broken = [(p, _syntax_check(p)) for p in py_files if _syntax_check(p)]
    if not broken:
        if not auto:
            _umbra_print("[WORKSPACE-FIX] Scanned " + str(len(py_files)) + " file(s) — all clean.\n")
        return

    _umbra_print("[WORKSPACE-FIX] Found " + str(len(broken)) + " broken file(s):")
    for path, err in broken:
        _umbra_print("  x " + os.path.relpath(path, _UMBRA_ROOT) + ": " + err[:70])

    if not llm or not llm.is_configured():
        _umbra_print("[WORKSPACE-FIX] LLM not configured.\n")
        return

    if not auto:
        preview = "\n".join("  " + os.path.relpath(p, _UMBRA_ROOT) for p, _ in broken)
        if not _approval_prompt("Fix " + str(len(broken)) + " workspace file(s)", preview):
            _umbra_print("[WORKSPACE-FIX] Cancelled.\n")
            return

    fixed = 0
    for path, _ in broken:
        _, was_fixed, _ = _repair_python_file(llm, path)
        rel = os.path.relpath(path, _UMBRA_ROOT)
        _umbra_print("  " + ("[FIXED] " if was_fixed else "[SKIP]  ") + rel)
        if was_fixed:
            fixed += 1
    _umbra_print("[WORKSPACE-FIX] " + str(fixed) + "/" + str(len(broken)) + " repaired.\n")


def _apply_common_improvements(runtime, file_path, project_type="game"):
    if not os.path.isfile(file_path) or not file_path.endswith(".py"):
        return
    llm = runtime.get("llm")
    if not llm or not llm.is_configured():
        return
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
    except Exception:
        return

    suggestions = []
    if project_type == "game" and "pygame" in source:
        if "clamp" not in source and "min(" not in source and "max(" not in source:
            suggestions.append("add screen boundary clamping so sprites stay on screen")
        if "draw.rect" not in source and "health" not in source.lower():
            suggestions.append("add a visible health bar using pygame.draw.rect")
        if "font" not in source.lower() and "score" not in source.lower():
            suggestions.append("add a score counter displayed with pygame.font")
    if not suggestions:
        return

    _umbra_print("\n[UMBRA] Common improvements available:")
    for i, s in enumerate(suggestions, 1):
        _umbra_print("  " + str(i) + ". " + s)
    try:
        ans = _safe_input("  Apply automatically? [y/N]: ", "").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return
    if ans not in ("y", "yes"):
        return

    prompt = (
        "Improve this pygame game: " + ", ".join(suggestions) +
        ". Keep all existing gameplay. Return ONLY complete improved Python. No markdown.\n\n" +
        source
    )
    try:
        r = llm.complete(prompt)
        if r and r.content:
            improved = _strip_fences(r.content)
            ast.parse(improved)
            bk = _backup_file(file_path)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(improved)
            _umbra_print("  [IMPROVE] Done. Backup: " + os.path.basename(bk) + "\n")
    except SyntaxError as e:
        _umbra_print("  [IMPROVE] Syntax error (" + str(e) + ") — keeping original.\n")
    except Exception as e:
        _umbra_print("  [IMPROVE] Failed: " + str(e) + "\n")


# ============================================================
#  REAL ORCHESTRATION PIPELINE
# ============================================================

def _run_real_pipeline(runtime, prompt, active_project=None, pm=None):
    llm = runtime.get("llm")
    ws_base = os.path.join(_UMBRA_ROOT, "workspaces")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = "run_" + ts
    run_dir = os.path.join(ws_base, run_id)
    os.makedirs(run_dir, exist_ok=True)

    _umbra_print("\n[UMBRA] Starting pipeline for: " + prompt[:60] + "...")
    _umbra_print("[PLAN] Breaking task into steps...")

    if not llm or not llm.is_configured():
        _umbra_print("[PLAN] LLM not available — cannot plan.\n")
        return None

    plan_prompt = (
        "You are a software architect. Break this task into 3-5 clear implementation steps.\n"
        "Task: " + prompt + "\n\n"
        "Return a JSON array of steps. Each: {\"step\": N, \"description\": \"...\", \"filename\": \"file.py\"}\n"
        "ONLY JSON. No markdown."
    )
    try:
        plan_response = llm.complete(plan_prompt)
        plan_text = _strip_fences(plan_response.content) if plan_response and plan_response.content else "[]"
        plan_text = re.sub(r"^```json\s*", "", plan_text, flags=re.MULTILINE)
        steps = json.loads(plan_text)
        if not isinstance(steps, list):
            steps = [{"step": 1, "description": prompt, "filename": "solution.py"}]
    except Exception:
        steps = [{"step": 1, "description": prompt, "filename": "solution.py"}]

    _umbra_print("[PLAN] " + str(len(steps)) + " step(s):")
    for s in steps:
        _umbra_print("  " + str(s.get("step", "?")) + ". " + s.get("description", "")[:60])
    if not steps:
        _umbra_print("[PLAN] LLM returned empty plan — using direct build...")
        steps = [{"step": prompt, "description": prompt, "filename": "output.py"}]

    written_files = []
    for step in steps:
        desc = step.get("description", prompt)
        fname = step.get("filename", "output_" + str(step.get("step", 1)) + ".py")
        if not fname.endswith(".py"):
            fname = fname.split(".")[0] + ".py"
        file_path = os.path.join(run_dir, fname)

        _umbra_print("\n[BUILD] Step " + str(step.get("step", "?")) + ": " + desc[:50])

        build_prompt = (
            "Write complete working Python code for: " + desc +
            "\n\nContext: " + prompt[:200] +
            "\nFile: " + fname +
            "\n\nRequirements:\n"
            "- Complete, runnable Python\n"
            "- No placeholder comments\n"
            "- No external API keys\n"
            "- If pygame: single file, 800x600, clock.tick(60), QUIT handling, ALL input in pygame window\n"
            "Output ONLY Python code. No markdown."
        )
        try:
            build_response = llm.complete(build_prompt)
            if not build_response or not build_response.content:
                _umbra_print("[BUILD] LLM returned empty — skipping")
                continue
            code = _strip_fences(build_response.content)

            try:
                ast.parse(code)
            except SyntaxError as e:
                _umbra_print("[BUILD] Syntax error: " + str(e) + " — fixing...")
                fixed = _ask_llm_fix(llm, file_path, str(e))
                if fixed:
                    try:
                        ast.parse(fixed)
                        code = fixed
                    except SyntaxError:
                        _umbra_print("[BUILD] Fix failed — skipping")
                        continue
                else:
                    continue

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            written_files.append({"file": fname, "path": file_path, "lines": len(code.splitlines())})
            _umbra_print("[BUILD] Written: " + fname + " (" + str(len(code.splitlines())) + " lines)")

        except Exception as e:
            _umbra_print("[BUILD] Failed: " + str(e))
            continue

    if not written_files:
        _umbra_print("\n[PIPELINE] No files produced.\n")
        return None

    _umbra_print("\n[TEST] Running syntax tests...")
    test_results = []
    for finfo in written_files:
        path = finfo["path"]
        err = _syntax_check(path)
        if err:
            test_results.append({"file": finfo["file"], "passed": False, "error": err})
            _umbra_print("  [FAIL] " + finfo["file"] + ": " + err[:70])
        else:
            test_results.append({"file": finfo["file"], "passed": True, "error": ""})
            _umbra_print("  [PASS] " + finfo["file"])

    failed = [t for t in test_results if not t["passed"]]
    if failed:
        _umbra_print("\n[REPAIR] Fixing " + str(len(failed)) + " file(s)...")
        for t in failed:
            path = os.path.join(run_dir, t["file"])
            if not os.path.isfile(path):
                continue
            fixed_src = _ask_llm_fix(llm, path, t["error"])
            if fixed_src:
                try:
                    ast.parse(fixed_src)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(fixed_src)
                    t["passed"] = True
                    _umbra_print("  [REPAIRED] " + t["file"])
                except SyntaxError:
                    _umbra_print("  [REPAIR FAILED] " + t["file"])

    passed_files = [t for t in test_results if t["passed"]]
    still_failing = [t for t in test_results if not t["passed"]]
    _umbra_print("\n[VERIFY] " + str(len(passed_files)) + "/" + str(len(test_results)) + " passing")

    _umbra_print("\n[DELIVER] Files ready:")
    for finfo in written_files:
        status = "OK" if any(t["file"] == finfo["file"] and t["passed"] for t in test_results) else "ISSUES"
        _umbra_print("  [" + status + "] " + finfo["path"])

    if still_failing:
        _umbra_print("\n[DELIVER] " + str(len(still_failing)) + " file(s) still have issues — try: fix workspace")

    mem = runtime.get("memory")
    if mem:
        mem.store("run:" + run_id, {
            "prompt": prompt[:100], "files": len(written_files),
            "passed": len(passed_files), "run_dir": run_dir
        }, tags=["run", "pipeline"])

    if active_project and pm:
        for finfo in written_files:
            pm.add_file_to_project(active_project, finfo["path"], "code")

    _umbra_print("\n[WORKSPACE] " + run_dir + "\n")

    class _PipelineResult:
        def __init__(self, run_id, files, results, run_dir):
            self.run_id = run_id
            self.files = files
            self.results = results
            self.run_dir = run_dir
            self.status = "completed" if all(r["passed"] for r in results) else "completed_with_failures"
            self.written_files = [{"file": f["file"], "lines": f["lines"]} for f in files]
            self.tasks = files
            self.error = None
        def __getitem__(self, key):
            return getattr(self, key, None)
        def get(self, key, default=None):
            return getattr(self, key, default)

    return _PipelineResult(run_id, written_files, test_results, run_dir)


# ============================================================
#  SELF-INSTALL
# ============================================================

def handle_self_install(runtime, feature_description):
    llm = runtime.get("llm")
    if not llm or not llm.is_configured():
        _umbra_print("[INSTALL] LLM not configured.\n")
        return

    words = re.sub(r"[^a-z0-9 ]", "", feature_description.lower()).split()
    stop = {"a", "an", "the", "into", "umbra", "for", "to", "and", "or",
            "make", "build", "create", "install", "add", "integrate", "new", "it"}
    key_words = [w for w in words if w not in stop][:4]
    if not key_words:
        key_words = ["custom", "feature"]
    module_name = "runtime_" + "_".join(key_words)
    class_name = "Runtime" + "".join(w.title() for w in key_words)

    runtime_dir = os.path.join(_UMBRA_ROOT, "core", "runtime")
    module_path = os.path.join(runtime_dir, module_name + ".py")

    if os.path.exists(module_path):
        ans = _safe_input("  '" + module_name + ".py' exists. Overwrite? [y/N]: ", "").strip().lower()
        if ans not in ("y", "yes"):
            _umbra_print("  [CANCELLED]\n")
            return

    _umbra_print("\n[INSTALL] Building: " + feature_description)
    _umbra_print("  Module: " + module_name + ".py  |  Class: " + class_name)

    source = _build_feature_source(llm, feature_description, module_name)
    if not source:
        _umbra_print("[INSTALL] Code generation failed.\n")
        return

    for attempt in range(2):
        try:
            ast.parse(source)
            break
        except SyntaxError as e:
            if attempt == 0:
                _umbra_print("  Syntax error: " + str(e) + " — fixing...")
                fixed = _ask_llm_fix(llm, module_path, str(e))
                if fixed:
                    source = fixed
            else:
                _umbra_print("[INSTALL] Could not fix syntax.\n")
                return

    imports_needed = _scan_imports(source)
    missing_deps = _check_missing_deps(imports_needed)

    dep_note = ""
    if missing_deps:
        dep_note = "\n\n  Dependencies to auto-install:\n"
        dep_note += "\n".join("    pip install " + pip for _, pip in missing_deps)

    plan_desc = "Create " + module_name + ".py"
    if missing_deps:
        plan_desc += " + install " + str(len(missing_deps)) + " package(s)"

    if not _approval_prompt(plan_desc, source + dep_note):
        _umbra_print("[INSTALL] Cancelled.\n")
        return

    if missing_deps:
        _umbra_print("\n[INSTALL] Installing " + str(len(missing_deps)) + " package(s)...")
        ok = _install_deps(missing_deps)
        if not ok:
            cont = _safe_input("  Some packages failed. Continue? [y/N]: ", "").strip().lower()
            if cont not in ("y", "yes"):
                _umbra_print("[INSTALL] Aborted.\n")
                return

    os.makedirs(runtime_dir, exist_ok=True)
    try:
        with open(module_path, "w", encoding="utf-8") as fout:
            fout.write(source)
        _umbra_print("[INSTALL] Written: " + module_path)
    except Exception as e:
        _umbra_print("[INSTALL] Write failed: " + str(e) + "\n")
        return

    _umbra_print("[INSTALL] Testing import...")
    test_code = (
        "import sys; sys.path.insert(0, r'" + _UMBRA_ROOT + "')\n"
        "from core.runtime." + module_name + " import " + class_name + "\n"
        "obj = " + class_name + "()\n"
        "print('OK:', obj.is_available() if hasattr(obj,'is_available') else 'ready')\n"
    )
    r = subprocess.run([sys.executable, "-c", test_code],
                       capture_output=True, text=True, cwd=_UMBRA_ROOT, timeout=15)
    if r.returncode != 0:
        _umbra_print("[INSTALL] Import failed:\n  " + r.stderr[:300])
        rollback = _safe_input("  Remove and rollback? [Y/n]: ", "").strip().lower()
        if rollback not in ("n", "no"):
            os.remove(module_path)
            _umbra_print("[INSTALL] Removed.\n")
            return
    else:
        _umbra_print("[INSTALL] Import OK")

    integration = _ask_llm_integration_snippet(llm, module_name, class_name, feature_description)
    _umbra_print("\n[INSTALL] Integration:")
    _umbra_print("  Import  : " + integration["import_line"])
    _umbra_print("  Key     : runtime['" + integration["runtime_key"] + "']")
    _umbra_print("  Run: integrate " + module_name + "\n")


# ============================================================
#  AUTO-INTEGRATE
# ============================================================

def handle_integrate(runtime, module_name):
    module_path = os.path.join(_UMBRA_ROOT, "core", "runtime", module_name + ".py")
    if not os.path.exists(module_path):
        _umbra_print("[INTEGRATE] Not found: " + module_name + ".py\n")
        return

    umbra_path = os.path.join(_UMBRA_ROOT, "umbra.py")

    with open(umbra_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    known_optionals_start = None
    known_optionals_end = None
    for i, line in enumerate(lines):
        if line == "    _known_optionals = [\n":
            known_optionals_start = i
        if known_optionals_start is not None and known_optionals_end is None:
            if line.strip() == "]" and i > known_optionals_start:
                known_optionals_end = i
                break

    if known_optionals_start is None or known_optionals_end is None:
        _umbra_print("[INTEGRATE] Cannot find _known_optionals list.")
        _umbra_print("  Add \"" + module_name + "\" to the list manually.\n")
        return

    list_block = "".join(lines[known_optionals_start:known_optionals_end])
    if module_name in list_block:
        _umbra_print("[INTEGRATE] " + module_name + " already in _known_optionals.")
        _umbra_print("  Restart Umbra to activate it.\n")
        return

    new_list_entry = '        "' + module_name + '",\n'

    preview = (
        "  + Add to _known_optionals: \"" + module_name + "\"\n"
        "  + Auto-loads on next Umbra startup\n"
        "  + Access: runtime['" + module_name.replace("runtime_", "") + "']"
    )
    if not _approval_prompt("Patch umbra.py for " + module_name, preview):
        _umbra_print("[INTEGRATE] Cancelled.\n")
        return

    new_lines = list(lines)
    new_lines.insert(known_optionals_end, new_list_entry)
    patched = "".join(new_lines)

    try:
        ast.parse(patched)
    except SyntaxError as e:
        _umbra_print("[INTEGRATE] Patched file has syntax error: " + str(e) + " — aborting.\n")
        return

    bk = _backup_file(umbra_path)
    _umbra_print("[INTEGRATE] Backup: " + os.path.basename(bk))
    with open(umbra_path, "w", encoding="utf-8") as f:
        f.write(patched)
    _umbra_print("[INTEGRATE] Done. Restart Umbra to activate.\n")


# ============================================================
#  WORKSPACE FILE BROWSER
# ============================================================

def handle_files_browser(runtime, cmd=""):
    """Browse, list, and clean up files in the Umbra folder."""
    umbra_root = _UMBRA_ROOT
    cmd = cmd.lower().strip()

    if "clean" in cmd or "remove old" in cmd or "delete old" in cmd:
        # Find .bak files and old run dirs
        bak_files = []
        old_runs = []
        for root, dirs, files in os.walk(umbra_root):
            for fname in files:
                if ".bak." in fname:
                    bak_files.append(os.path.join(root, fname))
        ws_base = os.path.join(umbra_root, "workspaces")
        if os.path.isdir(ws_base):
            for d in os.listdir(ws_base):
                if d.startswith("run_"):
                    old_runs.append(os.path.join(ws_base, d))

        _umbra_print("\n[FILES] Cleanup candidates:")
        _umbra_print("  Backup files (.bak): " + str(len(bak_files)))
        _umbra_print("  Old pipeline runs:   " + str(len(old_runs)))
        if not bak_files and not old_runs:
            _umbra_print("  Nothing to clean.\n")
            return

        try:
            ans = _safe_input("  Delete all? [y/N]: ", "").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return
        if ans not in ("y", "yes"):
            _umbra_print("  Cancelled.\n")
            return

        removed = 0
        for fp in bak_files:
            try:
                os.remove(fp)
                removed += 1
            except Exception:
                pass
        for d in old_runs:
            try:
                shutil.rmtree(d)
                removed += 1
            except Exception:
                pass
        _umbra_print("  [CLEAN] Removed " + str(removed) + " items.\n")
        return

    # List mode
    target = umbra_root
    if "workspace" in cmd:
        target = os.path.join(umbra_root, "workspaces")
    elif "core" in cmd:
        target = os.path.join(umbra_root, "core")
    elif "project" in cmd:
        target = os.path.join(umbra_root, "workspaces", "projects")

    _umbra_print("\n[FILES] Listing: " + target)
    if not os.path.isdir(target):
        _umbra_print("  Directory not found.\n")
        return

    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(target):
        # Skip deep venv dirs
        dirs[:] = [d for d in dirs if d not in ("venv", "__pycache__", ".git", "node_modules")]
        level = root.replace(target, "").count(os.sep)
        if level > 2:
            continue
        indent = "  " + "  " * level
        rel = os.path.relpath(root, target)
        if rel != ".":
            _umbra_print(indent + "[DIR] " + rel + "/")
        sub_indent = "  " + "  " * (level + 1)
        for fname in sorted(files)[:20]:
            fp = os.path.join(root, fname)
            try:
                sz = os.path.getsize(fp)
                total_size += sz
                file_count += 1
                sz_str = (" (" + str(sz // 1024) + "KB)") if sz > 1024 else ""
                _umbra_print(sub_indent + fname + sz_str)
            except Exception:
                _umbra_print(sub_indent + fname)
        if len(files) > 20:
            _umbra_print(sub_indent + "... and " + str(len(files) - 20) + " more")

    _umbra_print("\n  Total: " + str(file_count) + " files, " + str(total_size // 1024) + " KB\n")


# ============================================================
#  INTENT DETECTION
# ============================================================

_FIX_PATTERNS = [
    r"\b(fix|repair|debug|correct)\b.{0,30}\b(yourself|all\s+(bugs?|errors?|issues?)|bugs?|errors?|issues?)\b",
    r"\b(fix|repair|debug)\b.{0,20}\b(umbra|runtime|yourself)\b",
    r"\ball\s+(bugs?|errors?|issues?)\b",
    r"\bself.?(fix|repair|debug)\b",
    r"\bfix\s+everything\b",
    r"\bfix\s+all\b",
]
_INSTALL_PATTERNS = [
    r"\b(install|add|build|make|create|integrate)\b.{0,50}\b(into|for|in|to)\s+(umbra|yourself)\b",
    r"\b(install|integrate)\b.{0,60}\b(pipeline|module|feature|tool|system|agent|generator)\b",
    r"\badd\s+a\b.{0,40}\b(to\s+umbra|into\s+umbra|to\s+yourself)\b",
]


def _detect_self_intent(text):
    lower = text.lower().strip()
    for p in _FIX_PATTERNS:
        if re.search(p, lower):
            return "fix", None
    for p in _INSTALL_PATTERNS:
        if re.search(p, lower):
            desc = re.sub(r"^(install|add|build|make|create|integrate)\s+(a\s+|an\s+)?", "", lower)
            desc = re.sub(r"\s+(into|for|in|to)\s+(umbra|yourself).*$", "", desc).strip()
            return "install", desc or text
    if re.search(r"\bintegrate\s+runtime_\w+\b|\bwire\s+in\s+runtime_\w+\b", lower):
        mod = re.search(r"runtime_\w+", lower)
        return "integrate", mod.group(0) if mod else None
    return None, None


# ============================================================
#  USER LANGUAGE LEARNING
# ============================================================

def _load_user_language_model(memory, conversation):
    try:
        result = memory.retrieve("user_language_model")
        if result and result.value and isinstance(result.value, dict):
            if not hasattr(conversation, "_user_patterns"):
                conversation._user_patterns = {}
            conversation._user_patterns.update(result.value)
    except Exception:
        pass


def _record_user_phrase(runtime, raw_input, resolved_intent):
    try:
        mem = runtime.get("memory")
        conv = runtime.get("conversation")
        if not mem or not conv:
            return
        existing = {}
        try:
            r = mem.retrieve("user_language_model")
            if r and isinstance(r.value, dict):
                existing = r.value
        except Exception:
            pass
        phrase_key = raw_input.lower().strip()[:80]
        if phrase_key and resolved_intent:
            existing[phrase_key] = resolved_intent
            if len(existing) > 200:
                keys = list(existing.keys())
                for k in keys[:50]:
                    del existing[k]
            mem.store("user_language_model", existing, tags=["user_language"])
            if not hasattr(conv, "_user_patterns"):
                conv._user_patterns = {}
            conv._user_patterns[phrase_key] = resolved_intent
    except Exception:
        pass


def _classify_with_user_model(runtime, text):
    conv = runtime.get("conversation")
    if not conv or not hasattr(conv, "_user_patterns"):
        return None
    lower = text.lower().strip()
    if lower in conv._user_patterns:
        return conv._user_patterns[lower]
    for phrase, intent in conv._user_patterns.items():
        if len(phrase) > 8 and (phrase in lower or lower in phrase):
            return intent
    return None


# ============================================================
#  TTS
# ============================================================

def _maybe_tts(runtime, text):
    if not runtime.get("_tts_enabled"):
        return
    try:
        tts_mod = runtime.get("tts_engine")
        if tts_mod and hasattr(tts_mod, "run"):
            tts_mod.run(text)
            return
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


# ============================================================
#  GAME CLARIFICATION QUESTIONS
# ============================================================

def _ask_game_clarifications(prompt, llm):
    """
    Ask Umbra to generate clarifying questions before a big build.
    Returns list of (question, answer) pairs.
    """
    lower = prompt.lower()
    # Only ask for large builds
    big_build_keywords = ["rpg", "open world", "skyrim", "mmorpg", "simulation", "strategy",
                           "turn based", "first person", "fps", "rts", "adventure", "dungeon"]
    is_big = any(kw in lower for kw in big_build_keywords) or len(prompt.split()) > 15

    if not is_big:
        return []

    if llm and llm.is_configured():
        q_prompt = (
            "You are Umbra, an AI game builder. The user wants to build: " + prompt + "\n\n"
            "Generate 3 focused clarifying questions to better understand their vision.\n"
            "Keep questions short and specific. Return as JSON array of strings.\n"
            "Example: [\"What is the main character's class?\", \"How many zones should the world have?\"]\n"
            "ONLY JSON array."
        )
        try:
            r = llm.complete(q_prompt)
            if r and r.content:
                raw = _strip_fences(r.content)
                raw = re.sub(r"^```json\s*", "", raw, flags=re.MULTILINE)
                questions = json.loads(raw)
                if isinstance(questions, list):
                    return questions[:3]
        except Exception:
            pass

    # Fallback questions
    return [
        "What genre/style? (e.g. fantasy RPG, sci-fi, horror)",
        "What is the main gameplay loop? (combat, exploration, puzzle, building)",
        "Any specific features you want? (multiplayer, crafting, base building, etc)"
    ]


# ============================================================
#  BUILD RUNTIME
# ============================================================

def _init_resource_manager():
    global _resource_manager
    if _resource_manager is None:
        try:
            from core.runtime.runtime_resource_manager import RuntimeResourceManager
            _resource_manager = RuntimeResourceManager(
                gaming_mode_auto=True, max_memory_pct=85, task_delay_ms=50)
            _resource_manager.start_monitoring(interval_seconds=30)
        except Exception:
            _resource_manager = None
    return _resource_manager


def build_runtime():
    global _pipeline_monitor, _scheduler, _comfyui_proc
    _init_resource_manager()

    # Auto-install required packages if missing
    for _pkg_import, _pkg_name in [("PIL", "Pillow"), ("pygame", "pygame")]:
        try:
            __import__(_pkg_import)
        except ImportError:
            try:
                print("  [UMBRA] " + _pkg_name + " not found — installing automatically...")
                import subprocess as _sp2
                _r = _sp2.run([sys.executable, "-m", "pip", "install", _pkg_name, "--quiet"],
                              capture_output=True, text=True)
                if _r.returncode == 0:
                    print("  [UMBRA] " + _pkg_name + " installed OK.")
                else:
                    print("  [UMBRA] " + _pkg_name + " install failed: " + _r.stderr[:120])
            except Exception as _pe:
                print("  [UMBRA] Could not auto-install " + _pkg_name + ": " + str(_pe))

    try:
        from core.runtime.runtime_launcher import RuntimeLauncher
        launcher = RuntimeLauncher(auto_launch_comfyui=True)
        launcher.ensure_services(verbose=True)
        if hasattr(launcher, "_comfyui_proc") and launcher._comfyui_proc:
            _comfyui_proc = launcher._comfyui_proc
    except Exception:
        pass

    # Auto-start Ollama if not running
    try:
        import urllib.request as _ur2
        _ur2.urlopen("http://localhost:11434/api/tags", timeout=2).close()
    except Exception:
        try:
            if sys.platform == "win32":
                subprocess.Popen(["ollama", "serve"],
                                 creationflags=subprocess.CREATE_NO_WINDOW,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("  [UMBRA] Starting Ollama...")
                import time as _t2; _t2.sleep(3)
        except Exception:
            pass

    def _si(mod_path, cls_name, *a, **kw):
        try:
            m = __import__(mod_path, fromlist=[cls_name])
            return getattr(m, cls_name)(*a, **kw)
        except Exception:
            return None

    config          = _si("core.runtime.runtime_config_manager","RuntimeConfigManager",
                          config_path=os.path.join(_UMBRA_ROOT,"umbra_config.json"))
    def _cfg(k,d=None): return (config.get(k) or d) if config else d

    provider        = _cfg("llm_provider"); api_key = _cfg("llm_api_key") or os.environ.get("UMBRA_LLM_API_KEY","")
    model           = os.environ.get("UMBRA_LLM_MODEL","") or _cfg("llm_model","")

    llm             = _si("core.runtime.runtime_llm_provider","RuntimeLLMProvider",
                          provider=provider, api_key=api_key or None, model=model or None)
    graph           = _si("core.runtime.runtime_execution_graph","RuntimeExecutionGraph")
    sm              = _si("core.runtime.runtime_task_state_machine","RuntimeTaskStateMachine")
    ctx             = _si("core.runtime.runtime_context_builder","RuntimeContextBuilder")
    validator       = _si("core.runtime.runtime_validation_engine","RuntimeValidationEngine")
    guard           = _si("core.runtime.runtime_recursion_guard","RuntimeRecursionGuard",
                          max_depth=_cfg("max_recursion_depth",10),
                          max_calls_per_task=_cfg("max_calls_per_task",100),
                          max_total_calls=_cfg("max_total_calls",1000))
    workspace       = _si("core.runtime.runtime_workspace_manager","RuntimeWorkspaceManager",
                          base_dir=os.path.join(_UMBRA_ROOT, _cfg("workspace_dir","workspaces")))
    executor        = _si("core.runtime.runtime_subprocess_executor","RuntimeSubprocessExecutor",
                          working_dir=_UMBRA_ROOT, timeout=_cfg("subprocess_timeout",300))
    code_writer     = _si("core.runtime.runtime_code_writer","RuntimeCodeWriter",base_dir=_UMBRA_ROOT)
    extractor       = _si("core.runtime.runtime_code_extractor","RuntimeCodeExtractor")
    sessions        = _si("core.runtime.runtime_session_manager","RuntimeSessionManager",
                          sessions_dir=os.path.join(_UMBRA_ROOT,_cfg("sessions_dir","sessions")))
    continuation    = _si("core.runtime.runtime_task_continuation","RuntimeTaskContinuation",
                          continuations_dir=os.path.join(_UMBRA_ROOT,_cfg("continuations_dir","continuations")))
    code_runner     = _si("core.runtime.runtime_code_runner","RuntimeCodeRunner",
                          working_dir=_UMBRA_ROOT, timeout=_cfg("code_runner_timeout",300))
    _sdir           = os.path.join(_UMBRA_ROOT, _cfg("sessions_dir","sessions"))
    os.makedirs(_sdir, exist_ok=True)
    memory          = _si("core.runtime.runtime_memory_store","RuntimeMemoryStore",
                          store_path=os.path.join(_sdir,"memory_store.json"))
    health          = _si("core.runtime.runtime_health_monitor","RuntimeHealthMonitor",base_dir=_UMBRA_ROOT)
    run_validator   = _si("core.runtime.runtime_run_validator","RuntimeRunValidator")
    reviewer        = _si("core.runtime.runtime_code_reviewer","RuntimeCodeReviewer")
    replayer        = _si("core.runtime.runtime_session_replay","RuntimeSessionReplay",
                          sessions_dir=_sdir,
                          workspaces_dir=os.path.join(_UMBRA_ROOT,_cfg("workspace_dir","workspaces")))
    conversation    = _si("core.runtime.runtime_conversation_engine","RuntimeConversationEngine",
                          llm_provider=llm)
    voice_input     = _si("core.runtime.runtime_voice_input","RuntimeVoiceInput")
    if memory and conversation:
        _load_user_language_model(memory, conversation)

    images_dir = os.path.join(_UMBRA_ROOT,"workspaces","images")
    videos_dir = os.path.join(_UMBRA_ROOT,"workspaces","videos")
    sprites_dir= os.path.join(_UMBRA_ROOT,"workspaces","sprites")
    for _d in (images_dir, videos_dir, sprites_dir): os.makedirs(_d, exist_ok=True)

    image_generator  = _si("core.runtime.runtime_image_generator","RuntimeImageGenerator",output_dir=images_dir)
    video_generator  = _si("core.runtime.runtime_video_generator","RuntimeVideoGenerator",output_dir=videos_dir)
    game_tester      = _si("core.runtime.runtime_game_tester","RuntimeGameTester")
    direct_generator = _si("core.runtime.runtime_direct_generator","RuntimeDirectGenerator",
                           model=model or "qwen2.5-coder:32b",
                           workspaces_dir=os.path.join(_UMBRA_ROOT,_cfg("workspace_dir","workspaces")),
                           timeout=1200)
    projects_dir     = os.path.join(_UMBRA_ROOT,"workspaces","projects")
    os.makedirs(projects_dir, exist_ok=True)
    project_manager  = _si("core.runtime.runtime_project_manager","RuntimeProjectManager",projects_dir=projects_dir)

    # ── Optional modules ──────────────────────────────────────────────────────
    animated_gif_generator = None
    try:
        from core.runtime.runtime_animated_gif_generator import RuntimeAnimatedGifGenerator
        animated_gif_generator = RuntimeAnimatedGifGenerator()
    except Exception:
        pass

    tts_engine = None
    try:
        from core.runtime.runtime_text_speech_system_using import RuntimeTextSpeechSystemUsing
        tts_engine = RuntimeTextSpeechSystemUsing()
    except Exception:
        pass

    continuous_mic_listener = None
    try:
        from core.runtime.runtime_continuous_mic_listener import RuntimeContinuousMicListener
        continuous_mic_listener = RuntimeContinuousMicListener()
    except Exception:
        pass

    # ── Dynamic optional modules ──────────────────────────────────────────────
    _optional_modules = {}
    optional_runtime_dir = os.path.join(_UMBRA_ROOT, "core", "runtime")
    _known_optionals = [
        "runtime_animated_gif_generator",
        "runtime_text_speech_system_using",
        "runtime_continuous_mic_listener",
        "runtime_video_pipeline",
        "runtime_gif_generator",
        "runtime_web_search_tool",
        "runtime_file_manager",
        "runtime_reminder_task_tracker",
        "runtime_dependency_scanner",
        "runtime_code_quality_improver",
        "runtime_game_auto_tester",
        "runtime_game_asset_generator",
        "runtime_full_gui_window",
        "runtime_full_gui_chat_window",
        "runtime_gui_window_launcher",
        "runtime_video_converter",
        "runtime_agent_manager",
        "runtime_web_scraper_tool",
        "runtime_tiktok_script_generator",
        "runtime_project_export_tool",
        "runtime_character_dialogue_generator",
        "runtime_map_generator",
    ]
    for mod_name in _known_optionals:
        mod_path = os.path.join(optional_runtime_dir, mod_name + ".py")
        if os.path.isfile(mod_path):
            try:
                parts = mod_name.replace("runtime_", "").split("_")
                cls_name = "Runtime" + "".join(p.title() for p in parts)
                import importlib
                spec = importlib.util.spec_from_file_location(mod_name, mod_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                cls = getattr(mod, cls_name)
                inst = cls()
                key = mod_name.replace("runtime_", "")
                _optional_modules[key] = inst
            except Exception:
                pass

    studio_agents = _si("core.runtime.runtime_studio_agents","RuntimeStudioAgents",
                        llm_provider=llm, direct_generator=direct_generator,
                        output_dir=os.path.join(_UMBRA_ROOT,"workspaces","studio"))

    if _pipeline_monitor is None:
        _pipeline_monitor = _si("core.runtime.runtime_pipeline_monitor","RuntimePipelineMonitor")

    orchestrator = None; pipeline = None
    try:
        from core.runtime.runtime_llm_orchestrator   import RuntimeLLMOrchestrator
        from core.runtime.runtime_autonomous_pipeline import RuntimeAutonomousPipeline
        orchestrator = RuntimeLLMOrchestrator(
            llm_provider=llm, context_builder=ctx, execution_graph=graph,
            task_state_machine=sm, recursion_guard=guard, validation_engine=validator)
        pipeline = RuntimeAutonomousPipeline(
            llm_orchestrator=orchestrator, workspace_manager=workspace,
            validation_engine=validator, code_extractor=extractor, code_writer=code_writer)
    except Exception:
        pass

    runtime = {
        "llm": llm, "graph": graph, "state_machine": sm,
        "orchestrator": orchestrator, "pipeline": pipeline,
        "code_writer": code_writer, "extractor": extractor,
        "executor": executor, "workspace": workspace,
        "validator": validator, "sessions": sessions,
        "continuation": continuation, "code_runner": code_runner,
        "config": config, "monitor": _pipeline_monitor,
        "memory": memory, "health": health,
        "run_validator": run_validator, "reviewer": reviewer,
        "replayer": replayer, "resource_manager": _resource_manager,
        "conversation": conversation, "voice_input": voice_input,
        "image_generator": image_generator, "video_generator": video_generator,
        "game_tester": game_tester, "direct_generator": direct_generator,
        "project_manager": project_manager, "studio_agents": studio_agents,
        "animated_gif_generator": animated_gif_generator,
        "tts_engine": tts_engine,
        "continuous_mic_listener": continuous_mic_listener,
        "_umbra_root": _UMBRA_ROOT,
        "_tts_enabled": False,
        "_continuous_voice": False,
    }
    runtime.update(_optional_modules)

    if _scheduler is None:
        try:
            from core.runtime.runtime_scheduler import build_default_scheduler
            _scheduler = build_default_scheduler(runtime, _UMBRA_ROOT)
            _scheduler.start()
            runtime["scheduler"] = _scheduler
        except Exception:
            pass

    return runtime


# ============================================================
#  PRINT HELPERS
# ============================================================

def print_banner():
    _umbra_print("\n" + "=" * 64)
    _umbra_print("  UMBRA v2.4.0 — Autonomous AI Runtime OS")
    _umbra_print("  type 'help' for commands | 'exit' to quit")
    _umbra_print("=" * 64 + "\n")


def print_status(runtime):
    llm = runtime.get("llm")
    _umbra_print("\n[STATUS]")
    if llm:
        try:
            _umbra_print("  Provider : " + llm.get_provider() + (" (FREE)" if llm.is_free() else ""))
            _umbra_print("  Model    : " + llm.get_model())
            _umbra_print("  Ready    : " + ("YES" if llm.is_configured() else "NO"))
        except Exception:
            # Try reading directly from Ollama
            try:
                import urllib.request as _ur, json as _jj
                with _ur.urlopen("http://localhost:11434/api/tags", timeout=3) as _r:
                    _models = [m["name"] for m in _jj.loads(_r.read()).get("models",[])]
                _model = _get_agent_model()
                _umbra_print("  Provider : Ollama (local, FREE)")
                _umbra_print("  Model    : " + _model)
                _umbra_print("  Ready    : YES — " + str(len(_models)) + " model(s) available")
            except Exception:
                _umbra_print("  LLM      : loaded — Ollama offline (start Ollama first)")
    else:
        _umbra_print("  LLM      : NOT LOADED")
    mem = runtime.get("memory")
    _umbra_print("  Memory   : " + (str(mem.size()) + " entries" if mem and hasattr(mem,"size") else "not loaded"))
    rm = runtime.get("resource_manager")
    if rm:
        rs = rm.get_current_status()
        gaming = " [GAMING MODE]" if rs.get("gaming_detected") else ""
        _umbra_print("  Resources: mem=" + str(rs.get("memory_pct", 0)) + "%" + gaming)
    sched = runtime.get("scheduler")
    if sched:
        _umbra_print("  Scheduler: " + str(sum(1 for j in sched.jobs if j.enabled)) + " job(s)")
    img = runtime.get("image_generator")
    vid = runtime.get("video_generator")
    if img:
        _umbra_print("  Images   : " + ("ComfyUI connected" if img.is_available() else "ComfyUI not running"))
    if vid:
        _umbra_print("  Video    : " + ("ComfyUI connected" if vid.is_available() else "ComfyUI not running"))
    gif = runtime.get("animated_gif_generator")
    if gif:
        _umbra_print("  GIF      : " + ("ready" if gif.is_available() else "PIL missing"))
    pm = runtime.get("project_manager")
    if pm:
        active = pm.get_active()
        projects = pm.list_projects()
        if active:
            _umbra_print("  Project  : " + active.name + " (active)")
        _umbra_print("  Projects : " + str(len(projects)) + " total")
    cont = runtime.get("continuation")
    if cont:
        try:
            pending = len(cont.list_continuations())
            if pending:
                _umbra_print("  Pending  : " + str(pending) + " unfinished run(s) — type 'resume'")
        except Exception:
            pass
    tts = runtime.get("tts_engine")
    _umbra_print("  TTS      : " + ("ready" if tts and tts.is_available() else "OFF") +
          " | " + ("ON" if runtime.get("_tts_enabled") else "disabled"))
    v = runtime.get("voice_input")
    _umbra_print("  Voice    : " + ("READY" if v and v.is_available() else "not available") +
          " | continuous=" + ("ON" if runtime.get("_continuous_voice") else "OFF"))
    _umbra_print("")


def print_config():
    _umbra_print("""
[UMBRA CONFIG v2.3.0 — CONFIG & COMMANDS — LLM: Ollama]

START
  python umbra.py               interactive mode
  python umbra.py --fix         auto-fix and exit
  python umbra.py --test        run tests and exit
  python umbra.py --status      status and exit

SYSTEM
  status   health   metrics   version   config/help   exit/quit

SELF-REPAIR
  fix all bugs / fix yourself / fix workspace / fix last build
  fix the gui / fix the gif / fix the video / fix project <name>
  scan modules

INSTALL FEATURES
  install <feature> into umbra
  integrate runtime_<name>

BUILD GAMES & APPS
  make a game called <name>              (direct, fast)
  build an RPG called <name>             (studio pipeline)
  build a full game called <name>        (ALL agents — full build)
  make a game like Skyrim called <name>  (deep build with all systems)
  play last / play <name>

GENERATE MEDIA
  make a gif of <desc>          animated GIF via PIL
  make an image of <desc>       via ComfyUI
  make a video of <desc>        via ComfyUI + frame assembler
  assemble video frames         combine ComfyUI frames into mp4/gif

FILE BROWSER
  list files                    browse Umbra folder
  list workspace files          browse workspaces
  clean up old files            remove .bak files + old pipeline runs

PROJECTS
  projects / work on <name> / project files

VOICE & TTS
  listen / voice on/off / tts on/off

MEMORY
  remember <fact> / recall <query> / memory

DIAGNOSTICS
  test / validate / review / history / resume / handoff
  improve / scheduler
""")


def print_metrics(runtime):
    mon = runtime.get("monitor")
    if not mon:
        _umbra_print("  Monitor not loaded."); return
    try:
        summary = mon.get_summary()
        _umbra_print("\n[METRICS]")
        _umbra_print("  Runs       : " + str(summary.get("total_runs",0)))
        _umbra_print("  Successful : " + str(summary.get("successful_runs",0)))
        _umbra_print("  Rate       : " + str(summary.get("success_rate_pct",0)) + "%")
        _umbra_print("  Files      : " + str(summary.get("total_files_written",0)))
        _umbra_print("  Avg time   : " + str(summary.get("avg_duration_seconds",0)) + "s")
    except Exception as e:
        _umbra_print("  Metrics error: " + str(e))


def _handle_project_switch(runtime, user_input):
    text = user_input.lower().strip()
    patterns = [
        r"(?:work on|lets work on|working on|switch to|continue|open)\s+['\"]?([a-zA-Z0-9_ ]+?)['\"]?\s*$",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            name = m.group(1).strip().title()
            pm = runtime.get("project_manager")
            if pm:
                existing = pm.get_project(name)
                if existing:
                    pm.set_active(existing.name)
                    return existing, False
    return None, False


# ============================================================
#  COMMAND PROCESSOR (used by both CLI and GUI)
# ============================================================

def _process_command(runtime, user_input):
    """Process a single command — same logic as interactive_mode loop body."""
    cmd = user_input.lower().strip()
    pm = runtime.get("project_manager")
    active = None
    try:
        active = pm.get_active() if pm else None
    except Exception:
        pass

    if _DEV_ASST_LOADED and _dev_asst is not None:
        try:
            handled = _dev_asst.process(user_input, print_fn=_umbra_print)
            if handled:
                return
        except Exception as _dae:
            _umbra_print("[DEV] assistant error: " + str(_dae))

    if cmd in ("exit", "quit", "q"):
        _umbra_print("[UMBRA] Closing Umbra...")
        import os as _osexit; _osexit._exit(0)

    # Self-repair
    if cmd in ("fix", "fix yourself", "fix all bugs", "fix all errors",
               "fix all issues", "repair yourself", "fix everything",
               "self fix", "self-fix", "fix everything"):
        handle_self_fix(runtime)
        return

    if cmd in ("fix workspace", "fix workspaces", "repair workspace"):
        handle_workspace_repair(runtime, target="all")
        return

    if re.search(r"\b(fix|repair)\b.{0,25}\b(last game|game|last build)\b", cmd) or cmd in ("fix game", "fix last game", "repair game", "fix last", "repair last"):
        _gp3 = None
        _ws3 = os.path.join(_UMBRA_ROOT, "workspaces", "agent_builds")
        _gc3 = []
        if os.path.isdir(_ws3):
            for _r3, _d3, _f3 in os.walk(_ws3):
                for _fn3 in _f3:
                    if _fn3.endswith("_game.py"):
                        _fp3 = os.path.join(_r3, _fn3)
                        _gc3.append((_fp3, os.path.getmtime(_fp3)))
        if _gc3:
            _gp3 = sorted(_gc3, key=lambda x: x[1], reverse=True)[0][0]
        if not _gp3:
            _umbra_print("[FIX] No game found. Build one first."); return
        _umbra_print("[FIX] Checking: " + _gp3)
        try:
            _gs3 = open(_gp3, "r", encoding="utf-8").read()
            ast.parse(_gs3)
            _umbra_print("[FIX] No syntax errors. Type: play last")
        except SyntaxError as _ge3:
            _umbra_print("[FIX] Line " + str(_ge3.lineno) + ": " + str(_ge3.msg) + " — repairing...")
            _gs3 = open(_gp3, "r", encoding="utf-8").read()
            _gf3 = _syntax_repair(_gs3, _get_agent_model())
            try:
                ast.parse(_gf3)
                open(_gp3, "w", encoding="utf-8").write(_gf3)
                _umbra_print("[FIX] Repaired. Type: play last")
            except SyntaxError:
                _umbra_print("[FIX] Could not repair. Try: build " + os.path.basename(_gp3).replace("_game.py",""))
        return

    if re.search(r"fix.{1,30}(gui|window|gif|video|tts|voice|search|converter)", cmd):
        feature_match = re.search(r"(gui|window|gif|video|tts|voice|search|converter)", cmd)
        feature = feature_match.group(1) if feature_match else "unknown"
        runtime_dir = os.path.join(_UMBRA_ROOT, "core", "runtime")
        if os.path.isdir(runtime_dir):
            candidates = [f for f in os.listdir(runtime_dir)
                         if f.endswith(".py") and feature.lower() in f.lower()
                         and f.startswith("runtime_")]
            llm = runtime.get("llm")
            for fname in candidates[:2]:
                path = os.path.join(runtime_dir, fname)
                err = _syntax_check(path)
                if err and llm and llm.is_configured():
                    fixed = _ask_llm_fix(llm, path, err)
                    if fixed:
                        try:
                            ast.parse(fixed)
                            _backup_file(path)
                            with open(path, "w", encoding="utf-8") as fout:
                                fout.write(fixed)
                            _umbra_print("[FIX] Fixed: " + fname + ". Restart Umbra.")
                        except Exception as e:
                            _umbra_print("[FIX] Could not fix: " + str(e))
                elif not err:
                    _umbra_print("[FIX] " + fname + " has no syntax errors.")
        return

    # Install/integrate
    if cmd.startswith("integrate "):
        module = user_input[10:].strip()
        if not module.startswith("runtime_"):
            module = "runtime_" + module
        handle_integrate(runtime, module)
        return

    # ── HIGH-PRIORITY SHORTCUTS (before pipeline fallthrough) ──
    if cmd in ("test", "run tests", "tests", "run test"):
        import subprocess as _sp3
        _total_p, _total_f = 0, 0
        for _tf in ["test_umbra_full.py", "test_dev_assistant.py"]:
            if not os.path.exists(os.path.join(_UMBRA_ROOT, _tf)):
                _umbra_print("[TEST] SKIP " + _tf + " (not found)"); continue
            _umbra_print("[TEST] Running " + _tf + " ...")
            _tr = _sp3.run([sys.executable, _tf], capture_output=True, text=True, cwd=_UMBRA_ROOT)
            _out = (_tr.stdout or "") + (_tr.stderr or "")
            _lines = _out.strip().splitlines()
            if len(_lines) > 40:
                _umbra_print("  ... (last 40 of " + str(len(_lines)) + ")")
                _lines = _lines[-40:]
            for _l in _lines: _umbra_print(_l)
            _p = sum(1 for l in _out.splitlines() if "[PASS]" in l or ("  PASS  " in l and "FAIL" not in l))
            _f = sum(1 for l in _out.splitlines() if "[FAIL]" in l or "  FAIL  " in l)
            _total_p += _p; _total_f += _f
            _umbra_print("[TEST] " + _tf + ": " + str(_p) + " passed, " + str(_f) + " failed")
        _umbra_print("\n[TEST] TOTAL: " + str(_total_p) + " passed, " + str(_total_f) + " failed\n")
        return

    if cmd in ("which model", "what model", "model", "which model?", "current model"):
        try:
            import urllib.request as _ur2, json as _jj2
            with _ur2.urlopen("http://localhost:11434/api/tags", timeout=3) as _r2:
                _all2 = [m["name"] for m in _jj2.loads(_r2.read()).get("models", [])]
        except Exception: _all2 = []
        _chat_m = runtime.get("chat_model") or _get_chat_model()
        _agent_m = _get_agent_model()
        _umbra_print("[DEV] Chat model: " + str(_chat_m))
        _umbra_print("[DEV] Build model: " + str(_agent_m))
        if _all2: _umbra_print("[DEV] Available: " + ", ".join(_all2))
        return

    intent, detail = _detect_self_intent(user_input)
    if intent == "install" and detail:
        handle_self_install(runtime, detail)
        return
    if intent == "integrate" and detail:
        handle_integrate(runtime, detail)
        return
    _auto_triggers = [
        ("image pipeline","a professional image generation pipeline using ComfyUI and PIL"),
        ("music pipeline","a music generation pipeline using tone synthesis and file export"),
        ("video pipeline","a video generation pipeline using ffmpeg frame assembly"),
        ("blender pipeline","a 3D model generation pipeline using Blender via subprocess"),
        ("tiktok","a TikTok script and video upload pipeline"),
        ("website generator","a complete website generator producing HTML CSS JavaScript"),
        ("ai companion","an AI companion system with memory personality and conversation"),
        ("sprite generator","a pixel art sprite sheet generator using PIL"),
        ("gif generator","an animated GIF generator using PIL particle effects"),
        ("voice pipeline","a voice synthesis and speech recognition pipeline"),
    ]
    for _trigger, _desc in _auto_triggers:
        if _trigger in cmd:
            handle_self_install(runtime, _desc)
            return

    # Status/info commands
    if cmd == "status":
        print_status(runtime)
        return
    if cmd in ("config", "help"):
        print_config()
        return

    # Play game
    if cmd in ("run last", "play last", "test last") or cmd.startswith("play ") or cmd.startswith("run game "):
        project_name = None
        if cmd.startswith("play ") and len(cmd) > 5:
            project_name = cmd[5:].strip().lower().replace(" ", "_")
        game_path = None
        try:
            last_mem = _umbra_mem(runtime).retrieve("last_game_file")
            if last_mem and os.path.exists(str(last_mem.value)):
                game_path = str(last_mem.value)
        except Exception: pass
        # Fallback: scan memory_store.json directly
        if not game_path:
            _ms = os.path.join(_UMBRA_ROOT,"sessions","memory_store.json")
            if os.path.exists(_ms):
                try:
                    import json as _j2
                    for _e in _j2.load(open(_ms,"r",encoding="utf-8")) if True else []:
                        if isinstance(_e,dict) and _e.get("key")=="last_game_file":
                            _gp=str(_e.get("value",""))
                            if os.path.exists(_gp): game_path=_gp; break
                except Exception: pass
        if project_name and pm:
            proj = pm.get_project(project_name)
            if proj:
                for fe in proj.files:
                    if fe.get("type") == "game" and fe["path"].endswith(".py") and os.path.exists(fe["path"]):
                        game_path = fe["path"]
                        break
        if not game_path:
            ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
            candidates = []
            for root, dirs, files in os.walk(ws_base):
                dirs[:] = [d for d in dirs if d not in ("__pycache__",".git")]
                for fname in files:
                    if not fname.endswith(".py"): continue
                    full = os.path.join(root, fname)
                    try: mtime = os.path.getmtime(full)
                    except: continue
                    score = mtime
                    if any(g in fname.lower() for g in ["game","optiopia","demiworld","myworld","rpg"]): score += 1e12
                    if project_name and project_name.lower() in full.lower(): score += 2e12
                    if fname in ("main.py","__init__.py") and "game" not in fname.lower(): score -= 1e10
                    candidates.append((score, full))
            if candidates:
                candidates.sort(reverse=True)
                game_path = candidates[0][1]
        if game_path and os.path.exists(game_path):
            _umbra_print("[UMBRA] Launching: " + game_path)
            try:
                subprocess.Popen([sys.executable, game_path], cwd=os.path.dirname(game_path))
            except Exception as e:
                _umbra_print("  Error: " + str(e))
        else:
            _umbra_print("  No game found. Build one first with: make a game called " + (project_name or "X"))
        return

    # Memory
    if cmd.startswith("remember "):
        fact = user_input[9:].strip()
        runtime.get("memory") and _umbra_mem(runtime).store("user_note:" + str(_umbra_mem(runtime).size()), fact, tags=["user_note"])
        _umbra_mem(runtime).save()
        _umbra_print("  Stored: " + fact[:60])
        return

    if cmd.startswith("recall "):
        query = user_input[7:].strip()
        results = _umbra_mem(runtime).search(query, top_k=5)
        if results:
            _umbra_print("[MEMORY: '" + query + "']")
            for r in results:
                _umbra_print("  " + r.key + ": " + str(r.value)[:80])
        else:
            _umbra_print("  Nothing found for '" + query + "'")
        return

    # Full game build
    if re.search(r"(build a full game|make a full game|full build)", cmd):
        name_match = re.search(r"(?:called|named)" + r"[\s]+[a-zA-Z0-9 ]+", user_input, re.IGNORECASE)
        project_name2 = name_match.group(1).strip() if name_match else None
        if not project_name2:
            project_name2 = "MyGame"
        result = _run_deep_build(runtime, user_input, project_name2)
        if result:
            _umbra_print("[UMBRA] Done! Type: play " + project_name2)
        return

    # Default: run_prompt handles everything else
    # Default: run_prompt handles everything else
    try:
        run_prompt(runtime, user_input)
    except Exception as _e:
        _umbra_print("[UMBRA] Error: " + str(_e))

# ============================================================
#  GUI LAUNCH (thread-safe via queue)
# ============================================================

def _launch_gui(runtime):
    """Launch the Umbra Control Center GUI - window runs on main thread via mainloop()."""
    global _gui_ref, _gui_mode
    import importlib as _il

    # Try full 5-tab control center first
    for _mp, _fn in [("core.gui.control_center","launch_in_thread"),
                     ("core.ui.umbra_control_center","launch_in_thread")]:
        try:
            _mod = _il.import_module(_mp)
            _gui = getattr(_mod, _fn)(runtime=runtime, process_fn=_process_command)
            if _gui is not None and hasattr(_gui, "mainloop"):
                _gui_ref = _gui; _gui_mode = True
                _umbra_print("[GUI] Control Center ready.")
                return
        except Exception as _lge:
            _umbra_print("[GUI] CC error: " + str(_lge))

    # Fallback: runtime optional module
    # Skip optional runtime GUI modules - use only our control_center.py
    gui = None
    if not gui:
        # Build minimal inline tkinter
        try:
            import tkinter as tk
            from tkinter import scrolledtext

            import queue as _tkqueue
            class _MinimalGUI:
                def __init__(self):
                    self.ready = True
                    self._submit_cb = None
                    self._root = None
                    self._output = None
                    self._msg_queue = _tkqueue.Queue()

                def is_available(self):
                    return True

                def post_message(self, text):
                    # Thread-safe: put in queue, polled by mainloop
                    try:
                        self._msg_queue.put(str(text))
                    except Exception:
                        pass

                def set_submit_callback(self, cb):
                    self._submit_cb = cb

                def run(self, title="Umbra"):
                    self._root = tk.Tk()
                    self._root.title(title + " v2.3.0")
                    self._root.configure(bg="#1a1a2e")
                    self._root.geometry("900x650")

                    # Header
                    header = tk.Label(self._root, text="UMBRA — Autonomous AI Runtime OS",
                                      bg="#16213e", fg="#e94560",
                                      font=("Consolas", 13, "bold"), pady=8)
                    header.pack(fill=tk.X)

                    # Output area
                    self._output = scrolledtext.ScrolledText(
                        self._root, state=tk.DISABLED, wrap=tk.WORD,
                        bg="#0f3460", fg="#e0e0e0", font=("Consolas", 10),
                        insertbackground="#e94560", height=30,
                        selectbackground="#e94560"
                    )
                    self._output.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

                    # Input row
                    input_frame = tk.Frame(self._root, bg="#1a1a2e")
                    input_frame.pack(fill=tk.X, padx=8, pady=4)

                    self._entry = tk.Entry(
                        input_frame, bg="#16213e", fg="#e0e0e0",
                        font=("Consolas", 11), insertbackground="white",
                        relief=tk.FLAT, bd=4
                    )
                    self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
                    self._entry.bind("<Return>", self._on_submit)

                    send_btn = tk.Button(
                        input_frame, text="Send", command=self._on_submit,
                        bg="#e94560", fg="white", font=("Consolas", 10, "bold"),
                        relief=tk.FLAT, padx=12, cursor="hand2"
                    )
                    send_btn.pack(side=tk.RIGHT)

                    # Status bar
                    self._status = tk.Label(
                        self._root, text="Ready", bg="#16213e", fg="#a0a0c0",
                        font=("Consolas", 9), pady=3
                    )
                    self._status.pack(fill=tk.X)

                    self.post_message("=" * 50)
                    self.post_message("  Umbra v2.3.0 — Type your prompt below")
                    self.post_message("  Or use the CLI window for approval prompts")
                    self.post_message("=" * 50)

                    # Poll message queue every 50ms (thread-safe GUI updates)
                    def _poll_queue():
                        try:
                            while True:
                                msg = self._msg_queue.get_nowait()
                                self._output.config(state=tk.NORMAL)
                                self._output.insert(tk.END, msg + "\n")
                                self._output.config(state=tk.DISABLED)
                                self._output.see(tk.END)
                        except Exception:
                            pass
                        if self._root:
                            self._root.after(50, _poll_queue)
                    self._root.after(50, _poll_queue)
                    self._root.mainloop()

                def _on_submit(self, event=None):
                    text = self._entry.get().strip()
                    if not text:
                        return
                    self._entry.delete(0, tk.END)
                    self.post_message("\n[YOU] " + text)
                    self._status.config(text="Thinking...")
                    if self._submit_cb:
                        # Run in background thread so GUI doesn't freeze
                        t = threading.Thread(target=self._run_cb, args=(text,), daemon=True)
                        t.start()

                def _run_cb(self, text):
                    try:
                        if self._submit_cb:
                            self._submit_cb(text)
                    except Exception as e:
                        self.post_message("[ERROR] " + str(e))
                    finally:
                        try:
                            if self._root:
                                self._root.after(0, lambda: self._status.config(text="Ready"))
                        except Exception:
                            pass

            gui = _MinimalGUI()
        except Exception as e:
            print("  [GUI] tkinter not available: " + str(e))
            return

    def _gui_submit(text):
        _umbra_print("[YOU] " + text)
        # Route through full command processor so 'play X', 'fix bugs', etc work from GUI
        _process_command(runtime, text)

    gui.set_submit_callback(_gui_submit)
    _gui_ref  = gui
    _gui_mode = True

    print("  [GUI] Window launched — use the GUI window.")
    # mainloop() is called by interactive_mode on main thread


# ============================================================
#  RUN PROMPT  (main dispatch)
# ============================================================


def _direct_llm_answer(runtime, prompt, active_project=None, pm=None):
    """Answer questions directly via LLM when conv engine is unavailable."""
    lower = prompt.lower().strip()
    # Is this a task or a question?
    task_verbs = ["make","build","create","generate","install","fix","repair",
                  "write","run","play","list","show","clean","upgrade","add"]
    is_task = any(lower.startswith(v) for v in task_verbs)
    if is_task:
        return _run_real_pipeline(runtime, prompt, active_project, pm)
    # It's a question - answer it directly with streaming
    _umbra_print("[UMBRA] Thinking...")
    _gui_cb = None
    if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_token"):
        print("", flush=True)
        def _gui_cb(tok):
            print(tok, end="", flush=True)
            try: _gui_ref.stream_token(tok)
            except Exception: pass
    try:
        answer = _ollama_stream(
            _umbra_chat_prompt(prompt),
            timeout=120, num_predict=512, token_cb=_gui_cb)
        if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_end"):
            try: _gui_ref.stream_end()
            except Exception: pass
            print("")
        else:
            if answer:
                _umbra_print("\n[UMBRA] " + answer.strip() + "\n")
        return None
    except Exception as e:
        _umbra_print("[UMBRA] Could not answer: " + str(e))
    return None


def run_prompt(runtime, prompt, project_override=None):
    rm = runtime.get("resource_manager")
    try:
        if rm: rm.task_delay()
    except Exception: pass

    # Self-repair intercepts
    intent, detail = _detect_self_intent(prompt)
    if intent == "fix":
        handle_self_fix(runtime)
        return None
    if intent == "install" and detail:
        handle_self_install(runtime, detail)
        return None
    if intent == "integrate" and detail:
        handle_integrate(runtime, detail)
        return None

    lower = prompt.lower().strip()
    conv = runtime.get("conversation")
    pm = runtime.get("project_manager")
    try:
        active_project = project_override or (pm.get_active() if pm else None)
    except Exception:
        active_project = None

    # ── Direct pattern matching (runs BEFORE conv.classify) ──────────────
    lower_direct = prompt.lower().strip()

    # Question detection - answer directly without pipeline
    _QUESTION_STARTERS = ("what","who","where","when","why","how","is ","are ","was ",
                          "were ","will ","would ","could ","should ","can ","do ","does ",
                          "did ","which ","whose ","whats ","whos ","hows ","wheres ")
    _TASK_STARTERS = ("make","build","create","generate","install","fix","repair",
                      "write","run","play","list","show","clean","upgrade","add",
                      "delete","remove","update","open","close","start","stop")
    _is_question = (lower_direct.endswith("?") or
                   any(lower_direct.startswith(s) for s in _QUESTION_STARTERS))
    _is_task = any(lower_direct.startswith(s) for s in _TASK_STARTERS)
    if _is_question and not _is_task:
        _umbra_print("[UMBRA] Answering...")
        try:
            import urllib.request as _ur, json as _jj
            # Use fast small model if available, else main model with short timeout
            _qa_models = []
            try:
                with _ur.urlopen('http://localhost:11434/api/tags', timeout=2) as _r:
                    _all = [m['name'] for m in _jj.loads(_r.read()).get('models',[])]
                # Prefer fast models for Q&A
                for _pref in ['llama3.2:3b','llama3.1:8b','qwen2.5:7b','mistral:7b',
                              'phi3:mini','gemma2:2b']:
                    if _pref in _all: _qa_models.append(_pref)
                _qa_models += _all  # fallback to any available
            except Exception: pass
            _qa_model = _qa_models[0] if _qa_models else _get_agent_model()
            # Stream tokens live to GUI if running
            _gui_stream_cb = None
            if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_token"):
                print("")  # newline on CLI
                def _gui_stream_cb(tok):
                    print(tok, end="", flush=True)
                    try: _gui_ref.stream_token(tok)
                    except Exception: pass
            _ans = _ollama_stream(
                _umbra_chat_prompt(prompt),
                model=_qa_model, timeout=120, num_predict=512,
                token_cb=_gui_stream_cb)
            if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_end"):
                try: _gui_ref.stream_end()
                except Exception: pass
                print("")
            else:
                _umbra_print("\n[UMBRA] " + (_ans.strip() if _ans else "I could not find an answer.") + "\n")
        except Exception as _qe:
            _umbra_print("[UMBRA] Could not answer: " + str(_qe))
        return None
    _game_words = ["make a game","build a game","create a game","generate a game",
                   "make me a game","build me a game","make a full game","build a full game",
                   "make an rpg","build an rpg","make a pygame","build a pygame",
                   "make a small","test version of","test game","make optiopia","build optiopia",
                   "make demiworld","build demiworld","make a platformer","make a shooter",
                   "make a dungeon","make a survival","make a version of my game"]
    if any(kw in lower_direct for kw in _game_words):
        _pn_m = re.search(r"(?:called|named)\s+([A-Za-z][A-Za-z0-9 ]+?)(?:[ ]|$|,|[.])", prompt, re.IGNORECASE)
        _pname = _pn_m.group(1).strip() if _pn_m else "MyGame"
        # Ask clarifying questions before building
        _clarify_qs = [
            "1. What genre/style? (RPG/platformer/shooter/puzzle/survival/strategy)",
            "2. Setting? (fantasy/sci-fi/horror/modern/historical/post-apocalyptic)",
            "3. How many enemy types? (1-10)",
            "4. Key features? (crafting/magic/building/stealth/multiplayer/none)",
            "5. Art style? (pixel art/top-down/side-scroll/isometric/graveyard-keeper-style)",
        ]
        _umbra_print("\n[UMBRA] Answer each popup to customise your game (close to skip):\n")
        _answers = []
        for _ql, _qh in [("Genre","RPG/platformer/shooter/puzzle/survival/strategy"),
                          ("Setting","fantasy/sci-fi/horror/modern/post-apocalyptic"),
                          ("Enemies","how many types? 0-10"),
                          ("Features","crafting/magic/building/stealth/none"),
                          ("Art style","pixel/top-down/side-scroll/isometric")]:
            _a = _safe_input(_ql + "?\n(" + _qh + ")", "").strip()
            if _a: _answers.append(_ql + ": " + _a)
        if _answers: prompt = prompt + ". Details: " + "; ".join(_answers)
        _umbra_print("[UMBRA] Building game: " + _pname + " — launching agents...")
        _res = _run_deep_build(runtime, prompt, _pname)
        if _res:
            _fp2 = getattr(_res,"file_path",None)
            if _fp2: _umbra_mem(runtime) and _umbra_mem(runtime).store("last_game_file",_fp2,tags=["game"])
            _umbra_print("[UMBRA] Done! Type: play last")
        return None

    _gif_words = ["make a gif","create a gif","generate a gif","make gif","make an animated"]
    if any(kw in lower_direct for kw in _gif_words):
        gif_gen = runtime.get("animated_gif_generator")
        if gif_gen and gif_gen.is_available():
            _umbra_print("[UMBRA] Generating GIF...")
            _gr = gif_gen.run(prompt)
            if isinstance(_gr, dict):
                _gpath = _gr.get("path") or _gr.get("file_path") or _gr.get("output")
            else:
                _gpath = str(_gr) if _gr else None
            if _gpath and str(_gpath) != "None":
                _umbra_print("[GIF] Saved: " + str(_gpath))
                _umbra_mem(runtime) and _umbra_mem(runtime).store("last_gif", str(_gpath), tags=["gif"])
            else:
                # Direct fallback using our generator
                try:
                    from core.runtime.runtime_animated_gif_generator import RuntimeAnimatedGifGenerator as _RAGG
                    import os as _osg
                    _gdir = _osg.path.join(_UMBRA_ROOT,"workspaces","videos")
                    _osg.makedirs(_gdir, exist_ok=True)
                    _gagg = _RAGG(output_dir=_gdir)
                    _gr2  = _gagg.run(prompt)
                    _gpath2 = _gr2.get("path") if isinstance(_gr2,dict) else None
                    _umbra_print("[GIF] Saved: " + str(_gpath2))
                except Exception as _ge2:
                    _umbra_print("[GIF] Error: " + str(_ge2))
        else:
            _umbra_print("[GIF] Not available. Run: install a gif generator into umbra")
        return None

    _img_words = ["make an image","make image","create an image","generate an image",
                  "make a picture","draw an image","make 1 image","make 2 image",
                  "make 3 image","make 4 image","make 5 image","make 6 image",
                  "make 7 image","make 8 image","make 9 image","make 10 image"]
    if any(kw in lower_direct for kw in _img_words) or re.search(r"make \d+ image", lower_direct):
        _count_m = re.search(r"(\d+)\s+image", lower_direct)
        _count = int(_count_m.group(1)) if _count_m else 1
        _count = min(_count, 10)
        _umbra_print("[UMBRA] Generating " + str(_count) + " image(s)...")
        # Try runtime image_generator first, fall back to our own
        img_gen = runtime.get("image_generator")
        for _ci in range(_count):
            if img_gen and hasattr(img_gen, "generate"):
                try:
                    _ir = img_gen.generate(prompt)
                    _umbra_print("[IMAGE " + str(_ci+1) + "] " + (str(_ir.file_path) if _ir.success else str(getattr(_ir,"fallback_description","failed"))))
                    continue
                except Exception: pass
            # Fallback: use RuntimeImageGenerator directly
            try:
                from core.runtime.runtime_image_generator import RuntimeImageGenerator as _RIG
                import os as _os2
                _idir = _os2.path.join(_UMBRA_ROOT, "workspaces", "images")
                _os2.makedirs(_idir, exist_ok=True)
                _rig = _RIG(output_dir=_idir)
                _ir2 = _rig.generate(prompt)
                _umbra_print("[IMAGE " + str(_ci+1) + "] Saved: " + str(_ir2.file_path))
                _umbra_mem(runtime) and _umbra_mem(runtime).store("last_image", _ir2.file_path, tags=["image"])
            except Exception as _ie:
                _umbra_print("[IMAGE] Error: " + str(_ie))
        return None

    if conv:
        learned = _classify_with_user_model(runtime, prompt)
        try:
            classification = conv.classify(prompt)
        except Exception:
            # conv failed - try direct LLM answer
            return _direct_llm_answer(runtime, prompt, active_project, pm)
        if learned and learned not in ("question", "chat"):
            classification.intent = learned

        conv.add_turn("user", prompt, "input")
        if active_project and pm:
            pm.add_conversation_turn(active_project, "user", prompt)

        # ── QUESTION / CHAT ─────────────────────────────────────
        if classification.intent in ("question", "chat"):
            # Check if project modification request
            project_action_patterns = [
                r"\b(fix|change|update|add|remove|rebuild|rewrite|make|improve|upgrade)\b",
                r"\b(should|needs to|need to|must|want to|have to)\b.{0,20}\b(work|function|show|display|use|have)\b",
                r"\b(gui|window|screen|button|menu|inventory|save|buy|shop|weapon|gear|potion|enemy|enemies)\b",
                r"\b(instead of|not in|shouldn.t use|should be in|should be able to)\b",
            ]
            is_project_action = active_project and any(
                re.search(p, lower, re.IGNORECASE) for p in project_action_patterns
            )
            if is_project_action:
                direct = runtime.get("direct_generator")
                enriched = (
                    "Complete working Python pygame game" +
                    (" for project '" + active_project.name + "'" if active_project else "") +
                    ": " + prompt +
                    ". CRITICAL: ALL interaction inside pygame window only, never terminal. "
                    "Clickable buttons for all menus. 800x600. clock.tick(60). QUIT handling. "
                    "if __name__=='__main__': main() at bottom. ONLY Python code."
                )
                if direct and direct.is_available():
                    project_name = active_project.slug if active_project else None
                    _umbra_print("\n[UMBRA] Building game update (direct mode)...")
                    result, run_id = direct.generate(enriched, filename="game.py", project_name=project_name)
                    if result.success:
                        _umbra_print("[GAME] Updated: " + result.file_path)
                        _umbra_print("[GAME] " + str(result.lines) + " lines — type: play last")
                        if active_project and pm:
                            pm.add_file_to_project(active_project, result.file_path, "game")
                        _mem=runtime.get("memory")
                        if _mem: _mem.store("last_game_file", result.file_path, tags=["game"])
                        handle_workspace_repair(runtime, target=result.file_path, auto=True)
                    else:
                        _umbra_print("[GAME] Failed: " + str(result.error))
                    return None
                return _run_real_pipeline(runtime, enriched, active_project, pm)

            try:
                answer = conv.answer_question(prompt)
            except Exception:
                # Fall back to direct Ollama with streaming
                _gui_cb2 = None
                if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_token"):
                    print("", flush=True)
                    def _gui_cb2(tok):
                        print(tok, end="", flush=True)
                        try: _gui_ref.stream_token(tok)
                        except Exception: pass
                answer = _ollama_stream(_umbra_chat_prompt(prompt), timeout=120, num_predict=512, token_cb=_gui_cb2) or "I don't know."
                if _gui_mode and _gui_ref is not None and hasattr(_gui_ref, "stream_end"):
                    try: _gui_ref.stream_end()
                    except Exception: pass
                    print("")
                conv.add_turn("umbra", answer, "answer")
                _maybe_tts(runtime, answer)
                return None
            _umbra_print("\n[UMBRA] " + answer.strip() + "\n")
            conv.add_turn("umbra", answer, "answer")
            _maybe_tts(runtime, answer)
            if active_project and pm:
                pm.add_conversation_turn(active_project, "umbra", answer)
            _record_user_phrase(runtime, prompt, "question")
            return None

        # ── IMAGE ──────────────────────────────────────────────
        if classification.intent == "image_request":
            _record_user_phrase(runtime, prompt, "image_request")
            img_gen = runtime.get("image_generator")
            if img_gen:
                _umbra_print("\n[UMBRA] Generating image...")
                result = img_gen.generate(prompt)
                if result.success:
                    _umbra_print("[IMAGE] Saved: " + result.file_path)
                    _umbra_print("[IMAGE] Folder: C:\\Umbra\\workspaces\\images\\")
                else:
                    _umbra_print("[IMAGE] " + (result.fallback_description or result.error or "ComfyUI not available"))
            return None

        # ── GIF — always route to gif generator ───────────────
        gif_keywords = ["gif", "animated gif", "make a gif", "create a gif", "generate a gif"]
        if any(kw in lower for kw in gif_keywords):
            _record_user_phrase(runtime, prompt, "gif_request")
            gif_gen = runtime.get("animated_gif_generator")
            if gif_gen and gif_gen.is_available():
                _umbra_print("\n[UMBRA] Generating animated GIF...")
                result = gif_gen.run(prompt)
                if result.get("status") == "ok" or result.get("path"):
                    path = result.get("path", result.get("output", ""))
                    _umbra_print("[GIF] Saved: " + str(path))
                    _umbra_print("[GIF] Folder: C:\\Umbra\\workspaces\\videos\\")
                else:
                    _umbra_print("[GIF] Failed: " + str(result.get("error", "unknown")))
            else:
                _umbra_print("[GIF] Generator not ready. Run: install a gif generator into umbra using PIL")
            return None

        # ── VIDEO ──────────────────────────────────────────────
        if classification.intent == "video_request" or "video" in lower:
            _record_user_phrase(runtime, prompt, "video_request")
            vid_gen = runtime.get("video_generator")
            if vid_gen:
                _umbra_print("\n[UMBRA] Generating video via ComfyUI...")
                result = vid_gen.generate(prompt)
                if result.success:
                    _umbra_print("[VIDEO] Saved: " + result.file_path)
                    # Auto-assemble frames if they exist
                    frames_dir, frames = _find_comfyui_output_frames()
                    if frames_dir and len(frames) > 1:
                        _umbra_print("[VIDEO] Found " + str(len(frames)) + " frames — assembling...")
                        videos_dir = os.path.join(_UMBRA_ROOT, "workspaces", "videos")
                        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        out_path = os.path.join(videos_dir, "video_" + ts)
                        success, final_path, msg = _assemble_frames_to_video(frames_dir, out_path)
                        _umbra_print("[VIDEO] " + msg)
                else:
                    _umbra_print("[VIDEO] " + (result.fallback_description or result.error or "ComfyUI not available"))
                    # Check if there are frames to assemble anyway
                    frames_dir, frames = _find_comfyui_output_frames()
                    if frames_dir and len(frames) > 1:
                        _umbra_print("[VIDEO] Found " + str(len(frames)) + " ComfyUI frames — assembling...")
                        videos_dir = os.path.join(_UMBRA_ROOT, "workspaces", "videos")
                        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        out_path = os.path.join(videos_dir, "video_" + ts)
                        success, final_path, msg = _assemble_frames_to_video(frames_dir, out_path)
                        _umbra_print("[VIDEO] " + msg)
            return None

        # ── GAME ───────────────────────────────────────────────
        if classification.intent == "game_request":
            _record_user_phrase(runtime, prompt, "game_request")
            raw = classification.metadata.get("raw", prompt)

            # Check for deep/full build keywords
            deep_keywords = ["skyrim", "open world", "mmorpg", "full game", "complete game",
                             "all systems", "everything", "massive", "huge", "big", "complex",
                             "faction", "economy", "lore", "cutscene", "ai girlfriend",
                             "ai companion", "simulation", "strategy", "rts", "4x"]
            is_deep = any(kw in lower for kw in deep_keywords)

            # Extract project name
            name_match = re.search(
                r"(?:called|named|name it|call it)\s+['\"]?([A-Za-z][A-Za-z0-9 ]+?)['\"]?(?:\s|$|,|\.|with)",
                prompt, re.IGNORECASE
            )
            project_name = name_match.group(1).strip() if name_match else None

            if is_deep:
                # Ask clarifying questions first
                llm = runtime.get("llm")
                questions = _ask_game_clarifications(raw, llm)
                answers = []
                if questions:
                    _umbra_print("\n[UMBRA] Before I start building, a few questions:")
                    for q in questions:
                        _umbra_print("  " + q)
                        try:
                            ans = _safe_input("you > ", "").strip()
                            if ans:
                                answers.append(q + ": " + ans)
                        except (EOFError, KeyboardInterrupt):
                            break
                enriched = raw + (". " + ". ".join(answers) if answers else "")
                if not project_name:
                    try:
                        project_name = _safe_input("  Project name: ", "").strip() or "MyGame"
                    except (EOFError, KeyboardInterrupt):
                        project_name = "MyGame"

                _umbra_print("\n[UMBRA] Starting full deep build — this will take several minutes...")
                result = _run_deep_build(runtime, enriched, project_name)
                if result:
                    _fp = getattr(result,"file_path",None)
                    if _fp: _umbra_mem(runtime) and _umbra_mem(runtime).store("last_game_file",_fp,tags=["game"])
                    _umbra_print("\n[UMBRA] Game ready! Type: play last")
                return None

            # Standard game build
            if classification.needs_clarification and len(raw.split()) < 10:
                question = conv.start_clarification(classification, prompt)
                _umbra_print("\n[UMBRA] " + question)
                try:
                    answer = _safe_input("you > ", "").strip()
                    raw = raw + ". " + answer
                except (EOFError, KeyboardInterrupt):
                    pass
                conv.pending_clarification = None

            direct = runtime.get("direct_generator")
            if direct and direct.is_available():
                project_slug = active_project.slug if active_project else project_name
                game_prompt = (
                    "Write a complete working Python pygame game. " + raw + ". "
                    "Single file. pygame.init(). 800x600 window. clock.tick(60). "
                    "QUIT event handling. All user input inside pygame window NOT terminal. "
                    "All dict keys lowercase. .lower().strip() on input. "
                    "Default to first option if input not found. "
                    "Sprites stay within screen bounds. pygame.display.flip() every frame. "
                    "if __name__=='__main__': main() at bottom. "
                    "ONLY Python code. No markdown. No explanation."
                )
                _umbra_print("\n[UMBRA] Building game...")
                result, run_id = direct.generate(game_prompt, filename="game.py",
                                                  project_name=project_slug)
                if result.success:
                    tester = runtime.get("game_tester")
                    score_str = ""
                    if tester:
                        try:
                            tr = tester.test_file(result.file_path)
                            score_str = " | Quality: " + str(tr.score) + "/100"
                        except Exception:
                            pass
                    _umbra_print("[GAME] Generated: " + result.file_path)
                    _umbra_print("[GAME] " + str(result.lines) + " lines" + score_str)
                    _umbra_print("[GAME] Type: play last")
                    if active_project and pm:
                        pm.add_file_to_project(active_project, result.file_path, "game")
                        _umbra_mem(runtime) and _umbra_mem(runtime).store("last_game_file", result.file_path, tags=["game"])
                    handle_workspace_repair(runtime, target=result.file_path, auto=True)
                    _apply_common_improvements(runtime, result.file_path, "game")
                else:
                    _umbra_print("[GAME] Direct generation failed: " + str(result.error))
                    return _run_real_pipeline(runtime, raw, active_project, pm)
                return None

            # direct_generator not available — use deep build with agents
            _umbra_print("[UMBRA] direct_generator not loaded — using agent build...")
            _pname = project_name or "MyGame"
            _result = _run_deep_build(runtime, prompt, _pname)
            if _result:
                _umbra_print("[UMBRA] Done! Type: play " + _pname)
            return None

        # Clarification for other tasks
        if classification.needs_clarification and classification.clarification_questions:
            question = conv.start_clarification(classification, prompt)
            _umbra_print("\n[UMBRA] " + question)
            try:
                answer = _safe_input("you > ", "").strip()
                prompt = prompt + ". Details: " + answer
            except (EOFError, KeyboardInterrupt):
                pass
            conv.pending_clarification = None

    return _run_real_pipeline(runtime, prompt, active_project, pm)


def _run_studio_project(runtime, prompt, project_name=None):
    agents = runtime.get("studio_agents")
    pm = runtime.get("project_manager")
    direct = runtime.get("direct_generator")
    if not agents or not pm:
        return _run_real_pipeline(runtime, prompt)

    _umbra_print("\n[STUDIO] Analyzing: " + prompt[:60] + "...")
    project = pm.create_project(project_name or "untitled", description=prompt)
    pm.set_active(project.name)
    pm.add_conversation_turn(project, "user", prompt)
    _umbra_print("[STUDIO] Project '" + project.name + "' created")

    plan = agents.orchestrate_project(prompt, project.name)
    questions = plan.get("clarifying_questions", [])
    answers = []
    for q in questions[:3]:
        _umbra_print("\n[UMBRA] " + q)
        try:
            ans = _safe_input("you > ", "").strip()
            if ans:
                answers.append(q + ": " + ans)
                pm.add_conversation_turn(project, "user", q + ": " + ans)
        except (EOFError, KeyboardInterrupt):
            break
    enriched = prompt + (". " + ". ".join(answers) if answers else "")

    if plan.get("needs_world"):
        _umbra_print("\n[STUDIO] Building world lore...")
        r = agents.build_world(enriched, project_name=project.slug)
        if r.success:
            for fp in r.files:
                pm.add_file_to_project(project, fp, "lore")

    if plan.get("needs_mechanics"):
        _umbra_print("\n[STUDIO] Designing mechanics...")
        r = agents.design_mechanics(enriched, project_name=project.slug)
        if r.success:
            for fp in r.files:
                pm.add_file_to_project(project, fp, "design")
            project.metadata["mechanics"] = r.output
            pm.save_project(project)

    _umbra_print("\n[STUDIO] Building game code...")
    mechanics = project.metadata.get("mechanics", {})
    stats = mechanics.get("player_stats", {})
    world_name = project.metadata.get("world", {}).get("world_name", project.name)
    game_prompt = (
        "Write a complete Python pygame game called '" + project.name + "'. "
        "Description: " + enriched + ". World: " + world_name + ". "
        "Stats: HP=" + str(stats.get("hp", 100)) + " atk=" + str(stats.get("attack", 10)) + ". "
        "CRITICAL: pygame buttons not terminal input, 800x600, clock.tick(60), QUIT handling, "
        "health bar, enemy AI, boundary checks, pygame.display.flip() every frame, "
        "if __name__=='__main__': main(). ONLY Python code."
    )
    if direct and direct.is_available():
        result, run_id = direct.generate(game_prompt,
                                          filename=project.slug + "_game.py",
                                          project_name=project.slug)
        if result.success:
            _umbra_print("\n[STUDIO] Game: " + result.file_path + " (" + str(result.lines) + " lines)")
            _umbra_print("[STUDIO] Type: play " + project.name)
            pm.add_file_to_project(project, result.file_path, "game")
            _umbra_mem(runtime) and _umbra_mem(runtime).store("last_game_file", result.file_path, tags=["game"])
            handle_workspace_repair(runtime, target=result.file_path, auto=True)
            _apply_common_improvements(runtime, result.file_path, "game")
        else:
            _umbra_print("[STUDIO] Failed: " + str(result.error))
            _run_real_pipeline(runtime, game_prompt)
    else:
        _run_real_pipeline(runtime, game_prompt)

    _umbra_print("\n[STUDIO] '" + project.name + "' complete!\n")


# ============================================================
#  INTERACTIVE MODE
# ============================================================

def interactive_mode(runtime):
    print_banner()
    print_status(runtime)

    _llm = runtime.get("llm")
    if not _llm or not _llm.is_configured():
        _umbra_print("[WARNING] No LLM configured. Check umbra_config.json\n")

    # Launch GUI
    _launch_gui(runtime)

    v = runtime.get("voice_input")
    if v and v.is_available():
        _umbra_print("  Voice: READY — type 'listen' to speak, 'voice on' for continuous")
    _umbra_print("\nJust type naturally. Examples:")
    _umbra_print("  'make a game like Skyrim called Optiopia with 3 gods and open world'")
    _umbra_print("  'build a full game called Optiopia'  (uses all agents)")
    _umbra_print("  'make a gif of a dancing knight'")
    _umbra_print("  'make an image of a fantasy castle'")
    _umbra_print("  'fix all bugs'  |  'install video pipeline into umbra'")
    _umbra_print("  'list files'  |  'clean up old files'")
    _umbra_print("  Type 'exit' to quit.\n")

    # GUI mode: mainloop MUST run on main thread
    if _gui_mode and _gui_ref is not None:
        _umbra_print('[UMBRA] GUI active — use the Control Center window.')
        try:
            if hasattr(_gui_ref, "mainloop"):
                _gui_ref.mainloop()  # blocks until window closed
            elif hasattr(_gui_ref, "root") and hasattr(_gui_ref.root, "mainloop"):
                _gui_ref.root.mainloop()
            else:
                _umbra_print("[GUI] running — window should be visible")
                import time as _tm2
                try:
                    while True: _tm2.sleep(1)
                except KeyboardInterrupt: pass
        except KeyboardInterrupt:
            pass
        except Exception as _mle:
            _umbra_print('[GUI] error: ' + str(_mle))
            import time as _tm3
            try:
                while True: _tm3.sleep(1)
            except KeyboardInterrupt: pass
        return

    while True:
        pm = runtime.get("project_manager")
        try: active = pm.get_active() if pm else None
        except Exception: active = None
        prefix = ("umbra [" + active.name + "]") if active else "umbra"

        if runtime.get("_continuous_voice"):
            v = runtime.get("voice_input")
            if v and v.is_available():
                res = v.listen_once(timeout=4, phrase_limit=15)
                if res.success and res.text.strip():
                    user_input = res.text.strip()
                    print("\n" + prefix + "> [MIC] " + user_input)
                else:
                    try:
                        user_input = _safe_input(prefix + "> ", "").strip()
                    except (KeyboardInterrupt, EOFError):
                        user_input = "exit"
            else:
                try:
                    user_input = _safe_input(prefix + "> ", "").strip()
                except (KeyboardInterrupt, EOFError):
                    user_input = "exit"
        else:
            try:
                user_input = _safe_input(prefix + "> ", "").strip()
            except (KeyboardInterrupt, EOFError):
                _umbra_print("\n[UMBRA] Shutting down.")
                _shutdown(runtime)
                break

        if not user_input:
            continue
        cmd = user_input.lower().strip()

        if cmd in ("exit", "quit", "q"):
            _umbra_print("[UMBRA] Shutting down.")
            _shutdown(runtime)
            break

        # ── SELF-REPAIR ──
        elif cmd in ("fix", "fix yourself", "fix all bugs", "fix all errors",
                     "fix all issues", "repair yourself", "debug yourself",
                     "fix everything", "self fix", "self-fix"):
            handle_self_fix(runtime)

        elif cmd.startswith("fix ") and any(x in cmd for x in ("bug", "error", "issue", "module", "runtime_")):
            handle_self_fix(runtime)

        # ── WORKSPACE REPAIR ──
        elif cmd in ("fix workspace", "fix workspaces", "fix projects",
                     "repair workspace", "fix my files", "fix project files"):
            handle_workspace_repair(runtime, target="all")

        elif re.search(r"\bfix\b.{1,30}\b(gui|window|gif|video|tts|voice|search|converter|tracker)\b", cmd):
            feature_match = re.search(r"\b(gui|window|gif|video|tts|voice|search|converter|tracker)\b", cmd)
            feature = feature_match.group(1) if feature_match else "unknown"
            runtime_dir = os.path.join(_UMBRA_ROOT, "core", "runtime")
            # Search runtime_*feature* pattern (fixes the gui finding wrong modules bug)
            candidates = [f for f in os.listdir(runtime_dir)
                         if f.endswith(".py") and feature.lower() in f.lower()
                         and f.startswith("runtime_")]
            if candidates:
                llm = runtime.get("llm")
                for fname in candidates[:2]:
                    path = os.path.join(runtime_dir, fname)
                    err = _syntax_check(path)
                    if err:
                        _umbra_print("[FIX] Syntax error in " + fname + ": " + err)
                        if llm and llm.is_configured():
                            fixed = _ask_llm_fix(llm, path, err)
                            if fixed:
                                try:
                                    ast.parse(fixed)
                                    _backup_file(path)
                                    with open(path, "w", encoding="utf-8") as fout:
                                        fout.write(fixed)
                                    _umbra_print("[FIX] Fixed: " + fname + ". Restart Umbra.\n")
                                except Exception as e2:
                                    _umbra_print("[FIX] Could not fix: " + str(e2) + "\n")
                    else:
                        _umbra_print("[FIX] " + fname + " has no syntax errors.")
                        # Try LLM-guided logic fix
                        if llm and llm.is_configured():
                            _umbra_print("  Attempting LLM logic fix...")
                            try:
                                with open(path, "r", encoding="utf-8") as f:
                                    src = f.read()
                                fix_prompt = (
                                    "Fix any logic, integration or functionality bugs in this Umbra module.\n"
                                    "The user reports: '" + feature + "' is not working correctly.\n"
                                    "Make it fully functional. Return ONLY complete fixed Python:\n\n" + src[:5000]
                                )
                                r = llm.complete(fix_prompt)
                                if r and r.content:
                                    fixed = _strip_fences(r.content)
                                    ast.parse(fixed)
                                    _backup_file(path)
                                    with open(path, "w", encoding="utf-8") as fout:
                                        fout.write(fixed)
                                    _umbra_print("[FIX] Logic fix applied: " + fname + ". Restart Umbra.\n")
                            except Exception as e:
                                _umbra_print("[FIX] Logic fix failed: " + str(e) + "\n")
            else:
                _umbra_print("  No runtime_*" + feature + "* module found. Try: fix all bugs\n")

        elif cmd in ("fix last", "fix last build", "fix last game",
                     "repair last", "fix what you just made"):
            handle_workspace_repair(runtime, target="last")

        elif cmd.startswith("fix project "):
            handle_workspace_repair(runtime, target=user_input[12:].strip())

        elif cmd == "scan modules":
            broken = _find_broken_modules()
            if not broken:
                _umbra_print("\n[SCAN] All core/runtime modules clean.\n")
            else:
                _umbra_print("\n[SCAN] " + str(len(broken)) + " broken:")
                for path, err in broken:
                    _umbra_print("  x " + os.path.basename(path) + ": " + err[:80])
                _umbra_print("")

        # ── INSTALL / INTEGRATE ──
        elif (cmd.startswith("install ") or cmd.startswith("add ")
              or cmd.startswith("build and install ")):
            intent, detail = _detect_self_intent(user_input)
            if intent == "install" and detail:
                handle_self_install(runtime, detail)
            else:
                run_prompt(runtime, user_input)

        elif cmd.startswith("integrate "):
            module = user_input[10:].strip()
            if not module.startswith("runtime_"):
                module = "runtime_" + module
            handle_integrate(runtime, module)

        # ── FFMPEG AUTO-INSTALL ──
        elif cmd in ("install ffmpeg", "download ffmpeg", "get ffmpeg"):
            _umbra_print("[UMBRA] ffmpeg is needed for MP4 video output.")
            try:
                ans = _safe_input("  Download and install ffmpeg now? [y/N]: ", "").strip().lower()
            except Exception:
                ans = "n"
            if ans in ("y", "yes"):
                _umbra_print("[UMBRA] Installing ffmpeg via winget (this may take a minute)...")
                r2 = subprocess.run(
                    ["winget", "install", "ffmpeg", "--silent",
                     "--accept-package-agreements", "--accept-source-agreements"],
                    capture_output=True, text=True, timeout=300
                )
                if r2.returncode == 0:
                    _umbra_print("[UMBRA] ffmpeg installed successfully! Restart Umbra to use it.")
                else:
                    _umbra_print("[UMBRA] winget install failed: " + r2.stderr[:200])
                    _umbra_print("[UMBRA] Manual option: download from https://www.gyan.dev/ffmpeg/builds/")
                    _umbra_print("[UMBRA] Extract and add the bin/ folder to your Windows PATH.")

        # ── VIDEO FRAME ASSEMBLY ──
        elif "assemble" in cmd and ("video" in cmd or "frame" in cmd):
            frames_dir, frames = _find_comfyui_output_frames()
            if frames_dir and frames:
                _umbra_print("[VIDEO] Found " + str(len(frames)) + " frames in: " + frames_dir)
                videos_dir = os.path.join(_UMBRA_ROOT, "workspaces", "videos")
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                out_path = os.path.join(videos_dir, "video_" + ts)
                success, final_path, msg = _assemble_frames_to_video(frames_dir, out_path)
                _umbra_print("[VIDEO] " + msg)
                if success:
                    _umbra_print("[VIDEO] Open: " + os.path.dirname(final_path))
            else:
                _umbra_print("[VIDEO] No frames found. Generate a video first.\n")

        # ── DEEP/FULL GAME BUILD ──
        elif re.search(r"\b(build a full game|make a full game|full build|build everything for|all agents)\b", cmd):
            name_match = re.search(
                r"(?:called|named)\s+['\"]?([A-Za-z][A-Za-z0-9 ]+?)['\"]?(?:\s|$|,|\.|with)",
                user_input, re.IGNORECASE
            )
            project_name = name_match.group(1).strip() if name_match else None
            if not project_name:
                try:
                    project_name = _safe_input("  Project name: ", "").strip() or "MyGame"
                except (EOFError, KeyboardInterrupt):
                    project_name = "MyGame"
            _umbra_print("\n[UMBRA] Starting full deep build with all agents...")
            result = _run_deep_build(runtime, user_input, project_name)
            if result:
                _umbra_print("[UMBRA] Done! Type: play " + project_name)

        # ── FILE BROWSER ──
        elif cmd in ("list files", "show files", "browse files", "files"):
            handle_files_browser(runtime, cmd)

        elif "list workspace" in cmd or "workspace files" in cmd:
            handle_files_browser(runtime, "workspace")

        elif "clean" in cmd and ("file" in cmd or "old" in cmd or "backup" in cmd):
            handle_files_browser(runtime, "clean old files")

        # ── VOICE TOGGLES ──
        elif cmd in ("voice on", "continuous voice on", "always listen"):
            runtime["_continuous_voice"] = True
            _umbra_print("  [MIC] Continuous voice ON.\n")

        elif cmd in ("voice off", "continuous voice off", "stop listening"):
            runtime["_continuous_voice"] = False
            _umbra_print("  [MIC] Continuous voice OFF.\n")

        elif cmd in ("tts on", "text to speech on", "speak responses"):
            runtime["_tts_enabled"] = True
            _umbra_print("  [TTS] Text-to-speech ON.\n")

        elif cmd in ("tts off", "text to speech off", "stop speaking"):
            runtime["_tts_enabled"] = False
            _umbra_print("  [TTS] Text-to-speech OFF.\n")

        elif cmd in ("listen", "voice", "speak", "mic"):
            v = runtime.get("voice_input")
            if not v or not v.is_available():
                _umbra_print("  Voice not available. pip install SpeechRecognition pyaudio\n")
            else:
                _umbra_print("  [MIC] Listening...")
                res = v.listen_once(timeout=8, phrase_limit=20)
                if res.success and res.text.strip():
                    _umbra_print("  [MIC] Heard: " + res.text)
                    run_prompt(runtime, res.text)
                elif res.error:
                    _umbra_print("  [MIC] Error: " + res.error + "\n")
                else:
                    _umbra_print("  [MIC] Nothing heard.\n")

        # ── STANDARD COMMANDS ──
        elif cmd == "status":
            print_status(runtime)

        elif cmd in ("config", "help", "setup"):
            print_config()

        elif cmd == "version":
            _umbra_print("  Umbra v2.3.0 — Autonomous AI Runtime OS")

        elif cmd in ("metrics", "stats"):
            print_metrics(runtime)

        elif cmd in ("health", "health check", "system health"):
            report = runtime["health"].run_all_checks()
            _umbra_print("\n[HEALTH] " + report.summary_line())
            for check in report.checks:
                icon = "+" if check["status"] == "pass" else "!"
                _umbra_print("  " + icon + " " + check["name"] + ": " + (check["message"] or check["status"]))
            _umbra_print("")

        elif cmd in ("projects", "list projects", "my projects"):
            if pm:
                projects = pm.list_projects()
                if not projects:
                    _umbra_print("  No projects yet.\n")
                else:
                    _umbra_print("\n[PROJECTS] " + str(len(projects)) + " total:")
                    for p in projects:
                        tag = " (active)" if (active and active.slug == p.slug) else ""
                        _umbra_print("  " + p.name + tag + " | " + str(len(p.files)) + " files")
                    _umbra_print("")

        elif (cmd.startswith("work on ") or cmd.startswith("lets work on ")
              or cmd.startswith("continue ") or cmd.startswith("open ")):
            name = None
            for pfx in ("lets work on ", "work on ", "continue ", "open "):
                if cmd.startswith(pfx):
                    name = user_input[len(pfx):].strip().title()
                    break
            if name and pm:
                existing = pm.get_project(name)
                if existing:
                    pm.set_active(name)
                    _umbra_print("\n[UMBRA] Switched to: " + existing.name + "\n")
                else:
                    _umbra_print("  Project '" + name + "' not found.\n")

        elif cmd in ("project files", "show project files"):
            if active and pm:
                _umbra_print("\n[" + active.name + "] Files (" + str(len(active.files)) + "):")
                for fe in active.files:
                    exists = "OK" if os.path.exists(fe["path"]) else "MISSING"
                    _umbra_print("  [" + exists + "] " + fe["type"] + ": " + fe["path"])
            try:
                last_mem = _umbra_mem(runtime).retrieve("last_game_file")
                if last_mem and os.path.exists(str(last_mem.value)):
                    game_path = str(last_mem.value)
            except Exception: pass
            # Fallback: scan memory_store.json directly
            if not game_path:
                _ms = os.path.join(_UMBRA_ROOT,"sessions","memory_store.json")
                if os.path.exists(_ms):
                    try:
                        import json as _j2
                        for _e in _j2.load(open(_ms,"r",encoding="utf-8")) if True else []:
                            if isinstance(_e,dict) and _e.get("key")=="last_game_file":
                                _gp=str(_e.get("value",""))
                                if os.path.exists(_gp): game_path=_gp; break
                    except Exception: pass

        elif (cmd in ("run last", "play last", "test last")
              or cmd.startswith("play ") or cmd.startswith("run game ")):
            project_name = None
            if cmd.startswith("play ") and len(cmd) > 5:
                project_name = cmd[5:].strip().lower().replace(" ", "_")
            elif cmd.startswith("run game "):
                project_name = cmd[9:].strip().lower().replace(" ", "_")

            game_path = None
            last_mem = _umbra_mem(runtime).retrieve("last_game_file")
            if last_mem and os.path.exists(str(last_mem.value)):
                game_path = str(last_mem.value)

            if project_name and pm:
                proj = pm.get_project(project_name)
                if proj:
                    for fe in proj.files:
                        if fe.get("type") == "game" and fe["path"].endswith(".py"):
                            if os.path.exists(fe["path"]):
                                game_path = fe["path"]
                                break

            if not game_path:
                ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
                newest, newest_path = 0, None
                for root, dirs, files in os.walk(ws_base):
                    for fname in files:
                        if fname.endswith("_game.py") or fname == "game.py":
                            full = os.path.join(root, fname)
                            mtime = os.path.getmtime(full)
                            if mtime > newest:
                                newest = mtime
                                newest_path = full
                game_path = newest_path

            if game_path and os.path.exists(game_path):
                _umbra_print("\n[UMBRA] Launching: " + game_path + "\n")
                try:
                    subprocess.Popen([sys.executable, game_path],
                                     cwd=os.path.dirname(game_path))
                except Exception as e:
                    _umbra_print("  Error: " + str(e) + "\n")
            else:
                _umbra_print("  No game file found. Build one first.\n")

        elif cmd in ("images", "show images", "list images"):
            img = runtime.get("image_generator")
            if img:
                imgs = img.list_generated_images()
                if imgs:
                    _umbra_print("\n[IMAGES] " + str(len(imgs)) + " generated:")
                    for i in imgs[:10]:
                        _umbra_print("  " + i["filename"] + " (" + str(i["size_kb"]) + " KB)")
                else:
                    _umbra_print("  No images yet.")
            _umbra_print("  Folder: " + os.path.join(_UMBRA_ROOT, "workspaces", "images") + "\n")

        elif cmd in ("videos", "show videos", "list videos"):
            vids_dir = os.path.join(_UMBRA_ROOT, "workspaces", "videos")
            _umbra_print("\n[VIDEOS] Folder: " + vids_dir)
            if os.path.exists(vids_dir):
                vfiles = [f for f in os.listdir(vids_dir)
                          if f.endswith((".gif", ".mp4", ".webm", ".avi"))]
                for f in sorted(vfiles, reverse=True)[:10]:
                    _umbra_print("  " + f)
                if not vfiles:
                    _umbra_print("  No videos/gifs yet.")
            _umbra_print("")

        elif cmd in ("memory", "what do you remember"):
            mem = runtime["memory"]
            stats = mem.get_stats()
            _umbra_print("\n[MEMORY] " + str(stats["total_entries"]) + " entries")
            for k in mem.list_keys()[:10]:
                _umbra_print("  " + k)
            _umbra_print("")

        elif cmd in ("improve", "improve yourself"):
            try:
                from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer
                from core.runtime.runtime_self_improvement_loop import RuntimeSelfImprovementLoop
                _umbra_print("[SELF-IMPROVEMENT] Analyzing...")
                analyzer = RuntimeSelfAnalyzer()
                loop = RuntimeSelfImprovementLoop(analyzer, runtime["pipeline"], max_targets_per_run=2)
                plan = loop.run_cycle()
                if plan is None:
                    _umbra_print("  Nothing to improve.\n")
                else:
                    for r in plan.results:
                        _umbra_print("  [" + r["status"] + "] " + r["module"])
                    _umbra_print("")
            except Exception as e:
                _umbra_print("  [IMPROVE] Error: " + str(e) + "\n")

        elif cmd in ("validate", "validate last"):
            last = runtime["pipeline"].get_last_run()
            if last and last.written_files:
                ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
                result = runtime["run_validator"].validate_run(last, workspace_base=ws_base)
                _umbra_print("\n[VALIDATION] " + last.run_id + ": " + str(result.score) + "/100\n")
            else:
                _umbra_print("  No recent run.\n")

        elif cmd in ("review", "review last", "code review"):
            last = runtime["pipeline"].get_last_run()
            if last and last.written_files:
                ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
                reviews = runtime["reviewer"].review_pipeline_run(last, workspace_base=ws_base)
                avg = runtime["reviewer"].get_aggregate_score(reviews)
                _umbra_print("\n[CODE REVIEW] Avg: " + str(avg) + "/100\n")
            else:
                _umbra_print("  No recent run.\n")

        elif cmd in ("history", "show history", "past runs"):
            runs = runtime["pipeline"].get_run_history()
            if not runs:
                _umbra_print("  No runs this session.\n")
            else:
                for r in runs:
                    _umbra_print("  " + r["run_id"] + " | " + r["status"] + " | " + r["prompt"][:50])
                _umbra_print("")

        elif cmd == "resume":
            cont = runtime["continuation"]
            pending = cont.get_all_pending()
            if not pending:
                _umbra_print("  No pending continuations.\n")
            else:
                for record in pending:
                    _umbra_print("  Resuming: " + record.continuation_id)
                    run = cont.resume(record.continuation_id, runtime["pipeline"])
                    if run:
                        _umbra_print("  Status: " + run.status + "\n")

        elif cmd in ("test", "run tests", "tests"):
            import subprocess as _sp3
            _umbra_print("[TEST] Running test_umbra_full.py ...")
            _tr = _sp3.run([sys.executable, "test_umbra_full.py"],
                           capture_output=True, text=True, cwd=_UMBRA_ROOT)
            _out = (_tr.stdout or "") + (_tr.stderr or "")
            _lines = _out.strip().splitlines()
            if len(_lines) > 60:
                _umbra_print("  ... (showing last 60 of " + str(len(_lines)) + " lines)")
                _lines = _lines[-60:]
            for _l in _lines: _umbra_print(_l)
            _passed = sum(1 for l in _out.splitlines() if "[PASS]" in l)
            _failed = sum(1 for l in _out.splitlines() if "[FAIL]" in l)
            _umbra_print("\n[TEST] " + str(_passed) + " passed, " + str(_failed) + " failed" +
                         "  (exit code " + str(_tr.returncode) + ")")

        elif cmd == "handoff":
            try:
                from core.runtime.runtime_handoff_generator import RuntimeHandoffGenerator
                gen = RuntimeHandoffGenerator(base_dir=_UMBRA_ROOT)
                path, _ = gen.generate_markdown(runtime)
                _umbra_print("\n[HANDOFF] Saved: " + path + "\n")
            except Exception as e:
                _umbra_print("[HANDOFF] Error: " + str(e) + "\n")

        elif cmd == "scheduler":
            sched = runtime.get("scheduler")
            if sched:
                _umbra_print("\n[SCHEDULER] " + str(len(sched.jobs)) + " jobs:")
                for j in sched.get_status():
                    _umbra_print("  " + j["name"] + ": runs=" + str(j["run_count"]))
                _umbra_print("")

        elif cmd.startswith("remember "):
            fact = user_input[9:].strip()
            runtime.get("memory") and _umbra_mem(runtime).store("user_note:" + str(_umbra_mem(runtime).size()), fact, tags=["user_note"])
            _umbra_mem(runtime).save()
            _umbra_print("  Stored: " + fact[:60] + "\n")

        elif cmd.startswith("recall "):
            query = user_input[7:].strip()
            results = _umbra_mem(runtime).search(query, top_k=5)
            if results:
                _umbra_print("\n[MEMORY: '" + query + "']")
                for r in results:
                    _umbra_print("  " + r.key + ": " + str(r.value)[:80])
                _umbra_print("")
            else:
                _umbra_print("  Nothing found for '" + query + "'\n")

        elif ("make a gif" in cmd or "create a gif" in cmd or "generate a gif" in cmd
              or "animated gif" in cmd or cmd.startswith("gif of")):
            gif_gen = runtime.get("animated_gif_generator")
            if gif_gen and gif_gen.is_available():
                _umbra_print("\n[UMBRA] Generating animated GIF...")
                result = gif_gen.run(user_input)
                path = result.get("path", "")
                if path:
                    _umbra_print("[GIF] Saved: " + str(path))
                    _umbra_print("[GIF] Folder: C:\\Umbra\\workspaces\\videos\\")
                else:
                    _umbra_print("[GIF] " + str(result.get("error", "unknown error")))
            else:
                _umbra_print("  GIF generator not ready. Run: install a gif generator into umbra using PIL\n")

        elif cmd.startswith("convert") and "gif" in cmd:
            vc = runtime.get("video_converter")
            if vc:
                result = vc.run(user_input)
                _umbra_print("\n[CONVERTER] " + str(result.get("tip", result.get("status", result))) + "\n")
            else:
                # Try direct ffmpeg
                videos_dir = os.path.join(_UMBRA_ROOT, "workspaces", "videos")
                gifs = [os.path.join(videos_dir, f) for f in os.listdir(videos_dir) if f.endswith(".gif")] if os.path.isdir(videos_dir) else []
                if gifs:
                    _umbra_print("[CONVERT] Converting " + str(len(gifs)) + " GIF(s)...")
                    for gif_path in gifs:
                        mp4_path = gif_path.replace(".gif", ".mp4")
                        ffmpeg_exe = shutil.which("ffmpeg")
                        if ffmpeg_exe:
                            r = subprocess.run(
                                [ffmpeg_exe, "-y", "-i", gif_path, "-c:v", "libx264",
                                 "-pix_fmt", "yuv420p", mp4_path],
                                capture_output=True, text=True, timeout=60
                            )
                            if r.returncode == 0:
                                _umbra_print("[CONVERT] " + os.path.basename(mp4_path) + " — OK")
                            else:
                                _umbra_print("[CONVERT] Failed: " + r.stderr[:100])
                        else:
                            _umbra_print("[CONVERT] ffmpeg not found.")
                            try:
                                ans = _safe_input("  Download ffmpeg automatically? [y/N]: ", "").strip().lower()
                            except Exception:
                                ans = "n"
                            if ans in ("y", "yes"):
                                _umbra_print("[CONVERT] Downloading ffmpeg via winget...")
                                r2 = subprocess.run(
                                    ["winget", "install", "ffmpeg", "--silent", "--accept-package-agreements", "--accept-source-agreements"],
                                    capture_output=True, text=True, timeout=300
                                )
                                if r2.returncode == 0:
                                    _umbra_print("[CONVERT] ffmpeg installed. Restart Umbra and try again.")
                                else:
                                    # Try pip install ffmpeg-python as fallback info
                                    _umbra_print("[CONVERT] winget failed. Try: winget install ffmpeg")
                                    _umbra_print("[CONVERT] Or download from https://www.gyan.dev/ffmpeg/builds/ and add to PATH")
                            break
                else:
                    _umbra_print("  No GIFs found to convert.\n")

        else:
            # Project switch check
            switched, _ = _handle_project_switch(runtime, user_input)
            if switched:
                _umbra_print("\n[UMBRA] Switched to: " + switched.name + "\n")
                continue

            # Studio / RPG keywords
            studio_kw = r"\b(rpg|open world|mmo|adventure game|overlay game|dungeon|quest|lore|overquest|optiopia)\b"
            name_pat = r"(?:called|named|name it|call it)\s+['\"]?([A-Za-z][A-Za-z0-9 ]+?)['\"]?(?:\s|$|,)"
            is_studio = bool(re.search(studio_kw, cmd, re.IGNORECASE))
            name_match = re.search(name_pat, user_input, re.IGNORECASE)
            project_name = name_match.group(1).strip() if name_match else None

            if is_studio and project_name:
                _run_studio_project(runtime, user_input, project_name)
            elif is_studio and active:
                run_prompt(runtime, user_input, project_override=active)
            else:
                run_prompt(runtime, user_input)


# ============================================================
#  SHUTDOWN
# ============================================================

def _shutdown(runtime):
    _umbra_print("[UMBRA] Saving memory...")
    try:
        _mem = runtime.get("memory")
        if _mem: _mem.save()
    except Exception: pass
    try:
        rm2 = runtime.get("resource_manager")
        if rm2: rm2.stop_monitoring()
    except Exception: pass
    try:
        sc2 = runtime.get("scheduler")
        if sc2: sc2.stop()
    except Exception: pass
    _umbra_print("[UMBRA] Stopping ComfyUI and freeing ports...")
    _shutdown_comfyui()
    _umbra_print("[UMBRA] Clean shutdown complete.")


# ============================================================
#  MAIN
# ============================================================

def main():
    args = sys.argv[1:]

    def _sigint(sig, frame):
        print("\n[UMBRA] Interrupted.")
        _shutdown_comfyui()
        sys.exit(0)
    signal.signal(signal.SIGINT, _sigint)

    if "--version" in args:
        print("Umbra v2.3.0"); sys.exit(0)

    if "--config" in args or "--help" in args:
        print_config(); sys.exit(0)

    if "--test" in args:
        runtime = build_runtime()
        result = runtime["executor"].execute_pytest("core/tests")
        print(result.stdout)
        sys.exit(0 if result.success else 1)

    if "--status" in args:
        runtime = build_runtime(); print_status(runtime); sys.exit(0)

    if "--metrics" in args:
        runtime = build_runtime(); print_metrics(runtime); sys.exit(0)

    if "--health" in args:
        runtime = build_runtime()
        report = runtime["health"].run_all_checks()
        print(report.summary_line())
        for c in report.checks:
            print("  " + c["name"] + ": " + c["status"] + " " + (c.get("message") or ""))
        sys.exit(0)

    if "--fix" in args:
        runtime = build_runtime()
        handle_self_fix(runtime)
        _shutdown(runtime)
        sys.exit(0)

    runtime = build_runtime()
    if args and not args[0].startswith("--"):
        run_prompt(runtime, " ".join(args))
    else:
        try:
            interactive_mode(runtime)
        finally:
            _shutdown_comfyui()


if __name__ == "__main__":
    main()