import datetime

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\README.md"

with open(FP, "r", encoding="utf-8") as f:
    old = f.read()
with open(FP + f".bak45_{ts}", "w", encoding="utf-8") as f:
    f.write(old)

NEW_README = r'''# UMBRA — Local Autonomous AI Runtime OS

**v3.1.0** | Python 3.12 (venv) | Windows 11 | 100% local, no subscriptions, no API keys

Umbra is a fully local, subscription-free AI production studio. You describe
what you want in plain English; Umbra plans it, dispatches a multi-agent
pipeline, generates real working code/media, validates it automatically, and
tells you honestly whether it worked — before you ever have to find out the
hard way.

Everything runs on your own hardware: Ollama for language generation, ComfyUI
for images/animation, pygame for game output. No cloud, no per-token cost, no
account.

**The goal from day one:** Umbra should be able to build games on the scale
of *Graveyard Keeper*, *RuneScape*, *Skyrim*, or *Fable* — persistent worlds,
living NPCs, economies, quests, crafting, the works — not just small demo
games. Small test games are the current proving ground for the pipeline's
reliability, not the ceiling.

For day-to-day session continuity (what's actually done, what's broken, what
to do next), **`UMBRA_HANDOFF.md` is the live source of truth** — read it
fresh every session. This README is the stable overview: what Umbra is, how
it's built, and where it's headed.

---

## Quick Start

```powershell
cd C:\Umbra
python Umbra.py
```

This boots the GUI Control Center, auto-starts Ollama and ComfyUI if they
aren't already running, and drops you into a chat-style window. Just type
naturally:

```
make a game called QuickTest
build a full game called Optiopia          (all 7 agents, larger scope)
make an image of a fantasy castle
make a gif of a dragon flying
listen                                       (voice input)
fix all bugs
```

---

## Hardware / stack this is built for

| Piece | What we use |
|---|---|
| OS | Windows 11 |
| GPU | AMD Ryzen 9 3900XT / RX 7900 XT 20GB (DirectML - no CUDA) |
| RAM | 64GB |
| Language models | Ollama, local (`qwen2.5-coder:32b` for builds, `qwen3:14b` for chat) |
| Image/animation | ComfyUI + AnimateDiff-Evolved, DirectML backend |
| Game runtime | pygame |
| GUI | tkinter Control Center |

DirectML on this GPU is genuinely slow for some ops (documented upstream as
"barely works... might be removed soon") - this is why timeouts throughout
Umbra are generous (minutes, not seconds) and why the smoke test below
matters so much: local generation is too slow to just retry blindly.

---

## What Umbra can do right now (v3.1.0)

### Games (small test games - reliable; large-world scope - not yet)
- `make a game called X` - fast single-pass build
- `build a full game called X` / `build an RPG called X` - full 7-agent
  studio pipeline (world, character, item, mechanic, UI, quest, economy
  agents), stitched into one deterministic game file
- Every build runs an **automated headless smoke test** immediately after
  stitching - constructs the player (against every actual class-select
  option), camera, spawns enemies/NPCs, exercises their update/draw methods,
  all in an isolated subprocess in about a second - and tells you PASS/FAIL
  with a real traceback *before* declaring the build complete. This is not a
  guarantee of a bug-free game, but it catches the whole class of "crashes
  the instant you click something" bugs that used to only surface after a
  multi-hour build and a manual playthrough.
- `play last` / `play <name>` to launch
- `fix last build` to attempt an automatic repair if the smoke test fails

### Media generation
- `make an image of <description>` - real Stable Diffusion via ComfyUI,
  professional-grade negative prompts (anatomy, faces, eyes, teeth), runs
  in a background thread so the GUI stays responsive
- `make a gif of <description>` - real AnimateDiff-Evolved animation,
  VRAM-safe params, background thread
- `make a video of <description>` / `assemble video frames` - present in
  the command list; **not yet verified working** in practice, needs a
  real test pass

### Voice / TTS
- `listen` - one-shot mic capture, routes the transcribed text back through
  Umbra as if typed
- `voice on` / `voice off` - continuous listening
- `tts on` / `tts off` - spoken responses
- PyAudio auto-installs at boot (with a pipwin fallback for Windows)

### Self-repair / maintenance
- `fix all bugs`, `fix yourself`, `fix workspace`, `scan modules`
- `list files`, `clean up old files`
- `remember <fact>` / `recall <query>` - persistent memory store

### Not yet built (the rest of the original vision)
- Large-scale persistent game worlds (save systems, NPC schedules and
  personalities, living economies - "world brain")
- Music generation
- Verified working video generation
- 3D asset generation
- AI companion/girlfriend feature
- General-purpose multi-AI-agent helper framework (beyond game-building)
- General (non-game) application building

---

## Roadmap

### NOW (finish making the foundation actually solid)
1. Confirm the class-select crash class is fully closed with a fresh test
   log (batches 40-43 addressed the known causes; needs a clean
   post-fix confirmation, not another guess)
2. Constrain UI agent output size/scope - it has ballooned to 3000+ lines
   in a single build, which slows every build and is unnecessary surface
   area for bugs
3. Verify `make a video of X` / `assemble video frames` actually work end
   to end, or fix them
4. Keep `UMBRA_HANDOFF.md` updated every session - it fell 22 batches out
   of date once already; that must not happen again

### NEXT (scale the game builder toward the real target)
5. Persistent world state + save/load for generated games (not just a
   single play session)
6. NPC schedules, personalities, and simple dialogue/relationship systems
7. Living economy simulation across a game world ("world brain")
8. Larger, streamed/chunked maps instead of a single fixed layout
9. A genre-aware agent brief that scales the 7-agent pipeline's ambition
   up toward Graveyard Keeper / RuneScape / Skyrim / Fable-sized scope
   when asked for a "full" or "large" game, instead of always producing
   roughly the same small-scale result regardless of ask

### LATER (the rest of the original studio vision)
10. Music generation pipeline
11. 3D asset generation
12. AI companion/girlfriend feature
13. General-purpose multi-agent helper framework, usable outside games
14. General (non-game) application building

---

## Working conventions (for whoever is patching this - human or AI)

These rules exist because they were each learned the hard way over many
sessions. Breaking them re-introduces bugs that were already fixed once.

1. **Full drop-in files only.** Never send a snippet, diff fragment, or
   "add this somewhere" instruction. Every patch is a complete, runnable
   `apply_fixes_N.py` that can be run start to finish with no manual editing.
2. **Numbered batch scripts.** Each session's changes are
   `apply_fixes_N.py` (makes the edit, backs up the original, AST-validates
   the result) + `push_batchN.py` (git add/commit/push). N always increments
   from whatever the last batch in the repo was - check `UMBRA_HANDOFF.md`
   or `git log` first.
3. **AST-validate before delivering.** Every patch script parses the
   resulting file with `ast.parse()` and refuses to report success if it
   doesn't parse. This applies to `Umbra.py` and any other real Python file;
   `core/assets/game_skeleton.py` is a text *template* (has `__PLACEHOLDERS__`)
   so it's validated with placeholders substituted first.
4. **Verify the exact anchor text against the live repo before writing a
   patch**, not from memory of what a file looked like in an earlier batch.
   Pull first (`git pull origin main`), then grep/view the real current
   content, then build the `OLD`/`NEW` replacement from that.
5. **No PowerShell heredocs, no placeholders, no "insert your code here."**
   Every script is ready to run as-is.
6. **`git push every batch`.** Don't let local changes pile up unpushed.
7. **Compressed replies during active patching.** Patch scripts and short
   instructions, not long explanations, unless the user asks for the
   reasoning or a status/planning conversation like this one.
8. **Backup files are `.py.bakN_TIMESTAMP`** - covered by `.gitignore`
   (fixed in batch 33 after it turned out the old patterns didn't actually
   match this naming and silently committed every backup for months).
9. **Test new patches before delivering them.** Copy the target file from
   the live repo, run the patch script against the copy, confirm it reports
   success and (for logic changes) actually reproduces + fixes the original
   bug with a standalone repro script - not just "the patch applied."
10. **Update `UMBRA_HANDOFF.md` at the end of every session** with what
    shipped, what's still open, and what's next. It is the thing that
    carries context forward, not any single chat.

---

## Architecture

```
Umbra.py
├─ build_runtime()              -- assembles all subsystems, boot sequence
├─ interactive_mode()           -- CLI text loop (also has its own voice/tts handling)
├─ _launch_gui()                -- tkinter Control Center, mainloop
├─ _process_command()           -- routes ALL GUI input (single dispatcher):
│    ├─ gif/image regex          -> RuntimeAnimatedGifGenerator / RuntimeImageGenerator
│    │                              (ComfyUI HTTP API, background thread)
│    ├─ listen/voice/tts         -> RuntimeVoiceInput
│    ├─ verb+noun game detection -> _run_deep_build() (7-agent pipeline)
│    │    └─ _stitch_game()        -- assembles agent output + game_skeleton.py
│    │         ├─ strip_imports()   -- strips agent overrides of skeleton
│    │         │                       contract functions/classes
│    │         ├─ strip_toplevel_calls() -- removes stray executable agent code
│    │         ├─ UMBRA_PLAYER_PATCH, UMBRA_ENEMY_PATCH, UMBRA_METHOD_SAFETY_PATCH
│    │         │                       -- runtime safety nets for agent classes
│    │         └─ _run_smoke_test()  -- headless post-build validation, subprocess
│    ├─ generic step-pipeline    -> for non-game code requests
│    ├─ remember/recall          -> RuntimeMemoryStore
│    └─ fix yourself/etc.        -> self-repair handlers
├─ _ollama_stream()              -- HTTP streaming to Ollama, wall-clock timeout enforced
└─ RuntimeLauncher                -- auto-starts Ollama + ComfyUI at boot
```

### Key files
| What | File |
|---|---|
| Main entry point, command routing, build pipeline | `Umbra.py` |
| Game template (skeleton, `_umbra_flex`, contract fallbacks) | `core/assets/game_skeleton.py` |
| Image generation | `core/runtime/runtime_image_generator.py` |
| GIF/animation generation | `core/runtime/runtime_animated_gif_generator.py` |
| Ollama/ComfyUI auto-launch | `core/runtime/runtime_launcher.py` |
| Live session status/priorities | `UMBRA_HANDOFF.md` |

---

## Full command reference

```
START
  python Umbra.py                interactive GUI mode

SYSTEM
  status  health  metrics  version  help  exit

SELF-REPAIR
  fix all bugs / fix yourself / fix workspace / fix last build
  fix the gui / fix the gif / fix the video / fix project <name>
  scan modules

BUILD GAMES
  make a game called <name>              direct, fast, single pass
  build an RPG called <name>              studio pipeline
  build a full game called <name>         all 7 agents, full build
  make a game like Skyrim called <name>   deep build with all systems
  play last / play <name>

GENERATE MEDIA
  make a gif of <description>
  make an image of <description>
  make a video of <description>           unverified - test before relying on this
  assemble video frames                   unverified - test before relying on this

FILES
  list files / list workspace files / clean up old files

PROJECTS
  projects / work on <name> / project files

VOICE & TTS
  listen / voice on / voice off / tts on / tts off

MEMORY
  remember <fact> / recall <query> / memory

DIAGNOSTICS
  test / validate / review / history / resume / handoff / improve
```

---

## Running tests

```powershell
python test_umbra_full.py
python test_dev_assistant.py
python test_gameplay_crash.py
```

---

Built for one person's own hardware, one project at a time, patched batch by
batch with a human who isn't a coder and an AI that reads the whole repo
before touching it.
'''

with open(FP, "w", encoding="utf-8") as f:
    f.write(NEW_README)

print("README.md rewritten - now reflects v3.1.0, working conventions, and now/next/later roadmap")