import datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\UMBRA_HANDOFF.md"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak44_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD_START = "## CURRENT STATUS v3.1.0"
OLD_END = "- **Overall: ~88%**"

start_idx = src.find(OLD_START)
end_idx = src.find(OLD_END)
if start_idx == -1 or end_idx == -1:
    print("FAIL: could not locate status section boundaries")
    sys.exit(1)
end_idx = end_idx + len(OLD_END)

NEW_SECTION = '''## CURRENT STATUS v3.1.0 (updated after batch 43)

### FULLY WORKING
- Boot: `python Umbra.py` launches clean, GUI opens, status correct
- ComfyUI auto-launches at boot via `run_directml.bat`
- Real image generation via ComfyUI (dreamshaper_8, dpmpp_2m, 36 steps,
  professional-grade negative prompts incl. face/eyes/teeth)
- Real animated GIF via AnimateDiff-Evolved (8 frames, 384x384, 20 steps,
  cfg 7.0, neon/flicker negatives) - gif/image generation run in a
  background thread, GUI stays responsive during generation
- Voice: PyAudio auto-installs (pipwin fallback); `listen`/`voice on`/
  `tts on` all wired into the GUI command path (previously only worked
  in CLI interactive_mode)
- Game name extraction has a real fallback (no more silent "MyGame" when
  GUI can't prompt for stdin); game-detection is verb+noun co-occurrence,
  not a rigid phrase list ("make a 1 level snake game" now routes correctly)
- Game build pipeline has real contract-safety guarantees:
  - `draw_main_menu` and all UI "contract" functions (draw_class_select,
    draw_inventory, draw_shop, draw_pause, draw_crafting, draw_city_build,
    draw_world_map, draw_dialogue, draw_gameover, draw_hud, draw_panel,
    draw_bar) always use the skeleton's own safe implementation - agent
    overrides of these specific names are always stripped
  - Stray top-level agent code (demo/test instantiation lines that used to
    execute at import time and crash before real setup) is stripped
  - `_umbra_flex()` adaptively calls agent-class constructors/methods:
    handles both arity mismatches AND name/type mismatches (e.g. passing
    a Player object where an agent's method wants raw x/y coordinates)
  - Player construction survives the agent's own `__init__` validation
    raising (e.g. rejecting an unrecognized class name) via fallback retry
  - Every contract class (Player/Camera/Enemy/NPC/Projectile/FloatText/
    Building) is guaranteed to have working `update()`/`draw()` methods -
    missing ones get a safe no-op/fallback instead of crashing
  - Automated headless smoke test runs after every build, before "BUILD
    COMPLETE": constructs Player (incl. every actual class-select label),
    Camera, ticks camera.update, calls draw_main_menu/draw_class_select,
    spawns enemies/NPCs and calls their update() AND draw(). Runs in an
    isolated subprocess, ~1 second, reports PASS/FAIL with traceback.
- `_ollama_stream` enforces a real wall-clock timeout (was previously only
  a per-readline socket timeout and could hang indefinitely on a slow but
  technically-alive connection)
- Syntax-repair LLM call timeout raised 120s -> 600s (regenerating a full
  file is comparable cost to a full agent call, which takes minutes here)
- .gitignore now actually matches our backup-file naming and generated
  build-artifact folders (workspaces/agent_builds, workspaces/projects,
  workspaces/images) - these were being silently committed before
- Repo cleaned: 22 orphaned one-off debug scripts + 2 dead backup folders
  removed (all confirmed zero references before deletion)
- Memory: `remember X` / `memory` working
- Version: v3.1.0

### KNOWN ISSUES / UNVERIFIED (CURRENT PRIORITY)

1. **[NEEDS FRESH LOG] Game still reportedly closes on class-select** after
   batches 40-43 were pushed. Not yet confirmed whether this was tested
   against a build made AFTER applying 40-43, or an old cached build
   relaunched via `play last`. Need a fresh terminal+GUI log from a build
   started after all of batch 40-43 are applied to diagnose further -
   do not guess-patch again without one.

2. **GIF pipeline general quality** - still rough (motion/detail limited by
   DirectML speed/VRAM ceiling at 384x384/8 frames). Deferred/backlog,
   not blocking.

3. **OpenCV not available** warning at boot - cosmetic only.

4. **UI agent output size** - has ballooned as large as 3159 lines in one
   build (vs ~100 for other agents), which both slows builds and is more
   surface area for bugs. No prompt/scope constraint added yet.

### NOT YET BUILT - FUTURE SCOPE (confirm/prioritize with user)
Original vision was a full local multi-agent AI studio. Confirmed-working
today: games (with the 7-agent pipeline above), images, GIFs, voice/TTS,
memory. Explicitly NOT yet built, mentioned as desired at various points:
- Full large-scale game generation (Skyrim/Fable/Runescape scale): persistent
  world state, save systems, streaming/larger maps, NPC schedules and
  personalities, live economy simulation ("world brain")
- Music generation
- Video generation - `make a video of X` / `assemble video frames` appear
  in the help text but have not been exercised/verified in any session
  captured in this handoff; status unknown
- 3D asset generation
- AI companion/girlfriend feature
- General-purpose multi-AI-agent helper framework (beyond the 7-agent game
  builder specifically)
- General application building (beyond games)

## ARCHITECTURE (do not change)
```
Umbra.py -> build_runtime() -> interactive_mode() -> _launch_gui() -> mainloop()
_process_command() routes all input
  -> image regex -> RuntimeImageGenerator -> ComfyUI HTTP API (threaded)
  -> gif regex -> RuntimeAnimatedGifGenerator -> ComfyUI AnimateDiff-Evolved (threaded)
  -> listen/voice/tts -> RuntimeVoiceInput (now handled directly in _process_command)
  -> build/game (verb+noun match) -> _run_deep_build() -> 7-agent pipeline -> _stitch_game()
       -> strip_imports() strips agent overrides of contract fn/class names
       -> _run_smoke_test() headless subprocess validation before BUILD COMPLETE
  -> remember/recall -> RuntimeMemoryStore -> sessions/memory_store.json
  -> fix yourself -> handle_self_fix()
RuntimeLauncher auto-starts ComfyUI at boot (run_directml.bat)
```

## KEY FILES & LINE REFS (approximate, drifts each batch - grep to confirm)
| What | File | Approx line |
|---|---|---|
| Command router | Umbra.py | ~3570 |
| Game detection (verb+noun) | Umbra.py | ~3783 |
| GIF/image generation (threaded) | Umbra.py | ~3543 |
| Ollama stream (wall-clock timeout) | Umbra.py | ~692 |
| Syntax repair call | Umbra.py | ~886 |
| _run_smoke_test + harness | Umbra.py | ~1451 |
| Game stitch (strip_imports, method-safety patch) | Umbra.py | ~1001, ~1700 |
| UMBRA_PLAYER_PATCH | Umbra.py | ~1620 |
| ComfyUI launcher | core/runtime/runtime_launcher.py | full file |
| Image generator | core/runtime/runtime_image_generator.py | full file |
| GIF generator | core/runtime/runtime_animated_gif_generator.py | full file |
| Game skeleton (_umbra_flex, contract fallbacks) | core/assets/game_skeleton.py | full file |

## WHAT STILL NEEDS DOING FOR 100% (of the GAME BUILDER specifically)
Priority order:
1. Get a fresh log from a build made after batches 40-43 to confirm the
   class-select crash is actually resolved (or find the real remaining bug)
2. Constrain UI agent output size/scope (3159-line outputs are a symptom of
   an under-constrained prompt, not just a speed problem)
3. Decide + scope future feature set (see NOT YET BUILT above) with user
4. Update UMBRA_HANDOFF.md after every session (batches 22-43 were not
   reflected here until now - this must not happen again)

## COMPLETION
- Boot + GUI + ComfyUI auto-launch: 100%
- Image generation (real SD): 95% (quality much improved; GIF still rough)
- GIF generation (real AnimateDiff): 85% (non-blocking, neon/flicker fixed,
  quality still limited by hardware)
- Memory system: 100%
- Game build pipeline (small test games): ~90% (contract-safety + smoke
  test in place; class-select crash needs fresh-log confirmation)
- Voice/TTS: 95% (PyAudio auto-installs, listen/voice wired into GUI)
- Self-repair: 60%
- Large-scale game generation / world brain / economy / music / video /
  3D / AI companion / general app building: 0% (not started, scope needs
  confirming with user)
- **Overall on ORIGINAL small-game-studio scope: ~90%**
- **Overall on FULL expanded vision (large games + all media types): scope
  not yet fully defined - see NOT YET BUILT section**'''

new_src = src[:start_idx] + NEW_SECTION + src[end_idx:]

with open(FP, "w", encoding="utf-8") as f:
    f.write(new_src)

print("UMBRA_HANDOFF.md updated - now reflects batches 22-43 and full future scope")