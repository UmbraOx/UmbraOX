# UMBRA HANDOFF — Start every new chat with this

## HOW TO START
1. Paste this entire file at the start of a new chat
2. Say: "Continuing Umbra. Pull the repo first, then continue from CURRENT PRIORITY below."
3. Claude pulls repo, reads files, sends batch

---

## REPO & FILES
- **GitHub:** https://github.com/UmbraOx/UmbraOX (PUBLIC)
- **Main file:** `C:\Umbra\Umbra.py` (~4450 lines, v2.4.0)
- **Tests:** `C:\Umbra\test_umbra_full.py` (67 tests) | `C:\Umbra\test_dev_assistant.py` (39 tests)
- **GUI:** `C:\Umbra\core\gui\control_center.py`
- **Game skeleton:** `C:\Umbra\core\assets\game_skeleton.py`
- **Dev assistant:** `C:\Umbra\umbra_dev_assistant.py`

## SYSTEM SPECS
- Windows 11, AMD Ryzen 9 3900XT, RX 7900 XT 20GB, 64GB RAM
- Python 3.12 in `C:\Umbra\venv\` — activate with `venv\Scripts\activate`
- **Also has Python 3.10 installed** — games launch with 3.10 (pygame installed there too)
- Ollama: 14 models — `qwen3:14b` (chat), `qwen2.5-coder:32b` (build)
- ComfyUI: NOT running | Pillow: installed | pygame: installed (both 3.10 + 3.12)

---

## RULES — NEVER BREAK
- **COMPRESS ALL REPLIES — files and results only. Zero explanations. Zero narration.**
- Full drop-in files only. No snippets, no placeholders.
- Every fix needs a passing test before shipping.
- Push to git after every batch.
- 100% local, free, no API keys.
- Backup before every Umbra.py change.
- Open new chat every 2–3 messages to prevent drift.
- Fix support files FIRST. Touch Umbra.py LAST.
- Send downloadable `.py` patch scripts — PowerShell heredocs fail silently due to encoding.
- Never explain what you're doing. Do it. Show the file or result.

## GIT WORKFLOW (from your machine)
```powershell
cd C:\Umbra
venv\Scripts\activate
git add -A
git commit -m "describe"
git push origin main
```

## TO APPLY CLAUDE'S FIXES
Claude commits to its sandbox but CANNOT push. Claude sends `.py` patch scripts you download and run:
```powershell
cd C:\Umbra
python apply_fixes_N.py
git add -A && git commit -m "..." && git push origin main
python Umbra.py
```

---

## CONFIRMED WORKING (as of latest session)
- ✅ GUI opens, streams tokens live, code blocks in blue Consolas
- ✅ 67/67 + 39/39 tests pass (106 total)
- ✅ Game builds: 7/7 agents, 16/16 requirements
- ✅ Games LAUNCH and OPEN to main menu
- ✅ Clicking Start/New Game works (menu returns dict, not list)
- ✅ Enemy patch: handles string OR dict args, catches KeyError
- ✅ `draw_main_menu` agent override stripped — skeleton version always used
- ✅ `txt()` always defined (above draw_hud guard in skeleton)
- ✅ `_safe_input` shows tkinter askstring dialog in GUI mode
- ✅ `which model` lists all Ollama models
- ✅ `run tests` runs both test files, correct counts
- ✅ `fix last game` command works
- ✅ `play last` scans only agent_builds/*_game.py
- ✅ Per-question build popups (5 separate dialogs)
- ✅ dev_asst hooked into _process_command
- ✅ Planner timeout 600s, brief timeout 300s
- ✅ Item agent strict rules (no classes/functions/f-strings)
- ✅ UMBRA_MENU_DICT_PATCH appended to all built games

---

## KNOWN ISSUES / NEXT PRIORITY

### 🔴 CRITICAL
1. **Ollama HTTP 500 errors** — Ollama crashes under heavy agent load (7 agents × 32b model). Agents return empty, game builds with skeleton only. Fix: add retry logic when agent returns HTTP 500, reduce concurrent load, or add `ollama restart` detection.
2. **Build name always "MyGame"** — `build optiopia` should name the game Optiopia. The project name from the command isn't being extracted correctly.

### 🟡 MEDIUM  
3. **Item agent syntax error line 89 every build** — still fires even with strict prompt. Needs AST-validated retry with even stricter prompt.
4. **UI agent syntax error ~50% of builds** — same issue.
5. **Voice/TTS not available** — pyttsx3/SpeechRecognition not installed in venv. Run: `pip install pyttsx3 SpeechRecognition --break-system-packages`
6. **`snake game` command routes to pipeline** (outputs separate files) instead of agent game builder. Need to route "make a X game" to `_run_deep_build`.
7. **Game aesthetics** — games work but look basic. Agent prompts need art/polish pass.

### 🟢 LOW
8. **UTF-8 header missing** from Umbra.py — add `# -*- coding: utf-8 -*-` to line 1
9. **Status shows "v2.0.0 Runtime Core v2"** — remove duplicate from boot sequence
10. **apply_fixes_*.py scripts accumulating** in repo root — clean up after session

---

## ARCHITECTURE (do not change)
```
UmbraRuntimeKernel → UmbraRuntimeSpine → BossAgent → TaskEngine
  → GenerationEngine → AssetStore
Entry: python Umbra.py → build_runtime() → interactive_mode()
  → _launch_gui() → mainloop()
Dev assistant hooks into _process_command() before all other handlers.
```

## KEY FUNCTIONS
| Function | File | Purpose |
|---|---|---|
| `_process_command()` | Umbra.py:~2760 | Routes all GUI input |
| `_stitch_game()` | Umbra.py:~957 | Assembles 7 agent outputs |
| `_run_agent()` | Umbra.py:~845 | Runs single agent with retry |
| `_syntax_repair()` | Umbra.py:~821 | LLM-based syntax fix |
| `_ollama_stream()` | Umbra.py:~687 | Streams tokens from Ollama |
| `_safe_input()` | Umbra.py:~196 | tkinter dialog in GUI mode |
| `strip_imports()` | inside `_stitch_game` | Strips agent fn overrides |
| `draw_main_menu()` | game_skeleton.py:~713 | Always returns dict of Rects |

## COMPLETION STATUS
- Core boot + GUI: 95%
- Chat routing + dev assistant: 90%
- Game build pipeline: 82%
- Game launch + playability: 75% (opens, menu works, gameplay needs testing)
- Agent syntax reliability: 70%
- Self-repair: 60%
- **Overall: ~82%**

## WHAT'S LEFT FOR 100%
1. Fix Ollama 500 retry in agents
2. Fix project name extraction (build X → game named X)
3. Route "make a game" to deep build not pipeline
4. Fix item/UI agent syntax errors (needs AST retry)
5. Test full gameplay loop (combat, inventory, quests)
6. Install voice/TTS deps
7. Polish agent prompts for better game quality