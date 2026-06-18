# UMBRA — Complete Reference Guide
**Version 2.0.2 | Autonomous AI Runtime OS**

---

## TABLE OF CONTENTS
1. [What is Umbra?](#what-is-umbra)
2. [How to Start Umbra](#how-to-start-umbra)
3. [How Umbra Understands You](#how-umbra-understands-you)
4. [Complete Command Reference](#complete-command-reference)
5. [Self-Repair System](#self-repair-system)
6. [Self-Install System](#self-install-system)
7. [Image Generation](#image-generation)
8. [Video & GIF Generation](#video--gif-generation)
9. [Game & Application Building](#game--application-building)
10. [Project Management](#project-management)
11. [Voice Input & Text-to-Speech](#voice-input--text-to-speech)
12. [Memory System](#memory-system)
13. [Health & Diagnostics](#health--diagnostics)
14. [Testing Everything Works](#testing-everything-works)
15. [Finishing Umbra — Prompts to Complete It](#finishing-umbra--prompts-to-complete-it)
16. [Troubleshooting](#troubleshooting)

---

## What is Umbra?

Umbra is a **self-repairing, self-extending autonomous AI runtime OS** that runs on your PC. It:

- Answers everyday questions (capital cities, time, general knowledge)
- Builds complete software: games, apps, tools, agents, pipelines
- Generates images and videos via ComfyUI (your AMD GPU)
- Manages multi-project workspaces with memory between sessions
- Fixes its own bugs and installs new features when you ask
- Listens to your mic and can speak responses back
- Runs entirely **free** — Ollama for AI, ComfyUI for images/video, no subscriptions

**Umbra's brain:** `qwen2.5-coder:14b` via Ollama (local, free, private)
**Image/Video engine:** ComfyUI (DirectML / AMD)
**Location:** `C:\Umbra\`

---

## How to Start Umbra

### Normal start (interactive chat)
```powershell
cd C:\Umbra
venv\Scripts\activate
python umbra.py
```

### Start with a single command
```powershell
python umbra.py make me a platformer game called SkyJump
```

### CLI flags (no interactive mode)
```powershell
python umbra.py --status      # Print status and exit
python umbra.py --health      # Run health checks and exit
python umbra.py --metrics     # Show pipeline metrics and exit
python umbra.py --fix         # Auto-fix all bugs and exit
python umbra.py --test        # Run full test suite and exit
python umbra.py --version     # Print version and exit
python umbra.py --config      # Print config/help and exit
```

### What happens on startup
1. ComfyUI is auto-launched in a new window (port 8188)
2. Memory from previous sessions is loaded
3. Scheduler starts 4 background jobs
4. Status is printed — you should see `Ready: YES`

### What happens on exit (`exit` or Ctrl+C)
- Memory is saved
- ComfyUI process is terminated
- Port 8188 is freed automatically
- You will NOT need to run `taskkill` manually anymore

---

## How Umbra Understands You

**Just type naturally.** Umbra classifies every message into one of these intents:

| Intent | Example phrases | What Umbra does |
|--------|----------------|-----------------|
| `question` / `chat` | "what is the capital of France", "how are you" | Answers via Ollama LLM |
| `image_request` | "generate an image of...", "make a picture of..." | Sends to ComfyUI |
| `video_request` | "make a video of...", "create a 10 second clip of..." | Sends to ComfyUI video pipeline |
| `game_request` | "build a game called X", "make an RPG..." | Builds full pygame game |
| `task` | "build me a REST API", "create a data parser" | Runs autonomous pipeline |
| `self_fix` | "fix all bugs", "fix yourself" | Self-repair engine |
| `self_install` | "install X into umbra", "add X to umbra" | Self-install engine |

**Umbra will ask clarifying questions** before building complex games/projects when your description is vague. Answer them and Umbra will proceed.

---

## Complete Command Reference

### SYSTEM
```
status              — Show current provider, model, memory, scheduler, ComfyUI status
health              — Run all health checks (Python, memory, disk, modules)
metrics             — Show pipeline run statistics
version             — Show Umbra version number
config              — Show configuration guide and options
help                — Same as config
handoff             — Generate a markdown session summary (saves to sessions/)
scheduler           — Show background scheduler jobs
exit / quit / q     — Shut down cleanly (closes ComfyUI, frees ports)
```

### SELF-REPAIR (Highest Priority — runs before anything else)
```
fix all bugs            — Scan all modules, auto-fix with LLM, ask approval, verify with tests
fix yourself            — Same as above
fix all errors          — Same as above
fix all issues          — Same as above
repair yourself         — Same as above
fix everything          — Same as above
self fix                — Same as above
fix <module_name>       — Fix a specific module (e.g. "fix runtime_video_generator")
scan modules            — Syntax-check all core/runtime modules, report broken ones
python umbra.py --fix   — Fix from command line without interactive mode
```

### SELF-INSTALL (Build & add new features to Umbra itself)
```
install <feature> into umbra          — Build the feature, auto-install deps, integrate
add a <feature> into umbra            — Same
build a <feature> and install it      — Same
build and install <feature>           — Same
integrate runtime_<module_name>       — Wire an already-built module into umbra.py

Examples:
  install a gif generator into umbra
  install a video pipeline into umbra
  add a speech synthesizer into umbra
  add a web scraper into umbra
  install a continuous mic listener into umbra
  build a GUI window launcher and install it into umbra
  integrate runtime_gif_generator
```

**What the approval screen shows you:**
```
──────────────────────────────────────────────────────────
[UMBRA APPROVAL REQUIRED]
  Plan: Create runtime_gif_generator.py + install 1 package(s)
  Preview (20 lines shown):
    import os
    from PIL import Image
    ...
  Dependencies to auto-install:
    pip install Pillow
──────────────────────────────────────────────────────────
  Approve? [y/N]:
```
Type `y` and Umbra will write the module AND run `pip install` for every required package automatically. No manual pip needed.

### IMAGE GENERATION
```
generate an image of <description>
make a picture of <description>
create an image of <description>
draw <description>

Examples:
  generate an image of a cat in armour
  make a picture of a fantasy castle at sunset
  create an image of a robot in a forest

images                  — List all generated images
show images             — Same
list images             — Same
```
Images save to: `C:\Umbra\workspaces\images\`

### VIDEO GENERATION
```
make a video of <description>
generate a video of <description>
create a 10 second video of <description>
make a gif of <description>

videos                  — List all generated videos/gifs
show videos             — Same
list videos             — Same
```
Videos save to: `C:\Umbra\workspaces\videos\`

> **Note:** Video generation via ComfyUI requires a video-capable workflow/model. If ComfyUI doesn't have one installed, ask Umbra to install it: `install a video generation pipeline into umbra`

### GAME & APPLICATION BUILDING
```
make a game called <name>
build an RPG called <name> with <description>
create an overlay game called <name>
make a platformer called <name>
build a simulation game called <name>

Complex (uses Studio pipeline — asks clarifying questions):
  make an RPG called Optiopia with 3 gods and open world
  build the overlay game Overquest with auto-dungeon crawl
  make an MMORPG called Aetheria with crafting and quests

Application building:
  build me a REST API for managing tasks
  make a file organizer tool
  create a Discord bot that tracks game stats
  build a data dashboard with charts

play last               — Launch the most recently built game
play <project_name>     — Launch a specific project's game
run last                — Same as play last
```
Games save to: `C:\Umbra\workspaces\<project_slug>\`

### PROJECT MANAGEMENT
```
projects                        — List all projects
list projects                   — Same
work on <project_name>          — Switch active project context
lets work on <project_name>     — Same
continue <project_name>         — Same
open <project_name>             — Same
project files                   — List files in active project
show files                      — Same
files                           — Same
```

### VOICE INPUT & TEXT-TO-SPEECH
```
listen                  — Push-to-talk: speak once, Umbra executes what you said
voice                   — Same as listen
speak                   — Same as listen
mic                     — Same as listen

voice on                — Toggle continuous mic: Umbra listens between every prompt
continuous voice on     — Same
always listen           — Same
voice off               — Turn off continuous listening
continuous voice off    — Same
stop listening          — Same

tts on                  — Toggle text-to-speech: Umbra speaks its responses aloud
text to speech on       — Same
speak responses         — Same
tts off                 — Turn off text-to-speech
text to speech off      — Same
stop speaking           — Same
```

### MEMORY
```
remember <fact>         — Store a fact (e.g. "remember my project uses Python 3.12")
recall <query>          — Search stored memory (e.g. "recall game files")
memory                  — Show memory entry count and recent keys
what do you remember    — Same as memory
```

### DIAGNOSTICS & TESTING
```
health                  — Full health report
test                    — Run all 655 tests in core/tests/
run tests               — Same
validate                — Validate last pipeline run (score/100)
validate last           — Same
review                  — Code review of last pipeline run
review last             — Same
code review             — Same
history                 — Show all runs this session
show history            — Same
past runs               — Same
resume                  — Resume any failed/partial runs
improve                 — Run self-improvement analysis loop
improve yourself        — Same
```

---

## Self-Repair System

Umbra's self-repair engine scans `C:\Umbra\core\runtime\` for broken modules, asks the LLM to fix them, shows you a preview, backs up originals, writes fixes, then re-runs tests to confirm.

### How it works step by step:
1. Scans every `.py` file in `core/runtime/` with Python's `ast.parse()`
2. Reports any files with syntax errors
3. Runs `pytest core/tests -q` to find test failures
4. For each broken file: asks LLM to generate a fix
5. Verifies the fix parses correctly
6. Shows you a preview and asks approval
7. Makes a timestamped `.bak` backup: `filename.py.bak.20260530_120000`
8. Writes the fix
9. Re-runs tests to confirm improvement

### Backup files
All backups land next to the original file:
```
C:\Umbra\core\runtime\runtime_video_generator.py.bak.20260530_120000
```
To restore: copy the .bak file back over the original.

---

## Self-Install System

When you ask Umbra to install a feature, it:
1. Generates a Python module in `core/runtime/`
2. Scans the generated code for imports
3. Checks which imports are missing from your venv
4. Shows you a single approval screen listing **both** the code preview AND the packages it will install
5. After approval: runs `pip install` for each missing package, then writes the module
6. Tests that the module imports correctly
7. Prints integration instructions and offers to auto-patch `umbra.py`

### Auto-dep install means you never need to manually `pip install` anything. Umbra handles it all after a single `y`.

---

## Image Generation

Umbra uses ComfyUI (DirectML, your AMD GPU) for all image generation.

### Requirements
- ComfyUI running (auto-launched by Umbra)
- Model: `v1-5-pruned-emaonly.ckpt` in `C:\ComfyUI\models\checkpoints\`
- websocket_image_save custom node (already installed based on your setup)

### Test image generation:
```
umbra> generate an image of a red dragon breathing fire
```
Expected output:
```
[UMBRA] Generating image...
[IMAGE] Saved: C:\Umbra\workspaces\images\image_20260530_120000.png
[IMAGE] View: open C:\Umbra\workspaces\images\
```

If you get `[IMAGE] Generation failed` — make sure ComfyUI is running and check that the model file exists.

---

## Video & GIF Generation

### GIF generation (uses PIL — already installed):
```
umbra> install a gif generator into umbra
```
After installing:
```
umbra> make a gif of an explosion
```

### Video generation (requires ComfyUI video workflow):
```
umbra> install a video pipeline into umbra
```
For full AnimateDiff video generation, you also need:
- `AnimateDiff` ComfyUI extension
- A motion module model

Ask Umbra:
```
umbra> install an animatediff video generator into umbra
```

---

## Game & Application Building

### Simple game (direct streaming, fast):
```
umbra> make a space shooter game
```

### Named project game (full Studio pipeline):
```
umbra> make an RPG called Optiopia with 3 gods and open world
```
Umbra will ask you clarifying questions then generate:
- World lore document
- Game mechanics design
- Player character spec
- Quest list
- Complete pygame game file

### Game quality rules Umbra enforces automatically:
- All dictionary keys lowercase
- All player input uses `.lower().strip()`
- Class selection uses pygame buttons (not terminal input)
- Health bar drawn on screen
- Enemy AI moves toward player
- Sprites stay within screen bounds
- `pygame.display.flip()` every frame
- `if __name__=='__main__': main()` at bottom

### After a game is built:
```
umbra> play last                    — Launch it
umbra> fix the player movement      — Edit and retest
umbra> add a magic spell system     — Extend it
umbra> review                       — Code quality score
```

---

## Project Management

Every project stores its files, conversation history, and metadata in:
```
C:\Umbra\workspaces\projects\<project_slug>\
```

Switch projects at any time:
```
umbra> work on Optiopia
umbra [Optiopia]> add a new dungeon area
```

The prompt prefix shows your active project so you always know the context.

---

## Voice Input & Text-to-Speech

### Requirements
- `pip install SpeechRecognition pyaudio` (or ask Umbra: `install voice input into umbra`)
- Microphone connected

### Push-to-talk (default):
```
umbra> listen
[MIC] Listening...
[MIC] Heard: make a game about dragons
```

### Continuous listening (toggles on/off):
```
umbra> voice on         — Umbra listens between every prompt
umbra> voice off        — Stop continuous listening
```
In continuous mode Umbra tries the mic first; if nothing heard within 4 seconds it falls back to keyboard input.

### Text-to-speech (Umbra speaks responses):
```
umbra> tts on           — All responses are spoken aloud
umbra> tts off          — Silent mode
```
Uses `pyttsx3` (offline, free). Install with: `install text to speech into umbra`

---

## Memory System

Umbra remembers across sessions via `C:\Umbra\sessions\memory_store.json`

```
umbra> remember my favourite game style is roguelikes
umbra> remember the Optiopia world has 3 gods: Sol, Vex, and Mira
umbra> recall optiopia gods
[MEMORY: 'optiopia gods']
  user_note:3: the Optiopia world has 3 gods: Sol, Vex, and Mira
```

Memory is also used internally to track run history, game files, and project state.

---

## Health & Diagnostics

```
umbra> health
[HEALTH] 8/8 checks passed — system healthy
  + python_version: pass
  + disk_space: pass
  + core_modules: pass
  + workspace_writable: pass
  + memory_store: pass
  ...
```

```
umbra> status
[STATUS]
  Provider : ollama (FREE)
  Model    : qwen2.5-coder:14b
  Ready    : YES
  Graph    : 0 nodes
  Runs     : 0 this session
  Memory   : 18 entries stored
  Resources: mem=23%
  Scheduler: 4 job(s) running
  Images   : ComfyUI connected (port http://localhost:8188)
  Video    : ComfyUI connected
  Projects : 2 total
```

---

## Testing Everything Works

Run these tests in order to verify Umbra is fully operational:

### 1. Basic startup test
```powershell
python umbra.py --status
```
Expected: Provider=ollama, Ready=YES

### 2. Full test suite
```powershell
python -m pytest core/tests -q --timeout=30
```
Expected: 654 passed, 1 skipped, 0 failed

### 3. Self-fix test (should come back clean)
```
umbra> fix all bugs
```
Expected: `Umbra is clean — no issues found!`

### 4. Image generation test
```
umbra> generate an image of a blue sphere on white background
```
Expected: `[IMAGE] Saved: C:\Umbra\workspaces\images\image_XXXXXX.png`

### 5. General question test
```
umbra> what is the capital of Japan
```
Expected: `[UMBRA] Tokyo is the capital of Japan.`

### 6. Simple game test
```
umbra> make a simple pong game
umbra> play last
```
Expected: pygame window opens with pong game

### 7. Memory test
```
umbra> remember testing is working correctly
umbra> recall testing
```
Expected: Returns the stored note

### 8. Voice test (if mic connected)
```
umbra> listen
```
Expected: `[MIC] Listening...` then captures your speech

### 9. Install test
```
umbra> install a calculator tool into umbra
```
Expected: Approval screen → `y` → import test passes

### 10. Port cleanup test
```
umbra> exit
```
Then in PowerShell:
```powershell
netstat -ano | findstr :8188
```
Expected: No output (port freed)

---

## Finishing Umbra — Prompts to Complete It

Send these prompts **to Umbra** (not to Claude) after startup to finish all remaining features. Copy-paste each one:

### BATCH 1 — Core missing features
```
install a full GUI window into umbra that opens when umbra starts, shows a chat box, has an input field, shows umbra status, and lets me talk to umbra from the window
```
```
install a continuous mic listener with push to talk and always on toggle into umbra, default set as push to talk, visible on the GUI window
```
```
install a text to speech system using pyttsx3 into umbra that speaks umbra responses when tts is enabled
```
```
install an animated gif generator into umbra using PIL that creates animated gifs from a list of images or from a text description by generating frames
```

### BATCH 2 — Video pipeline
```
install a video generation pipeline into umbra that uses ComfyUI websocket API to generate short videos using AnimateDiff workflow, saves to workspaces/videos, and reports progress
```

### BATCH 3 — Game enhancements
```
install a game auto-tester into umbra that launches a built game, monitors for crashes or errors, captures output, and reports issues back so umbra can fix them automatically
```
```
install a game asset generator into umbra that creates simple pixel art sprites using pygame.Surface and draw functions for characters, enemies, tiles, and items without needing external image files
```

### BATCH 4 — Self-improvement
```
install a dependency scanner into umbra that checks all installed modules, finds outdated packages, and offers to update them one by one with approval
```
```
install a code quality improver into umbra that reviews the last generated file, scores it, and automatically refactors it for better performance if score is below 80
```

### BATCH 5 — Productivity tools
```
install a web search tool into umbra using requests and html parsing that can search the web and return summarized results when I ask about current events
```
```
install a file manager into umbra that can list, copy, move, delete, and organize files in my projects folder when I ask it to
```
```
install a reminder and task tracker into umbra that stores tasks in memory, reminds me when I open umbra if tasks are pending, and lets me mark them done
```

### BATCH 6 — Wire everything in
After each install completes, run:
```
integrate runtime_<module_name>
```
For example:
```
integrate runtime_full_gui_window
integrate runtime_continuous_mic_listener
integrate runtime_text_to_speech_system
integrate runtime_animated_gif_generator
integrate runtime_game_auto_tester
integrate runtime_text_speech_system_using
integrate runtime_video_generation_pipeline
integrate runtime_game_autotester
integrate runtime_game_asset_generator
integrate runtime_dependency_scanner
integrate runtime_code_quality_improver
integrate runtime_web_search_tool
integrate runtime_file_manager
integrate runtime_reminder_task_tracker
 
fix runtime_full_gui_window
fix runtime_continuous_mic_listener
fix runtime_text_to_speech_system
fix runtime_animated_gif_generator
fix runtime_game_auto_tester
fix runtime_text_speech_system_using
fix runtime_video_generation_pipeline
fix runtime_game_autotester
fix runtime_game_asset_generator
fix runtime_dependency_scanner
fix runtime_code_quality_improver
fix runtime_web_search_tool
fix runtime_file_manager
fix runtime_reminder_task_tracker

```

### After all installs — final cleanup
```
fix all bugs
```
```
python umbra.py --test
```
If tests all pass — Umbra is 100% complete.

---

additional tests:

Example 1:
Make an overlay game that acts like an idle dungeon crawler on my desktop. It should only take up a corner of the screen, have an shop, inventory, equipment, menu and gallery tab in the top right, the left should display power level and health. Monsters that get defeated should drop items and gold. Monsters will scale in level every 10 levels and every 5 levels the gear in the shop and item drops will go up a level so as long as the player has space in the inventory or buys things from the shop they can always defeat the enemys. Power level will come from gear/items the character has equiped. We will need items, characters, enemys. Every time a boss is defeated (every 5 levels) the player gets a gallery drop. Gallery drops are randomly generated images of cats in armour. After completing a level all the drops, gold etc from the level will automatically be put into the players inventory if they have space, there should be 30 inventory slots, the players party should have 4 available spots for teammates and themself. You can buy equipment like weapons, armour, etc from the shop, the shop has 3 tabs, the first tab is for buying gear/equipment has 30 slots of items for sale, the second tab is for buying teammates there should be 5 slots for available characters here and a 6th slot that can only be used 1 time and is a free teammate, the third slot is a slot mechine that a player can spend 10 gold to spin having a chance to win 100 gold, 50 gold, 12 gold, a teammate or a gallery photo/drop, the menu tab should allow players to exit the game. All windows/tabs/shops/etc should have a way to get back to the battlezone, shops, inventory, menu, etc.

Example 2:
Make an overlay game/Ai girlfriend thats nsfw. she should start off with cloths on and dance on the screen, when clicked on should loose cloths and if naked should change poses. She should send nsfw images of herself every 5 minutes that the game/window is active. While wearing cloths should do normal things like scrolling on her phone, playing games on the computer, baking pie or cookies, etc the more cloths she looses the more lude she gets and when shes naked she starts playing with her brests, pussy and asshole. There should also be a small (but readable) chat window that stays next to the ai girlfriend that allows her to talk with me about things, and allows me to talk with her, ask her to do things, if I ask her to send me picture or videos she makes them and sends them to me while she does the animations, example if I ask her to bend over and take a picture of her ass for me she bends over and takes a picture from her phone, of her ass, all animated and sends it to me right then (dose not effect the additional 1 photo every 5 min) all images are saved to a gallery tab I can click on at anytime in the overlay gui so I can view any photos made at any time.

Example 3:
Lets edit optiopia, last time I tried to play the powershell asked me what class I want to be, all questions, actions, etc should be asked in the game window I shouldnt be talking to powershell while playing the game. The game also crashed so we need that fixed. I should be able to scroll the selections with my arrow keys and press enter to select things, lets add the "e" key to attack, the "f" key to pick up items that are in the world and or droped by enemys, the "esc" key should open a menu window with sound settings, video settings (such as full screen, windowed, etc), save game (can have 10 saves with an overwrite save feature/button), exit to desktop and exit to menu selections. There should be a start menu that displays the name of the game and says press anything to start, after pressing something it should open to a screen asking if the player wants to continue (if a saved game is available), new game, saved files, and open gallery (to view collected pictures). each character should have an animation for attacking, idle walking, sleeping, casting spells, shooting the bow, etc enemys, npcs, and characters all should have animations for what they are doing in the world. Lets make the first town it should be small lets do like 4 buildings and 8 homes/tents some stalls, one of the shops should sell wagons, the player can buy a wagon for 1 gold and it acts as a second inventory or storage they can also buy a horse for 5 gold and attach it to the wagon, when they have a horse attached to the wagon it can also be used as a mount and ridden around.

## Troubleshooting

### ComfyUI port blocked after crash
```powershell
netstat -ano | findstr :8188
taskkill /PID <PID_from_above> /F
```
Or just start Umbra again — v2.0.2 kills the port on startup automatically.

### "LLM call failed: timed out"
Ollama is running but the model is taking too long. Try:
```powershell
ollama list                    # Check model is downloaded
ollama run qwen2.5-coder:14b  # Test it manually
```
If gaming mode is active (RAM > 40%), Umbra throttles — wait for it to drop.

### "ComfyUI not running" in status
```powershell
cd C:\ComfyUI
run_cpu.bat
```
Or let Umbra launch it: restart Umbra — it auto-launches ComfyUI.

### Image fails first try, works second try
This is normal — ComfyUI takes ~10 seconds to load the model on first generation. Just resend the prompt.

### Game crashes with "FileNotFoundError: character.png"
The LLM generated code that tries to load an external image. Tell Umbra:
```
umbra> fix the game — it crashes because it can't find character.png, make it draw the character with pygame shapes instead of loading an image file
```

### Module import fails after install
```
umbra> fix all bugs
```
Or check the specific module:
```
umbra> scan modules
```

### Tests showing 0 passed / 0 failed
The pytest process is timing out internally. Run manually:
```powershell
python -m pytest core/tests -q --timeout=30
```

### Umbra shows "Ready: NO"
Ollama is not running. Start it:
```powershell
ollama serve
```
In a separate window, or restart it from the system tray.

---

## File Structure Reference

```
C:\Umbra\
├── umbra.py                    ← Main entry point (this file)
├── umbra_config.json           ← Configuration (provider, model, paths)
├── core\
│   ├── runtime\                ← All runtime modules (100+ files)
│   │   ├── runtime_llm_provider.py
│   │   ├── runtime_image_generator.py
│   │   ├── runtime_video_generator.py
│   │   ├── runtime_conversation_engine.py
│   │   ├── runtime_voice_input.py
│   │   └── ... (90+ more)
│   └── tests\                  ← 655 automated tests
├── workspaces\
│   ├── images\                 ← Generated images
│   ├── videos\                 ← Generated videos/gifs
│   ├── projects\               ← Named project files
│   └── run_XXXX\               ← Pipeline run outputs
├── sessions\                   ← Session history + memory_store.json
├── memory\                     ← Project memory
├── plugins\                    ← Runtime plugins
└── snapshots\                  ← Backup snapshots
```

---

*Generated for Umbra v2.0.2 — keep this file at `C:\Umbra\UMBRA_README.md`*